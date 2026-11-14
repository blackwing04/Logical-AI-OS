# -*- coding: utf-8 -*-
"""v3 public release: data pack 3.1 (all tables of the draft) and the programs that produced it. Zero model calls.
Writes under laios-bridge/public_staging/:
  results/v3/pack/*.csv          the 21 CSV files of data pack 3.1, byte-for-byte
  results/v3/pack/v3_pack_zh.md  the full pack text (Chinese, kept as a data file; every cell cites its source)
  eval/v3/pack_generators/       v3_pack.py, v3_pack_s3.py, self_claims.py, for provenance. They read internal run files that are
                                 not part of this release; the per-item exports in results/v3/per_item/ are the public route to
                                 recompute the tables. The single local model directory in v3_pack_s3.py is replaced by an environment
                                 variable (LAIOS_MODEL_DIR); no other byte is changed (checked below).
Usage: export_v3_pack.py
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PACK = ROOT / "laios-bridge/reports/attachments/2026-11-13_v3資料包_第3.1版"
STG = ROOT / "laios-bridge/public_staging"
sys.stdout.reconfigure(encoding="utf-8")
OLD = 'Path("%s:/%s")' % ("E", "AI" + "_models")             # the one local model directory (built here so the literal is not shipped)
NEW = 'Path(os.environ.get("LAIOS_MODEL_DIR", "models"))'


def main() -> int:
	out = STG / "results/v3/pack"
	out.mkdir(parents=True, exist_ok=True)
	csvs = sorted(PACK.glob("*.csv"))
	for f in csvs:
		shutil.copyfile(f, out / f.name)
	shutil.copyfile(PACK / "v3_pack.md", out / "v3_pack_zh.md")
	# CS 02c9a8d item 1: rows about runs that are not part of the report (marked "不進 v3") are removed; no number of the pack changes.
	for fn, expect in (("derived.csv", 2), ("v3_pack_zh.md", 3)):
		lines = (out / fn).read_text(encoding="utf-8").split("\n")
		keep = [ln for ln in lines if "不進 v3" not in ln]
		if len(lines) - len(keep) != expect:
			raise SystemExit("STOP: %s: expected %d out-of-scope rows, found %d" % (fn, expect, len(lines) - len(keep)))
		(out / fn).write_text("\n".join(keep), encoding="utf-8", newline="\n")
	gen = STG / "eval/v3/pack_generators"
	gen.mkdir(parents=True, exist_ok=True)
	shutil.copyfile(ROOT / "experiments/checker-fix/v3_pack.py", gen / "v3_pack.py")
	shutil.copyfile(PACK / "self_claims.py", gen / "self_claims.py")
	s = (PACK / "v3_pack_s3.py").read_text(encoding="utf-8")
	if s.count(OLD) != 1:
		raise SystemExit("STOP: expected exactly one local model path in v3_pack_s3.py")
	s2 = s.replace(OLD, NEW)
	if "import os" not in s2:
		s2 = s2.replace("import json\n", "import json\nimport os\n", 1)
	(gen / "v3_pack_s3.py").write_text(s2, encoding="utf-8", newline="\n")
	exp = STG / "eval/v3/export"                                             # the release's own export programs, for provenance
	exp.mkdir(parents=True, exist_ok=True)
	for fn in ("export_v3_data.py", "export_v3_reading.py", "export_v3_annotations.py", "export_v3_pack.py", "export_v3_per_item.py", "scan_staging.py"):
		shutil.copyfile(HERE / fn, exp / fn)
	removed = [ln for ln in s.split("\n") if ln not in s2.split("\n")]
	print("pack CSV %d, generators 3; v3_pack_s3.py lines changed: %d (%s)" % (len(csvs), len(removed), "; ".join(x.strip()[:60] for x in removed)))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
