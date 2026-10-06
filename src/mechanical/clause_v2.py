# -*- coding: utf-8 -*-
"""子句站：切割器 ＋ 繼承器（2026-09-18 建站令）。**全封閉、零語義、零呼叫。**

--- 為什麼建這一站 ---
三修報告量到：修二丟的 5 句裡 3 句、修三丟的 5 句裡 2 句，**錯的不是規則，是容器**——
框架是句層判定，一個子句的訊號就挾持整句。本站把作用域從「句」降到「子句」。

--- 邊界訊號表（令文第一節，逐條對應）---
顯性界
  1 句末標點（。？！）——現行斷句器職權，本檔照收不另立
  2 逗號、頓號、分號
  3 **漢字間空格**（PI 裁：中文標點無空格，空格＝純斷開訊號）
    守衛：空格緊鄰拉丁字母／數字者不切（HAF X BEVO／天堂 W 型英文分詞空格）
隱形界（口語吞標點的還原，**白名單制，預設不切**）
  4 語氣詞宿主白名單＋後接內容：數字＋了／程度詞＋形容詞＋了／固定式閉集／嗎吧呢啦
    守衛：liǎo 閉集（12 條，沿用時間錨表）＋語氣詞構詞閉集（酒吧／吧台／網吧／啦啦隊／呢絨）
  5 話語標記（閉集）
  6 **動詞＋了一律不切**（體貌）——不對稱原則：漏切＝維持現狀，錯切＝新傷害

--- 一處令文未寫死、我照實作並標明的地方 ---
第 5 條寫「話語標記**前界**（標記起頭＝新子句）」，但它引的兩個出處都要求**標記後面也要斷**：
M04「**對了**十一月的山上」——對了在句首，只切前界等於沒切，而 §四.2 的哨兵寫明「對了十一月」**應切**；
M06「**喔對**還有一件事」同理。所以本檔對話語標記**前後都下界**，標記自成一個零訊號子句。
**這是為了通過令文自己的驗收哨兵所做的解讀，不是我自行加碼**，爆炸半徑實測見報告。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("H:/Projects/Logical-AI-OS")
for p in (HERE, REPO / "experiments/composite-classifier/src", REPO / "scripts", REPO):
	if str(p) not in sys.path:
		sys.path.insert(0, str(p))

import detectors as D
import lexicon_v2 as L
import pipeline_v2 as P
import reorder_v2 as R

# ============================================================================
# 邊界訊號表（全封閉）
# ============================================================================
END_PUNCT = "。？！?!"
MID_PUNCT = "，,、；;"
ALL_PUNCT = END_PUNCT + MID_PUNCT
SPACES = " \u3000\t"
_LATIN = re.compile(r"[A-Za-z0-9０-９Ａ-Ｚａ-ｚ]")

# 4a 數字＋了（快三十了／六十了）
_NUM_CHARS = "0-9０-９一二兩三四五六七八九十百千萬"
# 4b 程度詞＋形容詞＋了（太棒了／超麻煩了）。程度詞閉集，形容詞位置限 1~3 字。
DEGREE = ("太", "超", "很", "好", "真", "夠", "挺", "蠻", "滿", "非常", "特別", "十分")
# 4c 固定式閉集
FIXED_LE = ("就好了", "算了", "罷了", "夠了", "完了", "好了")
# 4d 句中語氣詞＋後接內容
PARTICLES = ("嗎", "吧", "呢", "啦")
PARTICLE_BLOCKERS = ("酒吧", "吧台", "網吧", "啦啦隊", "呢絨")
# 5 話語標記（閉集）。長詞在前，貪婪匹配。
DISCOURSE = ("喔對", "對了", "然後", "還有", "順便", "另外", "欸", "啊")

_DEGREE_RE = re.compile("(?:%s)[^%s]{0,3}了$" % ("|".join(DEGREE), ALL_PUNCT))


def _boundaries(text: str) -> set:
	"""回傳切點集合（切在 index 之前）。每個切點都附得出是哪一條訊號下的。"""
	cuts, why = set(), {}
	n = len(text)

	def add(i, tag):
		if 0 < i < n:
			cuts.add(i)
			why.setdefault(i, tag)

	# 1、2 顯性標點：切在標點之後
	for i, ch in enumerate(text):
		if ch in ALL_PUNCT:
			add(i + 1, "標點")

	# 3 漢字間空格
	for i, ch in enumerate(text):
		if ch not in SPACES:
			continue
		left = text[i - 1] if i > 0 else ""
		right = text[i + 1] if i + 1 < n else ""
		if (left and _LATIN.match(left)) or (right and _LATIN.match(right)):
			continue                                   # 守衛：英文分詞空格，不切
		add(i + 1, "漢字間空格")

	# 4a~4c 「了」白名單
	for m in re.finditer("了", text):
		i = m.start()
		if D._covered_by(text, i, 1, tuple(L.TIME_ANCHOR["liǎo語素排除表"])):
			continue                                   # 守衛：liǎo 語素
		if i + 1 >= n or text[i + 1] in ALL_PUNCT:
			continue                                   # 已有顯性界或句尾，不重複下界
		head = text[:i + 1]
		if i > 0 and re.match("[%s]" % _NUM_CHARS, text[i - 1]):
			add(i + 1, "數字＋了")
		elif _DEGREE_RE.search(head):
			add(i + 1, "程度詞＋形容詞＋了")
		elif any(head.endswith(f) for f in FIXED_LE):
			add(i + 1, "固定式了")
		# else：動詞＋了 → **不切**（令文第 6 條，不對稱原則）

	# 4d 句中語氣詞
	for p in PARTICLES:
		for m in re.finditer(p, text):
			i = m.start()
			if D._covered_by(text, i, 1, PARTICLE_BLOCKERS):
				continue                               # 守衛：語氣詞構詞
			if i + 1 >= n or text[i + 1] in ALL_PUNCT:
				continue
			add(i + 1, "語氣詞＋後接內容")

	# 5 話語標記：前後都下界（理由見檔頭）
	for d in DISCOURSE:
		for m in re.finditer(d, text):
			add(m.start(), "話語標記前界")
			add(m.end(), "話語標記後界")

	return cuts, why


def split_clauses(text: str) -> list[dict]:
	"""切成子句。純標點／純空白的段丟掉，不成子句。"""
	cuts, why = _boundaries(text)
	marks = [0] + sorted(cuts) + [len(text)]
	out = []
	for a, b in zip(marks, marks[1:]):
		seg = text[a:b]
		if not seg.strip(ALL_PUNCT + SPACES):
			continue                                   # 純標點段
		out.append({"text": seg, "start": a, "end": b, "界": why.get(a, "句首")})
	return out or [{"text": text, "start": 0, "end": len(text), "界": "句首"}]


# ============================================================================
# 繼承器（令文第二節）
# ============================================================================
# 子句不是孤島：中文 pro-drop，主語與時錨會從前一子句帶過來。
RESIDUAL_TIME = ("要", "了", "過", "才", "正在")

# --- 收官配置（PI 2026-09-18，依診斷臂採納）---
# **拆時態繼承**：時態是局部的，不跨子句（「吵了好幾次」的過去不外溢到「預算抓十五萬」）。
# **拆人稱繼承**：概念封存不作廢，待有正確消費者再議。
# 保留：主語 pro-drop 的**祈使重置**與**引述域規則**。
# 註：人稱繼承拆掉之後，「引述域不外洩」沒有東西可攔——傳播鏈本身已經沒了。
#     照令保留該碼路與旗標，但它目前**是惰性的**，照實記，不假裝它在生效。
TIME_INHERIT = False
PERSON_INHERIT = False

# ── F1 篇級句子地位（2026-10-05 規則對齊修正令 §二 F1，PI 簽）────────────────
# 令文：「classify() 進入子句前先跑篇級：篇內有請求句（軸一＝主請求／空框請求）時，
#        其他**非請求句且無第一人稱**（我／我們／我方／咱／本人，含我-領屬複合）
#        → 句子地位＝「材料」（貼文／引述／敘事），表五不進場、軸二＝材料；
#        帶第一人稱者→自陳情境照舊。指向詞（後指／前指）仍可用作地位證據，
#        但**不是唯一觸發**。」
#
# 這是審計 D1 要補的那一層——A1「組合層＝前段，先讀整篇、依任務分離句子地位」。
# 它是 D1／D3b／C2 三條偏離的共同根，所以 F3 的適用域閘與 C2 的篇級化都掛在它身上。
#
# **兩趟制**：第一趟只為取每句的軸一（判有無請求句），第二趟才帶著地位跑。
# 第一趟不能用地位（還沒算出來），所以它一定是「地位＝自陳」的那一版——
# 照實記：**篇級地位只影響第二趟**。
F1_DOC_STATUS = True      # 2026-10-06 F2/F4 裁決令：全開配置，驗收全過

# ── F1-WS 寫作規格形豁免（2026-10-06 F1規格形豁免與卷七令 §二，PI 裁）────────
# 令文：「F1 加寫作規格形豁免：篇級句子地位判『材料』時，句內表五命中含
#        **已簽核寫作規格形**（字數／不少於／格式／篇幅等簽核表）者**不鎖**，
#        照舊進場——與刀1-C 句級版同一豁免表，不新增詞。」
#
# **根因（聊天端自查，卷六開獎）**：F1 令文把「無第一人稱」當成篇級材料的
# 唯一代理，而規格句本來就沒有第一人稱——卷六漏抓 36 句裡有 22 句框架＝
# 「篇級材料」，G54「不少於600字」15 句我方 0/15、裸 7B 12/15。
# 與審計 D2「無主→自陳」同類：把 PI 的原則壓成單一表面特徵。
F1_WRITING_SPEC_EXEMPT = True
# 令文寫「**句內**表五命中」。字面是句級，但 F1 的鎖是逐子句施加的，
# 所以「句內」也可讀成「該子句內」。**兩種都實作、都量，不由 CC 挑**：
#   "sentence" ——整句任一子句命中規格形，整句不鎖（照「句內」字面）
#   "clause"   ——只有命中的那個子句不鎖，同句其餘子句照鎖
F1_WS_SCOPE = "sentence"
F3_IMPERATIVE_YOU = True  # 同令：標籤面對齊，判定零影響（動 0 句，照實入冊）
# C2 句級貼文範圍：F1 上線後退為後備（令文 F1 末「旗標分開」）
KNIFE1C_AS_FALLBACK = True

_REQ_A1 = ("主請求", "空框請求")


def _doc_status(units: list[dict]) -> dict:
	"""篇級句子地位。回 {sid: "材料" | "自陳"}。

	觸發：篇內有請求句。其他非請求句且**無第一人稱**者判「材料」。
	指向詞另記為證據欄（`地位證據`），**不作為觸發條件**（令文：不是唯一觸發）。
	"""
	import re as _re
	first_pass = []
	for u in units:
		sig = P.signals(u["text"], [])
		a1, _r = P.axis1(sig, u["text"])
		has_first = bool(sig["人稱"]["我"])          # 含領屬複合（領屬由第一人稱衍生）
		pw = [w for w in PASTE_FORWARD if w in u["text"]]
		pw += [m.group(0) for p in PASTE_FORWARD_RE
		       for m in [_re.search(p, u["text"])] if m]
		bw = [w for w in PASTE_BACKWARD if w in u["text"]]
		first_pass.append({"sid": u["sid"], "軸一": a1, "有第一人稱": has_first,
		                   "後指詞": pw, "前指詞": bw})
	has_req = any(x["軸一"] in _REQ_A1 for x in first_pass)
	out = {}
	for x in first_pass:
		if has_req and x["軸一"] not in _REQ_A1 and not x["有第一人稱"]:
			ev = []
			if x["後指詞"]:
				ev.append("後指詞 %s" % "、".join(x["後指詞"]))
			if x["前指詞"]:
				ev.append("前指詞 %s" % "、".join(x["前指詞"]))
			out[x["sid"]] = {"地位": "材料", "依據": "篇內有請求句＋本句非請求＋無第一人稱",
			                 "地位證據": ev, "首趟軸一": x["軸一"]}
		else:
			out[x["sid"]] = {"地位": "自陳",
			                 "依據": ("篇內無請求句" if not has_req
			                        else "本句是請求句" if x["軸一"] in _REQ_A1
			                        else "帶第一人稱"),
			                 "地位證據": [], "首趟軸一": x["軸一"]}
	return out


def enrich(clause_texts: list[str], later_texts: list[str],
           status: str = "自陳") -> list[dict]:
	"""逐子句跑偵測器，套主語繼承與時間繼承，回傳每個子句的**有效訊號**。"""
	prev_person = None                                 # (標籤, 有第三方主語)
	prev_time = None
	out = []
	for i, ct in enumerate(clause_texts):
		later = clause_texts[i + 1:] + later_texts
		sig = P.signals(ct, later)

		# --- 主語繼承 ---
		own = sig["人稱"]
		label, third, psrc = own["標籤"], own["有第三方主語"], "自身"
		if sig["祈使"]["命中"] and not (F1_DOC_STATUS and status == "材料"):
			# 祈使框重置：請教／求／幫我／麻煩（受詞守衛已在 imperative() 內生效）
			# 出處：野外句「…他平常看片辦公 請教一下30K」——請教的主語是說話者，不是「他」。
			#
			# ── F3（2026-10-05 規則對齊修正令 §二 F3，PI 簽）──────────────
			# 令文：「祈使子句隱含人稱標籤**照令文設「你」**
			#        （有第三方主語＝False 不變）；**適用域閘由 F1 提供**
			#        （材料地位句不套語氣定人稱）。」
			# 舊版設「我」是令文走樣（審計 D3a）：令文 A6 寫的是
			# 「隱含人稱由語氣決定：敘述→我、祈使→你」。
			# `有第三方主語=False` 保持不變——那是功能面，令文明訂不動。
			label, third, psrc = (("你", False, "祈使框重置（F3）")
			                      if F3_IMPERATIVE_YOU else ("我", False, "祈使框重置"))
		elif PERSON_INHERIT and own["標籤"] == "沒掛人" and prev_person:
			label, third, psrc = prev_person[0], prev_person[1], "繼承前子句"
		if not sig["引述"]["命中"]:
			prev_person = (label, third)               # 引述域的主語不外洩
		else:
			psrc += "／引述域不外洩"

		# --- 時間繼承 ---
		own_t = sig["時間"]
		has_own = bool(own_t["證據"]) or any(m in ct for m in RESIDUAL_TIME)
		if has_own or not TIME_INHERIT:
			tlabel, tsrc = own_t["標籤"], "自身"        # 收官配置：時態一律局部，不繼承
		elif prev_time:
			tlabel, tsrc = prev_time, "繼承前子句"
		else:
			tlabel, tsrc = own_t["標籤"], "自身（無前文）"
		prev_time = tlabel

		sig2 = dict(sig)
		sig2["人稱"] = {**own, "標籤": label, "有第三方主語": third}
		sig2["時間"] = {**own_t, "標籤": tlabel}
		out.append({"text": ct, "sig": sig2, "人稱來源": psrc, "時間來源": tsrc,
		            "自身人稱": own["標籤"], "自身時間": own_t["標籤"],
		            "時間證據": own_t["證據"]})
	return out


# ============================================================================
# 框架／表五改制 ＋ 句級聚合（令文第三節）
# ============================================================================
# 令文：句級軸二＝子句級判定的優先聚合，**限制 > 材料 > 無**。
AXIS2_PRIORITY = ("限制", "材料", "無")
# 令文：「任一子句主請求→句記主請求（既有行為不變）；其餘聚合按現行標籤優先序。」
# **現行標籤優先序**在規則表裡是「規則順序」，而規則順序把非請求排在主請求之前——
# 那與「任一子句主請求→句記主請求」直接矛盾。所以這裡取的是**標籤優先序**：
# 主請求 > 空框請求 > 隱性需求 > 非請求。這是唯一與令文該句相容的讀法，標明為解讀。
AXIS1_PRIORITY = ("主請求", "空框請求", "隱性需求", "非請求")

# ── 刀1 聚合修復（2026-10-06 v4.2 開站令）────────────────────────────────────
# 令文：「機械層子句聚合 bug（E17/s02 型：軸一軸二取自不同子句）——
#        修為**主請求所在子句之軸二為準**」。
#
# 病的形狀（卷四驗屍 §3c 的證物）：E17/s02 的軸一來自子句 2（主請求），
# 軸二來自子句 4（限制），而**子句 2 自己的軸二是「無」**——
# 機械層自己認為那個請求不帶條件，「限制」是從一個軸一為「非請求」的子句借來的。
# 兩軸的語義前提（「這是個請求」／「這個請求帶條件」）要求它們指同一個言語行為，
# 舊聚合各軸獨立取優先序，沒有要求同源。
#
# **令文未定而我自選的兩點，標明**：
#   (a) 若有**多個**主請求子句，軸二在**那些子句之間**按既有 AXIS2_PRIORITY 聚合。
#       令文只說「主請求所在子句」，沒說多個時怎麼辦；取既有優先序是最小改動。
#   (b) 若**沒有**主請求子句（軸一聚合為空框請求／隱性需求／非請求），
#       **行為完全不變**（全句優先序聚合）。令文只指定主請求這一支，
#       空框請求是否同病待裁——我不順手一起改。
#
# ── **預設 False：已實作、未啟用、停工呈裁** ─────────────────────────────────
# 迴歸量到的是最高條款所指的「蹺蹺板互吃」，所以不啟用：
#
#   1. **全部 243 個主請求子句的軸二都是「無」，無一例外。**
#      所以令文的修法在數學上等價於「軸一＝主請求 ⇒ 句級軸二＝無」。
#      原因是 axis2 規則 1「主請求結構推導 → 軸二無」本身**無條件成立**——
#      也就是說**軸二本來就設計成由非主請求子句承擔**。
#      「兩軸來自不同子句」是這一層的**常態**，不是病。
#   2. 後果：四卷＋開發集共 **103 句**離開模型層（限制→無 35、**材料→無 68**），
#      而「材料→無」那 68 句原本是要進模型層的，現在機械層直接定案為無。
#   3. 開發集（gold 可見）量到：14 句變動裡 **9 句 gold＝限制**
#      （其中 4 句原本是**正確**直收，修後變漏抓），只有 2 句是真的修掉誤收。
#      **效益 2 : 代價 9。** 而卷四驗屍剛量出本代的瓶頸是召回不是誤收。
#
# 證物：`experiments/control-station/knife1_agg_regression.{md,json}`。
# 啟用前請先裁（切回 True 即生效，程式碼不必再動）。
KNIFE1_AGG_FIX = False


# ── 刀1-C 貼文範圍規則（2026-10-06 刀1 棄決與替換兩刀令 §三）──────────────────
# 令文：「主請求子句之請求動詞受詞為**指向後文的材料詞**（封閉詞表，CC 自凍結碼／
#        語料枚舉後呈簽，候選：這段話／這段文字／這條X／下面／如下／以下
#        （僅當冒號在其後且同句尚有子句））時，同句內其後所有子句軸二鎖「材料」。
#        指向前文者（以上／上面）不觸發；冒號在句尾無後續子句者不觸發。」
#
# **詞表來源**：候選由令文給定，CC 另自五份語料枚舉實證。
# **材料詞表（含 CC 加的前指詞「上述／前面」）已由 PI 整表簽核**
# （2026-10-06 刀1CD 裁決與刀2 開量令 §一）。
#
# ── 補洞（同令 §一；因 D17/s01 誤鎖）────────────────────────────────────────
# 聊天端對卷：8 句動到，7 對 1 傷——D17/s01（**原句已去語料**：該句的
# 指向詞後面接的是**規格**不是貼文）應為 A 型，
# **CC 誤分 C 型**。補洞照令文兩分支：
#
#   1. 指向詞之後**緊接冒號** → 鎖同句其後**全部**子句（原行為）；
#   2. **無冒號** → 只鎖到**下一個主請求／祈使子句之前**為止，該子句及其後不鎖。
#
# 「緊接冒號」的判法：指向詞命中位置之後，**跳過非標點字元之前**先遇到的標點是
# 冒號（全形或半形）。E04/E07 的「這段話：」、C09 的「這條建議：」屬此；
# C03 的「這段話，」、D17 的「下面一段文字，」不屬此。
KNIFE1C_PASTE_SCOPE = True     # 2026-10-06 刀2詞表簽核與刀1C啟用令 §二：三條驗收全過，開啟

# 後指材料詞（指向後文的貼上文本）
PASTE_FORWARD = ("這段話", "這段文字", "下面", "如下", "以下")
# 「這條X」是構式而非定詞：這條＋一個字以上的名詞
PASTE_FORWARD_RE = (r"這條[^\s，。、；：:,.;]{1,6}",)
# 前指詞：指向已經說過的內容，**不觸發**
PASTE_BACKWARD = ("以上", "上面", "上述", "前面")


_PUNCT = "，。、；：！？,.;:!?"
_COLON = "：:"
# 寫作規格形豁免用的詞集：**自已簽核的 `v2寫作規格形` 讀出**，不另抄一份。
_WRITING_SPEC = frozenset(w[0] for w in L.CONSTRAINT_SHAPE["v2寫作規格形"])
# 表五「寫作規格形」這一族的族標。偵測器對每個 cue 標 `source`，
# `v2_writing_spec` 就是本族——**比族不比字面**，所以「式」條目（`N字`）
# 代入後的 `600字` 也接得到。零新增詞：族的成員由簽核表決定，不由這裡決定。
_WS_SOURCE = "v2_writing_spec"


def _is_ws(cu: dict) -> bool:
	return cu.get("source") == _WS_SOURCE


def _ws_label(cu: dict) -> str:
	"""回報用：有「詞形」就報樣式（`N字`），否則報 cue 本身（`字數`）。"""
	return cu.get("詞形") or cu.get("cue")


def _colon_right_after(text, end):
	"""指向詞命中（結束於 end）之後，先遇到的標點是不是冒號。"""
	for ch in text[end:]:
		if ch in _PUNCT:
			return ch in _COLON
	return False                          # 其後無標點＝沒有冒號


def _paste_scope_span(detail):
	"""回傳 (起, 迄) 半開區間——該區間內的子句軸二鎖「材料」；無則 None。

	條件（全部照令文）：
	  1. 該子句軸一為主請求；
	  2. 子句內出現後指材料詞（且該處不是前指詞）；
	  3. **同句尚有其後子句**；
	  4. 補洞：指向詞後緊接冒號 → 迄＝句末；否則迄＝**下一個主請求／祈使子句**。
	"""
	import re as _re
	for i, d in enumerate(detail):
		if d["軸一"] != "主請求":
			continue
		t = d["子句"]
		if any(b in t for b in PASTE_BACKWARD):
			continue                      # 前指，不觸發
		end = None
		for w in PASTE_FORWARD:
			k = t.find(w)
			if k >= 0:
				end = k + len(w)
				break
		if end is None:
			for p in PASTE_FORWARD_RE:
				m = _re.search(p, t)
				if m:
					end = m.end()
					break
		if end is None:
			continue
		if i + 1 >= len(detail):
			continue                      # 其後無子句，不觸發
		if _colon_right_after(t, end):
			return i + 1, len(detail)     # 分支 1：鎖到句末
		# 分支 2：鎖到下一個主請求／祈使子句之前
		stop = len(detail)
		for j in range(i + 1, len(detail)):
			if detail[j]["軸一"] in ("主請求", "空框請求") or detail[j]["語氣"] == "祈使":
				stop = j
				break
		if stop <= i + 1:
			return None                   # 緊接著就是下一個請求 → 無可鎖範圍
		return i + 1, stop
	return None


def _agg(labels, priority):
	for p in priority:
		if p in labels:
			return p
	return labels[0] if labels else "非請求"


def _agg_axis2(detail, a1):
	"""句級軸二聚合。刀1：軸一為主請求時，只看主請求子句的軸二。"""
	if KNIFE1_AGG_FIX and a1 == "主請求":
		src = [d["軸二"] for d in detail if d["軸一"] == "主請求"]
		if src:
			return _agg(src, AXIS2_PRIORITY), "刀1：主請求子句之軸二為準（%d 句主請求）" % len(src)
	return _agg([d["軸二"] for d in detail], AXIS2_PRIORITY), "全句優先序聚合"


def classify(units: list[dict]) -> list[dict]:
	"""句 → 子句 → 逐子句框架 → 句級聚合。**零呼叫**（模型戶停用）。"""
	out = []
	# F1 第一趟：只取每句軸一與第一人稱，算篇級地位。第二趟才帶地位跑。
	status_map = _doc_status(units) if F1_DOC_STATUS else {}
	for i, u in enumerate(units):
		later_units = [v["text"] for v in units[i + 1:]]
		st = status_map.get(u["sid"], {"地位": "自陳", "依據": "F1 未開",
		                               "地位證據": [], "首趟軸一": None})
		clauses = split_clauses(u["text"])
		rich = enrich([c["text"] for c in clauses], later_units, st["地位"])
		# F2 句級作用域用的：整句有沒有第一人稱
		_sent_first = bool(D.person(u["text"])["我"])
		detail = []
		# F1-WS 豁免（2026-10-06 F1規格形豁免與卷七令 §二）：先算整句的
		# 寫作規格形命中，供句級讀法使用。零新增詞——用的是刀1-C 那張
		# 已簽核的 `v2寫作規格形`（同一個 `_WRITING_SPEC`，令文明定同表）。
		# **按語義族比，不按字面 cue 比**（條款 5）。表五的寫作規格形有「式」條目
		# （`N字`／`N個字`／`N段`／`N句`），偵測器吐出的 cue 是**代入後**的字串
		# （`600字`），拿它去 `in _WRITING_SPEC` 永遠不中——G54 的
		# 「（不少於600字）」就是這樣漏掉的。cue 自帶 `source="v2_writing_spec"`，
		# 那就是「已簽核寫作規格形」這一族的族標，用它。
		_ws_sent = sorted({_ws_label(cu) for r in rich
		                   for cu in r["sig"]["限制形狀"]["cues"]
		                   if _is_ws(cu)})
		for c, r in zip(clauses, rich):
			a1, r1 = P.axis1(r["sig"], c["text"])
			_ws_cl = [_ws_label(cu) for cu in r["sig"]["限制形狀"]["cues"]
			          if _is_ws(cu)]
			_ws_hit = _ws_sent if F1_WS_SCOPE == "sentence" else _ws_cl
			_lock = F1_DOC_STATUS and st["地位"] == "材料"
			if _lock and F1_WRITING_SPEC_EXEMPT and _ws_hit:
				# 令文：「句內表五命中含已簽核寫作規格形者**不鎖**，照舊進場。」
				# 根因是 F1 把「無第一人稱」當成篇級材料的唯一代理，而
				# 「不少於600字」「格式」這類規格句本來就沒有第一人稱——
				# 它們講的是**怎麼處理材料**，不是材料本身，和刀1-C 的豁免同一理。
				_lock = False
			if _lock:
				# F1：篇級地位＝材料 → 表五不進場、軸二＝材料。
				# **在框架之前**生效（令文「進入子句前先跑篇級」的作用面）。
				fr = {"框架": "篇級材料", "表五": "不進場", "軸二": "材料",
				      "表五命中": [], "依據": st["依據"]}
			else:
				fr = R.frame_and_axis2(a1, r["sig"], _sent_first)
			if (F1_DOC_STATUS and F1_WRITING_SPEC_EXEMPT
					and st["地位"] == "材料" and _ws_hit):
				fr = dict(fr)
				fr["F1豁免_寫作規格形"] = list(_ws_hit)
			detail.append({"子句": c["text"], "界": c["界"], "軸一": a1, "軸一規則": r1,
			               "F1豁免_寫作規格形": fr.get("F1豁免_寫作規格形"),
			               # 刀1-C 的豁免要按族比（2026-10-06 F2豁免令 §②），
			               # 而 `表五命中` 只存代入後的 cue 字串，比不出族來。
			               # 所以把這個子句的**族命中**一起帶下去。
			               "族命中_寫作規格形": _ws_cl,
			               "框架": fr["框架"], "表五": fr["表五"], "表五命中": fr["表五命中"],
			               "軸二": fr["軸二"], "人稱": r["sig"]["人稱"]["標籤"],
			               "人稱來源": r["人稱來源"], "時間": r["sig"]["時間"]["標籤"],
			               "時間來源": r["時間來源"], "語氣": r["sig"]["語氣"]["標籤"],
			               "引述": bool(r["sig"]["引述"]["命中"])})
		a1 = _agg([d["軸一"] for d in detail], AXIS1_PRIORITY)
		# 刀1-C：主請求子句的受詞指向後文貼文 → 其後子句軸二鎖「材料」。
		# 鎖的是**子句級**讀數，所以聚合照常跑，只是進料被改過。
		# C2：F1 上線後句級貼文範圍退為**後備**（令文 F1 末「旗標分開」）——
		# 篇級已把該句判成材料時就不必再跑句級；篇級沒接到才由句級兜。
		_c2_on = KNIFE1C_PASTE_SCOPE and not (
			F1_DOC_STATUS and KNIFE1C_AS_FALLBACK and st["地位"] == "材料")
		span = _paste_scope_span(detail) if _c2_on else None
		if span is not None:
			for d in detail[span[0]:span[1]]:
				# 寫作規格形豁免（2026-10-06 刀2詞表簽核與刀1C啟用令 §二，採 CC 候選）：
				# 鎖的對象是「貼上的材料」，而命中寫作規格形的子句在講
				# **怎麼處理材料**——它不是材料，所以不鎖。
				# 用的是**已簽核的既有詞表**（`v2寫作規格形` 23 詞），零新增詞。
				# 立案句：D17/s01 子句2（**原句片段已去語料**），命中詞＝`字數`。
				#
				# **2026-10-06 F2豁免令 §②：改按族比。** 原本寫
				# `any(h in _WRITING_SPEC for h in d["表五命中"])`，而 `表五命中`
				# 存的是代入後的 cue（`600字`），所以表裡四條「式」條目
				# （`N字`／`N個字`／`N段`／`N句`）接不到。它當初過驗收是因為
				# 立案句剛好踩在字面條目 `字數` 上，**不是寫法對**。
				if d["族命中_寫作規格形"]:
					d["刀1C豁免_寫作規格形"] = list(d["族命中_寫作規格形"])
					continue
				if d["軸二"] != "材料":
					d["刀1C鎖材料_原軸二"] = d["軸二"]
					d["軸二"] = "材料"
		a2, a2_why = _agg_axis2(detail, a1)
		if span is not None:
			a2_why = "刀1-C：第 %d〜%d 子句鎖材料；%s" % (span[0] + 1, span[1], a2_why)
		out.append({"sid": u["sid"], "sentence": u["text"], "軸一": a1, "軸二": a2,
		            "軸二聚合": a2_why,
		            "篇級地位": st["地位"], "地位依據": st["依據"],
		            "地位證據": st["地位證據"], "首趟軸一": st["首趟軸一"],
		            "子句數": len(detail), "子句": detail,
		            "框架": "／".join(dict.fromkeys(d["框架"] for d in detail)),
		            "表五命中": [x for d in detail for x in d["表五命中"]]})
	return out
