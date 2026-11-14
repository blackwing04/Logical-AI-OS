# -*- coding: utf-8 -*-
"""v3 public release: blind packs, annotations and unblinded keys (rulings 482b1a3 items 3 and 7). Zero model calls.
Copies data files byte-for-byte into ASCII paths under laios-bridge/public_staging/data/v3/annotations/<slug>/ and, for every
markdown file that contains tables, also writes each table as CSV next to it (<name>.table<N>.csv, cells verbatim).
Not copied: program files (*.py; the published checker and export scripts replace them), files that carry run metadata with local
paths, and files that carry retry-prompt text (ruling 2: retry messages are not published). Every exclusion is listed with its reason.
The 14 unblinded condition keys used by v3 are copied to annotations/blind_keys/ with "_private" removed from the name.
Writes annotations/MAP.csv (staged path, original path, bytes, sha256) and annotations/EXCLUDED.csv.
Usage: export_v3_annotations.py
"""
from __future__ import annotations

import csv
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATT = ROOT / "laios-bridge/reports/attachments"
OUT = ROOT / "laios-bridge/public_staging/data/v3/annotations"
sys.path.insert(0, str(HERE))
sys.stdout.reconfigure(encoding="utf-8")
from export_v3_reading import md_tables                                    # noqa: E402

FOLDERS = {  # bridge attachment folder -> (slug, paper section)
	"2026-11-08_品質揭鑰": ("quality_unblind_station2a_v114", "5, 6 table 4"),
	"2026-11-09_站2品質包b揭鑰": ("quality_unblind_station2b", "5, 6"),
	"2026-11-09_14B品質包與重抽基線登記": ("quality_pack_14b", "5, 6"),
	"2026-11-09_規模站與確認性放大包": ("confirm_scale_packs", "6 table 4"),
	"2026-11-09_確認性實驗包": ("confirm_pack", "8.4"),
	"2026-11-09_確認性放大揭鑰": ("confirm_scale_unblind", "6 table 4, 8.4"),
	"2026-11-09_確認性與14B兩標註者揭鑰": ("confirm_two_raters_unblind", "6 table 4, 8.4"),
	"2026-11-09_第二標註者_GPT": ("second_rater_gpt_labels", "8.4"),
	"2026-11-09_解碼對照品質盲標揭鑰": ("decode_v23_unblind", "appendix A"),
	"2026-11-11_D1′品質揭鑰": ("decode_v23p_unblind", "appendix A"),
	"2026-11-12_確認性重盲標包": ("confirm_l1v2_packs", "8.4"),
	"2026-11-12_確認性第三列揭鑰": ("confirm_l1v2_unblind", "8.4"),
	"2026-11-12_整體偏好盲測包": ("preference_packs", "5 table 2"),
	"2026-11-12_整體偏好盲測揭鑰": ("preference_unblind", "5 table 2"),
	"2026-11-12_整體偏好盲測_人工抽核": ("preference_human_check", "5 table 2"),
	"2026-11-12_偏好盲測_架構vs裸": ("preference_governed_vs_bare", "5 table 2"),
	"2026-11-11_自述可靠性站真值審核包": ("truth_audit_packs", "7.3, 8.1"),
	"2026-11-11_自述可靠性站真值審核_GPT": ("truth_audit_gpt", "8.1"),
	"2026-11-11_翻判抽審_GPT": ("flip_audit_gpt", "8.2"),
	"2026-11-11_CS翻判抽審回應與j": ("flip_audit_cs_response", "8.2"),
	"2026-11-09_退回驗屍乙驗證包": ("retry_autopsy_b_validation", "7.3"),
	"2026-11-12_自述可靠性站主分析": ("self_report_main_analysis", "7.3"),
	"2026-11-11_退回後空答診斷": ("empty_after_retry", "7.2"),
	"2026-11-11_核對器修正登記與歷史重算": ("checker_revision_1_registration_and_recompute", "8.2"),
	"2026-11-11_核對器修正v2依慣例裁定": ("checker_revision_2_conventions_1_to_3", "8.2"),
	"2026-11-11_核對器修正v2慣例二": ("checker_revision_3_conventions_4_to_6", "8.2"),
	"2026-11-11_確認性v2重算與L1新口徑登記": ("checker_revision_4_confirmatory_recompute", "8.2"),
}
EXCLUDE = {  # file name -> reason
	"meta_jp.json": "run metadata with a local model path", "meta_v.json": "run metadata with a local model path",
	"dry_jp.json": "contains retry-prompt text (ruling 2)", "partial_jp.jsonl": "contains retry-prompt text (ruling 2)",
}
KEYS = ["experiments/gpu-station2/outputs/condition_key_private_quality30.json", "experiments/gpu-station2/outputs/condition_key_private_quality60.json",
        "experiments/gpu-station2/outputs/condition_key_private_quality14b.json", "experiments/local-patch/outputs/v114/condition_key_private_quality_v114.json",
        "experiments/local-patch/outputs/v114/decode/condition_key_private_decode_v23.json", "experiments/local-patch/outputs/v114/decode_p/condition_key_private_decode_v23p.json",
        "experiments/local-patch/outputs/v114/scale/condition_key_private_confirm_q3.json", "experiments/local-patch/outputs/v114/scale/condition_key_private_confirm_q14.json",
        "experiments/checker-fix/outputs/confirm_l1v2/condition_key_private_confirm_l1v2_q3.json",
        "experiments/checker-fix/outputs/confirm_l1v2/condition_key_private_confirm_l1v2_q14.json",
        "experiments/pref-blind/outputs/condition_key_private_pref_q3.json", "experiments/pref-blind/outputs/condition_key_private_pref_q14.json",
        "experiments/retry-autopsy/outputs/runs_b/condition_key_private_b_val.json", "experiments/retry-autopsy/outputs/confirm/condition_key_private_confirm.json"]


