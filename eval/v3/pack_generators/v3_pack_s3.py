# -*- coding: utf-8 -*-
"""v3 資料包第 3 版新增節（聊天端 v3 稿要；Joe 6334b68）——v3_pack.py 呼叫；零呼叫、只讀既有產物、不重算判定。
八、模型與材料：模型確切型號、載入方式（量化）、題庫名稱與篇數、衍生子集；型號與裝置以各站跑批檔的 meta 逐檔核對。
九、使用者層：偏好盲測架構 vs 裸（Joe 算法，三種做法合起來看；6334b68 問題一）＋字數第一關（72 篇）各做法達標篇數。
附錄 A、單一做法版（架構內部各做法對底；6334b68 問題二，內部診斷）。
來源：pref-blind/outputs/arch_vs_bare.json、effective-body/outputs/padding_audit.json、gpu-station2／r1-station／checker-fix／effective-body 跑批檔、
  laios-bridge/data（S3、ComplexBench）、src/model/hf_backend.py。
"""
from __future__ import annotations

import glob
import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

MODELS = [  # 代號、確切型號、出處／底座、規模、生成上限（token）、所用臂
	("q3", "Qwen2.5-3B-Instruct", "Qwen 官方指令版（Qwen2.5 系列）", "3B", "2048", "B0g（底）、B1g（整篇退回）、LPq3（局部修補）、保守q3"),
	("q7", "Qwen2.5-7B-Instruct", "Qwen 官方指令版（Qwen2.5 系列）", "7B", "2048", "A0g（底）、A1g、P0q7、P1q7、E1q7、LPq7、保守q7、A1gL"),
	("q14", "Qwen2.5-14B-Instruct", "Qwen 官方指令版（Qwen2.5 系列）", "14B", "2048", "M0（底）、M1、LPq14、保守q14"),
	("r1", "DeepSeek-R1-Distill-Qwen-7B", "DeepSeek 以 DeepSeek-R1 產生的約 80 萬筆樣本微調而成；底座 Qwen2.5-Math-7B（Qwen 系、7B；模型卡 Base Model 欄）",
	 "7B", "4096（含思考段）", "R0（底）、R1v13、P0r1、P1r1、E1r1、LPr1、保守r1、R1v13L"),
]
MDIR = {"q3": "qwen2.5-3b-instruct", "q7": "qwen2.5-7b-instruct", "q14": "qwen2.5-14b-instruct", "r1": "deepseek-r1-distill-qwen-7b"}
RUN_GLOBS = ["experiments/gpu-station2/outputs/results_*.json", "experiments/r1-station/outputs/results_*_R0.json",
             "experiments/checker-fix/outputs/rerun_l1v2/*results*.json", "experiments/effective-body/outputs/rerun_eff/results_*_v113eff_full.json"]
DERIVED = [  # 子集、模型、篇、由來、備註、出處（reports/ 或本包節）
	("規格層全卷（各臂）", "q3／q7／q14／r1", "329／臂", "S3 120＋CB 209 全收", "", "本包一、二節"),
	("確認性包 D", "q7", "55", "v1.14 全卷站 A1g 觸發退回篇全收（S3 17、CB 38）", "", "2026-11-09_確認性實驗包.md:9-11"),
	("14B 包 C", "q14", "30", "M0／M1 品質抽核", "", "2026-11-09_確認性與14B兩標註者揭鑰.md"),
	("確認放大 G／H", "q3／q14", "60／60", "v1.13 觸發篇，S3／CB 按候選比例分層抽（B1g 觸發 S3 73、CB 97；M1 觸發 S3 61、CB 77）", "", "2026-11-09_確認性放大登記.md:11-13"),
	("偏好盲測 PG／PH", "q3／q14", "49／41（計 90）", "G、H 的 60 篇去掉四臂全同者（3B 11、14B 19）", "", "2026-11-12_整體偏好盲測包.md"),
	("字數第一關", "q3／q14", "72", "偏好盲測 90 篇中有長度條目者", "", "本包九節"),
	("讀題考卷 v2／v3／v4", "（不經模型）", "150／125／115 句", "聊天端出卷；讀題為規則、不呼叫模型", "", "本包六節"),
	("GPU 序 2 有效正文重跑", "q3／q7／q14／r1", "596 篇次", "六架構臂 × S3／CB 範圍內篇（12 格）", "不進 v3（裁）", "2026-11-13_GPU序2正式_無迴圈防護版.md"),
	("自述可靠性站", "q7／q14／r1", "配對 150／150／168", "各模型自己的底臂答案 × 條目；問法重做主要比較 266 組（q7 134、q14 132）", "不進 v3（裁）", "2026-11-12_自述可靠性站主分析.md"),
]
NAMES = ("CS v2", "CS v3", "GPT 單選", "GPT 複選", "Joe")
ARMS3 = ("整篇退回 v1.13", "局部修補 v1.14", "保守")
ARM_SHOW = {"底": "底（裸）", "整篇退回 v1.13": "整篇退回", "局部修補 v1.14": "局部修補", "保守": "保守"}


