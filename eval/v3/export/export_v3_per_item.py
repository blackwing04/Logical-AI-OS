# -*- coding: utf-8 -*-
"""v3 public release: per-item and per-article verdicts, computed with the published standalone checker (checker/laios_checker_v2.py)
on the original (unredacted) answers. Zero model calls. Rulings 482b1a3 items 1 and 8.
Writes under laios-bridge/public_staging/:
  data/v3/items/checkable_items.jsonl   per article: bank, id, items [{sid, check_type, check_arg, weight}] (the reading layer's output)
  results/v3/per_item/item_verdicts.csv  bank, id, arm, sid, check_type, v1, v2_no_length, v2_full   (1 / 0 / empty = not checkable)
  results/v3/per_item/article_allpass.csv bank, id, arm, allpass_v1, allpass_v2_no_length, allpass_v2_full
  results/v3/per_item/allpass_by_arm.csv  arm, articles, allpass under each scale
  eval/v3/checker/                        laios_checker_v2.py, its two tables, README.md
Checks (printed, and written to experiments/public-v3/outputs/per_item_checks.md):
  1 for the 24 arms of the frozen reference, every verdict equals ref_verdicts.jsonl (frozen checker);
  2 all-pass counts per arm equal the data pack's scale_arms.csv (v1, v2 without length, v2 full; L1 v2 rerun column for *_L1v2).
Usage: export_v3_per_item.py
"""
from __future__ import annotations

import csv
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STG = ROOT / "laios-bridge/public_staging"
CK = HERE / "checker"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(CK))
sys.stdout.reconfigure(encoding="utf-8")
import export_v3_data as X                                                 # noqa: E402  (arm table and conservative construction)
import laios_checker_v2 as LC                                              # noqa: E402

PACK = ROOT / "laios-bridge/reports/attachments/2026-11-13_v3資料包_第3.1版/scale_arms.csv"
DROP_ARG = ("trigger", "material_scope")                                   # CS 02c9a8d item 2: reading-rule trigger words are governance-side; the checker does not read either


def b01(v):
	return "" if v is None else ("1" if v else "0")


