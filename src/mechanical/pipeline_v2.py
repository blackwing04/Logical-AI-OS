# -*- coding: utf-8 -*-
"""v2 判斷層組裝：偵測器 → 規則 → 標籤 ＋ 權重。

**機械戶零呼叫。** 模型只在軸二規則 5b／6 被觸發時問一題（片語級任務相關性）。

規則順序照 `rules_v2`，每一步把開火的規則記進 `依據`——
判錯的時候要看得出是哪一條規則做的，不是給一個標籤了事。
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path("H:/Projects/Logical-AI-OS")
for p in (HERE, REPO / "experiments/composite-classifier/src", REPO / "scripts", REPO):
	if str(p) not in sys.path:
		sys.path.insert(0, str(p))

import detectors as D
from classifier import weight_of, route_of

MODEL_POST_ASK = ("使用者的任務是「{任務}」。"
                  "這段話裡的「{片語}」，回答時需不需要遷就它？")
MODEL_POST_OPTIONS = ("需要遷就", "不需要遷就")
MODEL_POST_REVISION = "model_post signed_v1"


def signals(text: str, later: list[str]) -> dict:
	return {
		"人稱": D.person(text),
		"疑問": D.interrogative(text),
		"祈使": D.imperative(text),
		"引述": D.reported(text),
		"反問": D.rhetorical(text),
		"認知": D.cognitive(text),
		"空框": D.empty_frame(text),
		"語氣": D.mood_v2(text),
		"時間": D.time_anchor_v2(text),
		"限制形狀": D.constraint_shape(text),
		"交棒": D.handoff(text, later),
	}


# ── F4 功能層：Form≠Function（2026-10-05 規則對齊修正令 §二 F4，PI 簽）────────
# 令文：「新增功能層：疑問形/祈使形命中後再判功能——**嵌入疑問**（疑問詞所在子句
#        語氣＝敘述、句尾無問號、或過去體貌）**不推主請求**；其餘照舊。」
#
# 表**單獨落檔** `signed_tables/function_layer.json`，本檔只讀不抄。
#
# **令文的條件組合有兩種讀法**（「、」與「或」混寫），CC 標明為解讀點：
#   `or`  ——任一條件成立即判嵌入疑問（字面的「或」）
#   `and` ——三條件全成立才算（嵌入疑問的典型形狀）
# 本檔**兩種都實作**，由 `F4_COMBINE` 選，預設取字面的 `or`；
# 兩種讀法的主請求召回對照數在迴歸報告裡並列，**不由 CC 挑**。
import json as _json
from pathlib import Path as _Path

_FL = _json.loads((_Path(__file__).resolve().parent
                   / "signed_tables/function_layer.json").read_text(encoding="utf-8"))
F4_FUNCTION_LAYER = True          # 旗標，迴歸用 off/on 同次執行
# "or"＝聊天端原寫法（已證殺保護線）；"and"＝對照；"third"＝PI 裁的第三讀法
# ── 定案（2026-10-06 F2/F4 裁決令 §F4，CC 依數自動定案）────────────────────
# 令文：「第三讀法過保護線（≥60/62）→採用；不過→**退回「且」讀法**，
#        CC 依數自動定案不再呈。」
# 實測（722 句、F6 保護線實跑）：
#   or    （三條件任一）     → 57/62（−3）  殺 3 句，病在「句尾無問號」單獨成立
#   third （敘述 or 過去）   → **59/62（−1）** 殺 1 句：M15/s04（**原句已去語料**：
#                              該句含完成貌標記「了」而觸發過去體貌，但句尾帶問號、
#                              是真問句）
#   and   （三條件全成立）   → **60/62（+0）** 殺 0 句；「句尾無問號」那一條正是保住
#                              M15/s04 的那道門
# → **第三讀法不過，依令文自動定案為「且」讀法。**
F4_COMBINE = "and"
F4_QMARKS = tuple(_FL["本令實作的唯一一條"]["問號集"])


def _f4_embedded_question(sig: dict, text: str) -> tuple[bool, list[str]]:
	"""這個疑問形是不是**嵌入疑問**（Form 疑問、Function 非請求）。

	三條件全部用既有簽核訊號，零新增詞：
	  語氣＝敘述（`mood_v2`）／句尾無問號（字面）／過去體貌（`time_anchor_v2`）
	"""
	hit = []
	if sig["語氣"]["標籤"] == "敘述":
		hit.append("語氣=敘述")
	if not text.rstrip().endswith(F4_QMARKS):
		hit.append("句尾無問號")
	if sig["時間"]["標籤"] == "過去":
		hit.append("過去體貌")
	if F4_COMBINE == "and":
		return len(hit) == 3, hit
	if F4_COMBINE == "third":
		# **第三讀法**（2026-10-06 F2/F4 裁決令 §F4）：PI 裁「令文三條件混寫是
		# 聊天端之誤；殺保護線 3 句者為『句尾無問號』單獨成立」。
		# 故刪該條，條件＝「語氣＝敘述 **或** 過去體貌」。
		k = [h for h in hit if h != "句尾無問號"]
		return bool(k), k
	return bool(hit), hit


def axis1(sig: dict, text: str = "") -> tuple[str, str]:
	"""回傳 (軸一, 開火的規則)。順序照 rules_v2.AXIS1_RULES。"""
	if sig["引述"]["命中"] and sig["人稱"]["有第三方主語"]:
		return "非請求", "1 引述否決"
	if sig["反問"]["命中"]:
		return "非請求", "2 反問否決"
	if (sig["祈使"]["命中"] and sig["人稱"]["有第三方主語"]
			and sig["時間"]["標籤"] == "過去"):
		return "非請求", "2b 請託事件敘事否決"
	if sig["疑問"]["命中"] and sig["認知"]["命中"] and not sig["祈使"]["命中"]:
		if sig["交棒"]["命中"]:
			return "非請求", "4 交棒 → 非請求"
		return "隱性需求", "5 自己收掉 → 隱性需求"
	if (sig["祈使"]["命中"] or sig["疑問"]["命中"]) and sig["空框"]["命中"]:
		return "空框請求", "6 空框請求"
	if sig["祈使"]["命中"] or sig["疑問"]["命中"]:
		# F4 功能層：Form 命中之後再判 Function。
		# **只擋「疑問形單獨撐起主請求」那一支**——祈使形命中者不套，
		# 因為令文只給了嵌入疑問這一條判準，祈使的功能判準未定（五分類留槽）。
		if (F4_FUNCTION_LAYER and sig["疑問"]["命中"]
				and not sig["祈使"]["命中"]):
			emb, why = _f4_embedded_question(sig, text)
			if emb:
				return "非請求", "F4 嵌入疑問不推主請求（%s）" % "／".join(why)
		return "主請求", "7 主請求"
	return "非請求", "8 兜底"


def axis2_mechanical(a1: str, sig: dict, text: str) -> dict:
	"""機械能定案的部分。定不了的回 `送模型戶` 與要問的片語。"""
	if a1 == "主請求":
		return {"軸二": "無", "規則": "1 主請求結構推導"}
	if a1 == "空框請求":
		return {"軸二": "無", "規則": "2 空框結構推導"}
	shape = sig["限制形狀"]["命中"]
	if not shape:
		# 裁四之一：祈使構式命中但限制形狀零命中 → 取賓語送模型戶（規格型限制）
		if sig["語氣"]["標籤"] == "祈使":
			obj = D.imperative_object(text)
			if obj["片語"]:
				return {"軸二": None, "規則": "5b 規格型限制 → 送模型戶",
				        "片語": obj["片語"], "動詞": obj["verb"]}
		return {"軸二": "材料", "規則": "3 限制形狀未命中"}
	if sig["時間"]["標籤"] == "過去" and sig["語氣"]["標籤"] == "敘述":
		return {"軸二": "材料", "規則": "4 過去敘述否決"}
	if sig["語氣"]["標籤"] == "祈使":
		return {"軸二": "限制", "規則": "5 祈使限制"}
	return {"軸二": None, "規則": "6 其餘 → 送模型戶",
	        "片語": sig["限制形狀"]["片語"][0] if sig["限制形狀"]["片語"] else None}


def classify_units(units: list[dict], *, ask_fn=None, task: str = "") -> list[dict]:
	"""units: [{sid, text}]。`ask_fn(片語, 任務) -> (答案, entry)`；None 則不問、留待補。"""
	out = []
	for i, u in enumerate(units):
		later = [v["text"] for v in units[i + 1:]]
		sig = signals(u["text"], later)
		a1, r1 = axis1(sig, u["text"])
		a2 = axis2_mechanical(a1, sig, u["text"])
		model_entry = None
		if a2["軸二"] is None:
			if ask_fn and a2.get("片語"):
				ans, model_entry = ask_fn(a2["片語"], task)
				a2["軸二"] = "限制" if ans == MODEL_POST_OPTIONS[0] else "材料"
				a2["模型答"] = ans
			else:
				a2["軸二"] = "材料"           # 沒接模型戶時的保守落點，標明
				a2["模型答"] = "（未問）"
		out.append({
			"sid": u["sid"], "sentence": u["text"],
			"軸一": a1, "軸一規則": r1,
			"軸二": a2["軸二"], "軸二規則": a2["規則"],
			"片語": a2.get("片語"), "模型答": a2.get("模型答"),
			"人稱": sig["人稱"]["標籤"],
			"語氣": sig["語氣"]["標籤"], "時間": sig["時間"]["標籤"],
			"權重": weight_of(a1, a2["軸二"]), "路由": route_of(a1, a2["軸二"]),
			"model_entry": model_entry,
		})
	return out