def sha(p: Path) -> str:
	return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
	if OUT.exists():
		shutil.rmtree(OUT)                                                     # staging is regenerated from sources every run
	OUT.mkdir(parents=True)
	mp, ex, n_tab = [], [], 0
	for folder, (slug, sec) in FOLDERS.items():
		src_dir = ATT / folder
		for f in sorted(src_dir.iterdir()):
			rel_src = "laios-bridge/reports/attachments/%s/%s" % (folder, f.name)
			if f.suffix == ".py":
				ex.append((rel_src, "program file (not published; replaced by the published checker and export scripts)"))
				continue
			if f.name in EXCLUDE:
				ex.append((rel_src, EXCLUDE[f.name]))
				continue
			if not f.name.isascii():
				raise SystemExit("STOP: non-ASCII file name %s" % rel_src)
			dst = OUT / slug / f.name
			dst.parent.mkdir(parents=True, exist_ok=True)
			shutil.copyfile(f, dst)
			mp.append((dst.relative_to(OUT.parents[2]).as_posix(), rel_src, dst.stat().st_size, sha(dst), sec))
			if f.suffix == ".md":
				for i, t in enumerate(md_tables(f.read_text(encoding="utf-8")), 1):
					tp = dst.with_name("%s.table%d.csv" % (f.stem, i))
					with tp.open("w", encoding="utf-8", newline="\n") as fh:
						csv.writer(fh, lineterminator="\n").writerows(t)
					n_tab += 1
					mp.append((tp.relative_to(OUT.parents[2]).as_posix(), rel_src + " (table %d)" % i, tp.stat().st_size, sha(tp), sec))
	for k in KEYS:
		src = ROOT / k
		dst = OUT / "blind_keys" / src.name.replace("condition_key_private_", "condition_key_")
		dst.parent.mkdir(parents=True, exist_ok=True)
		shutil.copyfile(src, dst)
		mp.append((dst.relative_to(OUT.parents[2]).as_posix(), k, dst.stat().st_size, sha(dst), "unblinding key"))
	with (OUT / "MAP.csv").open("w", encoding="utf-8", newline="\n") as fh:
		w = csv.writer(fh, lineterminator="\n")
		w.writerow(["staged_path", "original_path", "bytes", "sha256", "paper_section"])
		w.writerows(mp)
	with (OUT / "EXCLUDED.csv").open("w", encoding="utf-8", newline="\n") as fh:
		w = csv.writer(fh, lineterminator="\n")
		w.writerow(["original_path", "reason"])
		w.writerows(ex)
	print("copied %d data files, %d tables as CSV, %d keys; excluded %d" % (len(mp) - n_tab - len(KEYS), n_tab, len(KEYS), len(ex)))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
