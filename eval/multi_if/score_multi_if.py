# -*- coding: utf-8 -*-
"""Score responses on the Multi-IF Chinese subset (turn 1) with the **official** Multi-IF checker.

The checker is facebookresearch/Multi-IF at commit 1cdb53ed18499ad729e0766e5d3099dd5344406f
(Apache-2.0): `ifeval.py` and `metrics.py`, used unmodified. They are not redistributed here; fetch them:

    https://raw.githubusercontent.com/facebookresearch/Multi-IF/1cdb53ed18499ad729e0766e5d3099dd5344406f/ifeval.py
    https://raw.githubusercontent.com/facebookresearch/Multi-IF/1cdb53ed18499ad729e0766e5d3099dd5344406f/metrics.py

sha256 of the files used in Phase II:
    ifeval.py   61a56d4510a0b8cbacc511d50d4707d20ff72e521d02e29a2898dec69a5507b2
    metrics.py  3aa15edc8e5f6d2f92abe0ec7ae12e9568ed6aadd1f82efc7805808fef76dc2b
Runtime dependencies used: pythainlp 5.4.0, nltk 3.10.4 (+ punkt, punkt_tab), langdetect 1.0.9, emoji 2.16.0
(metrics.py also imports numpy, pandas, scipy).

The headline metric in results/phase2 is per question: all instructions pass under `gen_acc_strict`.

Usage:
    python score_multi_if.py --vendor-dir dir_with_ifeval_and_metrics --questions zh_turn1.jsonl \
        --responses B0=b0.jsonl --responses B1=b1.jsonl ... --out scores.json

questions: JSON Lines {"key", "instruction_id_list", "kwargs"} (turn-1 Chinese items from the Multi-IF data).
responses: JSON Lines {"key", "answer"}.
"""
from __future__ import annotations

import argparse
import json
import sys

# Multi-IF instruction id -> this project's constraint type; ids not listed are outside our 11 types.
MAP = {
	"length_constraints:number_words": "length", "length_constraints:number_sentences": "length",
	"detectable_format:number_bullet_lists": "count",
	"detectable_format:title": "format", "detectable_format:json_format": "format",
	"length_constraints:number_paragraphs": "structure", "detectable_format:multiple_sections": "structure",
	"keywords:existence": "term_required", "keywords:frequency": "term_required",
	"keywords:forbidden_words": "term_forbidden",
	"punctuation:no_comma": "forbidden_charset",
}


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--vendor-dir", required=True)
	ap.add_argument("--questions", required=True)
	ap.add_argument("--responses", action="append", required=True, metavar="ARM=PATH")
	ap.add_argument("--out", required=True)
	a = ap.parse_args()
	sys.path.insert(0, a.vendor_dir)
	from metrics import gen_acc_loose, gen_acc_strict  # noqa: E402  (official, unmodified)
	q = {r["key"]: r for r in (json.loads(l) for l in open(a.questions, encoding="utf-8") if l.strip())}
	res = {}
	for spec in a.responses:
		arm, path = spec.split("=", 1)
		res[arm] = {r["key"]: r.get("answer") or "" for r in (json.loads(l) for l in open(path, encoding="utf-8") if l.strip())}
	keys = sorted(set(q).intersection(*(set(v) for v in res.values())))
	out = {"meta": {"scorer": "facebookresearch/Multi-IF@1cdb53e metrics.gen_acc_strict / gen_acc_loose (unmodified)", "mapping": MAP},
	       "rows": []}
	for k in keys:
		ids, kws = q[k]["instruction_id_list"], q[k]["kwargs"]
		mapped = [MAP.get(i) for i in ids]
		row = {"key": k, "instruction_id_list": ids, "our_types": mapped, "arms": {}}
		for arm in res:
			x = {"response": res[arm][k], "instruction_id_list": ids, "kwargs": kws}
			st, lo = gen_acc_strict(x), gen_acc_loose(x)
			sub = [i for i, m in enumerate(mapped) if m]
			row["arms"][arm] = {"strict": st["follow_instruction_list"], "loose": lo["follow_instruction_list"],
			                    "all_strict": all(st["follow_instruction_list"]), "all_loose": all(lo["follow_instruction_list"]),
			                    "mappable_all_strict": (all(st["follow_instruction_list"][i] for i in sub) if sub else None)}
		out["rows"].append(row)
	json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
	n = len(out["rows"])
	for arm in res:
		qs = sum(r["arms"][arm]["all_strict"] for r in out["rows"])
		ins = [x for r in out["rows"] for x in r["arms"][arm]["strict"]]
		print("%s: questions all-pass strict %d/%d (%.1f%%); instructions strict %d/%d (%.1f%%)"
		      % (arm, qs, n, 100 * qs / n, sum(ins), len(ins), 100 * sum(ins) / len(ins)))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
