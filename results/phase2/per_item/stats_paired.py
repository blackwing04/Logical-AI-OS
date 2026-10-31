# -*- coding: utf-8 -*-
"""Paired statistics for the Phase II per-item results: McNemar exact test and a bootstrap 95% CI.

Reads the per-item CSV files in this directory and writes stats_paired.csv next to them.
Standard library only; no project code is imported.

Unit of analysis
    S1-S3, Multi-IF, ComplexBench prompt level: one item (prompt); outcome = all constraints / rules passed.
    ComplexBench mappable subset: items whose rules include at least one mappable rule; outcome = all mappable rules passed.
    ComplexBench rule level: one rule; outcome = the rule passed (an unscored rule counts as not passed).

Statistics
    up / down   discordant pairs: items that fail in the base arm and pass in the compared arm, and the reverse.
    mcnemar_p   two-sided exact McNemar test (binomial on the discordant pairs, p = 0.5).
    ci_low/high percentile bootstrap of the item-level difference (compared minus base, percentage points):
                items are resampled with replacement, B = 10,000, fixed seed. Each prompt was sampled once at a fixed
                seed, so the interval covers item sampling only, not run-to-run generation variance.

Against the Part II report: the up/down counts and the p values reproduce exactly. The report's intervals were
computed with the same method but a seed that was not recorded, so interval ends differ by up to 0.8 points
(5 of the 11 reported intervals differ at all). delta_pts here is computed from the counts; the report subtracts
two rounded percentages, so two cells differ by 0.1 (ComplexBench 7B prompt level +7.2 vs +7.1, rule level +5.2 vs +5.1).

Usage: python stats_paired.py            (writes stats_paired.csv)
"""
from __future__ import annotations

import csv
import math
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
B = 10_000
SEED = 20261029

# (paper, comparison label, file, unit, base arm, compared arm, status)
GROUPS = [
	("S1", "3B v1.3 vs bare", "s1_items.csv", "item", "B0", "B1", "formal"),
	("S1", "7B v1.3 vs bare", "s1_items.csv", "item", "A0", "A1", "formal"),
	("S2", "3B v1.6 vs bare", "s2_items.csv", "item", "B0", "B1", "formal"),
	("S2", "7B v1.6 (retry arm) vs bare", "s2_items.csv", "item", "A0", "A1'", "formal"),
	("S2", "3B v1.7 vs bare", "s2_items.csv", "item", "B0", "B1_v1.7", "development"),
	("S2", "3B oracle vs bare", "s2_items.csv", "item", "B0", "B_oracle", "development (ceiling of the v1.6 flow)"),
	("S3", "3B v1.8 vs bare", "s3_items.csv", "item", "B0", "B1", "formal"),
	("S3", "3B v1.7 vs bare", "s3_items.csv", "item", "B0", "B2", "formal (ablation)"),
	("S3", "7B v1.8 vs bare", "s3_items.csv", "item", "A0", "A1", "formal"),
	("Multi-IF zh", "3B v1.9 vs bare", "multiif_zh_items.csv", "item", "B0", "B1", "formal (blind)"),
	("Multi-IF zh", "7B v1.9 vs bare", "multiif_zh_items.csv", "item", "A0", "A1", "formal (blind)"),
	("ComplexBench", "3B v1.11 vs bare, prompt level", "complexbench_rule_items.csv", "item", "B0", "B1", "formal (blind)"),
	("ComplexBench", "7B v1.11 vs bare, prompt level", "complexbench_rule_items.csv", "item", "A0", "A1", "formal (blind)"),
	("ComplexBench", "3B v1.11 vs bare, mappable subset", "complexbench_rule_items.csv", "mappable", "B0", "B1", "formal (blind)"),
	("ComplexBench", "7B v1.11 vs bare, mappable subset", "complexbench_rule_items.csv", "mappable", "A0", "A1", "formal (blind)"),
	("ComplexBench", "3B v1.11 vs bare, rule level", "complexbench_rule_items.csv", "rule", "B0", "B1", "formal (blind)"),
	("ComplexBench", "7B v1.11 vs bare, rule level", "complexbench_rule_items.csv", "rule", "A0", "A1", "formal (blind)"),
]


def read_rows(name: str) -> list[dict]:
	with open(HERE / name, encoding="utf-8", newline="") as fh:
		return list(csv.DictReader(fh))


def outcomes(rows: list[dict], unit: str) -> dict[str, dict[str, int]]:
	"""Return {arm: {unit id: 0/1}}."""
	out: dict[str, dict[str, int]] = defaultdict(dict)
	for r in rows:
		arm = r["arm"]
		if unit == "rule":
			out[arm]["%s/%s" % (r["item"], r["point_id"])] = int(r["pass"] == "1")
		elif unit == "mappable":
			if r["mappable_all_pass"] != "":
				out[arm][r["item"]] = int(r["mappable_all_pass"])
		else:
			key = "all_strict" if "all_strict" in r else "all_pass"
			out[arm][r["item"]] = int(r[key])
	return out


def mcnemar_exact(up: int, down: int) -> float:
	n = up + down
	if n == 0:
		return 1.0
	k = min(up, down)
	tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
	return min(1.0, 2 * tail)


def bootstrap_ci(x: list[int], y: list[int], rng: random.Random) -> tuple[float, float]:
	n = len(x)
	d = [b - a for a, b in zip(x, y)]
	stats = []
	for _ in range(B):
		s = 0
		for _ in range(n):
			s += d[rng.randrange(n)]
		stats.append(100 * s / n)
	stats.sort()
	return stats[int(0.025 * B)], stats[int(0.975 * B) - 1]


def main() -> int:
	cache: dict[str, list[dict]] = {}
	out = []
	for paper, label, name, unit, base, arm, status in GROUPS:
		rows = cache.setdefault(name, read_rows(name))
		o = outcomes(rows, unit)
		ids = sorted(set(o[base]) & set(o[arm]))
		assert ids and len(ids) == len(o[base]) == len(o[arm]), (label, len(ids), len(o[base]), len(o[arm]))
		x = [o[base][i] for i in ids]
		y = [o[arm][i] for i in ids]
		up = sum(1 for a, b in zip(x, y) if not a and b)
		down = sum(1 for a, b in zip(x, y) if a and not b)
		lo, hi = bootstrap_ci(x, y, random.Random(SEED))
		n = len(ids)
		out.append({"paper": paper, "comparison": label, "unit": unit, "n": n, "base_arm": base, "arm": arm,
		            "base_pass": sum(x), "arm_pass": sum(y), "base_pct": round(100 * sum(x) / n, 1),
		            "arm_pct": round(100 * sum(y) / n, 1), "delta_pts": round(100 * (sum(y) - sum(x)) / n, 1),
		            "up": up, "down": down, "mcnemar_p": round(mcnemar_exact(up, down), 4),
		            "ci_low": round(lo, 1), "ci_high": round(hi, 1), "bootstrap_B": B, "seed": SEED, "status": status})
	with open(HERE / "stats_paired.csv", "w", encoding="utf-8", newline="") as fh:
		w = csv.DictWriter(fh, fieldnames=list(out[0].keys()), lineterminator="\n")
		w.writeheader()
		w.writerows(out)
	for r in out:
		print("%-13s %-36s n=%-3d %5.1f -> %5.1f (%+5.1f)  up/down %2d/%-2d  p=%.4f  CI [%+.1f, %+.1f]" % (
			r["paper"], r["comparison"], r["n"], r["base_pct"], r["arm_pct"], r["delta_pts"], r["up"], r["down"],
			r["mcnemar_p"], r["ci_low"], r["ci_high"]))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
