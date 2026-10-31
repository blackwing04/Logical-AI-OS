"""Excerpt of the internal `experiments/composite-classifier/src/classifier.py`: the weight and route mapping only.

`weight_of`, `LexiconNotRegistered` and `route_of` are verbatim. The registry is read from the same signed table,
`signed_tables/lexicon_registry.json`, by a path relative to this file. The rest of the internal file asks the
model and is not published. Record: PUBLIC_NOTES.md section 7.
"""
from __future__ import annotations

import json
from pathlib import Path

_REG_PATH = Path(__file__).resolve().parent / "signed_tables/lexicon_registry.json"
try:
	_REGISTRY = json.loads(_REG_PATH.read_text(encoding="utf-8"))
except Exception as _e:        # 註冊表讀不到就是配置壞了，**不靜默**
	raise SystemExit("F5 註冊表讀取失敗（%s）：%s" % (_REG_PATH, _e))

REGISTERED = set(_REGISTRY["已註冊"])


def weight_of(axis1: str, axis2: str) -> str:
	"""雙軸權重映射（雙軸修正令第二節第 3 項）：
	高＝軸一主請求 或 軸二限制；中＝隱性需求／空框請求；低＝其餘。
	複合句（兩軸皆有值）取較高者，因為它同時承擔兩種義務。"""
	if axis1 == "主請求" or axis2 == "限制":
		return "高"
	if axis1 in ("隱性需求", "空框請求"):
		return "中"
	return "低"


class LexiconNotRegistered(RuntimeError):
	"""未註冊的域被請求路由。**拋錯不靜默**（令文 F5）。"""


def route_of(axis1: str, axis2: str) -> list[str]:
	"""路由改屬性鑰匙（第二節第 2 項）：複合句兩域都進，各取所需。

	F5：回傳前先過註冊表。**未註冊不得執行**——
	靜默略過一個該開的域，正是「規則端對供應端的契約假設未經驗證」那一族
	（條款 5 的同形病灶），所以這裡拋錯。
	"""
	domains = []
	if axis1 == "主請求":
		domains.append("問句詞表域")
	if axis2 == "限制":
		domains.append("限制詞表域")
	for d in domains:
		if d not in REGISTERED:
			raise LexiconNotRegistered(
				"域「%s」未註冊於 %s——未註冊不得執行（令文 F5）"
				% (d, _REG_PATH.name))
	return domains
