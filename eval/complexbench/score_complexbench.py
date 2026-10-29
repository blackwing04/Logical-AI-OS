# -*- coding: utf-8 -*-
"""Score responses on the ComplexBench rule-only subset with the **official** con_rule.py (unmodified).

Evaluated object: the official pipeline first asks GPT-4 to extract the "evaluation object" from a
response and then applies the rule. This script calls no API; it passes the **whole response** to the
official `decompose_judge(rule, [response])` (for non-model rules that ends in
`rule(decom(r)) or rule(r)`). Start / end / paragraph-specific rules are therefore judged more strictly
than in the official pipeline.

Dependencies (`dep`): officially, a rule whose dependency fails is itself failed. Most dependencies
are LLM-judged points that cannot be judged here, so every rule is judged independently and
`dep_on_llm` is recorded; the summary also prints columns that drop those rules.

Usage:
    python score_complexbench.py --con-rule path/to/con_rule.py --rules pure_rules.jsonl \
        --responses B0=b0.jsonl --responses B1=b1.jsonl ... --out scores.json

Each responses file is JSON Lines: {"key": "CB0001", "answer": "..."}.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import defaultdict

from rule_mapping import mappable


def load_con_rule(path: str):
	spec = importlib.util.spec_from_file_location("cb_con_rule", path)
	m = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(m)
	return m, hashlib.sha256(open(path, "rb").read()).hexdigest()


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--con-rule", required=True)
	ap.add_argument("--rules", required=True, help="output of extract_rule_subset.py")
	ap.add_argument("--responses", action="append", required=True, metavar="ARM=PATH")
	ap.add_argument("--out", required=True)
	a = ap.parse_args()
	cr, cr_sha = load_con_rule(a.con_rule)
	rules = [json.loads(l) for l in open(a.rules, encoding="utf-8") if l.strip()]
	pure_ids = {(r["key"], r["point_id"]) for r in rules}
	by: dict[str, list[dict]] = defaultdict(list)
	for r in rules:
		by[r["key"]].append(r)
	res = {}
	for spec in a.responses:
		arm, path = spec.split("=", 1)
		res[arm] = {r["key"]: r.get("answer") or "" for r in (json.loads(l) for l in open(path, encoding="utf-8") if l.strip())}
	keys = sorted(set(by).intersection(*(set(v) for v in res.values())))
	out = {"meta": {"scorer": "ComplexBench con_rule.py (unmodified), decompose_judge(rule, [whole response])",
	                "con_rule_sha256": cr_sha, "object": "whole response", "dep_policy": "independent; dep_on_llm recorded"},
	       "rows": []}
	for k in keys:
		meta = [{"point_id": r["point_id"], "rule": r["rule"], "kind": r["kind"], "dep": r["dep"],
		         "dep_on_llm": any((k, d) not in pure_ids for d in r["dep"]), "mappable": mappable(r["rule"])} for r in by[k]]
		row = {"key": k, "rules": meta, "arms": {}}
		for arm in res:
			v = []
			for m in meta:
				x = cr.decompose_judge(m["rule"], [res[arm][k]])
				v.append(None if x == 2 else bool(x))
			sub = [i for i, m in enumerate(meta) if m["mappable"]]
			row["arms"][arm] = {"pass": v, "all_pass": all(x is True for x in v),
			                    "mappable_all_pass": (all(v[i] is True for i in sub) if sub else None)}
		out["rows"].append(row)
	json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

	cols = [("all rules", lambda m: True), ("mappable subset", lambda m: m["mappable"]),
	        ("all rules, minus LLM-dependent", lambda m: not m["dep_on_llm"]),
	        ("mappable, minus LLM-dependent", lambda m: m["mappable"] and not m["dep_on_llm"])]
	print("questions: %d; con_rule sha256: %s" % (len(keys), cr_sha))
	print("| column | " + " | ".join("%s rules" % x for x in res) + " | " + " | ".join("%s questions" % x for x in res) + " |")
	print("| --- |" + " ---: |" * (2 * len(res)))
	for title, pred in cols:
		cells_r, cells_q = [], []
		for arm in res:
			n = ok = q = qok = 0
			for row in out["rows"]:
				idx = [i for i, m in enumerate(row["rules"]) if pred(m)]
				s = row["arms"][arm]["pass"]
				n += len(idx); ok += sum(1 for i in idx if s[i] is True)
				if idx:
					q += 1; qok += all(s[i] is True for i in idx)
			cells_r.append("%d/%d (%.1f%%)" % (ok, n, 100 * ok / max(1, n)))
			cells_q.append("%d/%d (%.1f%%)" % (qok, q, 100 * qok / max(1, q)))
		print("| %s | %s | %s |" % (title, " | ".join(cells_r), " | ".join(cells_q)))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
