# -*- coding: utf-8 -*-
"""Run the v4.5 recognizer (mechanical layer, zero model calls) on your own Chinese text.

The text is split by the canonical sentence splitter (src/tools/split_sentences.py), then each
sentence goes through the clause station (src/mechanical/clause_v2.py) with the flags as sealed in
manifest/v45_manifest.md. For each sentence it prints:

    axis 1   主請求 (main request) / 空框請求 (empty-frame request) / 隱性需求 (implicit need) / 非請求 (not a request)
    axis 2   限制 (constraint) / 材料 (material) / 無 (none: the sentence is the request itself)
    frame    the sentence frame that decided whether table 5 was consulted
    table-5  the criterion-table cues that fired, with their source table

Usage:
    python src/run_recognizer.py "你的句子。"
    python src/run_recognizer.py --file request.txt [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
for p in (HERE / "mechanical", HERE / "tools"):
	sys.path.insert(0, str(p))

import clause_v2 as C  # noqa: E402
import detectors as D  # noqa: E402
from split_sentences import split_text  # noqa: E402


def recognize(text: str) -> list[dict]:
	sents, _ = split_text(text)
	units = [{"sid": "s%02d" % (i + 1), "text": s} for i, s in enumerate(sents)]
	return C.classify(units)


def main() -> int:
	ap = argparse.ArgumentParser()
	ap.add_argument("text", nargs="?")
	ap.add_argument("--file")
	ap.add_argument("--json", action="store_true", help="print the full per-clause record as JSON Lines")
	a = ap.parse_args()
	if not a.text and not a.file:
		ap.error("give the text or --file")
	text = Path(a.file).read_text(encoding="utf-8") if a.file else a.text
	sys.stdout.reconfigure(encoding="utf-8")
	for r in recognize(text):
		if a.json:
			print(json.dumps(r, ensure_ascii=False))
			continue
		# 表五命中 holds the cue strings; the source table is looked up again on the clause text.
		src = {c["cue"]: c["source"] for d in r["子句"] for c in D.constraint_shape(d["子句"])["cues"]}
		cues = "、".join("%s (%s)" % (x, src.get(x, "?")) for x in r["表五命中"]) or "-"
		print("%s  %s" % (r["sid"], r["sentence"]))
		print("     axis 1: %s   axis 2: %s   frame: %s" % (r["軸一"], r["軸二"], r["框架"]))
		print("     table-5 cues: %s" % cues)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
