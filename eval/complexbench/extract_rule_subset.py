# -*- coding: utf-8 -*-
"""Build the ComplexBench rule-only subset used in Phase II.

A scoring point is "rule-only" when its `rule` field is non-null and does not start with `model`
(the `model_*` rules need an LLM to extract a span first). On the official `data_final.json`
(1,150 instructions) this gives 252 rules over 209 instructions. One rule is spelled
`modek_keyword` upstream; `con_rule.py` judges it as a keyword rule by substring, and so does this
pipeline.

Usage:
    python extract_rule_subset.py --data data_final.json --out pure_rules.jsonl

Output, one JSON object per rule:
    {"key", "main_id", "point_id", "rule", "kind", "dims", "composition", "dep", "question"}
"""
from __future__ import annotations

import argparse
import json


def is_pure(q: dict) -> bool:
	return bool(q.get("rule")) and not q["rule"].startswith("model")


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--data", required=True, help="official ComplexBench data_final.json")
	ap.add_argument("--out", required=True)
	a = ap.parse_args()
	data = json.load(open(a.data, encoding="utf-8"))
	pure = [(r, q) for r in data for q in r["scoring_questions"] if is_pure(q)]
	with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
		for r, q in pure:
			fh.write(json.dumps({"key": "CB%04d" % r["main_id"], "main_id": r["main_id"], "point_id": q["point_id"],
			                     "rule": q["rule"], "kind": q["rule"].split(":")[0], "dims": q["constraint_dimensions"],
			                     "composition": q["composition_types"], "dep": q["dep"], "question": q["question"]},
			                    ensure_ascii=False) + "\n")
	print("rules: %d, instructions: %d" % (len(pure), len({r["main_id"] for r, _ in pure})))
	kinds: dict[str, int] = {}
	for _, q in pure:
		kinds[q["rule"].split(":")[0]] = kinds.get(q["rule"].split(":")[0], 0) + 1
	print("kinds: %s" % dict(sorted(kinds.items(), key=lambda kv: -kv[1])))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
