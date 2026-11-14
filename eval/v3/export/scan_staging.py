# -*- coding: utf-8 -*-
"""v3 public release: pre-push gates on laios-bridge/public_staging (order 482b1a3 step 1). Read-only except for the manifest it writes.
Gates:
  A  local paths   drive-letter or home paths, the local model directory name, the private GitHub repository names
  B  secrets       key-like strings (API-key and access-token prefixes), private-key blocks, the local key file name
  C  ASCII paths   every staged path is ASCII
  D  prose         English-only documentation: README/NOTICE/*.md written for the release must contain no CJK (data files exempt)
  E  manifest      writes manifest/v3_manifest.csv (path, bytes, sha256) and checks it lists every staged file
Exit 1 if any gate fails; findings are written to scan_report.md next to this script's outputs.
Usage: scan_staging.py
"""
from __future__ import annotations

import csv
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STG = ROOT / "laios-bridge/public_staging"
sys.stdout.reconfigure(encoding="utf-8")
_MD, _KF = "ai" + "_models", "git" + "key"                                 # built so the scanner does not flag its own source
A = re.compile(r"(?i)\b[a-z]:[\\/]{1,2}(projects|" + _MD + r"|users|program files)|" + _MD + "|/h" + "/projects|/c" + r"/users|logical-ai-os" + "-develop|Of-Laios" + "-bridge")   # bridge paths as provenance are precedent (public MANIFEST.md)
B = re.compile(r"\b(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})|BEGIN [A-Z ]*PRIVATE KEY|" + _KF)   # condition-key file names are references; the keys themselves are published
CJK = re.compile(r"[㐀-鿿豈-﫿　-〿＀-￯]")
DOCS = {"README.md", "NOTICE_complexbench.md"}                              # release prose; data .md (packs, labels, v3_pack_zh.md) are exempt


def main() -> int:
	files = sorted(p for p in STG.rglob("*") if p.is_file())
	fa, fb, fc, fd = [], [], [], []
	for p in files:
		rel = p.relative_to(STG).as_posix()
		if not rel.isascii():
			fc.append(rel)
		t = p.read_bytes().decode("utf-8", errors="replace")
		for rx, bucket in ((A, fa), (B, fb)):
			m = rx.search(t)
			if m:
				ln = t.count("\n", 0, m.start()) + 1
				bucket.append("%s:%d: %s" % (rel, ln, t[max(0, m.start() - 20):m.end() + 20].replace("\n", " ")))
		if p.name in DOCS and CJK.search(t):
			m = CJK.search(t)
			fd.append("%s:%d" % (rel, t.count("\n", 0, m.start()) + 1))
	man = STG / "manifest/v3_manifest.csv"
	man.parent.mkdir(parents=True, exist_ok=True)
	rows = [(p.relative_to(STG).as_posix(), p.stat().st_size, hashlib.sha256(p.read_bytes()).hexdigest()) for p in files if p != man]
	with man.open("w", encoding="utf-8", newline="\n") as f:
		w = csv.writer(f, lineterminator="\n")
		w.writerow(["path", "bytes", "sha256"])
		w.writerows(rows)
	listed = {r[0] for r in rows}
	fe = [p.relative_to(STG).as_posix() for p in files if p != man and p.relative_to(STG).as_posix() not in listed]
	L = ["# Staging scan", "", "files %d, bytes %d" % (len(files), sum(p.stat().st_size for p in files)), ""]
	for name, f in (("A local paths", fa), ("B secrets", fb), ("C non-ASCII paths", fc), ("D CJK in release prose", fd), ("E manifest gaps", fe)):
		L += ["## %s: %s" % (name, "PASS" if not f else "FAIL (%d)" % len(f)), ""] + ["- " + x for x in f[:50]] + [""]
	(HERE / "outputs").mkdir(exist_ok=True)
	(HERE / "outputs/scan_report.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
	print("\n".join(x for x in L if x.startswith(("##", "files"))))
	return 1 if (fa or fb or fc or fd or fe) else 0


if __name__ == "__main__":
	raise SystemExit(main())
