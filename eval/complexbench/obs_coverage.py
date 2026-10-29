# -*- coding: utf-8 -*-
"""Reading coverage and "missed vs. broke" split for a record-only arm.

A record-only arm answers with the bare arm's answer but records what the architecture *read* for each
question and whether it *would* have triggered a retry. Crossing that record with the official per-rule
verdicts of the bare arm and of the real architecture arm separates two failure sources:
  * the reading step never saw the rule (missed / no matching type), versus
  * the rule was read, but the retry rewrite broke a rule the bare arm had passed.

Inputs:
    --readings  JSON Lines, one per question: {"key", "retry_triggered": bool,
                "retry_items": [{"sid": ...}, ...], "items_read": [{"idx", "type", "arg", "sid"}, ...]}
    --rules     output of extract_rule_subset.py
    --scores    output of score_complexbench.py (must contain the bare arm and the architecture arm)
    --base B0 --arm B1

The readings file is produced by the architecture, which is not public; this script documents how the
coverage numbers in results/phase2 were computed from it.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

from rule_mapping import gold_of, match

KINDS = ("hit", "right type, wrong parameters", "missed", "no matching type")


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--readings", required=True)
	ap.add_argument("--rules", required=True)
	ap.add_argument("--scores", required=True)
	ap.add_argument("--base", required=True)
	ap.add_argument("--arm", required=True)
	a = ap.parse_args()
	reads = {r["key"]: r for r in (json.loads(l) for l in open(a.readings, encoding="utf-8") if l.strip())}
	by: dict[str, list[dict]] = defaultdict(list)
	for r in (json.loads(l) for l in open(a.rules, encoding="utf-8") if l.strip()):
		by[r["key"]].append(r)
	sc = {r["key"]: r for r in json.load(open(a.scores, encoding="utf-8"))["rows"]}
	rows = []
	for k in sorted(by):
		o = reads[k]
		cand = o["items_read"]
		violated = {x["sid"] for x in (o.get("retry_items") or [])}
		used: set[int] = set()
		for j, r in enumerate(by[k]):
			g = gold_of(r["rule"])
			if g["type"] is None:
				res, idx = "no matching type", []
			else:
				idx, ok, _ = match(g, cand, used)
				used |= set(idx)
				res = "hit" if ok else ("right type, wrong parameters" if idx else "missed")
			read_items = [c for c in cand if c["idx"] in idx]
			m = sc[k]["rules"][j]
			assert m["point_id"] == r["point_id"]
			rows.append({"key": k, "read": res, "triggered": bool(o.get("retry_triggered")),
			             "read_item_was_violated": any(c.get("sid") in violated for c in read_items),
			             "base_pass": sc[k]["arms"][a.base]["pass"][j] is True,
			             "arm_pass": sc[k]["arms"][a.arm]["pass"][j] is True})
	n_q = len(by)
	n_tr = sum(1 for k in by if reads[k].get("retry_triggered"))
	print("trigger rate: %d/%d (%.1f%%)" % (n_tr, n_q, 100 * n_tr / n_q))
	print("reading: " + ", ".join("%s %d" % (t, sum(1 for x in rows if x["read"] == t)) for t in KINDS))
	print("coverage (hits / all rules): %.1f%%" % (100 * sum(1 for x in rows if x["read"] == "hit") / len(rows)))
	print("\n| read | rules | base pass -> arm pass | base pass -> arm fail | base fail -> arm pass | base fail -> arm fail |")
	print("| --- | ---: | ---: | ---: | ---: | ---: |")
	for t in KINDS:
		xs = [x for x in rows if x["read"] == t]
		c: dict[tuple[bool, bool], int] = defaultdict(int)
		for x in xs:
			c[(x["base_pass"], x["arm_pass"])] += 1
		print("| %s | %d | %d | %d | %d | %d |" % (t, len(xs), c[(True, True)], c[(True, False)], c[(False, True)], c[(False, False)]))
	print("\n| bare arm failed; grouped by reading | rules | turned to pass in arm |\n| --- | ---: | ---: |")
	for title, ts in (("read (hit)", ("hit",)), ("read, wrong parameters", ("right type, wrong parameters",)),
	                  ("not read (missed + no matching type)", ("missed", "no matching type"))):
		xs = [x for x in rows if x["read"] in ts and not x["base_pass"]]
		print("| %s | %d | %d |" % (title, len(xs), sum(1 for x in xs if x["arm_pass"])))
	bad = [x for x in rows if x["base_pass"] and not x["arm_pass"]]
	print("\nbroken by the arm (bare pass -> arm fail): %d; the broken rule was itself the retry target: %d; collateral: %d"
	      % (len(bad), sum(1 for x in bad if x["read_item_was_violated"]), sum(1 for x in bad if not x["read_item_was_violated"])))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