def main() -> int:
	items = {}
	for ln in (CK / "outputs/items.jsonl").read_text(encoding="utf-8").split("\n"):
		if ln.strip():
			r = json.loads(ln)
			items[(r["bank"], r["article"])] = [dict(it, check_arg={k: v for k, v in it["check_arg"].items() if k not in DROP_ARG})
			                                     if isinstance(it.get("check_arg"), dict) else it for it in r["items"]]
	# original answers for every published arm
	answers = {}
	for arm, (_, _, pat) in X.ARMS.items():
		for b in X.BANKS:
			for r in X.rows_of(Path(str(pat) % b)):
				answers[(arm, b, r["篇"])] = r.get("answer") or ""
	for mk, base in X.CONS.items():
		sc = json.loads((X.V114 / "scale" / ("scale_%s.json" % mk)).read_text(encoding="utf-8"))
		cons = {(x["paper"].lower(), x["篇"]): x["texts"]["保守"] for x in sc["recs"]}
		for (arm, b, k), t in list(answers.items()):
			if arm == base:
				answers[("Conservative%s" % mk, b, k)] = cons.get((b, k), t)
	iv, ap = [], {}
	for (arm, b, k), t in sorted(answers.items()):
		its = items[(b, k)]
		v1, v2n, v2 = LC.check_items_v1(its, t), LC.check_items(its, t, exclude=("length",)), LC.check_items(its, t)
		for it in its:
			s = it["sid"]
			iv.append([b, k, arm, s, it["check_type"], b01(v1.get(s)), b01(v2n.get(s)), b01(v2.get(s))])
		ap[(arm, b, k)] = tuple(all(x is not False for x in d.values()) for d in (v1, v2n, v2))
	# check 1: frozen reference
	ref_n = ref_bad = 0
	bad = []
	name = {"保守" + mk: "Conservative" + mk for mk in X.CONS}
	for ln in (CK / "outputs/ref_verdicts.jsonl").read_text(encoding="utf-8").split("\n"):
		if not ln.strip():
			continue
		r = json.loads(ln)
		arm = name.get(r["arm"], r["arm"])
		t = answers[(arm, r["bank"], r["article"])]
		its = items[(r["bank"], r["article"])]
		mine = {"v1": LC.check_items_v1(its, t), "v2_no_length": LC.check_items(its, t, exclude=("length",)), "v2_full": LC.check_items(its, t)}
		for var in ("v1", "v2_no_length", "v2_full"):
			for s, v in r[var].items():
				ref_n += 1
				if mine[var].get(s) != v:
					ref_bad += 1
					bad.append((arm, r["bank"], r["article"], var, s, v, mine[var].get(s)))
	# check 2: all-pass counts against the data pack
	pack = {r["臂"]: r for r in csv.DictReader(PACK.read_text(encoding="utf-8").splitlines())}
	by_arm = {}
	for (arm, b, k), a in ap.items():
		by_arm.setdefault(arm, [0, 0, 0, 0])
		by_arm[arm][0] += 1
		for i in range(3):
			by_arm[arm][i + 1] += a[i]
	cmp = []
	for arm, (n, a1, a2n, a2) in sorted(by_arm.items()):
		pk = arm.replace("Conservative", "保守")
		if pk.endswith("_L1v2"):
			exp = pack.get(pk[:-5], {}).get("全守_L1v2重跑")
			cmp.append((arm, "v2_full vs pack L1 v2 rerun", a2, exp, str(a2) == (exp or "").strip()))
		elif pk in pack:
			for got, col in ((a1, "全守_v1"), (a2n, "全守_v2不含字數"), (a2, "全守_v2完整")):
				cmp.append((arm, col, got, pack[pk][col], str(got) == pack[pk][col].strip()))
	# write
	out = STG / "results/v3/per_item"
	out.mkdir(parents=True, exist_ok=True)
	with (out / "item_verdicts.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["bank", "id", "arm", "sid", "check_type", "v1", "v2_no_length", "v2_full"])
		w.writerows(iv)
	with (out / "article_allpass.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["bank", "id", "arm", "allpass_v1", "allpass_v2_no_length", "allpass_v2_full"])
		w.writerows([[b, k, arm] + [b01(x) for x in a] for (arm, b, k), a in sorted(ap.items(), key=lambda z: (z[0][0], z[0][1], z[0][2]))])
	with (out / "allpass_by_arm.csv").open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["arm", "articles", "allpass_v1", "allpass_v2_no_length", "allpass_v2_full"])
		w.writerows([[arm] + v for arm, v in sorted(by_arm.items())])
	(STG / "data/v3/items").mkdir(parents=True, exist_ok=True)
	(STG / "data/v3/items/checkable_items.jsonl").write_text("".join(json.dumps({"bank": b, "id": k, "items": its}, ensure_ascii=False) + "\n"
	                                                                    for (b, k), its in sorted(items.items())), encoding="utf-8", newline="\n")
	ck = STG / "eval/v3/checker"
	ck.mkdir(parents=True, exist_ok=True)
	for fn in ("laios_checker_v2.py", "zh_s2t_table.json", "zh_t2s_table.json", "README.md"):
		shutil.copyfile(CK / fn, ck / fn)
	L = ["# per-item export checks", "", "item verdict rows %d; article rows %d; arms %d" % (len(iv), len(ap), len(by_arm)), "",
	     "1. frozen reference: %d verdicts compared, %d differ" % (ref_n, ref_bad)] + ["   - %s" % (x,) for x in bad[:30]]
	L += ["", "2. all-pass counts vs data pack scale_arms.csv: %d compared, %d differ" % (len(cmp), sum(1 for c in cmp if not c[4])), ""]
	L += ["| arm | column | export | pack | same |", "| --- | --- | --- | --- | --- |"] + ["| %s | %s | %s | %s | %s |" % c for c in cmp]
	(HERE / "outputs").mkdir(exist_ok=True)
	(HERE / "outputs/per_item_checks.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
	print("\n".join(L[:6]))
	print("pack comparison: %d compared, %d differ" % (len(cmp), sum(1 for c in cmp if not c[4])))
	for c in cmp:
		if not c[4]:
			print("  DIFF", c)
	return 0 if not ref_bad and all(c[4] for c in cmp) else 1


if __name__ == "__main__":
	raise SystemExit(main())
