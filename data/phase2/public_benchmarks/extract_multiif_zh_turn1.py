# -*- coding: utf-8 -*-
"""Rebuild the Multi-IF Chinese turn-1 item list used in Phase II (454 prompts, keys MIF001..MIF454).

The answers in multiif_zh_answers.jsonl carry only the key; this script restores the prompts and
instruction lists from your own copy of the dataset, so the two can be joined.

Source: facebook/Multi-IF on Hugging Face, file multiIF_20241018.csv at revision
0ab97ce0b45c7f57772e8ba2ac1616f4b00bd3aa (sha256 6c588af031fe67b17c535b9ba0ccc14a1b9d77b4faf88c294f83aaa5a3000018,
7,402,992 bytes, 4,501 rows). The dataset is licensed CC BY-NC 2.0 and is not redistributed here.

Filter: language == "Chinese"; turn 1 only. Keys are assigned in source row order.
The output is byte-identical to the file used in Phase II when the source matches the hash above
(output sha256 946f8fcbbbe42f67791c57604f76bab8e5a878bf0062c0b4e47637c27cf62330).

Usage: python extract_multiif_zh_turn1.py --csv multiIF_20241018.csv --out zh_turn1.jsonl
Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys

SRC_SHA256 = "6c588af031fe67b17c535b9ba0ccc14a1b9d77b4faf88c294f83aaa5a3000018"
OUT_SHA256 = "946f8fcbbbe42f67791c57604f76bab8e5a878bf0062c0b4e47637c27cf62330"


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("--csv", required=True)
	ap.add_argument("--out", required=True)
	a = ap.parse_args()
	src = open(a.csv, "rb").read()
	if hashlib.sha256(src).hexdigest() != SRC_SHA256:
		print("warning: source CSV does not match the pinned revision; keys may not line up", file=sys.stderr)
	csv.field_size_limit(10 ** 9)
	lines = []
	with open(a.csv, encoding="utf-8", newline="") as fh:
		for row in csv.DictReader(fh):
			if row["language"] != "Chinese":
				continue
			lines.append({
				"key": "MIF%03d" % (len(lines) + 1),
				"source_id": row["key"],
				"prompt": json.loads(row["turn_1_prompt"])["content"],
				"instruction_id_list": json.loads(row["turn_1_instruction_id_list"]),
				"kwargs": [json.loads(k) for k in json.loads(row["turn_1_kwargs"])],
				"language": row["language"],
				"source_turn": 1,
			})
	data = "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in lines).encode("utf-8")
	with open(a.out, "wb") as fh:
		fh.write(data)
	got = hashlib.sha256(data).hexdigest()
	print("%d prompts written; output sha256 %s (%s)" % (len(lines), got, "matches Phase II" if got == OUT_SHA256 else "DIFFERS from Phase II"))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
