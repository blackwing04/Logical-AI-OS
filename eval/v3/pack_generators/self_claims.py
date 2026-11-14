# -*- coding: utf-8 -*-
"""偏好盲測 233 份回答中，模型對自己字數的宣稱：有幾份、以正文字數核對後屬實幾份（v3 資料包 3.1 版；正式重算聊天端 e44ba02 的粗掃）——零呼叫。
份＝偏好包的一份回答（同篇文字相同的臂合併為一份，份別 A／B／C 同盲標包）。
找宣稱（程式，事前定）：逐句（eff_body.sentences），句長 ≤160 字、且不是題目原句（eff_body.in_question），符合下列之一：
  長度宣稱：eff_body 結尾規則的 _T_CLAIM（字數／篇幅／N 字 與 符合／達到／超過／以內／左右／要求 在 30 字內相鄰）或 _T_BARE（獨立一行「約 N 字」）；
  明說不足：不足／少於（前面不是「不」）／未達／還差／不夠 後 10 字內有「字」。
限制：宣稱若只講某一部分（例：「每段約 500 字」），達標型仍以整份的長度條目判，不另核那一部分。
分型：句中有「要求／符合／滿足／達到／達標／以內／不超過／以上／至少」者為「達標型」，否則有數字＋字者為「報數型」。
核對（正文＝eff_body 剝除對使用者說的話後的文字；字數一律 v2 count_text_chars）：
  達標型 → 屬實＝該份長度條目在有效正文下全部達標（Joe 標準；取 padding_audit.json 逐份判定）；題目沒有長度條目者記「無長度條目，無從核」；
  報數型 → 屬實＝宣稱數與正文字數相差在 ±10% 內（引導建議；宣稱數、正文字數、有效字數全列）。
輸出（LF）：outputs/self_claims.md／.json。用法：self_claims.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.stdout.reconfigure(encoding="utf-8")
import eff_body as E                                                        # noqa: E402
import pack as P                                                            # noqa: E402

OUT = HERE / "outputs"
C = E.V2.count_text_chars
TOL = 0.10                                                                  # 引導建議：報數型的容差
SHORT_FALL = re.compile(r"(?:不足|(?<!不)少於|(?<!不)少于|未達|未达|還差|还差|不夠|不够).{0,10}字")    # 「不少於」是下限要求，不是明說不足
MEET = re.compile(r"(?:要求|符合|滿足|满足|達到|达到|達標|达标|以內|以内|不超過|不超过|以上|至少)")
NUM = re.compile(r"(\d[\d,]*)\s*(?:個|个)?\s*(?:中文)?字")
CS_LIST = {("PG03", "A"), ("PG06", "B"), ("PG20", "A"), ("PG22", "A"), ("PG23", "B"), ("PG35", "A"), ("PG35", "B"), ("PH26", "A"), ("PH08", "A"), ("PH09", "C")}


def claims(text: str, question: str) -> list[dict]:
	out = []
	for s in E.sentences(text):
		t = s.strip()
		if not t or len(t) > 160 or E.in_question(t, question):
			continue
		short = bool(SHORT_FALL.search(t))
		if not (short or E._T_CLAIM.search(t) or E._T_BARE.match(t)):
			continue
		m = NUM.search(t)
		kind = "明說不足" if short else "達標型" if MEET.search(t) else "報數型" if m else "達標型"
		out.append({"句": t, "型": kind, "宣稱數": int(m.group(1).replace(",", "")) if m else None})
	return out


def main() -> int:
	pa = {(r["id"], r["arm"]): r for r in json.loads((OUT / "padding_audit.json").read_text(encoding="utf-8"))["rows"]}
	recs = {u["id"]: u for us in P.records().values() for u in us}
	rows, n_copies = [], 0
	for cp in P.copies():
		n_copies += 1
		u = recs[cp["id"]]
		cl = claims(cp["text"], u["question"])
		if not cl:
			continue
		b = E.effective(cp["text"], question=u["question"])
		body = b.chars_body
		pr = pa[(cp["id"], cp["arms"][0])]
		len_ok = None if not int(pr["n_len"]) else all(v[0] is not False for v in pr["effective"].values())
		for c in cl:
			if c["型"] == "報數型":
				ok = abs(c["宣稱數"] - body) <= TOL * c["宣稱數"]
				why = "宣稱 %d 字，正文 %d 字（有效 %d）" % (c["宣稱數"], body, b.chars_effective)
			elif c["型"] == "明說不足":
				ok = len_ok is False if len_ok is not None else None
				why = "長度條目（有效正文）%s" % ({True: "全部達標", False: "未達", None: "無長度條目"}[len_ok])
			else:
				ok = len_ok
				why = "長度條目（有效正文）%s；正文 %d 字（有效 %d）" % ({True: "全部達標", False: "未達", None: "無長度條目，無從核"}[len_ok], body, b.chars_effective)
			rows.append({"id": cp["id"], "份": cp["slot"], "臂": cp["arms"], "型": c["型"], "句": c["句"], "宣稱數": c["宣稱數"], "正文字數": body,
			             "有效字數": b.chars_effective, "長度條目": [v[1] for v in pr["effective"].values()], "屬實": ok, "說明": why,
			             "聊天端粗掃列入": (cp["id"], cp["slot"]) in CS_LIST})
	per = {}
	for r in rows:                                                            # 一份可有多句：任一句不實即該份不實；全部無從核才記無從核
		k = (r["id"], r["份"])
		per.setdefault(k, []).append(r["屬實"])
	verdict = {k: (False if False in v else None if all(x is None for x in v) else True) for k, v in per.items()}
	claim_copies = {k for k in per if any(r["型"] != "明說不足" for r in rows if (r["id"], r["份"]) == k)}
	short_copies = {k for k in per if any(r["型"] == "明說不足" for r in rows if (r["id"], r["份"]) == k)}
	L = ["# 偏好盲測 %d 份回答：模型對自己字數的宣稱（程式正式算）" % n_copies, "",
	     "找法、分型、核對口徑見程式檔頭。報數型容差 ±%d%%（引導建議）。一份有多句宣稱時，任一句不實即該份記不實。" % int(TOL * 100), "",
	     "| 項 | 份 |", "| --- | --- |",
	     "| 聲稱字數達標或報出字數（達標型＋報數型） | %d |" % len(claim_copies),
	     "| 其中屬實 | %d |" % sum(1 for k in claim_copies if verdict[k] is True),
	     "| 其中不實 | %d |" % sum(1 for k in claim_copies if verdict[k] is False),
	     "| 其中無從核（題目無長度條目） | %d |" % sum(1 for k in claim_copies if verdict[k] is None),
	     "| 明說自己字數不足 | %d |" % len(short_copies), "",
	     "聊天端粗掃（e44ba02）列的 10 份：程式也找到 %d 份；程式另找到、粗掃未列 %d 份；粗掃列了、程式沒找到 %d 份（%s）。" % (
	         len(claim_copies & CS_LIST), len(claim_copies - CS_LIST), len(CS_LIST - claim_copies),
	         "、".join("%s %s" % k for k in sorted(CS_LIST - claim_copies)) or "—"), "",
	     "## 逐份逐句", "", "| 份 | 臂 | 型 | 宣稱句 | 核對 | 屬實 | 粗掃列入 |", "| --- | --- | --- | --- | --- | --- | --- |"]
	for r in sorted(rows, key=lambda x: (x["id"], x["份"])):
		L.append("| %s %s | %s | %s | %s | %s | %s | %s |" % (r["id"], r["份"], "、".join(r["臂"]), r["型"], r["句"].replace("|", "｜"), r["說明"],
		                                                  {True: "屬實", False: "不實", None: "無從核"}[r["屬實"]], "是" if r["聊天端粗掃列入"] else ""))
	(OUT / "self_claims.json").write_text(json.dumps({"copies": n_copies, "rows": rows, "verdict": {"%s|%s" % k: v for k, v in verdict.items()}}, ensure_ascii=False, indent=1),
	                                      encoding="utf-8", newline="\n")
	(OUT / "self_claims.md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
	print("\n".join(L))
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