def blob(p: Path) -> str:
	b = p.read_bytes()
	return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()[:16]


def fp(p) -> str:
	return "—" if p is None else ("%.4f" % p if p >= 0.0001 else "<0.0001")


def run_check() -> dict:
	"""各站正式跑批檔（不含 smoke）逐檔讀 meta：模型路徑、device_map、解碼、上限。"""
	R = {k: {"files": 0, "dm_files": 0, "dm_devices": set(), "decoding": set(), "max_new": set(), "rows": 0} for k in MDIR}
	inv = {v: k for k, v in MDIR.items()}
	for g in RUN_GLOBS:
		for f in sorted(glob.glob(str(ROOT / g))):
			if "smoke" in Path(f).name or "STOPPED" in Path(f).name:
				continue
			d = json.loads(Path(f).read_text(encoding="utf-8"))
			if not isinstance(d, dict) or "rows" not in d or not d.get("model"):
				continue
			mk = inv.get(Path(str(d["model"]).replace("\\", "/")).name)
			if mk is None:
				raise SystemExit("**停**：%s 的模型 %s 不在清單" % (f, d["model"]))
			r = R[mk]
			r["files"] += 1
			r["rows"] += len(d["rows"])
			dm = d.get("device_map")                                         # 跑批檔記的是模型各層所在裝置的去重清單
			if isinstance(dm, dict):
				dm = list(dm.values())
			if dm:
				r["dm_files"] += 1
				r["dm_devices"] |= {str(v) for v in dm}
			if d.get("decoding"):
				r["decoding"].add(str(d["decoding"]))
			if d.get("max_new_tokens"):
				r["max_new"].add(int(d["max_new_tokens"]))
	return R


def banks() -> dict:
	s3 = json.loads((ROOT / "laios-bridge/data/mstation/synth3/articles_s3_final.json").read_text(encoding="utf-8"))
	cb = [json.loads(l) for l in (ROOT / "laios-bridge/data/complexbench/test_sentences_cb.jsonl").read_text(encoding="utf-8").split("\n") if l.strip()]
	return {"s3": len(s3), "s3_甲": sum(x["source_class"] == "甲" for x in s3), "s3_乙": sum(x["source_class"] == "乙" for x in s3),
	        "s3_哨兵": sum(bool(x.get("哨兵")) for x in s3), "cb": len({x["篇"] for x in cb})}


RETRY = {"q3": ("B0g", "B1g"), "q7": ("A0g", "A1g"), "q14": ("M0", "M1"), "r1": ("R0", "R1v13")}
BR = "reports/"                                                             # 出處前綴（橋）


def gen_total(mk: str, arm: str, rnd: str) -> float:
	if arm == "R0":
		p = ROOT / ("experiments/r1-station/outputs/results_%s_R0.json" % rnd)
	else:
		p = ROOT / ("experiments/gpu-station2/outputs/results_%s_%s%s.json" % (rnd, arm, "" if arm.endswith(("0g", "M0")) else "_v113"))
	d = json.loads(p.read_text(encoding="utf-8"))
	if d.get("gen_seconds_total") is None:
		raise SystemExit("**停**：%s 無 gen_seconds_total" % p)
	return float(d["gen_seconds_total"])


