# -*- coding: utf-8 -*-
"""生成早停條件（刀3 落地；`orders/2026-10-05_三裁與卷四備戰令.md` §二①）。

**這是唯一一份。** `knife3_stopcond.py`（離線驗證）與 `run_perf.py`（上線）
都 import 這裡的函式，不各寫一份——判準與實作分兩份抄寫過的東西，
在這個專案裡毀過一張量詞表（條款 8）。

## 這兩個條件憑什麼算「判定零影響」

必須滿足：`cond(前綴)` 成立 ⟹ 消費端吃前綴的結果 ＝ 吃全文的結果。

- **感知段**：`schema_v1.parse_slots` 逐行掃、每欄取第一次出現。
  所以四欄各自的行都**完成**之後，`parse_slots` 的結果就定了。
  條件另外三個消費端（`rule_v2`／`parse`／`adjudicate`）是全文掃描的，
  後文理論上可能再命中規則——所以這個條件**不是從原理推出來就算數**，
  是在三卷 204 句上逐句驗過「成立 ⟹ 判定不變」才落地的
  （`knife3_stopcond.py`，不合格 0 句）。
- **丙-1 濾網段**：消費端是 `search(第一句…無)`，**找不到就回「有」**。
  所以唯一安全的停點是「匹配已出現」——出現了就不可能再變回「有」。
  反過來（還沒出現就停）會讓全部句子投「有」，那是把那一站關掉，不是零影響。
  這個陷阱在刀3 算帳時踩到過一次，記在那份報告 §三。

貪婪解碼（`do_sample=False`）下，早停只是**不要尚未產生的尾段**，
前綴逐 token 與完整生成相同，所以等價性是逐位元組的，不是統計上的。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
for _p in (_ROOT / "experiments/perf-station",
           _ROOT / "laios-bridge/reports/attachments/2026-09-24_框架消費b路"):
	if str(_p) not in sys.path:
		sys.path.insert(0, str(_p))

import rules_v2 as _RV        # noqa: E402  凍結件，只呼叫 norm()
import schema_v1 as _SCH      # noqa: E402  凍結件，只借用 _FIELD_RE

FIELDS = ("判定", "理由", "A", "B")
_AD_RE = re.compile(r"第一句[：:]?\s*無")      # 逐位元組同 run_perf.py 濾網讀法


def sense_done(text: str) -> bool:
	"""感知段早停：四欄齊，且**最後出現那一欄所在的行已被換行終結**。

	行未終結就停，會把半行餵給 `splitlines`，那一欄的內容被截斷——
	所以「行已終結」這個條件不是保守，是必要。
	"""
	lines = text.split("\n")
	complete = lines if text.endswith("\n") else lines[:-1]
	seen = set()
	for line in complete:
		m = _SCH._FIELD_RE.match(line.strip())
		if m:
			seen.add(m.group(1))
	return all(f in seen for f in FIELDS)


def filter_done(text: str) -> bool:
	"""丙-1 濾網段早停：`無` 的匹配已出現。沒出現時**不可**停。"""
	return bool(_AD_RE.search(_RV.norm(text)))


def make_criteria(tok, n_prompt: int, cond):
	"""包成 transformers 的 StoppingCriteriaList。cond 為 None 時回 None（不早停）。"""
	if cond is None:
		return None
	from transformers import StoppingCriteria, StoppingCriteriaList

	class _CondStop(StoppingCriteria):
		def __init__(self):
			self.fired = False

		def __call__(self, input_ids, scores, **kw):
			tail = tok.decode(input_ids[0][n_prompt:], skip_special_tokens=True)
			if cond(tail):
				self.fired = True
				return True
			return False

	return StoppingCriteriaList([_CondStop()])
