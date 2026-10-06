# -*- coding: utf-8 -*-
"""句號級切分器 ＋ 以卷一 105 句做逐字迴歸。

**為什麼有這支腳本**：2026-10-02 放行令 §二.1 要「以卷一凍結切分腳本」產句子檔，
但卷一的 `test_sentences_105.jsonl` 是**聊天端**提交的（bridge commit `ed4066b`，
作者 `claude-chat`），執行端這側從來沒有那支腳本。

所以這裡**不自己發明規則**，而是從卷一的輸入（候選正取 20 篇原文）與輸出
（105 句）反推切分規則，再以卷一全卷做**逐字迴歸**：
規則若能把 20 篇原文切回與卷一完全相同的 105 句，它在效果上就是卷一那支切分器。
迴歸不過就停工回報，不拿一個沒驗證過的切法去切正式輪的卷。

反推出的規則（四條）：
  1. 先按換行切段；**換行本身丟棄**，空白段（含只有空白的段）丟棄。
  2. 段內按 `。？！?！` 切句，**標點保留在前句尾**。
  3. 每句去除前後空白（`\\t` 在句中者保留，例如 `1.\\t藍芽燈…`）。
  4. `.` **不是切點**——卷一「…把利潤減低. 」的切點是其後的換行，
     而「1.\\t」裡的 `.` 並未造成切裂。

放行令 §二.1 允許加的那一條後處理（孤立標點併入前句）也實作了，
但卷一迴歸顯示它在卷一零觸發（見報告），對卷二則據實回報觸發數。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
BR = Path("H:/Projects/Logical-AI-OS/laios-bridge/data/blindtest")

# 切點標點：`。` 與**半形** `?` `!`。
# **全形 ？！ 不是切點**——這是從卷一反推出來的，不是我選的：
# 卷一 85 個切點裡「。」62 個、半形「?」1 個、全形「？」0 個、全形「！」0 個；
# 而卷一的 B03（全形「！」處）與 B18（全形「？」處）在聊天端的卷一裡都
# **沒有**在該標點處斷開（**原句片段已去語料**）。先前把全形也當切點時，
# 這兩篇各多切一句（107 vs 105），改掉後 20 篇逐字全符。
SENT_END = "。?!"
# 孤立標點：整段只剩標點／空白，無任何文字內容
_ONLY_PUNCT = re.compile(r"^[\s。，、；：？！…—－\-·.,;:!?'\"“”‘’（）()「」『』【】《》\[\]]+$")


def split_text(text: str) -> tuple[list[str], int]:
	"""回傳（句列表, 孤立標點併入前句的次數）。"""
	out: list[str] = []
	merged = 0
	for line in text.split("\n"):
		if not line.strip():
			continue
		buf = ""
		pieces: list[str] = []
		for ch in line:
			buf += ch
			if ch in SENT_END:
				pieces.append(buf)
				buf = ""
		if buf:
			pieces.append(buf)
		for p in pieces:
			p = p.strip()
			if not p:
				continue
			# §二.1 允許的唯一後處理：孤立標點併入前句
			if _ONLY_PUNCT.match(p) and out:
				out[-1] = out[-1] + p
				merged += 1
				continue
			out.append(p)
	return out, merged


def regress_round1() -> bool:
	"""以卷一全卷做逐字迴歸。回傳是否全符。"""
	cand = [json.loads(l) for l in
	        (BR / "candidates_40.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
	gold = [json.loads(l) for l in
	        (BR / "test_sentences_105.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
	main20 = [x for x in cand if x["正備"] == "正"]
	want: dict[str, list[str]] = {}
	for g in gold:
		want.setdefault(g["篇"], []).append(g["句子"])

	print("## 卷一逐字迴歸（反推規則 vs 聊天端 `ed4066b` 的 105 句）")
	print()
	print("| 篇 | 期望句數 | 實得 | 逐字相同 | 孤立標點併入 |")
	print("| --- | --- | --- | --- | --- |")
	ok = True
	tot_got = tot_want = tot_merged = 0
	for i, r in enumerate(main20, 1):
		p = "B%02d" % i
		got, merged = split_text(r["text"])
		exp = want[p]
		same = got == exp
		ok &= same and len(got) == len(exp)
		tot_got += len(got)
		tot_want += len(exp)
		tot_merged += merged
		print("| %s | %d | %d | %s | %d |"
		      % (p, len(exp), len(got), "✓" if same else "**✗**", merged))
	print()
	print("合計：期望 **%d** 句、實得 **%d** 句；孤立標點併入 **%d** 次。"
	      % (tot_want, tot_got, tot_merged))
	print()
	if ok:
		print("**迴歸全符：20 篇、%d 句逐字相同。**" % tot_want)
		print("→ 本規則在效果上即卷一那支切分器，可用於卷二。")
	else:
		print("**迴歸不符——停工回報，不以未驗證的切法切正式輪的卷。**")
		for i, r in enumerate(main20, 1):
			p = "B%02d" % i
			got, _ = split_text(r["text"])
			if got != want[p]:
				print()
				print("### %s 不符明細" % p)
				for k in range(max(len(got), len(want[p]))):
					a = got[k] if k < len(got) else "（無）"
					b = want[p][k] if k < len(want[p]) else "（無）"
					if a != b:
						print("- s%02d 實得 `%s`" % (k + 1, a[:60]))
						print("  期望 `%s`" % b[:60])
	return ok


# 卷二逐篇期望句數：2026-10-02 **gold 修訂與放行令 v2（v2.1 答案本）** §二.2。
# 前令（bridge 1b48fa1）的 109 句規格已由該令明文作廢，故此處不留舊值。
EXPECT_R2 = {"C01": 4, "C02": 3, "C03": 6, "C04": 4, "C05": 4, "C06": 1, "C07": 4,
             "C08": 3, "C09": 4, "C10": 6, "C11": 6, "C12": 7, "C13": 12, "C14": 3,
             "C15": 5, "C16": 4, "C17": 9, "C18": 3, "C19": 6, "C20": 5}


# 卷三逐篇期望句數：2026-10-03 **卷三 gold 凍結與三臂放行令** §二.1（合計 97）。
EXPECT_R3 = {"D01": 3, "D02": 3, "D03": 3, "D04": 9, "D05": 7, "D06": 3, "D07": 3,
             "D08": 10, "D09": 3, "D10": 2, "D11": 4, "D12": 4, "D13": 8, "D14": 5,
             "D15": 7, "D16": 4, "D17": 4, "D18": 8, "D19": 3, "D20": 4}

# 卷四逐篇期望句數：2026-10-05 **卷四 gold 凍結與三臂放行令**（合計 116）。
EXPECT_R4 = {"E01": 8, "E02": 4, "E03": 3, "E04": 4, "E05": 7, "E06": 5, "E07": 4,
             "E08": 10, "E09": 3, "E10": 3, "E11": 6, "E12": 3, "E13": 4, "E14": 8,
             "E15": 5, "E16": 8, "E17": 4, "E18": 9, "E19": 13, "E20": 5}

# 卷五逐篇**草切**句數：2026-10-05 卷五 gold 凍結與兩臂放行令 §二（草切合計 118）。
# **這是參考值不是閘**——令文明訂「逐篇句數以 CC 正典切分為準」。
DRAFT_R5 = {"F01": 3, "F02": 6, "F03": 21, "F04": 3, "F05": 9, "F06": 7, "F07": 7,
            "F08": 2, "F09": 4, "F10": 4, "F11": 4, "F12": 12, "F13": 3, "F14": 4,
            "F15": 5, "F16": 5, "F17": 5, "F18": 3, "F19": 8, "F20": 3}

# 輪次設定表。**`split_text` 與卷一迴歸段一字不動**，只把輪次參數化：
#   候選檔／篇標前綴／期望句數／輸出檔／令文出處
ROUNDS = {
	"r2": {"cand": "round2/candidates_after_ruling.jsonl", "prefix": "C",
	       "expect": EXPECT_R2, "out": "round2/test_sentences_r2.jsonl",
	       "label": "卷二", "src": "gold 修訂與放行令 v2 §二.2"},
	"r3": {"cand": "round3/candidates_40.jsonl", "prefix": "D",
	       "expect": EXPECT_R3, "out": "round3/test_sentences_r3.jsonl",
	       "label": "卷三", "src": "卷三 gold 凍結與三臂放行令 §二.1"},
	"r4": {"cand": "round4/candidates_40.jsonl", "prefix": "E",
	       "expect": EXPECT_R4, "out": "round4/test_sentences_r4.jsonl",
	       "label": "卷四", "src": "卷四 gold 凍結與三臂放行令"},
	# 卷五：令文 §三.1 寫「**逐篇句數以 CC 正典切分為準**；與草切不同處逐筆列」，
	# 所以草切數字是**參考不是閘**（`gate: False`）——這與卷二～四不同，
	# 那幾卷的期望句數是令文指定、不合即停工。
	# 理由在令文 §二：F03／F12／F17 有孤立標點與斷行，正典併句後聊天端重對位。
	"r5": {"cand": "round5/candidates_40.jsonl", "prefix": "F",
	       "expect": DRAFT_R5, "out": "round5/test_sentences_r5.jsonl",
	       "label": "卷五", "src": "卷五 gold 凍結與兩臂放行令（**草切，參考值**）",
	       "gate": False},
	# 卷六：**沒有草切可比**——卷六是先出句子檔、聊天端才提 gold，
	# 所以 `expect` 不存在，也沒有期望句數閘。篇的選取改由**裁定**驅動：
	# `ruling` 的四個數字全部出自 orders/2026-10-06_卷六候選裁定令.md，CC 不自撰。
	"r6": {"cand": "round6/candidates_40.jsonl", "prefix": "G",
	       "out": "round6/test_sentences_r6.jsonl",
	       "label": "卷六", "src": "卷六候選裁定令（**裁定驅動組卷，無草切**）",
	       "gate": False,
	       "ruling": {"剔": [42, 59, 60],        # 序42 真程式題／序59 與序55 全等／序60 X0
	                  "遞補自": 61,              # 備取依序
	                  "最少句數": 300,           # 令文門檻
	                  "互斥取一": [[65, 68]]}},  # 近重複 0.950，先到先取，另一跳過
	# 卷七＝真正的畢業考（2026-10-06 F1規格形豁免與卷七令 §三）。
	# 候選處置**依卷六裁定例由 CC 自處**（令文授權），逐條落在 `ruling` 裡：
	#   真程式題／毒性／全等近重複 → 剔；文字工作 → 留；0.70~0.95 → 不剔。
	# 卷七實際只有一筆要判：序12（**原句已去語料**）命中「演算法」，
	# 但那是**文字改寫**（材料恰好是技術論文段落），與卷六留下的序41（論文評審）
	# 同型 → **留**。X0 零筆；卷內近重複零組（最高相似度 0.200）。
	# 所以 `剔` 是空的——**空不是沒查，是查完沒有該剔的**。
	"r7": {"cand": "round7/candidates_40.jsonl", "prefix": "H",
	       "out": "round7/test_sentences_r7.jsonl",
	       "label": "卷七", "src": "卷七令（**裁定例自處，無草切**）",
	       "gate": False,
	       "ruling": {"剔": [],                  # 依卷六例查完：無該剔者
	                  "遞補自": 61,              # 備取依序
	                  "最少句數": 300,           # 令文門檻
	                  "互斥取一": []}},          # 卷內近重複 0 組，無互斥組
}


def _apply_ruling(cand: list[dict], ruling: dict) -> tuple[list[dict], dict]:
	"""照裁定組卷。**四個數字全部來自令文，本函式不含任何自撰判準。**

	順序嚴格照令文字面：
	  1. 正取剔掉 `剔` 列的序；
	  2. 不足 `最少句數` 時，自 `遞補自` 起的備取**依序**遞補；
	  3. `互斥取一` 的組內先到先取，另一**跳過**（不是停工，令文寫「跳過」）；
	  4. 一旦達到門檻即停——令文寫「補至 ≥300 句」，不是「補滿」。

	句數認定一律走 `split_text`（正典切分），與卷檔同一支，不另計。
	"""
	by = {r["序"]: r for r in cand}
	drop = set(ruling["剔"])
	kept = [r for r in cand if r["正備"] == "正" and r["序"] not in drop]
	n = sum(len(split_text(r["text"])[0]) for r in kept)
	taken, skipped = [], []
	# 互斥組：組內只要已取過一篇，同組其餘一律跳過
	groups = [set(g) for g in ruling.get("互斥取一", [])]
	picked_in = [None] * len(groups)
	for seq in sorted(s for s in by if by[s]["正備"] == "備"):
		if n >= ruling["最少句數"]:
			break
		if seq < ruling["遞補自"]:
			continue
		gi = next((i for i, g in enumerate(groups) if seq in g), None)
		if gi is not None and picked_in[gi] is not None:
			skipped.append((seq, "與序%d 互斥（近重複），令文「只准取其一」"
			                % picked_in[gi]))
			continue
		r = by[seq]
		kept.append(r)
		taken.append((seq, len(split_text(r["text"])[0])))
		n += len(split_text(r["text"])[0])
		if gi is not None:
			picked_in[gi] = seq
	return kept, {"剔": sorted(drop), "遞補": taken, "跳過": skipped,
	              "句數": n, "門檻": ruling["最少句數"]}


def build_round(cfg: dict, write: bool) -> bool:
	cand = [json.loads(l) for l in
	        (BR / cfg["cand"]).read_text(encoding="utf-8").splitlines()
	        if l.strip()]
	ruling = cfg.get("ruling")
	if ruling:
		main20, fill_log = _apply_ruling(cand, ruling)
		EXPECT = None
	else:
		main20 = [x for x in cand if x["正備"] == "正"]
		assert len(main20) == 20, "正取不是 20 篇，停工"
		EXPECT = cfg["expect"]
		fill_log = None

	print()
	print("## %s切分與對齊核驗（期望句數由%s指定）" % (cfg["label"], cfg["src"]))
	print()
	gate = cfg.get("gate", True)
	has_exp = EXPECT is not None
	if fill_log:
		print("### 裁定套用（令文 §裁定，CC 不自撰）")
		print()
		print("| 項 | 值 |")
		print("| --- | --- |")
		print("| 剔除序 | **%s** |"
		      % ("／".join("序%d" % x for x in fill_log["剔"])
		         or "無（依例查完，沒有該剔的）"))
		print("| 遞補序（句數） | **%s** |"
		      % ("／".join("序%d（%d 句）" % t for t in fill_log["遞補"])
		         or "—"))
		print("| 互斥跳過 | %s |"
		      % ("；".join("序%d：%s" % t for t in fill_log["跳過"]) or "無"))
		print("| 組卷篇數 | **%d** |" % len(main20))
		print("| 句數 ／ 門檻 | **%d** ／ %d%s |"
		      % (fill_log["句數"], fill_log["門檻"],
		         " ✓" if fill_log["句數"] >= fill_log["門檻"] else " **不足**"))
		print()
	if has_exp:
		print("| 篇 | 候選序 | %s | 實得 | %s | 孤立標點併入 |"
		      % ("令文期望" if gate else "草切（參考）", "合否" if gate else "差"))
		print("| --- | --- | --- | --- | --- | --- |")
	else:
		print("| 篇 | 候選序 | 正備 | 實得句數 | 孤立標點併入 |")
		print("| --- | --- | --- | --- | --- |")
	rows = []
	ok = True
	diffs = []
	tot = tot_merged = 0
	for i, r in enumerate(main20, 1):
		p = "%s%02d" % (cfg["prefix"], i)
		got, merged = split_text(r["text"])
		tot += len(got)
		tot_merged += merged
		if not has_exp:
			print("| %s | %d | %s | **%d** | %d |"
			      % (p, r["序"], r["正備"], len(got), merged))
			task = ";".join(got)
			for k, sent in enumerate(got, 1):
				rows.append({"id": "%s/s%02d" % (p, k), "篇": p,
				             "任務": task, "句子": sent})
			continue
		exp = EXPECT[p]
		hit = len(got) == exp
		ok &= hit
		if len(got) != exp:
			diffs.append((p, exp, len(got), len(got) - exp, merged,
			              "孤立標點併入 %d 次" % merged if merged
			              else "切點數不同（斷行／標點）"))
		if gate:
			print("| %s | %d | %d | **%d** | %s | %d |"
			      % (p, r["序"], exp, len(got), "✓" if hit else "**✗**", merged))
		else:
			d = len(got) - exp
			print("| %s | %d | %d | **%d** | %s | %d |"
			      % (p, r["序"], exp, len(got),
			         "—" if d == 0 else "**%+d**" % d, merged))
		task = ";".join(got)
		for k, sent in enumerate(got, 1):
			rows.append({"id": "%s/s%02d" % (p, k), "篇": p, "任務": task, "句子": sent})
	print()
	print("| 項 | 值 |")
	print("| --- | --- |")
	if has_exp:
		print("| %s合計 | **%d** |"
		      % ("令文期望" if gate else "草切（參考）", sum(EXPECT.values())))
	print("| 實得合計 | **%d** |" % tot)
	if has_exp:
		print("| 逐篇全合 | %s |" % ("**是**" if ok else "**否**"))
	print("| 孤立標點併入前句 | %d 次 |" % tot_merged)
	if has_exp and not gate:
		print()
		print("**草切是參考值不是閘**（令文 §三.1：逐篇句數以 CC 正典切分為準）。")
		print("與草切不同的篇逐筆如下，供聊天端重對位：")
		print()
		print("| 篇 | 草切 | 正典切分 | 差 | 孤立標點併入 | 成因 |")
		print("| --- | --- | --- | --- | --- | --- |")
		for d in diffs:
			print("| %s | %d | **%d** | **%+d** | %d | %s |" % d)

	if gate and not ok:
		print()
		print("**逐篇句數不合——停工回報，不自行裁句。**")
		return False
	if write:
		out = BR / cfg["out"]
		out.parent.mkdir(parents=True, exist_ok=True)
		out.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in rows) + "\n",
		               encoding="utf-8")
		import hashlib
		h = hashlib.sha256(out.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
		print()
		print("已寫出 `data/blindtest/%s`（%d 句，%d bytes，sha256 `%s`）。"
		      % (cfg["out"], len(rows), out.stat().st_size, h))
	return True


def main() -> None:
	rnd = next((r for r in ("r7", "r6", "r5", "r4", "r3", "r2")
	            if "--round=%s" % r in sys.argv), "r2")
	cfg = ROUNDS[rnd]
	print("# %s句子檔：切分器反推、卷一迴歸、%s對齊核驗" % (cfg["label"], cfg["label"]))
	print()
	# 卷一迴歸是每次都跑的前置閘：規則若動過，它會先死在這裡。
	if not regress_round1():
		raise SystemExit("卷一迴歸不過，停工")
	if not build_round(cfg, write="--write" in sys.argv):
		raise SystemExit("%s逐篇句數不合，停工" % cfg["label"])


if __name__ == "__main__":
	main()
