# -*- coding: utf-8 -*-
"""v2 偵測器本體。**零模型呼叫。**

憲法（README 2026-09-10）：
  禁開放類子字串裸掃；**封閉類訊號 ＋ 詞邊界 ＋ 構式 ＝ 合法機械**。
  凡偵測器必附詞邊界處理 ＋ 雙向單元測例。

本檔只做一件事：把 `lexicon_v2` 的表變成會回報**位置**的偵測函式。
所有比對一律走 `scan()`，**沒有任何一處直接用 `in`**——
因為 `in` 就是裸子字串比對，那正是四次復發的病灶。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
	sys.path.insert(0, str(HERE))
if "H:/Projects/Logical-AI-OS/scripts" not in sys.path:
	sys.path.insert(0, "H:/Projects/Logical-AI-OS/scripts")

import lexicon_v2 as L
from canon_v3.prompts import detect_table5_constraint_cues


# ============================================================================
# 詞邊界比對核心
# ============================================================================
def _covered_by(text: str, index: int, length: int, blockers: tuple) -> bool:
	"""命中是否整段落在某個 blocker 詞的範圍內（例如「他」落在「其他」裡）。"""
	for b in blockers:
		start = 0
		while True:
			i = text.find(b, start)
			if i < 0:
				break
			if i <= index and index + length <= i + len(b):
				return True
			start = i + 1
	return False


def scan(text: str, terms, *, left=None, right=None, blockers=()) -> list[dict]:
	"""封閉類詞表比對，**帶詞邊界**。

	`left`／`right`：{詞: (守衛字,...)}。守衛字出現在該位置時，這一次命中作廢。
	`blockers`：整段包住命中的詞（`想說` 之於 `說`），命中作廢。
	"""
	hits = []
	for t in terms:
		if not t:
			continue
		start = 0
		while True:
			i = text.find(t, start)
			if i < 0:
				break
			start = i + 1
			if blockers and _covered_by(text, i, len(t), blockers):
				continue
			lg = (left or {}).get(t, ())
			if lg and i > 0 and text[i - 1] in lg:
				continue
			rg = (right or {}).get(t, ())
			end = i + len(t)
			if rg and end < len(text) and text[end] in rg:
				continue
			hits.append({"term": t, "start": i, "end": end})
	return sorted(hits, key=lambda h: (h["start"], -len(h["term"])))


def scan_re(text: str, patterns) -> list[dict]:
	out = []
	for p in patterns:
		for m in re.finditer(p, text):
			out.append({"term": m.group(0), "start": m.start(), "end": m.end(), "pattern": p})
	return sorted(out, key=lambda h: h["start"])


# ============================================================================
# 1 人稱
# ============================================================================
def person(text: str) -> dict:
	P = L.PERSON
	first = scan(text, P["第一人稱"], left=P["左守衛"])
	second = scan(text, P["第二人稱"], left=P["左守衛"])
	third = scan(text, P["第三人稱"], left=P["左守衛"])
	# 領屬複合：第一人稱後方 0~1 字接關係名詞 → 指第三方
	poss = []
	for h in first:
		tail = text[h["end"]: h["end"] + 4]
		for r in P["關係名詞"]:
			if tail.startswith(r):
				poss.append({"term": h["term"] + r, "start": h["start"],
				             "end": h["end"] + len(r)})
				break
	# 非指稱名詞單獨出現不算第三方
	nonref = scan(text, P["非指稱名詞"])
	label = "沒掛人"
	if third or poss:
		label = "第三方"
	elif second:
		label = "你"
	elif first:
		label = "我"
	return {"我": first, "你": second, "第三方": third, "領屬複合": poss,
	        "非指稱": nonref, "標籤": label,
	        "有第三方主語": bool(third or poss)}


# ============================================================================
# 2 疑問
# ============================================================================
def interrogative(text: str) -> dict:
	Q = L.INTERROGATIVE
	terms = (Q["疑問詞"] + Q["句尾語氣"] + Q["正反問"] + Q["提問動詞"]
	         + Q["選擇連詞"] + Q["句尾標點"])
	hits = scan(text, terms, left=Q["左守衛"], right=Q["右守衛"])
	# 句尾語氣詞只在句尾才算
	body = text.rstrip("，。？！；,.?!; ")
	hits = [h for h in hits
	        if h["term"] not in Q["句尾語氣"] or h["end"] >= len(body)]
	anb = scan_re(text, (Q["A不A構式"],))
	all_hits = hits + anb

	# --- 裁一（PI 2026-09-10）：「幾」歧義規則 ---
	# 疑問訊號**只有**「幾」、且是「幾＋量詞」、且句中無其他提問訊號 → 不觸發疑問。
	# 守衛層做不到這件事（`現在幾點` 也是幾＋量詞），因為條件是**句子層**的：
	# 要看整句還有沒有別的提問訊號。所以它是規則，不是守衛。
	# 註：`現在幾點` 之所以照樣命中，是因為「點」在 canon_v3 的 MEASURE_WORD_EXCLUSIONS 裡
	# （下／點／些／會／陣／打），本表的量詞集沿用那個判斷，不另立。
	suppressed = None
	if all_hits and all(h["term"] == "幾" for h in all_hits):
		h = all_hits[0]
		tail = text[h["end"]:]
		is_quantity = any(tail.startswith(u) for u in Q["幾_後接量詞"])
		others = [o for o in Q["其他提問訊號"] if o != "幾" and o in text]
		if is_quantity and not others:
			suppressed = {"why": "裁一：僅『幾』且幾＋量詞且無其他提問訊號", "hits": all_hits}
			all_hits = []
	return {"hits": all_hits, "命中": bool(all_hits), "裁一抑制": suppressed}


# ============================================================================
# 3 祈使
# ============================================================================
# 終測案二（PI 2026-09-18，一發制）：程度副詞閉集＋麻煩 → 不觸發祈使。詞表與出處見 lexicon_v2。
CASE2_DEGREE_GUARD = True


def imperative(text: str) -> dict:
	I = L.IMPERATIVE
	raw = scan(text, I["請求標記"], left=I["左守衛"], right=I["右守衛"])
	kept, dropped = [], []
	for h in raw:
		t = h["term"]
		if CASE2_DEGREE_GUARD and t == "麻煩":
			head = text[:h["start"]]
			if any(head.endswith(d) for d in I["麻煩_程度守衛"]):
				dropped.append({**h, "why": "程度守衛：程度副詞＋麻煩＝形容詞"})
				continue
		if t in I["帶受詞的請託動詞"] and t not in I["受詞守衛_豁免標記"]:
			tail = text[h["end"]:]
			if any(tail.startswith(o) for o in I["受詞守衛_不觸發祈使"]):
				dropped.append({**h, "why": "受詞守衛：受詞是說話者或第三方"})
				continue
		kept.append(h)
	want = scan(text, I["想要標記"])
	return {"hits": kept, "受詞守衛擋下": dropped, "想要標記": want,
	        "命中": bool(kept)}


# ============================================================================
# 4 引述框
# ============================================================================
_PUNC_CHARS = "，。、；！？,.;!?…\n "


def reported(text: str) -> dict:
	"""引述框。

	--- 修一之三：B08 查案（PI 2026-09-18「先攤實作原因再修，不准悄悄改」）---
	**查案結果：`引語動詞` 這一欄算出來之後從未接進 `命中`。**
	舊版 `命中 = bool(frame or hear)`，整張引語動詞表（說／講／要求／建議…11 個詞）
	對下游是**死欄位**——B08「藥師建議…」的 `建議` 有命中該欄，但引述框仍回 False。

	**而單元測試看不見這件事**：`test_detectors.hit_of` 斷言在
	`轉述框 + 傳聞 + 引語動詞` 的**聯集**上，供應端算了就算綠，
	消費端（`命中`）根本沒讀那一欄。所以詞表裡「我爸的**要求**是一定要買日系的 →
	**應**命中」這條 trap 長期顯示綠燈，實測 `命中=False`。
	**這是 CLAUDE.md 條款 5「消費端對供應端的契約假設未經驗證」的第五次同型病灶。**

	--- 修法：引語構式三條件（不是把裸詞接上去）---
	`寫`／`開` 是開放類動詞，憲法禁裸掃；既有 11 個詞同樣是動詞，一併走構式：
	  (1) 動詞命中且不被「構詞排除」整段包住（開會／填寫／離開…）
	  (2) 右方直接接**引述內容**：非標點、非體貌／補語標記（寫了／開起／問題…）
	  (3) 句子人稱標籤 ≠「我」——第一人稱自述不是轉述別人（詞表 note 原本就寫了聯用）
	轉述框與傳聞標記照舊直接命中（它們本身就是構式／多字閉集）。
	"""
	R = L.REPORTED
	frame = scan(text, R["轉述框"], blockers=R["排除"])
	hear = scan(text, R["傳聞標記"], blockers=R["排除"])
	verb = scan(text, R["引語動詞"],
	            right=R["引語動詞_右守衛"],
	            blockers=R["排除"] + R["傳聞標記"] + R["轉述框"] + R["引語動詞_構詞排除"])
	first_person = person(text)["標籤"] == "我"
	quoting = []
	for h in verb:
		tail = text[h["end"]:]
		if not tail or tail[0] in _PUNC_CHARS:
			continue                                  # 條件 2：右方沒有引述內容
		if first_person:
			continue                                  # 條件 3：第一人稱自述
		quoting.append(h)
	return {"轉述框": frame, "傳聞": hear, "引語動詞": verb, "引語構式": quoting,
	        "命中": bool(frame or hear or quoting)}


# ============================================================================
# 5 反問框
# ============================================================================
def rhetorical(text: str) -> dict:
	hits = scan_re(text, L.RHETORICAL["正則"])
	return {"hits": hits, "命中": bool(hits)}


# ============================================================================
# 6 認知框
# ============================================================================
def cognitive(text: str) -> dict:
	C = L.COGNITIVE
	terms = C["斟酌"] + C["不確定"] + C["困惑"] + C["推測"] + C["擔憂"]
	hits = scan(text, terms, left=C["左守衛"], right=C["右守衛"])
	return {"hits": hits, "命中": bool(hits)}


# ============================================================================
# 8 空框
# ============================================================================
def empty_frame(text: str) -> dict:
	E = L.EMPTY_FRAME
	opens = scan(text, E["開口標記"])
	best = None
	for o in opens:
		tail = text[o["end"]:]
		for w in E["空內容詞"]:
			if tail.startswith(w):
				best = {"term": o["term"] + w, "start": o["start"], "end": o["end"] + len(w)}
				break
		if best:
			break
	if not best:
		return {"命中": False, "片語": None}
	rest = text[:best["start"]] + text[best["end"]:]
	return {"命中": not interrogative(rest)["命中"], "片語": best,
	        "扣除後剩餘": rest}


# ============================================================================
# 9 語氣體貌 ＋ 10 時間錨（裁三重建版，pattern 由 279 句草標的**建半**歸納）
# ============================================================================
# 舊版兩側都要正面證據，滿手「未定」（非限制側語氣 15/21 未定、時間 19/21 未定），
# 軸二規則 4 因此 0/21 開火。草標分佈說明了為什麼：
# **敘述 182／疑問 53／祈使 32／混合 12——敘述是無標記的多數，祈使才是有標記的。**
# 新版改單邊舉證，「未定」這個值結構上不存在。
# held-out 驗收（141 句，只跑一次）：祈使／敘述 83.5%、未定率 6.4%，兩線皆過。
#
# **代價照實記**：預設值吃掉所有沒被 pattern 接到的句子，
# 敘述的正確率被墊高（驗半 86.3%），**祈使召回才是真正被考的**（驗半 64.3%）。

IMP_VERBS = ("挑", "選", "買", "做", "交", "用", "裝在", "裝", "註冊", "換成", "改成",
             "找", "訂", "排", "壓在", "統一用", "統一", "安排", "推薦")
IMP_TAIL = (r"就夠", r"就可以", r"就好", r"即可")
PERFECTIVE = (r"[^，。]{1,12}了", r"[^，。]{1,12}過[^，。]{0,8}[，。]?$")
COPULA = (r"是[^，。]{1,16}的[，。]?$", r"^[^，。]{0,10}是[^，。]{2,}")

# --- 第一輪修正（只看建半）---
# 錯誤群 B：`想買／想從眼鏡換成／想去做` 被判祈使。
# 標註端邊界政策第 4 條寫得很清楚：「我想知道…」→ 敘述（**陳述意圖，無指令形**）。
# 所以意圖標記在祈使動詞左邊時，那次命中作廢。
INTENT_LEFT = ("想", "要", "會", "沒", "被", "在", "很", "都", "還")
# `用不到`／`訂房` 這種動詞併進複合詞的，右邊守衛擋掉。
VERB_RIGHT = {"用": ("不", "到", "來", "了"), "訂": ("房",), "做": ("了",), "買": ("了",)}


def _has(text: str, pats) -> bool:
	return any(re.search(p, text) for p in pats)


def imperative_evidence(text: str) -> list[str]:
	ev = []
	if imperative(text)["命中"]:
		ev.append("請求標記")
	if _has(text, IMP_TAIL):
		ev.append("句尾就夠型")
	if re.search(r"^求.{1,6}", text):
		ev.append("求＋動詞")
	if not _has(text, PERFECTIVE) and not _has(text, COPULA):
		for v in IMP_VERBS:
			for h in scan(text, (v,), right={v: VERB_RIGHT.get(v, ())}):
				if h["start"] > 0 and text[h["start"] - 1] in INTENT_LEFT:
					continue                      # 意圖標記：想買／要做／還用
				tail = text[h["end"]:].strip("，。 ")
				if len(tail) >= 1:
					ev.append("祈使動詞:%s" % v)
					break
			if ev and ev[-1].startswith("祈使動詞"):
				break
	return ev


# --- 第一輪修正（只看建半）---
# 錯誤群 A：19 句 gold 敘述被疑問偵測器接走。逐句看是四種非疑問用法：
#   說什麼（引語，不是提問）／還是＝仍然（副詞，不是選擇連詞）／
#   三十幾、六十幾（概數，不是提問）／句尾「吧」揣測（標註端政策第 3 條 → 敘述）
# 以及標註端政策第 1 條：**句中嵌入的自問、主幹為陳述 → 敘述**（認知框命中者）。
NOT_QUESTION_BLOCKERS = ("說什麼", "沒什麼", "算什麼", "為什麼都", "什麼的")

# 刀1-D 軸一誤命中守衛（三條令文守衛 ＋ CC 增設的 2'）**已依 2026-10-06
# 刀1CD 裁決與刀2 開量令 §二 撤除**：四條在 619 句上全部零句級作用。
# 撤除理由（量過的，證物在 reports/2026-10-06_刀1CD_report.md §三）：
#   (1) `想要標記` 不餵軸一（唯一消費端是 ASK 排序的 request_form.py）；
#   (2) `NOT_QUESTION_BLOCKERS` 只餵 question_evidence()→mood_v2，
#       而軸一讀的 interrogative() 依設計不吃 blocker（「寧可多接」）；
#   (3) 「來一個」落在敘述語氣的唯一一筆，軸一本來就是非請求；
#   (2') 守衛進 interrogative() 碰得到軸一，但靶心句 E17/s02 的主請求
#        由「什麼」與「如何」雙來源撐住，句級一動也沒動。
# D 型真病灶（嵌入疑問「學會了如何X」14 句）**掛帳不開站**（令文 §二）。
STILL_ADVERB = (r"還是[那這]樣", r"還是[想要會不]", r"還是[硬軟好壞]", r"還是沒")
APPROX_NUM = r"[0-9０-９一二兩三四五六七八九十百千萬]幾"


def question_evidence(text: str) -> bool:
	"""供語氣體貌用的提問判定——**比原始疑問偵測器嚴**。

	原始偵測器負責軸一的請求判定，寧可多接；
	語氣體貌問的是「這句的語氣是不是在發問」，嵌入的自問不算。
	"""
	if cognitive(text)["命中"]:
		return False                              # 政策 1：嵌入自問、主幹陳述
	hits = [h["term"] for h in interrogative(text)["hits"]]
	if not hits:
		return False
	kept = []
	for t in hits:
		if t == "什麼" and any(scan(text, (b,)) for b in NOT_QUESTION_BLOCKERS):
			continue
		if t == "還是" and _has(text, STILL_ADVERB):
			continue
		if t == "幾" and re.search(APPROX_NUM, text):
			continue
		if t == "吧":
			continue                              # 政策 3：吧尾揣測 → 敘述
		if t in ("想知道", "想了解"):
			continue                              # 政策 4：陳述意圖，無指令形
		kept.append(t)
	return bool(kept)


def mood_v2(text: str) -> dict:
	imp = imperative_evidence(text)
	q = question_evidence(text)
	if imp and q:
		label = "混合"
	elif imp:
		label = "祈使"
	elif q:
		label = "疑問"
	else:
		label = "敘述"          # **預設值**：無標記即敘述
	return {"標籤": label, "祈使證據": imp, "提問": q}


# ============================================================================
# 時間錨（裁三第 4 項，同法同批）
# ============================================================================
# 同樣改單邊舉證：**過去是有標記的**（了／過／那次／上禮拜…），其餘為「非過去」。
PAST_WORDS = ("那次", "當時", "上次", "之前", "昨天", "上禮拜", "上個月", "去年",
              "以前", "當初", "上一期", "本來", "原本", "小時候", "第一次")
PAST_ASPECT_GUO = (r"[^，。]{1,12}過[，。]?$", r"[^，。]{1,10}過[^，。]{0,4}[，。]")

# --- 修二（PI 2026-09-18）：「了」三分法 ---
# 舊版的兩條「了」構式錨的正好是**句尾的了**，而句尾了是固定語氣詞（le），不是時態；
# 句中的「動詞＋了」（寫了一頁）反而因為要求後方緊接標點而漏掉。修二把顛倒改正。
# 三層全封閉：位置 → liǎo 閉集 → 位置。**沒有一條要看詞義。**
_LE_PUNC = "，。、；！？,.;!?…\n "


def _le_perfective(text: str) -> list[str]:
	"""句中「動詞＋了」＝完成貌。回傳逐處證據（片語），空 list ＝ 沒有完成貌。"""
	out = []
	for h in scan(text, ("了",), blockers=L.TIME_ANCHOR["liǎo語素排除表"]):
		if h["start"] == 0:
			continue                                   # 句首孤了，無動詞可附
		tail = text[h["end"]:]
		if not tail or tail[0] in _LE_PUNC:
			continue                                   # (1) 句尾／標點前 → 語氣詞，不錨
		out.append("完成貌:%s" % text[max(0, h["start"] - 2): h["end"] + 2])
	return out                                         # (3) 句中且右方有內容 → 錨


def time_anchor_v2(text: str) -> dict:
	ev = [w for w in PAST_WORDS if scan(text, (w,))]
	ev += _le_perfective(text)
	if _has(text, PAST_ASPECT_GUO):
		ev.append("經歷貌:過")
	return {"標籤": "過去" if ev else "非過去", "證據": ev}



# ============================================================================
# 11 限制形狀（表五原樣沿用，含其既有守衛）
# ============================================================================
_NUM = r"(?:[0-9０-９]+|[一二兩三四五六七八九十百千萬半]+)"

# ── 修正二（2026-09-25 最小修正令）：表五限定頭詞邊界守衛 ──────────────────
# 復活 9/18 表五修繕令 §一.2：「內／上下／左右」需**前鄰數字、量級詞或範圍語境**
# 才命中（治「內容」的內——子字串病第五次）。**僅此一條**；量詞語境化等其餘
# 表五改動不做。
# 紅線 canon_v3 零動 → 守衛寫在 v2 這側，對生產偵測器回傳的 cue 做後濾，
# 與上面 v2 補充單位同樣是「並聯、不改生產」的形狀。
_BOUNDARY_GUARDED_HEADS = ("內", "上下", "左右")
# 量級詞不另立詞表：定義為「數字之後、不跨標點也不跨『的/得/地』的緊鄰字段」。
# 「的」是關鍵 blocker——「一個人的內心」的數字屬於別的中心語，不構成範圍。
_QTY_STOP = "的得地，。！？；：、,.!?;:「」『』（）()　 \t\r\n"
_LEFT_QUANTITY = re.compile(
	r"(?:[0-9０-９]+|[〇零一二兩三四五六七八九十百千萬億半幾數]+)[^%s]{0,4}$"
	% re.escape(_QTY_STOP)
)


def _guarded_head_ok(text: str, term: str) -> bool:
	"""該限定頭在全句中是否**至少一次**出現具備前鄰數量／範圍語境。

	雙向：有合格出現即整句放行（保守偏收），全無合格出現才撤掉該 cue。
	"""
	for m in re.finditer(re.escape(term), text):
		q = _LEFT_QUANTITY.search(text[: m.start()].rstrip())
		if q is None:
			continue
		# 序數不是範圍：「第三章內容」的「三」屬 ordinal，不得放行「內」。
		left = text[: m.start()].rstrip()
		if q.start() > 0 and left[q.start() - 1] == "第":
			continue
		return True
	return False


# ── 刀2「一＋物件量詞」規則（2026-10-06 刀2 詞表簽核與刀1C啟用令 §一，PI 簽）──
# 規則：表五命中「一＋物件量詞」且無例外前綴 → **該命中不進場**（不算限制）。
#       它是任務本體的命名，不是要求。
#
# **兩張表單獨落檔**（令文明訂「不得混入程式常量」）：
#   `signed_tables/knife2_one_classifier.json`
# 本檔只讀不寫、不複製、不內嵌——詞表抄寫在這個專案裡毀過一張量詞表（條款 8）。
#
# 三條界線（全部照令文）：
#   1. 只套**「一」**起頭；**「半」整個拿掉**（半小時／半天 為真數量）。
#   2. 量詞須在**物件量詞白名單**內（度量單位不入，「一句話」「一天」照舊進場）。
#      判斷以白名單為準，**不以度量單位黑名單為準**——白名單才關得住未知詞。
#   3. 前鄰 6 字內出現**例外前綴**（只／就／僅／一次／限／每）→ 保留，仍為要求。
KNIFE2_ONE_CLASSIFIER = True   # 2026-10-06 同令 §一：619 句迴歸過（裁決後 A/B 型 0），開啟

_K2_PATH = HERE / "signed_tables/knife2_one_classifier.json"
_K2 = json.loads(_K2_PATH.read_text(encoding="utf-8"))
K2_OBJECT_CLASSIFIERS = tuple(_K2["物件量詞"])
K2_PREFIX_EXEMPT = tuple(_K2["例外前綴"])
K2_PREFIX_WINDOW = 6


def _k2_drop(text: str, cue: dict) -> bool:
	"""這個表五命中是否該被刀2 擋掉（不進場）。"""
	lit = str(cue.get("cue") or "")
	if not lit.startswith("一"):
		return False                      # 界線 1：只套「一」，半不套
	if cue.get("value") != 1:
		return False                      # 「一萬五千元」之類不是「一＋量詞」
	measure = cue.get("measure")
	if measure not in K2_OBJECT_CLASSIFIERS:
		return False                      # 界線 2：白名單制
	k = text.find(lit)
	if k < 0:
		return False
	left = text[max(0, k - K2_PREFIX_WINDOW):k]
	if any(m in left for m in K2_PREFIX_EXEMPT):
		return False                      # 界線 3：例外前綴 → 仍為要求
	return True


def constraint_shape(text: str) -> dict:
	"""表五（canon_v3 原樣，含其既有守衛）**並聯** v2 補充單位。

	裁四之四：補 千／磅／公升／坪。**不動 canon_v3**（紅線：生產零動、v2 為新線），
	所以補充單位由 v2 自帶一張小表，在這裡與生產的偵測器並聯。

	修正二（2026-09-25）：生產回傳的限定頭 cue 再過一道 v2 詞邊界守衛
	（`_guarded_head_ok`），「內／上下／左右」無前鄰數量／範圍語境即撤除。
	"""
	cues = [c for c in detect_table5_constraint_cues(text)
	        if not (c.get("source") == "table5_limiting_head"
	                and c.get("cue") in _BOUNDARY_GUARDED_HEADS
	                and not _guarded_head_ok(text, str(c["cue"])))]
	pats = [_NUM + "(?:" + "|".join(L.CONSTRAINT_SHAPE["v2_supplementary_units"]) + ")"]
	# 修一：英文單位字母。**左邊必須是阿拉伯數字**（含全形），大小寫皆收。
	letters = "".join(L.CONSTRAINT_SHAPE["v2_english_unit_letters"])
	pats.append(r"[0-9０-９]+[%s%s]" % (letters, letters.lower()))
	extra = scan_re(text, tuple(pats))
	for e in extra:
		if not any(c["cue"] in e["term"] or e["term"] in str(c.get("phrase", "")) for c in cues):
			cues.append({"cue": e["term"], "source": "v2_supplementary_unit",
			             "phrase": text[max(0, e["start"] - 4): e["end"] + 4].strip()})
	for w in _writing_spec(text):
		if not any(c["cue"] == w["cue"] for c in cues):
			cues.append(w)
	# 刀2：在**全部 cue 都收齊之後**才擋，否則擋掉的那一筆可能讓
	# 後面的並聯邏輯（`any(c["cue"] in e["term"] …)`）判斷依據變掉。
	dropped = []
	if KNIFE2_ONE_CLASSIFIER:
		keep = []
		for c in cues:
			if _k2_drop(text, c):
				dropped.append(c)
			else:
				keep.append(c)
		cues = keep
	return {"cues": cues, "命中": bool(cues),
	        "片語": [c.get("phrase") or c["cue"] for c in cues],
	        "刀2擋下": dropped}


# ── 修三（2026-09-25 修三補位令第二節）：表五增補「寫作規格形」 ─────────────
# 與既有表五**同等地位、同一入口**——掛在 `constraint_shape` 裡，
# 所以照樣受 `reorder_v2` 的框架閘管（主請求框／過去敘事框／描述框不進場）。
# 詞表與每一詞形的類別歸屬理由在 `lexicon_v2.CONSTRAINT_SHAPE["v2_writing_spec_form"]`。
_WS = L.CONSTRAINT_SHAPE["v2_writing_spec_form"]
_WS_CAT = {w[0]: (w[1], w[2]) for w in _WS}
_WS_TERMS = tuple(w[0] for w in _WS if w[3] == "詞")
_WS_BLOCKERS = L.CONSTRAINT_SHAPE["v2_writing_spec_form_blockers"]
# 數字構式帶負向右界：「一段時間」「一段路」不是篇幅，「五十字體」不是字數。
_WS_PATTERNS = {
	"N個字": _NUM + "個字",
	"N字": _NUM + "字(?!" + "|".join(L.CONSTRAINT_SHAPE["v2_writing_spec_form_char_neg_right_bound"]) + ")",
	"N段": _NUM + "段(?!" + "|".join(L.CONSTRAINT_SHAPE["v2_writing_spec_form_para_neg_right_bound"]) + ")",
	"N句": _NUM + "句",
}


def _writing_spec(text: str) -> list[dict]:
	"""寫作規格形偵測。**全部走詞邊界**，無一處裸子字串比對。"""
	out = []
	for h in scan(text, _WS_TERMS, blockers=_WS_BLOCKERS):
		cat, why = _WS_CAT[h["term"]]
		out.append({"cue": h["term"], "source": "v2_writing_spec", "類別": cat, "歸屬": why,
		            "phrase": text[max(0, h["start"] - 4): h["end"] + 4].strip()})
	for form, pat in _WS_PATTERNS.items():
		cat, why = _WS_CAT[form]
		for h in scan_re(text, (pat,)):
			# 「N個字」與「N字」重疊時只留長的那個（scan_re 不跨 pattern 去重）。
			if any(o["start"] <= h["start"] and h["end"] <= o["end"]
			       for o in out if "start" in o):
				continue
			out.append({"cue": h["term"], "source": "v2_writing_spec", "類別": cat,
			            "歸屬": why, "詞形": form, "start": h["start"], "end": h["end"],
			            "phrase": text[max(0, h["start"] - 4): h["end"] + 4].strip()})
	for o in out:
		o.pop("start", None)
		o.pop("end", None)
	return out


# ============================================================================
# 裁四之一：祈使動詞賓語抽取（模型戶入口放寬用）
# ============================================================================
# 限制形狀零命中、但句子是祈使構式時，把祈使動詞的賓語抽出來當片語送模型戶。
# 規格型限制（站票／黃光／APA／點com）是**開放類、真的列舉不完**——
# 照 PI 的架構裁決，那正是模型該站的位置；機械只負責把片語切出來。
OBJECT_VERBS = ("挑", "選", "換成", "改成", "用", "買", "訂", "裝在", "放在", "找", "註冊", "壓在")


def imperative_object(text: str) -> dict:
	"""取祈使動詞後方到句末（或標點）的片語。取不到就誠實回 None。"""
	best = None
	for v in OBJECT_VERBS:
		for h in scan(text, (v,)):
			obj = text[h["end"]:].strip("，。？！；,.?!; ")
			if not obj:
				continue
			if best is None or h["start"] > best["verb_at"]:
				best = {"verb": v, "verb_at": h["start"], "片語": obj}
	return best or {"verb": None, "verb_at": None, "片語": None}


# ============================================================================
# 7 交棒（位置條件，需要整篇）
# ============================================================================
STOPWORDS = set("的了是在有我你他她它我們你們他們這那就都也很和跟與而但可以會要不沒個之其"
                "上下前後裡外中對於把被就才還再又都很好嗎呢吧啊喔耶ㄟ")


def _content_bigrams(text: str) -> set:
	clean = "".join(ch for ch in text if ch not in STOPWORDS and ch.strip())
	return {clean[i:i + 2] for i in range(len(clean) - 1)}


def handoff(text: str, later_texts: list[str]) -> dict:
	"""後方存在正式請求句，且與本句主題連結（機械近似：2 字實詞重疊）。"""
	mine = _content_bigrams(text)
	for j, nxt in enumerate(later_texts):
		req = imperative(nxt)["命中"] or interrogative(nxt)["命中"]
		if not req or cognitive(nxt)["命中"]:
			continue
		shared = mine & _content_bigrams(nxt)
		if shared:
			return {"命中": True, "接手句": nxt, "共有實詞": sorted(shared)[:4], "offset": j + 1}
	return {"命中": False, "接手句": None, "共有實詞": [], "offset": None}


DETECTOR_FUNCS = {
	"1_人稱": person, "2_疑問": interrogative, "3_祈使": imperative,
	"4_引述框": reported, "5_反問框": rhetorical, "6_認知框": cognitive,
	"8_空框": empty_frame, "9_語氣體貌": mood_v2, "10_時間錨": time_anchor_v2,
	"11_限制形狀": constraint_shape,
}


# 舊名保留為別名：既有呼叫點（測例、組裝）不必改。
mood = mood_v2
time_anchor = time_anchor_v2
