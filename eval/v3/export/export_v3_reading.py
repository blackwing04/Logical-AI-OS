# -*- coding: utf-8 -*-
"""v3 public release: reading exams v2-v4 (section 7.1, table 5). Zero model calls. Rulings 482b1a3 item 6/7:
the reader's raw output is exported with only the extracted requirements and the conflict judgement; internal rule-table codes
(item "source", conflict "kind", keep/drop id lists, version meta fields) are not exported. Markdown tables become CSV.
Writes under laios-bridge/public_staging/data/v3/reading_exams/:
  v{2,3,4}/exam.jsonl            exam sentences (id, sentence), copied field by field
  v{2,3,4}/answer_key.csv        answer key table (from exam_v*_gold.md), header translated, cells verbatim
  v{2,3,4}/reader_output.jsonl   id, requirements [{id, type, param, quote}], conflicts [{a, b, kept}]
  second_annotator_275.csv       second annotator (GPT) reading annotations for E001-E150 and V001-V125
Usage: export_v3_reading.py
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATT = ROOT / "laios-bridge/reports/attachments"
OUT = ROOT / "laios-bridge/public_staging/data/v3/reading_exams"
sys.stdout.reconfigure(encoding="utf-8")
EXAMS = {"v2": ("2026-11-09_讀題考卷v2", "2026-11-09_讀題考卷v2盲打原始輸出"),
         "v3": ("2026-11-10_讀題考卷v3", "2026-11-10_讀題考卷v3盲打原始輸出"),
         "v4": ("2026-11-10_讀題考卷v4", "2026-11-10_讀題考卷v4盲打原始輸出")}
GOLD_HDR = {"卷號": "id", "類": "category", "句子": "sentence", "gold 條目": "gold_requirements", "備註／衝突 gold": "note_or_conflict_gold"}
ANN_HDR = {"編號": "id", "要求（逐條，用；分隔）": "requirements", "矛盾（是／否＋說明）": "conflict"}


def md_tables(text: str) -> list[list[list[str]]]:
	tabs, cur = [], []
	for ln in text.split("\n"):
		s = ln.strip()
		if s.startswith("|") and s.endswith("|"):
			cells = [c.strip() for c in s[1:-1].split("|")]
			if all(set(c) <= set("-: ") for c in cells):
				continue
			cur.append(cells)
		elif cur:
			tabs.append(cur)
			cur = []
	if cur:
		tabs.append(cur)
	return tabs


def write_csv(p: Path, header: list[str], rows: list[list[str]]) -> int:
	p.parent.mkdir(parents=True, exist_ok=True)
	with p.open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(header)
		w.writerows(rows)
	return len(rows)


def main() -> int:
	counts = []
	for v, (qd, rd) in EXAMS.items():
		exam = [json.loads(x) for x in (ATT / qd / ("exam_%s.jsonl" % v)).read_text(encoding="utf-8").split("\n") if x.strip()]
		o = OUT / v
		o.mkdir(parents=True, exist_ok=True)
		(o / "exam.jsonl").write_text("".join(json.dumps({"id": r["id"], "sentence": r["句子"]}, ensure_ascii=False) + "\n" for r in exam), encoding="utf-8", newline="\n")
		tabs = [t for t in md_tables((ATT / qd / ("exam_%s_gold.md" % v)).read_text(encoding="utf-8")) if t and t[0][0] == "卷號"]
		if len(tabs) != 1:
			raise SystemExit("STOP: %s answer key: expected one table, found %d" % (v, len(tabs)))
		hdr = [GOLD_HDR.get(h, h) for h in tabs[0][0]]
		n_gold = write_csv(o / "answer_key.csv", hdr, tabs[0][1:])
		rd_rows = json.loads((ATT / rd / ("exam_%s_read.json" % v)).read_text(encoding="utf-8"))["rows"]
		pub = [{"id": r["id"], "requirements": [{"id": i["sid"], "type": i["type"], "param": i.get("param"), "quote": i.get("quote")} for i in r["items"]],
		        "conflicts": [{"a": c.get("a"), "b": c.get("b"), "kept": c.get("keep_txt")} for c in r["conflicts"]]} for r in rd_rows]
		(o / "reader_output.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in pub), encoding="utf-8", newline="\n")
		counts.append((v, len(exam), n_gold, len(pub)))
	tabs = [t for t in md_tables((ATT / "2026-11-10_讀題天花板/gpt_reading_annotations_275.md").read_text(encoding="utf-8")) if t and t[0][0] == "編號"]
	rows = [r for t in tabs for r in t[1:]]
	n_ann = write_csv(OUT / "second_annotator_275.csv", [ANN_HDR.get(h, h) for h in tabs[0][0]], rows)
	for v, ne, ng, nr in counts:
		print("%s: exam %d, answer key %d, reader output %d%s" % (v, ne, ng, nr, "" if ne == ng == nr else "  **MISMATCH**"))
	print("second annotator rows %d (expected 275)" % n_ann)
	return 0 if all(ne == ng == nr for _, ne, ng, nr in counts) and n_ann == 275 else 1


if __name__ == "__main__":
	raise SystemExit(main())
