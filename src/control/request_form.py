# -*- coding: utf-8 -*-
"""請求形特徵枚舉器（刀1-R；2026-10-05 刀1R 重設計令 §一.2）。

令文紀律，逐條落實：

> **請求形特徵＝機械層既有凍結特徵**（請求動詞「幫我/請/麻煩」、要求標記
> 「要求/需要/必須/切忌」、條列編號行首、祈使句式）——**嚴禁新增任何從
> 卷一~三漏抓句習得之具體詞**；特徵清單由 CC 自機械層凍結碼中枚舉引用，
> 逐條列出處，聊天端覆核。

所以本檔**一個字面詞都不寫**。每一條特徵都是
（a）呼叫 `detectors.py` 的凍結函式，或
（b）讀 `lexicon_v2.py` 的凍結表，
詞表內容在 import 時才取得。本檔若被改成內含詞串，`self_audit()` 會當場抓出來。

## 令文四族 → 凍結件對位（缺的照實報，不補）

| 令文所舉 | 凍結件 | 狀態 |
| --- | --- | --- |
| 請求動詞「幫我/請/麻煩」 | `IMPERATIVE["請求標記"]`（閉集，經左／右／受詞／程度四守衛） | **有** |
| 要求標記「需要」 | `IMPERATIVE["想要標記"]` | **有** |
| 要求標記「要求」 | 只存在於 `REPORTED["引語動詞"]` | **語義反向，不取**（見 F_NOTES） |
| 要求標記「必須」「切忌」 | 全機械層凍結碼**查無** | **缺**（新增＝判準層物件，需 PI 簽） |
| 條列編號行首 | 無任何偵測器；表五只有句中字面「條列／列點」 | **缺**（同上） |
| 祈使句式 | `D.mood_v2()` 標籤（`imperative_evidence` ＋ `MOOD_ASPECT["祈使體構式"]`） | **有** |

`要求` 不取的理由寫在 F_NOTES["F2b"]：它在凍結碼裡的身分是**引語動詞**，
命中代表「第三方的要求被敘述出來」（軸一規則 1 引述否決的材料），
拿它當請求形特徵會把方向接反。這不是我省略了令文一項，是**凍結碼裡那個詞的語義
與令文想要的語義相反**，照實報，不自行改表。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_MECH = ROOT / "experiments/mechanical-v2"
if str(_MECH) not in sys.path:
	sys.path.insert(0, str(_MECH))

import detectors as D          # noqa: E402  凍結件，只呼叫不改寫
import lexicon_v2 as L         # noqa: E402  凍結件，只讀不改寫

# ── 特徵定義：每一條只呼叫凍結函式 ────────────────────────────────────────────
# 回傳 (命中?, 證據)。證據一律是凍結件自己吐出來的物件，不另行描述。


def f1_request_marker(text: str):
	"""F1 請求動詞：`D.imperative()` 的 `請求標記` 命中（已過四守衛）。"""
	r = D.imperative(text)
	return bool(r["命中"]), [h["term"] for h in r["hits"]]


def f2_want_marker(text: str):
	"""F2 要求／想要標記：`D.imperative()` 的 `想要標記` 命中（含「需要」）。"""
	r = D.imperative(text)
	return bool(r["想要標記"]), [h["term"] for h in r["想要標記"]]


def f3_mood_imperative(text: str):
	"""F3 祈使句式：`D.mood_v2()` 標籤判祈使（或祈使與疑問並存的混合）。"""
	m = D.mood_v2(text)
	return m["標籤"] in ("祈使", "混合"), {"標籤": m["標籤"], "祈使證據": m["祈使證據"]}


def f4_imperative_evidence(text: str):
	"""F4 祈使證據非空：`D.imperative_evidence()`（F1 ∪ 句尾就夠型 ∪ 求＋動詞 ∪ 祈使動詞）。"""
	ev = D.imperative_evidence(text)
	return bool(ev), ev


def f5_imperative_construction(text: str):
	"""F5 祈使體構式：`MOOD_ASPECT["祈使體構式"]` 三條正則（位置條件，非裸詞）。"""
	hits = D.scan_re(text, L.MOOD_ASPECT["祈使體構式"])
	return bool(hits), [h["term"] for h in hits]


FEATURES = {
	"F1_請求動詞": (f1_request_marker,
	             "lexicon_v2.py:111 IMPERATIVE[請求標記] ＋ detectors.py:153 imperative()"),
	"F2_想要標記": (f2_want_marker,
	             "lexicon_v2.py:112 IMPERATIVE[想要標記] ＋ detectors.py:172 imperative()"),
	"F3_語氣祈使": (f3_mood_imperative,
	             "detectors.py:351 mood_v2() 標籤 ∈ {祈使, 混合}"),
	"F4_祈使證據": (f4_imperative_evidence,
	             "detectors.py:292 imperative_evidence()（IMP_VERBS/IMP_TAIL，detectors.py:273-285）"),
	"F5_祈使體構式": (f5_imperative_construction,
	              "lexicon_v2.py:316 MOOD_ASPECT[祈使體構式] ＋ detectors.py:74 scan_re()"),
}

# ── 令文四族的「取」與「不取」──────────────────────────────────────────────────
# 第一級的布林值＝令文四族中**凍結件存在且語義同向**者的聯集。
# 為什麼是這三條、不是五條：F4／F5 是 F1／F3 的上下位（F4 ⊇ F1，F3 由 F4 導出），
# 把它們也放進聯集不會改變聯集值，只會讓「哪一條開火」失去可讀性。
# **不是我按開發集表現挑的**——F4／F5 的逐卷命中率在報告裡照樣全出，供覆核。
PRIMARY = ("F1_請求動詞", "F2_想要標記", "F3_語氣祈使")

F_NOTES = {
	"F2b_要求": "凍結碼裡「要求」的身分是 REPORTED[引語動詞]（lexicon_v2.py:173），"
	          "命中代表第三方要求被敘述（軸一規則 1 引述否決的材料）。"
	          "語義與令文想要的「說話者提出要求」**相反**，故不取。"
	          "lexicon_v2.py:200 的 trap 正是「我爸的要求是一定要買日系的」＝真引述。",
	"必須": "全機械層凍結碼查無此詞形（lexicon_v2.py／detectors.py／rules_v2.py 皆無）。"
	      "新增＝動判準層詞表，條款 1 要 PI 簽，CC 不自撰。",
	"切忌": "同上，查無。",
	"條列編號行首": "無任何偵測器處理行首編號結構。"
	           "表五 v2_writing_spec_form 有「條列」「列點」（lexicon_v2.py:430-431），"
	           "但那是**句中字面詞**（格式結構形），不是「行首 1./①/一、」的版面結構。"
	           "且正典切分器以換行切段並丟棄換行，**句子層看不到行首**——"
	           "這一族要上線得先改切分器（判準層），不在本刀範圍。",
}


def request_form(text: str) -> dict:
	"""逐句算出全部五條特徵 ＋ 第一級布林值。"""
	out, ev = {}, {}
	for k, (fn, _src) in FEATURES.items():
		hit, e = fn(text)
		out[k] = hit
		ev[k] = e
	return {"特徵": out, "證據": ev,
	        "帶請求形特徵": any(out[k] for k in PRIMARY),
	        "命中條": [k for k in PRIMARY if out[k]]}


def provenance() -> list[dict]:
	"""特徵清單 ＋ 出處 ＋ 當場從凍結表讀出的詞形內容（供聊天端覆核）。"""
	rows = []
	for k, (_fn, src) in FEATURES.items():
		if k == "F1_請求動詞":
			terms = list(L.IMPERATIVE["請求標記"])
			guards = {"左守衛": L.IMPERATIVE["左守衛"], "右守衛": L.IMPERATIVE["右守衛"],
			          "受詞守衛_不觸發": L.IMPERATIVE["受詞守衛_不觸發祈使"],
			          "受詞守衛_豁免": L.IMPERATIVE["受詞守衛_豁免標記"],
			          "麻煩_程度守衛": L.IMPERATIVE["麻煩_程度守衛"]}
		elif k == "F2_想要標記":
			terms, guards = list(L.IMPERATIVE["想要標記"]), {}
		elif k == "F3_語氣祈使":
			terms, guards = ["（構式，無裸詞）"], {"判準": L.MOOD_ASPECT["判準"]}
		elif k == "F4_祈使證據":
			terms = list(D.IMP_VERBS)
			guards = {"IMP_TAIL": D.IMP_TAIL, "INTENT_LEFT": D.INTENT_LEFT,
			          "VERB_RIGHT": D.VERB_RIGHT,
			          "完成貌／繫詞否決": {"PERFECTIVE": D.PERFECTIVE, "COPULA": D.COPULA}}
		else:
			terms, guards = list(L.MOOD_ASPECT["祈使體構式"]), {}
		rows.append({"特徵": k, "出處": src, "凍結內容": terms, "守衛": guards,
		             "入第一級": k in PRIMARY})
	return rows


def self_audit() -> list[str]:
	"""五條特徵函式體內不得出現「用來比對的中文字面值」。

	那正是令文禁止的「新增具體詞」。稽核面**只取五個特徵函式的原始碼**——
	比對只可能發生在那裡（docstring／出處字串／report 的格式字串都不參與比對，
	把它們掃進來只會把稽核變成雜訊，反而掩蓋真違規）。

	允許的中文字面值只有兩類，兩類都**不是詞**：
	  (a) 凍結表的 key（`請求標記`／`想要標記`／`命中`…）——拿它去 index 凍結表；
	  (b) 凍結件自己的回傳標籤值（`祈使`／`混合`）——拿它去比對 `mood_v2` 的輸出。
	其餘任何含中日韓字的字串常值 ＝ 違規。
	"""
	import inspect
	import re
	allowed = set()
	for d in (L.IMPERATIVE, L.MOOD_ASPECT):
		allowed |= {str(k) for k in d}
	allowed |= {"命中", "標籤", "祈使證據", "hits", "term"}      # 凍結件回傳欄名
	# 允許的標籤值＝**凍結函式自己原始碼裡的那組字面值**，不由我列舉。
	allowed |= set(re.findall(r'"([^"\n]*)"', inspect.getsource(D.mood_v2)))
	bad = []
	for k, (fn, _src) in FEATURES.items():
		body = inspect.getsource(fn)
		body = re.sub(r'"""(?:.|\n)*?"""', "", body)
		body = re.sub(r"(?m)#.*$", "", body)
		for m in re.finditer(r'"([^"\n]*)"', body):
			s = m.group(1)
			if re.search(r"[㐀-鿿]", s) and s not in allowed:
				bad.append("%s: %r" % (k, s))
	return bad


if __name__ == "__main__":
	import json
	sys.stdout.reconfigure(encoding="utf-8")
	bad = self_audit()
	print("# 請求形特徵清單（刀1-R §一.2；自機械層凍結碼枚舉）")
	print()
	print("自檢：本檔可執行行內的非結構字面詞 = %s"
	      % ("**0**（無新增具體詞）" if not bad else "**違規** %s" % bad))
	print()
	for r in provenance():
		print("## %s%s" % (r["特徵"], "　**（入第一級）**" if r["入第一級"] else "　（僅報，不入第一級）"))
		print()
		print("- 出處：`%s`" % r["出處"])
		print("- 凍結內容（import 時自表讀出，共 %d 項）：%s"
		      % (len(r["凍結內容"]), "、".join("`%s`" % t for t in r["凍結內容"])))
		if r["守衛"]:
			print("- 守衛：`%s`" % json.dumps(r["守衛"], ensure_ascii=False))
		print()
	print("## 令文所舉但凍結碼缺／不同向者（照實報，不補）")
	print()
	for k, v in F_NOTES.items():
		print("- **%s**：%s" % (k, v))
	print()
	print("第一級布林值 ＝ %s 的聯集。" % " ∪ ".join("`%s`" % k for k in PRIMARY))
