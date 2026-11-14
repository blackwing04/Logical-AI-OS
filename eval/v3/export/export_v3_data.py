# -*- coding: utf-8 -*-
"""v3 public release: export items and per-arm answers to the staging tree (order f104917, rulings 482b1a3). Zero model calls.
Writes (LF, UTF-8, ASCII paths) under laios-bridge/public_staging/:
  data/v3/items/s3_items.jsonl                 120 articles: id, user_message (exactly what every bare arm received), group, sentinel, topic_source
  data/v3/items/complexbench_subset_items.jsonl 209 articles: id, user_message
  data/v3/answers/<arm>_<bank>.jsonl            one row per article: bank, id, arm, model, answer, gen_seconds, n_new_tokens
  data/v3/answers/arms.csv                      arm -> model, method family
  data/v3/export_counts.csv                     exported rows vs source rows per file (must match)
Only the listed fields are copied; governance-side fields (retry prompts, retry items, gate reasons, ask texts, ...) and run metadata
(local model paths) are never read into the output.
Usage: export_v3_data.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STG = ROOT / "laios-bridge/public_staging"
sys.stdout.reconfigure(encoding="utf-8")

S2O, R1O = ROOT / "experiments/gpu-station2/outputs", ROOT / "experiments/r1-station/outputs"
V114, CF = ROOT / "experiments/local-patch/outputs/v114", ROOT / "experiments/checker-fix/outputs"
MODEL = {"q3": "Qwen2.5-3B-Instruct", "q7": "Qwen2.5-7B-Instruct", "q14": "Qwen2.5-14B-Instruct", "r1": "DeepSeek-R1-Distill-Qwen-7B"}
# arm -> (model key, family, source file pattern %s=bank)
ARMS = {
	"A0g": ("q7", "bare", S2O / "results_%s_A0g.json"), "A1g": ("q7", "whole-answer retry", S2O / "results_%s_A1g_v113.json"),
	"B0g": ("q3", "bare", S2O / "results_%s_B0g.json"), "B1g": ("q3", "whole-answer retry", S2O / "results_%s_B1g_v113.json"),
	"M0": ("q14", "bare", S2O / "results_%s_M0.json"), "M1": ("q14", "whole-answer retry", S2O / "results_%s_M1_v113.json"),
	"R0": ("r1", "bare", R1O / "results_%s_R0.json"), "R1v13": ("r1", "whole-answer retry", S2O / "results_%s_R1v13_v113.json"),
	"P0q7": ("q7", "bare, restated input (P)", S2O / "results_%s_P0q7.json"), "P1q7": ("q7", "whole-answer retry, restated input (P)", S2O / "results_%s_P1q7_v113.json"),
	"P0r1": ("r1", "bare, restated input (P)", S2O / "results_%s_P0r1.json"), "P1r1": ("r1", "whole-answer retry, restated input (P)", S2O / "results_%s_P1r1_v113.json"),
	"E1q7": ("q7", "generic redo (retry message without the failed-item list)", S2O / "results_%s_E1q7.json"), "E1r1": ("r1", "generic redo (retry message without the failed-item list)", S2O / "results_%s_E1r1.json"),
	"LPq7": ("q7", "local patch", V114 / "results_%s_LPq7_v114.json"), "LPr1": ("r1", "local patch", V114 / "results_%s_LPr1_v114.json"),
	"LPq3": ("q3", "local patch", V114 / "results_%s_LPq3_v114.json"), "LPq14": ("q14", "local patch", V114 / "results_%s_LPq14_v114.json"),
	"A1gL": ("q7", "whole-answer retry, rerun with the v1.14 length control (a cut ends at a sentence boundary)", V114 / "results_%s_A1gL_v114.json"),
	"R1v13L": ("r1", "whole-answer retry, rerun with the v1.14 length control (a cut ends at a sentence boundary)", V114 / "results_%s_R1v13L_v114.json"),
}
for a in ("A1g", "B1g", "M1", "R1v13", "P1q7", "P1r1"):
	ARMS[a + "_L1v2"] = (ARMS[a][0], ARMS[a][1] + ", rerun with revised length control", CF / ("rerun_l1v2/results_%%s_%s_v113l1v2.json" % a))
for mk in ("q7", "r1", "q3", "q14"):
	ARMS["LP%s_L1v2" % mk] = (mk, "local patch, rerun with revised length control", CF / ("rerun_lp_l1v2/results_%%s_LP%s_v114.json" % mk))
CONS = {"q7": "A0g", "r1": "R0", "q3": "B0g", "q14": "M0"}                 # conservative arm: delivered text where triggered, else the bare answer
BANKS = ("s3", "cb")


BASE = {"A1g": "A0g", "B1g": "B0g", "M1": "M0", "R1v13": "R0", "P1q7": "P0q7", "P1r1": "P0r1", "E1q7": "A0g", "E1r1": "R0",
        "LPq7": "A0g", "LPr1": "R0", "LPq3": "B0g", "LPq14": "M0", "A1gL": "A0g", "R1v13L": "R0",
        "P0q7": "A0g", "P0r1": "R0"}                                        # P0 arms read the restated input too
for _a in list(BASE):
	if _a in ("A1g", "B1g", "M1", "R1v13", "P1q7", "P1r1"):
		BASE[_a + "_L1v2"] = BASE[_a]
	if _a.startswith("LP"):
		BASE[_a + "_L1v2"] = BASE[_a]
RETRY_OF = {"q7": "A1g", "r1": "R1v13", "q3": "B1g", "q14": "M1"}
RW, RMIN, GAP = 6, 8, 4                                                     # same rule as the Phase II package (v2.0.1)
WS = re.compile(r"\s+")
REDACTED = []                                                              # (bank, id, arm, chars, text) -- text kept out of staging


def template_sources(arm: str, r: dict) -> list[str]:
	"""Text the model saw that is governance-side wording: retry message, patch messages and closings, the P-arm restated input."""
	src = [r.get("retry_message") or ""]
	for s in ((r.get("v114") or {}).get("steps") or []):
		src += [s.get("patch_message") or "", s.get("closing") or ""]
	if arm.startswith("P"):
		src.append(r.get("full_text") or "")
	return [x for x in src if x]


def _runs(flags: list[bool], gap: int = 0) -> list[tuple[int, int]]:
	out, st, last = [], None, None
	for i, f in enumerate(flags):
		if f:
			if st is not None and i - last - 1 > gap:
				out.append((st, last + 1))
				st = None
			if st is None:
				st = i
			last = i
	if st is not None:
		out.append((st, last + 1))
	return out


def redact(answer: str, sources: list[str], own: str, bare: str) -> tuple[str, list[tuple[int, int]]]:
	"""Replace blocks of the answer copied from governance-side wording. A core is a run of >=RMIN chars (whitespace ignored) made of
	RW-char windows found in the sources but neither in the user message nor in the bare arm's answer; a block is the core extended over
	adjacent text that matches the sources (gaps up to GAP chars)."""
	if not sources or not answer:
		return answer, []
	idx = [i for i, c in enumerate(answer) if not c.isspace()]
	a_n = "".join(answer[i] for i in idx)
	own_n, bare_n = WS.sub("", own), WS.sub("", bare)
	cover = set()
	for s in sources:
		s_n = WS.sub("", s)
		cover |= {s_n[i:i + RW] for i in range(len(s_n) - RW + 1)}
	spec = {w for w in cover if w not in own_n and w not in bare_n}
	cov, sp = [False] * len(a_n), [False] * len(a_n)
	for i in range(len(a_n) - RW + 1):
		w = a_n[i:i + RW]
		if w in cover:
			cov[i:i + RW] = [True] * RW
		if w in spec:
			sp[i:i + RW] = [True] * RW
	cores = [(s, e) for s, e in _runs(sp) if e - s >= RMIN]
	keep = [(s, e) for s, e in _runs(cov, gap=GAP) if any(cs >= s and ce <= e for cs, ce in cores)]
	spans = [(idx[s], idx[e - 1] + 1) for s, e in keep]
	for a, b in sorted(spans, reverse=True):
		answer = answer[:a] + "[governance-side text redacted, %d chars]" % (b - a) + answer[b:]
	return answer, spans


def wl(p: Path, rows: list[dict]) -> None:
	p.parent.mkdir(parents=True, exist_ok=True)
	p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")


def rows_of(p: Path) -> list[dict]:
	return json.loads(p.read_text(encoding="utf-8"))["rows"]


def main() -> int:
	counts = []
	# items: the user message every bare arm received (A0g = B0g = M0 = R0, checked)
	bare = {b: {r["篇"]: r.get("full_text") for r in rows_of(ARMS["A0g"][2].parent / (ARMS["A0g"][2].name % b))} for b in BANKS}
	for b in BANKS:
		for a in ("B0g", "M0", "R0"):
			other = {r["篇"]: r.get("full_text") for r in rows_of(Path(str(ARMS[a][2]) % b))}
			if other != bare[b]:
				raise SystemExit("STOP: bare arm %s %s received a different user message than A0g" % (a, b))
	s3meta = {x["篇"]: x for x in json.loads((ROOT / "laios-bridge/data/mstation/synth3/articles_s3_final.json").read_text(encoding="utf-8"))}
	grp = {"甲": "A (rewritten prompts)", "乙": "B (original, topic from a public forum board title)"}
	s3 = [{"id": k, "user_message": bare["s3"][k], "group": grp.get(s3meta[k]["source_class"], s3meta[k]["source_class"]),
	       "sentinel": bool(s3meta[k].get("哨兵")), "topic_source_board": s3meta[k].get("cc_source_board")} for k in sorted(bare["s3"])]
	mid = {}
	for ln in (ROOT / "laios-bridge/data/complexbench/pure_rules.jsonl").read_text(encoding="utf-8").split("\n"):
		if ln.strip():
			r = json.loads(ln)
			mid[r["篇"]] = r["main_id"]
	cb = [{"id": k, "main_id": mid[k], "user_message": bare["cb"][k]} for k in sorted(bare["cb"])]   # main_id = position in upstream data_final.json (as in Phase II)
	wl(STG / "data/v3/items/s3_items.jsonl", s3)
	wl(STG / "data/v3/items/complexbench_subset_items.jsonl", cb)
	counts += [("data/v3/items/s3_items.jsonl", len(s3), len(s3meta)), ("data/v3/items/complexbench_subset_items.jsonl", len(cb), len(bare["cb"]))]
	# answers
	raw = {(arm, b): {r["篇"]: r for r in rows_of(Path(str(pat) % b))} for arm, (_, _, pat) in ARMS.items() for b in BANKS}
	texts = {}
	arm_rows = []
	for arm, (mk, fam, pat) in ARMS.items():
		for b in BANKS:
			src = raw[(arm, b)]
			out = []
			for k, r in src.items():
				ans = r.get("answer") or ""
				if arm in BASE:
					ans, spans = redact(ans, template_sources(arm, r), bare[b][k], raw[(BASE[arm], b)][k].get("answer") or "")
					REDACTED.extend((b, k, arm, y - x, (r.get("answer") or "")[x:y]) for x, y in spans)
				out.append({"bank": b, "id": k, "arm": arm, "model": MODEL[mk], "answer": ans,
				            "gen_seconds": r.get("gen_seconds"), "n_new_tokens": r.get("n_new_tokens")})
			texts[(arm, b)] = {r["id"]: r["answer"] for r in out}
			rel = "data/v3/answers/%s_%s.jsonl" % (arm, b)
			wl(STG / rel, out)
			counts.append((rel, len(out), len(src)))
		arm_rows.append({"arm": arm, "model": MODEL[mk], "family": fam})                  # CS 02c9a8d item 3: no internal source path
	for mk, base in CONS.items():
		sc = json.loads((V114 / "scale" / ("scale_%s.json" % mk)).read_text(encoding="utf-8"))
		cons = {(x["paper"].lower(), x["篇"]): x["texts"]["保守"] for x in sc["recs"]}
		arm = "Conservative%s" % mk
		for b in BANKS:
			out = []
			for k, t in sorted(texts[(base, b)].items()):
				ans = cons.get((b, k), t)
				if (b, k) in cons:                                              # delivered text may come from the patch or the retry: redact with both sources
					srcs = template_sources("LP" + mk, raw[("LP" + mk, b)][k]) + template_sources(RETRY_OF[mk], raw[(RETRY_OF[mk], b)][k])
					orig = ans
					ans, spans = redact(ans, srcs, bare[b][k], t)
					REDACTED.extend((b, k, arm, y - x, orig[x:y]) for x, y in spans)
				out.append({"bank": b, "id": k, "arm": arm, "model": MODEL[mk], "answer": ans, "gen_seconds": None, "n_new_tokens": None,
				            "conservative_triggered": (b, k) in cons})
			rel = "data/v3/answers/%s_%s.jsonl" % (arm, b)
			wl(STG / rel, out)
			counts.append((rel, len(out), len(texts[(base, b)])))
		arm_rows.append({"arm": arm, "model": MODEL[mk], "family": "conservative (delivered text where triggered, else the %s answer)" % base})
	with (STG / "data/v3/answers/arms.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.DictWriter(f, fieldnames=["arm", "model", "family"], lineterminator="\n")
		w.writeheader()
		w.writerows(arm_rows)
	with (STG / "data/v3/export_counts.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["file", "exported_rows", "source_rows", "match"])
		for rel, n, m in counts:
			w.writerow([rel, n, m, n == m])
	with (STG / "data/v3/answers/REDACTIONS.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["bank", "id", "arm", "chars_replaced"])
		w.writerows([x[:4] for x in REDACTED])
	(HERE / "outputs").mkdir(exist_ok=True)                                  # the replaced text stays in the private repository
	(HERE / "outputs/redaction_log_private.jsonl").write_text("".join(json.dumps(dict(zip(("bank", "id", "arm", "chars", "text"), x)), ensure_ascii=False) + "\n"
	                                                                  for x in REDACTED), encoding="utf-8", newline="\n")
	print("redacted blocks %d in %d answers" % (len(REDACTED), len({x[:3] for x in REDACTED})))
	bad = [c for c in counts if c[1] != c[2]]
	print("files %d, rows %d, mismatched %d" % (len(counts), sum(c[1] for c in counts), len(bad)))
	return 1 if bad else 0


if __name__ == "__main__":
	raise SystemExit(main())