def cost_section(write_csv) -> list[str]:
	import csv
	arms = {r["臂"]: r for r in csv.DictReader((HERE / "outputs/v3_pack/scale_arms.csv").read_text(encoding="utf-8").splitlines())}
	rows = []
	for mk, (b, a) in RETRY.items():
		tb = sum(gen_total(mk, b, r) for r in ("s3", "cb"))
		ta = sum(gen_total(mk, a, r) for r in ("s3", "cb"))
		n = int(arms[a]["篇"])
		g1 = int(arms[a]["全守_v1"]) - int(arms[b]["全守_v1"])
		g2 = int(arms[a]["全守_v2完整"]) - int(arms[b]["全守_v2完整"])
		rows.append([mk, "%s → %s" % (b, a), n, "%.0f" % tb, "%.1f" % (tb / n), "%.0f" % ta, "%.1f" % (ta / n), "%.0f%%" % (100 * ta / tb),
		             g1, "%.0f" % (ta / g1), g2, "%.0f" % (ta / g2)])
	write_csv("cost_time.csv", ["模型", "底 → 整篇退回", "篇", "底臂生成秒（合計）", "底臂每篇秒", "整篇退回多出秒（合計）", "每篇多出秒", "多出比例",
	                            "全守增量 v1", "每多一篇全守的邊際秒 v1", "全守增量 v2 完整", "每多一篇全守的邊際秒 v2 完整"], rows)
	lp = []
	for mk in ("q3", "q7", "q14", "r1"):
		txt = (ROOT / ("experiments/checker-fix/outputs/rerun_lp_l1v2/log_lp_%s.txt" % mk)).read_bytes().decode("utf-8", errors="replace")   # log 混有終端進度條的非 UTF-8 位元組
		import re
		got = re.findall(r"落盤 results_(s3|cb)_LP\w+\.json（(\d+) 篇、(\d+) 次呼叫）", txt)
		if len(got) != 2:
			raise SystemExit("**停**：%s 局部修補 log 找不到兩卷的呼叫數" % mk)
		lp.append([mk, sum(int(x[1]) for x in got), sum(int(x[2]) for x in got)])
	write_csv("cost_lp_calls.csv", ["模型", "局部修補處理篇（S3＋CB）", "修補呼叫次數"], lp)
	L = ["", "## 十、代價", "", "### (a) 時間成本", "",
	     "**整篇退回：實測。** 底臂與整篇退回臂（v1.13）各跑一次 S3＋CB 全卷，生成時間取跑批檔記錄的 `gen_seconds_total`（牆鐘、逐題貪婪生成、同一台機器）。"
	     "架構臂沿用底臂答案，只另跑退回那一次生成，所以整篇退回臂記錄的生成時間就是「多出的時間」。"
	     "邊際成本＝多出秒合計 ÷ 全守增量（全守取同一批 v1.13 產物在 v1 與 v2 完整量尺下的篇數，見一節），是由實測時間**計算**出的數。", "",
	     "| 模型 | 底 → 整篇退回 | 篇 | 底臂每篇秒 | 每篇多出秒 | 多出比例 | 全守增量 v1／v2 完整 | 每多一篇全守的邊際秒 v1／v2 完整 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
	L += ["| %s | %s | %d | %s | %s | %s | +%d／+%d | %s／%s |" % (r[0], r[1], r[2], r[4], r[6], r[7], r[8], r[10], r[9], r[11]) for r in rows]
	L += ["",
	      "- 讀題加核對每題 0.006–0.035 秒，可忽略（%s2026-11-07_站2最終件.md 第 103 行）；多出的時間幾乎全是退回那一次生成（同檔第 104–107 行：7B S3 83%%、CB 41%%，R1 S3 34%%、CB 51%%，與本表分卷數字一致）。" % BR,
	      "- 硬體與設定：RTX 5070 Ti 16 GB、4-bit（八節）、一次一題。時間會隨硬體、量化、批次大小改變，只作同條件下的比較。",
	      "- **局部修補：時間未實測。** 重跑時只記了呼叫次數（下表，取自 L1 v2 局部修補重跑 log）；不可定位的篇走整篇退回後備，時間同上表。",
	      "- **保守：不另呼叫模型**（交付序＝機械修→局部修補產物→交底），時間未單獨量。",
	      "- 來源檔：experiments/gpu-station2/outputs/results_{s3,cb}_{A0g,A1g_v113,B0g,B1g_v113,M0,M1_v113,R1v13_v113}.json、experiments/r1-station/outputs/results_{s3,cb}_R0.json（整理為 cost_time.csv）。", "",
	      "| 模型 | 局部修補處理篇（S3＋CB） | 修補呼叫次數 |", "| --- | --- | --- |"]
	L += ["| %s | %d | %d |" % tuple(r) for r in lp]

	# (b) 空答與重寫變差仍取用
	us = json.loads((ROOT / "experiments/local-patch/outputs/v114/scale/unblind_confirm_scale.json").read_text(encoding="utf-8"))
	gh = []
	for rater in ("聊天端（修正後）", "GPT"):
		for mk, nm in (("q3", "G（3B）"), ("q14", "H（14B）")):
			rr = us["by_rater"][rater][mk]["rows"]
			cell = []
			for a in ("整篇退回 v1.13", "局部修補 v1.14", "保守"):                # 同七節比較欄口徑：底可用、該臂不可用（截短或內容變差）；括號內為其中內容變差
				bad = [x for x in rr if x["label"]["底"] == "可用" and x["label"][a] != "可用"]
				cell.append("%d（%d）" % (len(bad), sum(1 for x in bad if x["label"][a] == "內容變差")))
			gh.append([nm, rater, len(rr), sum(1 for x in rr if x["label"]["底"] == "可用")] + cell)
	write_csv("cost_worse_gh.csv", ["包", "標註者", "篇", "底可用", "整篇退回不可用（其中內容變差）", "局部修補不可用（其中內容變差）", "保守不可用（其中內容變差）"], gh)
	L += ["", "### (b) 空答，與「重寫後比原答案差仍取用」", "",
	      "**空答**", "",
	      "| 項 | 篇 | 出處 |", "| --- | --- | --- |",
	      "| 真空答（正文 0 字），全歷史 | 3（Q074、PQ2r1 C01、CB0391；皆推理模型思考段迴圈撞額度） | %s2026-11-11_退回後空答診斷.md 第 5–6 行 |" % BR,
	      "| 近空候選（非 0 字；退回指令本身要求極小字數） | 44：讀題誤讀 11、限制互斥 14、題目本要短答 19（已剔除） | 同檔第 8–11 行 |",
	      "| GPU 序 2 有效正文重跑（無迴圈防護版；不進 v3） | 空答 2→1 | %s2026-11-13_GPU序2正式_無迴圈防護版.md 第 32 行 |" % BR, "",
	      "**重寫後比原答案差仍取用**：整篇退回一律交出重寫版。下列為品質盲標中「底（原答案）可用、交出的版本不可用（截短或內容變差）」的篇數，口徑同七節比較欄；確認放大包另以括號列其中內容變差者。", "",
	      "| 包 | 模型 | 標註者 | 篇 | 底可用 | 整篇退回 | 局部修補 | 保守 | 出處 |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
	L += ["| 確認放大 %s | %s | %s | %d | %d | %s | %s | %s | experiments/local-patch/outputs/v114/scale/unblind_confirm_scale.json（逐篇標記計） |" % (
		r[0], "3B" if "3B" in r[0] else "14B", r[1], r[2], r[3], r[4], r[5], r[6]) for r in gh]
	L += ["| 品質抽核 30 | 7B | CS | 30 | — | 16（底→架構 16:2） | — | — | %s2026-11-06_站2補記六_揭鑰勘誤與佇列.md 第 27–28、45 行 |" % BR,
	      "| v1.14 兩包 | 7B／R1 | CS | 60 | — | 23（底→整篇 23:2） | 13（底→局部 13:1） | — | %s2026-11-08_品質揭鑰_v1.14兩包與站2包a.md 第 34–36 行 |" % BR,
	      "| 站 2 包 a | R1 | CS | 30 | — | 7（底→架構 7:3） | — | — | 同檔第 81–82 行 |",
	      "| 站 2 包 b | 7B | CS | 30 | — | 9（底→架構 9:0） | — | — | %s2026-11-09_站2品質包b揭鑰.md 第 21–23 行 |" % BR,
	      "| 14B 包 C | 14B | CS／GPT | 30 | — | 14／10（底→架構 CS 14:4、GPT 10:1） | — | — | %s2026-11-09_確認性與14B兩標註者揭鑰.md 第 65–66 行 |" % BR, "",
	      "- 確認放大包以逐篇標記直接計；其餘各包取報告中「底→架構 變差：變好」的變差數（＝底可用、架構不可用的篇；見七節比較欄口徑）。",
	      "- 各包之間有重疊的篇，不可相加。保守臂的修補段來自局部修補，故有與局部修補相同的變差篇；保守只在修補後全守時才採用。"]
	return L


def self_report_section(write_csv) -> list[str]:
	sc = json.loads((ROOT / "experiments/effective-body/outputs/self_claims.json").read_text(encoding="utf-8"))
	rows, verdict = sc["rows"], sc["verdict"]
	claim_keys = sorted({"%s|%s" % (r["id"], r["份"]) for r in rows if r["型"] != "明說不足"})
	short_keys = sorted({"%s|%s" % (r["id"], r["份"]) for r in rows if r["型"] == "明說不足"})
	cs10 = {"%s|%s" % (r["id"], r["份"]) for r in rows if r["聊天端粗掃列入"]}
	tv = lambda k: {True: "屬實", False: "不實", None: "無從核"}[verdict[k]]
	write_csv("self_claims.csv", ["份", "臂", "型", "宣稱句", "核對", "屬實"],
	          [["%s %s" % (r["id"], r["份"]), "、".join(r["臂"]), r["型"], r["句"], r["說明"], {True: "屬實", False: "不實", None: "無從核"}[r["屬實"]]] for r in rows])
	L = ["", "## 十一、模型自述", "",
	     "### (a) 模型說已修正、實際未修正（J′）", "",
	     "J′：架構把錯在哪、目標值都標明後，請模型只改這些並逐條回報（退回驗屍乙，2026-11-09；7B，30 篇中 27 篇呼叫）。", "",
	     "| 項 | 數 | 出處 |", "| --- | --- | --- |",
	     "| 逐條回報「已改」 | 25 條 | %s2026-11-09_退回驗屍乙驗證包.md 第 43–44 行 |" % BR,
	     "| 其中重核真過 | 7 條 | 同檔第 43 行 |",
	     "| **其中重核未過（說已改、實際未改到）** | **18 條（72%）** | 同檔第 44 行 |",
	     "| 只回報、不給答案 | 13／27 篇 | 同檔第 51 行 |",
	     "| 附帶傷害（原本通過的條目被改壞） | 9／27 篇 | 同檔第 52 行 |",
	     "| J′ 交付 | 0 篇（30 篇全數退回上一版） | 同檔第 56 行 |", "",
	     "### (b) 偏好盲測 %d 份回答中，主動聲稱字數達標或報出字數者" % sc["copies"], "",
	     "**程式正式算**（experiments/effective-body/self_claims.py；取代聊天端 e44ba02 的粗掃）。找法：逐句，句長 ≤160 字且不是題目原句，"
	     "符合長度宣稱樣式（字數／篇幅／N 字 與 符合／達到／超過／以內／左右／要求 相鄰，或獨立一行「約 N 字」）；另找明說不足（不足、少於、未達、還差、不夠＋字）。"
	     "核對：句中講「達到／符合要求」等者（達標型）以該份長度條目在有效正文下是否全部達標判（Joe 標準）；只報字數者（報數型）以宣稱數與正文字數相差 ±10% 內為屬實（引導建議）。"
	     "一份有多句時，任一句不實即記不實。", "",
	     "| 項 | 份 |", "| --- | --- |",
	     "| 聲稱字數達標或報出字數 | %d |" % len(claim_keys),
	     "| 其中屬實 | %d |" % sum(1 for k in claim_keys if verdict[k] is True),
	     "| 其中不實 | %d |" % sum(1 for k in claim_keys if verdict[k] is False),
	     "| 其中無從核（題目沒有長度條目） | %d |" % sum(1 for k in claim_keys if verdict[k] is None),
	     "| 明說自己字數不足 | %d |" % len(short_keys), "",
	     "- 與粗掃（e44ba02：10 份，屬實 1、不實 9）比：粗掃的 10 份程式全部找到；程式判屬實 %d 份（%s）、不實 %d 份。差在 PG22 A：宣稱「116 words」，"
	     "以 Word 算法計正文 124 字、長度條目達標，程式判屬實，粗掃判不實。程式另找到 %d 份粗掃未列者（多為開頭「以下是…確保字數…」與英文「meets the word count requirement」）。" % (
	         sum(1 for k in cs10 if verdict[k] is True), "、".join(k.replace("|", " ") for k in sorted(cs10) if verdict[k] is True),
	         sum(1 for k in cs10 if verdict[k] is False), len(set(claim_keys) - cs10)),
	     "- 限制：宣稱若只講某一部分（例：「每段結語大約 500 字」），仍以整份的長度條目判，不另核那一部分。", "",
	     "| 份 | 臂 | 型 | 宣稱句 | 核對 | 判 |", "| --- | --- | --- | --- | --- | --- |"]
	L += ["| %s %s | %s | %s | %s | %s | %s |" % (r["id"], r["份"], "、".join(r["臂"]), r["型"], r["句"].replace("|", "｜"), r["說明"],
	                                           {True: "屬實", False: "不實", None: "無從核"}[r["屬實"]]) for r in sorted(rows, key=lambda x: (x["id"], x["份"]))]
	return L


def sections(write_csv) -> list[str]:
	L = []
	# 八、模型與材料
	rc = run_check()
	hb = ROOT / "src/model/hf_backend.py"
	src = hb.read_text(encoding="utf-8")
	for s in ("load_in_4bit=True", 'bnb_4bit_quant_type="nf4"', "bnb_4bit_use_double_quant=True", "bnb_4bit_compute_dtype=torch.float16"):
		if s not in src:
			raise SystemExit("**停**：hf_backend.py 找不到 %s" % s)
	dtypes = {mk: json.loads((Path(os.environ.get("LAIOS_MODEL_DIR", "models")) / d / "config.json").read_text(encoding="utf-8")).get("torch_dtype") for mk, d in MDIR.items()}
	rows = []
	for mk, name, origin, size, cap, arms in MODELS:
		r = rc[mk]
		dev = "、".join(sorted(r["dm_devices"])) or "—"
		rows.append([mk, name, origin, size, "bitsandbytes 4-bit NF4（雙重量化、計算 fp16）；原檔 %s" % dtypes[mk], cap, arms,
		             "%d 檔（%d 篇次）；記 device_map 者 %d 檔，全為 %s" % (r["files"], r["rows"], r["dm_files"], dev)])
		if r["dm_devices"] - {"cuda:0"}:
			raise SystemExit("**停**：%s 有不在 cuda:0 的層：%s" % (mk, r["dm_devices"]))
	write_csv("models.csv", ["代號", "確切型號", "出處／底座", "規模", "載入", "生成上限", "所用臂", "跑批檔核對"], rows)
	b = banks()
	brows = [["S3", "合成卷 S3（2026-10-22 出卷）", b["s3"], "繁體中文",
	          "甲類 %d 篇：聊天端原創材料＋簽核模板限制；乙類 %d 篇：CC 原創材料與請求句，題材與問法取自 PTT 等網路熱門看板（只取題材，不貼原文）；含哨兵 %d 篇"
	          % (b["s3_甲"], b["s3_乙"], b["s3_哨兵"]), "laios-bridge/data/mstation/synth3/articles_s3_final.json"],
	         ["CB", "ComplexBench 純規則子集", b["cb"], "簡體中文",
	          "Wen et al., NeurIPS 2024（arXiv 2407.03978）；thu-coai/ComplexBench @749f457，MIT；原 1150 題中限制全可由規則核對者",
	          "laios-bridge/data/complexbench/（NOTICE.md）"]]
	write_csv("banks.csv", ["卷", "名稱", "篇", "語言", "來源", "檔"], brows)
	write_csv("derived.csv", ["子集", "模型", "篇", "由來", "備註", "出處"], [list(x) for x in DERIVED])
	L += ["", "## 八、模型與材料（限制與聲明用）", "",
	      "**四個模型皆以 4-bit 量化載入**（bitsandbytes NF4、雙重量化、fp16 計算；詳見下方模型表與附註）。", "",
	      "**本研究的結論只在以下條件成立**（Joe 指定）：① 目前這批材料（下表兩卷，中文，題型與限制類型照列）；② 同一模型家族（Qwen 系，含以其為底座的推理模型）；③ 模型規模最高 14B。", "",
	      "### 模型", "", "| 代號 | 確切型號 | 出處／底座 | 規模 | 載入 | 生成上限 | 所用臂 | 跑批檔核對 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(str(x) for x in r) for r in rows]
	L += ["",
	      "- **量化：四個模型都以 4-bit 載入，不只 14B。** 全部經同一載入器（src/model/loader.py → hf_backend.py，blob %s），有 CUDA 時一律用 bitsandbytes：`load_in_4bit=True`、`bnb_4bit_quant_type=\"nf4\"`、"
	      "`bnb_4bit_use_double_quant=True`、`bnb_4bit_compute_dtype=float16`（hf_backend.py 第 11–18 行）。權重檔為官方原檔（config 記 bfloat16），量化在載入時進行，不是預量化版本。" % blob(hb),
	      "- 載入器另有 CPU 卸載後備（第一次載入失敗才走；卸載層以 fp32 留在 CPU）。上表各模型的跑批檔凡記有 device_map 者全為 cuda:0，**記錄所及沒有任何一層卸載到 CPU**。"
	      "未記 device_map 的檔（E1 臂、L1 v2 重跑的合併檔）與局部修補、保守臂的產物（格式不同，不在核對範圍）走同一載入器、同一台機器，但無法由檔案直接核。",
	      "- 解碼一律貪婪（do_sample=False）；r1 經 R1Proxy 分離思考段，上限 4096 含思考段。",
	      "- 硬體與套件：NVIDIA GeForce RTX 5070 Ti（16 GB）；torch 2.11.0+cu128、transformers 5.5.4（底臂跑批檔記載）；bitsandbytes 0.49.2、accelerate 1.13.0（現行環境，跑批檔未記）。",
	      "- 同一量化設定早於本階段即已使用：2026-09-10_7B需求清單_report.md 第 42–67 行（3B 基線與 7B 同為 4-bit NF4＋雙重量化＋fp16 計算）。",
	      "- 本包七節「14B 包 C」模型欄寫「14B 4-bit」，其餘各列未寫，但同為 4-bit。", "",
	      "### 題庫", "", "| 卷 | 名稱 | 篇 | 語言 | 來源 | 檔 |", "| --- | --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(str(x) for x in r) for r in brows]
	L += ["", "### 衍生子集（皆出自 S3＋CB）", "", "| 子集 | 模型 | 篇 | 由來 | 備註 | 出處 |", "| --- | --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(x) for x in DERIVED]

	# 九、偏好盲測（問題一）與字數第一關
	av = json.loads((ROOT / "experiments/pref-blind/outputs/arch_vs_bare.json").read_text(encoding="utf-8"))
	T = av["tally"]
	prow = []
	for nm in NAMES:
		for mode in ("原", "有效正文未達改記未選"):
			t = T["%s｜%s" % (nm, mode)]
			c = [t[m] for m in ("q3", "q14", "合併")]
			prow.append([nm, "原判" if mode == "原" else "字數未達改記未選（探索性）"] +
			            ["%d：%d（%s）" % (x["架構"], x["裸"], fp(x["p"])) for x in c] +
			            ["%d（都不選 %d、兩邊都選 %d）" % (x["都不選"] + x["兩邊都選"], x["都不選"], x["兩邊都選"]) for x in c])
	write_csv("pref_arch_vs_bare.csv", ["標註者", "口徑", "3B 架構：裸（p）", "14B 架構：裸（p）", "合併 架構：裸（p）", "3B 排除", "14B 排除", "合併 排除"], prow)
	L += ["", "## 九、使用者層：偏好盲測——架構 vs 裸（架構三種做法合起來看）", "",
	      "算法（Joe 636abe1；6334b68 問題一）：每題只看標註者選了誰。只選了架構的答案（整篇退回、局部修補、保守，一份或多份）而沒選底＝**架構**；只選了底＝**裸**；"
	      "兩邊都選或都不選＝**排除**。底與架構某臂文字相同（包內合併成一份）時，選了它算兩邊都選。檢定＝架構：裸 精確二項雙尾。",
	      "篇：偏好盲測 90 篇（3B 49、14B 41；確認放大 G、H 的觸發篇）。Joe 20 題為分層抽樣、未加權，p 僅供對照。", "",
	      "| 標註者 | 口徑 | 3B 架構：裸（p） | 14B 架構：裸（p） | **合併 架構：裸（p）** | 3B 排除 | 14B 排除 | 合併 排除 |", "| --- | --- | --- | --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(r) for r in prow]
	L += ["", "- 「字數未達改記未選」：標註者選中、但該臂有效正文長度條目未達者改記為未選（Joe 裁「字數未達＝不可接受」）；只剔除、不重選，屬探索性。",
	      "- 兩兩配對比較中，兩臂文字相同而無從比較的題數：局部修補 vs 整篇退回 3B %d、14B %d；保守 vs 底 3B %d、14B %d。"
	      % (av["same_text"]["局部修補 v1.14 vs 整篇退回 v1.13"]["q3"], av["same_text"]["局部修補 v1.14 vs 整篇退回 v1.13"]["q14"],
	         av["same_text"]["保守 vs 底"]["q3"], av["same_text"]["保守 vs 底"]["q14"])]
	pa = json.loads((ROOT / "experiments/effective-body/outputs/padding_audit.json").read_text(encoding="utf-8"))
	lid = {}
	for r in pa["rows"]:
		if r["arm"] == "底" and int(r["n_len"]):
			lid.setdefault(r["mk"], set()).add(r["id"])
	n72 = sum(len(v) for v in lid.values())
	T2 = pa["表二"]
	grow = [[ARM_SHOW[a], T2[a]["frozen"], T2[a]["effective"], "、".join(T2[a]["lost"]) or "—", "、".join(T2[a]["gained"]) or "—"] for a in ("底",) + ARMS3]
	write_csv("gate1_length.csv", ["做法", "凍結 v2（交付物界定＋原文）", "有效正文（Joe 標準）", "凍結達標→有效未達", "凍結未達→有效達標"], grow)
	L += ["", "### 字數第一關：各做法長度條目全部達標的篇數（有長度條目的 %d 篇：3B %d、14B %d）" % (n72, len(lid.get("q3", ())), len(lid.get("q14", ()))), "",
	      "| 做法 | 凍結 v2（交付物界定＋原文） | **有效正文（Joe 標準）** | 凍結達標→有效未達 | 凍結未達→有效達標 |", "| --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(str(x) for x in r) for r in grow]
	L += ["", "- 有效正文＝剝除對使用者說的話、扣除一字不差的重複句後的正文（Joe 裁 Q1–Q4 8daa6d2、區塊規則 CS c56d7bc）；判定沿用 v2 check_length、Word 算法，只換量的對象。",
	      "- Joe 裁 Q2：不保留交付物界定，故有效正文欄不再做界定（凍結 v2 欄照凍結件原樣，含界定）。"]

	L += cost_section(write_csv) + self_report_section(write_csv)

	# 附錄 A、單一做法版（問題二）
	S = av["single"]
	srow = []
	for mode in ("原", "有效正文未達改記未選"):
		for nm in NAMES:
			cells = []
			for a in ARMS3:
				x = S["%s｜%s｜%s" % (nm, mode, a)]["合併"]
				cells.append("%d：%d（%s）" % (x["架構"], x["裸"], fp(x["p"])))
			srow.append(["原判" if mode == "原" else "字數未達改記未選（探索性）", nm] + cells)
	same = [S["CS v2｜原｜%s" % a]["合併"]["同文"] for a in ARMS3]
	write_csv("pref_single.csv", ["口徑", "標註者", "整篇退回 vs 底（p）", "局部修補 vs 底（p）", "保守 vs 底（p）"], srow)
	L += ["", "## 附錄 A、架構內部各做法對底（單一做法版）——內部診斷", "",
	      "**內部診斷、下一步優化架構的判別方向**（Joe 6334b68 問題二：架構內部各做法的比較與挑選）。", "",
	      "算法：每次只看某一臂與底兩份。只選該臂＝架構；只選底＝裸；兩邊都選或都不選＝排除；該臂與底文字相同的題整題排除（同文）。合併 3B＋14B，精確二項雙尾；分卷見 pref_single.csv 來源檔。", "",
	      "| 口徑 | 標註者 | 整篇退回 vs 底 | 局部修補 vs 底 | 保守 vs 底 |", "| --- | --- | --- | --- | --- |"]
	L += ["| %s |" % " | ".join(r) for r in srow]
	L += ["| 同文排除題數（90 題） | | %d | %d | %d |" % tuple(same), "",
	      "- 三種做法共用同一批題、彼此不獨立，不做多重比較校正。"]
	return L
