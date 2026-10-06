# -*- coding: utf-8 -*-
"""裁決器 v4 原型（控制層站 §二；2026-10-04 簽核放行令 §3）。

B = f(I, C, R) 的 **B 出口工程**：感知層候選在此被裁決為三類出口——
**執行 ／ 降權棄答 ／ 反問(ASK)**。

兩個感測器（政策首裁已裁）：
  **感測器一（吵架→ASK）**：降權候選（摺疊是 × 濾網無）不再靜默壓制，改入 ASK 池。
  **感測器二（機械×模型旁聽）**：機械定案限制句全數旁聽（一次前傳），模型反對→入池。

守側匯率（誤殺 1 : 防冤 10.7）為設計基準：**寧漏勿掰**，
所以池內未獲配額者一律**自動降權**（不是自動放行）。

## CC 不跨的三條界線（照令文）

1. **反問句模板不寫**：放行令 §3 明訂 CC 以佔位符 `[ASK:{句id}]` 落盤，
   模板文本由聊天端起草呈簽。本檔只產佔位符，**一個字都不撰**。
2. **K 配額不選**：§二.3 說「K 於開發集定」，放行令 §4 說開發集探索交數後由
   聊天端起草、PI 簽。所以本檔**輸出完整池序與各 K 的出口曲線，不挑 K**。
3. **型標不發明**：契約 §二 表要求 C 的型標（寫作規格／個人條件／資源清單／其他），
   可機械推導的只有**寫作規格**（修三 `v2寫作規格形` cue 命中）；
   個人條件／資源清單無任何既有偵測器，要新詞表＝判準層物件。
   故填「寫作規格」或「其他（型標詞表未簽，無法機械分型）」，**不自造分類器**。

## 池內排序：兩個方向都出，不鎖一個

§二.3 只寫「按裕度排序」，未寫方向。本檔同時輸出：
  `uncertain_first`（|裕度| 升冪＝最沒把握的先問）——ASK 的直覺用法
  `confident_first`（|裕度| 降冪＝感測器最有把握的先問）
兩序的各 K 出口計數都給，**選哪一個屬判準層決定**。

純度條款（契約 §二）：`rules_v2` 的 **R1（傳聞）命中者排除出 C** 並記理由。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import torch

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("H:/Projects/Logical-AI-OS")
BR = ROOT / "laios-bridge"
OUT = ROOT / "experiments/blindtest/outputs"
CS = ROOT / "experiments/control-station"
for p in (ROOT, ROOT / "experiments/semantic-station/scripts",
          ROOT / "experiments/mechanical-v2", ROOT / "scripts"):
	if str(p) not in sys.path:
		sys.path.insert(0, str(p))

from run_station2 import PROMPT_TEMPLATE as PROMPT_LISTEN

ADAPTER = "E:/AI_models/lora_output/qwen2.5-3b-instruct/zh-TW/negative-v1"
BASE = "E:/AI_models/qwen2.5-3b-instruct"
K_GRID = [0, 1, 2, 3, 5, 8, 10, 15, 20, 30, 50, 10 ** 9]

# 反問模板 v1：**PI 簽核「一字不改」**（2026-10-03 v4 驗收簽核令 §1）。
# **本檔在執行時從令文檔案直接讀取，全程不經人手轉寫**——
# 它是判準層物件，而條款 8 的量詞表事故就是轉寫毀的。
# 抽不到就 SystemExit，**不回退到任何手打副本**。
ASK_TEMPLATE_SRC = BR / "orders/2026-10-04_v4驗收預簽與卷三備戰案_draft.md"
_TPL_RE = re.compile(r"單一模板,佔位符替換:\n「(.+?)」\n", re.S)


def ask_template() -> str:
	import re as _re
	m = _TPL_RE.search(ASK_TEMPLATE_SRC.read_text(encoding="utf-8"))
	if not m:
		raise SystemExit("反問模板抽取失敗（%s）——停工回報，不以手打副本代替"
		                 % ASK_TEMPLATE_SRC.name)
	t = m.group(1)
	if "{原句}" not in t:
		raise SystemExit("反問模板缺 {原句} 佔位符，停工回報")
	return t
# 開發集 gold（**非遮盲**，在 repo 內，§三.1 明訂開發集自由迭代）。
# 兩張已燒卷的 gold＝答案本，由聊天端持有，執行端不可見也不計分。
DEV_GOLD = ROOT / "experiments/composite-classifier/gold/gold_40_dual_v1.jsonl"


def margin_of(rec):
	"""摺疊裕度＝P是 −(P否+P不)，即距 argmax 門檻的距離。"""
	fr = rec.get("摺疊_三跑")
	if not fr:
		return None
	r = fr[0]
	return r["P是"] - (r["P否"] + r["P不"])


def type_tag(rec):
	"""C 的型標。只認可機械推導的那一類，其餘照實標為未供應。"""
	hits = rec.get("表五命中") or []
	try:
		import lexicon_v2 as L
		ws = {w[0] for w in L.CONSTRAINT_SHAPE["v2寫作規格形"] if w[3] == "詞"}
	except Exception:
		ws = set()
	if any(h in ws for h in hits):
		return "寫作規格"
	return "其他（型標詞表未簽，無法機械分型）"


def main() -> None:
	ap = argparse.ArgumentParser()
	ap.add_argument("--corpus", required=True)
	ap.add_argument("--pipeline-tag", required=True)
	ap.add_argument("--label", required=True)
	# K 配額：簽核令已定 K＝全卷句數 10%（無條件捨去）。
	# 給 --k-pct 10 就按比例算；不給則沿用「不選 K、只交曲線」的探索模式。
	ap.add_argument("--k-pct", type=float, default=None)
	a = ap.parse_args()

	cp = BR / a.corpus
	if not cp.exists():
		cp = ROOT / a.corpus
	cases = {}
	for line in cp.read_text(encoding="utf-8").splitlines():
		if line.strip():
			c = json.loads(line)
			cases[c["id"]] = c
	pipe = json.loads((OUT / ("main_results_%s.json" % a.pipeline_tag)).read_text(encoding="utf-8"))
	rows = {r["id"]: r for r in pipe["rows"]}
	mech = pipe["mech"]
	final = pipe["final"]

	# ── 感測器二：機械定案限制句旁聽 ────────────────────────────────────────
	listen_ids = sorted(cid for cid, v in final.items() if v["來源"] == "機械層定案")
	from src.model.loader import load_model
	from src.model.chat_template import format_chat_prompt
	t0 = time.time()
	art = load_model(ADAPTER, base_model_dir=BASE)
	load_s = time.time() - t0
	tok, model = art.tokenizer, art.model
	dev = next(model.parameters()).device
	YES = tok.encode("是", add_special_tokens=False)[0]
	NO = tok.encode("否", add_special_tokens=False)[0]
	BU = tok.encode("不", add_special_tokens=False)[0]
	torch.manual_seed(20260924)

	listen = {}
	t0 = time.time()
	for cid in listen_ids:
		c = cases[cid]
		ids = tok(format_chat_prompt(tok, PROMPT_LISTEN.format(任務=c["任務"], 句子=c["句子"])),
		          return_tensors="pt").to(dev)
		with torch.no_grad():
			pr = torch.softmax(model(**ids).logits[0, -1, :].float(), dim=-1)
		py, pn, pb = pr[YES].item(), pr[NO].item(), pr[BU].item()
		listen[cid] = {"P是": py, "P否": pn, "P不": pb,
		               "傾向": "是" if py > pn + pb else "否", "裕度": py - (pn + pb)}
	listen_s = time.time() - t0

	# ── ASK 池 ──────────────────────────────────────────────────────────────
	TPL = ask_template()

	def ask_text(cid):
		"""反問句＝簽核模板替換 {原句}。模板文本在執行時自令文讀取，不經轉寫。"""
		return TPL.replace("{原句}", cases[cid]["句子"])

	# ── 池覆蓋補縫（2026-10-05 刀1R 令 §一.3）─────────────────────────────────
	# 令文：「凡吵架（摺疊是×濾網無）一律入池掛感測器一，**不得旁落**」。
	#
	# 舊路徑是**字串前綴比對 `端到端判` 開頭是「非限制（降權」**——那是消費端對
	# 供應端的標籤契約假設（條款 5 同形病灶）：修正一改一次標籤字樣，池就漏人，
	# 而漏人不會報錯，只會讓 ASK 少幾句。
	# 新路徑直接從 rows 的**原始條件**算吵架：摺疊判＝是 × 任一票＝無。
	# 兩路徑的差集逐句落盤（`pool_patch`），差集為 0 就是「本卷無旁落」的證據。
	def _is_fight(r):
		return (r.get("摺疊_判") == "是"
		        and (r.get("濾網_adapter票") == "無" or r.get("濾網_規則票") == "無"))

	fight_ids = {r["id"] for r in pipe["rows"] if _is_fight(r)}
	label_ids = {cid for cid, v in final.items()
	             if str(v["端到端判"]).startswith("非限制（降權")}
	pool_patch = {"吵架條件": sorted(fight_ids), "舊標籤路徑": sorted(label_ids),
	              "補縫新增（吵架但舊路徑旁落）": sorted(fight_ids - label_ids),
	              "舊路徑多收（非吵架卻在池）": sorted(label_ids - fight_ids)}

	pool = []
	for cid in sorted(fight_ids | label_ids):
		m = margin_of(rows.get(cid, {}))
		pool.append({"id": cid, "感測器": "一（吵架：摺疊是×濾網無）",
		             "裕度": m if m is not None else 0.0,
		             "標記": (rows.get(cid) or {}).get("標記"),
		             "入池路徑": ("吵架條件＋舊標籤" if cid in fight_ids and cid in label_ids
		                      else "吵架條件（補縫新增）" if cid in fight_ids
		                      else "舊標籤路徑（非吵架）"),
		             "反問句": ask_text(cid), "反問句_id標記": "[ASK:%s]" % cid})
	for cid in listen_ids:
		if listen[cid]["傾向"] == "否":
			pool.append({"id": cid, "感測器": "二（機械定案×模型旁聽反對）",
			             "裕度": listen[cid]["裕度"],
			             "標記": "模型反對（旁聽）",
			             "反問句": ask_text(cid), "反問句_id標記": "[ASK:%s]" % cid})
	for x in pool:
		x["裕度絕對值"] = abs(x["裕度"])
	order_u = sorted(pool, key=lambda x: (x["裕度絕對值"], x["id"]))
	order_c = sorted(pool, key=lambda x: (-x["裕度絕對值"], x["id"]))

	# ── v4.1 刀1：ASK 排序調頭（2026-10-05 B 站開工令 §刀1）─────────────────
	# 令文定義：「感測器一（吵架）句按**摺疊 P是 降冪**優先，感測器二句**殿後**」。
	# 立據＝保險絲帳本（誤殺 6 句 P是 偏高）＋開發集重驗。
	#
	# **令文未定的一點，照實標明**：感測器二句殿後之後，它們**彼此**的排序沒有指定。
	# 我按同一套邏輯延伸——感測器一用 P是 降冪是因為「高信心被誤殺最值得問」，
	# 那麼感測器二內部就用 |裕度| 升冪（反對信心越低、越不確定壓制是對的、越值得問）。
	# **這是我的選擇，不是令文規定。**
	for x in pool:
		if x["感測器"].startswith("一"):
			fr = (rows.get(x["id"]) or {}).get("摺疊_三跑")
			x["摺疊P是"] = fr[0]["P是"] if fr else None
		else:
			x["摺疊P是"] = None
	order_v41 = sorted(
		pool,
		key=lambda x: (0 if x["感測器"].startswith("一") else 1,
		               -(x["摺疊P是"] if x["摺疊P是"] is not None else -1.0)
		               if x["感測器"].startswith("一") else x["裕度絕對值"],
		               x["id"]))

	# ── v4.1 刀1-R：句型先行排序（2026-10-05 刀1R 重設計令 §一.1）──────────────
	# PI 裁：「可救句與廢料在**模型信心軸上不可分**、在**句型軸上可分**；
	#          病根＝用模型內在分數排序，違反句型先行原則」。
	# 令文定義（兩級，**未提感測器別**，所以刀1 的「感測器二殿後」整條撤掉）：
	#   第一級＝帶請求形特徵者優先；第二級（同級內）＝|裕度| 升冪。
	# 請求形特徵＝`request_form.py` 自機械層凍結碼枚舉，**零新增詞**（§一.2）。
	import request_form as RF
	for x in pool:
		rf = RF.request_form(cases[x["id"]]["句子"])
		x["帶請求形特徵"] = rf["帶請求形特徵"]
		x["請求形命中條"] = rf["命中條"]
		x["請求形特徵全表"] = rf["特徵"]
		x["請求形證據"] = rf["證據"]
	order_v41r = sorted(
		pool,
		key=lambda x: (0 if x["帶請求形特徵"] else 1, x["裕度絕對值"], x["id"]))

	# ── 出口三分（參數化於 K）────────────────────────────────────────────────
	def exits(K, order):
		ask = {x["id"] for x in order[:K]}
		out = {}
		for cid, v in final.items():
			src = v["來源"]
			inpool = any(p["id"] == cid for p in pool)
			if cid in ask:
				out[cid] = ("ASK", "配額內：%s" % next(p["感測器"] for p in pool if p["id"] == cid))
			elif inpool:
				out[cid] = ("降權棄答", "池內未獲配額，按守側匯率自動發落")
			elif v["端到端判"] == "限制":
				out[cid] = ("執行", src)
			else:
				out[cid] = ("降權棄答", src)
		return out

	print("# 裁決器 v4 原型：%s" % a.label)
	print()
	print("| 項 | 值 |")
	print("| --- | --- |")
	print("| 卷 | `%s`（%d 句 ／ %d 篇） |"
	      % (cp.relative_to(ROOT), len(cases), len({c["篇"] for c in cases.values()})))
	print("| 管線來源 | 丙-1 快檢台 `main_results_%s.json` |" % a.pipeline_tag)
	print("| 感測器一進料（降權候選） | **%d** |"
	      % sum(1 for p in pool if p["感測器"].startswith("一")))
	print("| 感測器二旁聽句（機械定案限制） | %d |" % len(listen_ids))
	print("| 感測器二反對票→入池 | **%d** |"
	      % sum(1 for p in pool if p["感測器"].startswith("二")))
	print("| **ASK 池合計** | **%d** |" % len(pool))
	print("| 池覆蓋補縫：吵架條件算出 | %d |" % len(fight_ids))
	print("| 池覆蓋補縫：**補縫新增（舊路徑旁落）** | **%d**%s |"
	      % (len(pool_patch["補縫新增（吵架但舊路徑旁落）"]),
	         "" if not pool_patch["補縫新增（吵架但舊路徑旁落）"]
	         else "（%s）" % "、".join(pool_patch["補縫新增（吵架但舊路徑旁落）"])))
	print("| 池覆蓋補縫：舊路徑多收（非吵架卻在池） | %d%s |"
	      % (len(pool_patch["舊路徑多收（非吵架卻在池）"]),
	         "" if not pool_patch["舊路徑多收（非吵架卻在池）"]
	         else "（%s）" % "、".join(pool_patch["舊路徑多收（非吵架卻在池）"])))
	print("| **帶請求形特徵（刀1-R 第一級）** | **%d ／ %d**（感一 %d ／ 感二 %d） |"
	      % (sum(1 for p in pool if p["帶請求形特徵"]), len(pool),
	         sum(1 for p in pool if p["帶請求形特徵"] and p["感測器"].startswith("一")),
	         sum(1 for p in pool if p["帶請求形特徵"] and p["感測器"].startswith("二"))))
	print("| 感測器二耗時 | %.1fs（%.3fs/句；模型載入另計 %.1fs） |"
	      % (listen_s, listen_s / max(len(listen_ids), 1), load_s))
	print()

	# ── 已定 K：出口三分落盤 ─────────────────────────────────────────────────
	K_DECIDED = None
	if a.k_pct is not None:
		K_DECIDED = int(len(cases) * a.k_pct / 100.0)   # 無條件捨去
		print("## 〇、已定 K（簽核令）")
		print()
		print("| 項 | 值 |")
		print("| --- | --- |")
		print("| K 規則 | 全卷句數 × %.0f%%，無條件捨去 |" % a.k_pct)
		print("| 全卷句數 | %d |" % len(cases))
		print("| **K** | **%d** |" % K_DECIDED)
		# v4.1 封筆（2026-10-05 刀4裁定與v4.1封筆令 §2）：
		# **已定 K 的出口三分改用刀1-R 序**（PI 裁「刀1-R 採用」）。
		# 舊序 order_u 與刀1 的 order_v41 仍逐句落盤，但**不再是出口的依據**。
		print("| 排序 | **刀1-R 句型先行**（第一級＝帶請求形特徵，第二級＝\\|裕度\\| 升冪） |")
		print("| ASK 率 | %.2f%%（驗收線 ≤10%%） |" % (100.0 * min(K_DECIDED, len(pool)) / len(cases)))
		print()
		e = exits(min(K_DECIDED, len(pool)), order_v41r)
		import collections as _c
		cc = _c.Counter(v[0] for v in e.values())
		print("| 出口 | 句數 |")
		print("| --- | --- |")
		for k in ("執行", "降權棄答", "ASK"):
			print("| %s | **%d** |" % (k, cc[k]))
		print()
		print("### 本卷實際 ASK 的 %d 句（含簽核模板替換後的反問句）" % cc["ASK"])
		print()
		print("| 序 | 句 | 感測器 | 帶請求形 | |裕度| | 反問句 |")
		print("| --- | --- | --- | --- | --- | --- |")
		for i, x in enumerate(order_v41r[:min(K_DECIDED, len(pool))], 1):
			print("| %d | %s | %s | %s | %.6f | %s |"
			      % (i, x["id"], x["感測器"][:1],
			         "**是**（%s）" % "、".join(x["請求形命中條"]) if x["帶請求形特徵"] else "否",
			         x["裕度絕對值"], x["反問句"].replace("|", "｜")))
		print()

	print("## 一、ASK 池（按裕度排序，兩序都出；曲線照交）")
	print()
	print("反問句＝**簽核模板 v1 替換 `{原句}`**（2026-10-03 簽核令 §1「一字不改」）。")
	print("模板文本由本腳本**在執行時自令文檔案讀取**，全程不經人手轉寫；")
	print("抽不到即停工，不回退到任何手打副本。另留 `反問句_id標記` 欄供追溯。")
	print()
	print("模板原文：`%s`" % TPL)
	print()
	print("### 1a 各 K 的出口計數（uncertain_first：|裕度| 升冪）")
	print()
	print("| K | ASK | 降權棄答 | 執行 |")
	print("| --- | --- | --- | --- |")
	import collections
	seen = set()
	for K in K_GRID:
		kk = min(K, len(pool))
		if kk in seen:
			continue
		seen.add(kk)
		c = collections.Counter(v[0] for v in exits(kk, order_u).values())
		print("| %s | %d | %d | %d |"
		      % ("全部（%d）" % kk if kk == len(pool) else str(kk),
		         c["ASK"], c["降權棄答"], c["執行"]))
	print()
	print("### 1b 各 K 的出口計數（confident_first：|裕度| 降冪）")
	print()
	print("| K | ASK | 降權棄答 | 執行 |")
	print("| --- | --- | --- | --- |")
	seen = set()
	for K in K_GRID:
		kk = min(K, len(pool))
		if kk in seen:
			continue
		seen.add(kk)
		c = collections.Counter(v[0] for v in exits(kk, order_c).values())
		print("| %s | %d | %d | %d |"
		      % ("全部（%d）" % kk if kk == len(pool) else str(kk),
		         c["ASK"], c["降權棄答"], c["執行"]))
	print()
	print("**執行欄不隨 K 變動**——池內句無論問或不問都不會變成「執行」，")
	print("這是守側匯率的直接結果（寧漏勿掰）。K 只決定「問」與「悄悄降權」的比例。")
	print()
	print("### 1c 池內逐句（uncertain_first 序）")
	print()
	print("| 序 | 句 | 感測器 | 裕度 | |裕度| | 標記 | 反問句 |")
	print("| --- | --- | --- | --- | --- | --- | --- |")
	for i, x in enumerate(order_u, 1):
		print("| %d | %s | %s | %+.6f | %.6f | %s | `%s` |"
		      % (i, x["id"], x["感測器"], x["裕度"], x["裕度絕對值"],
		         x["標記"] or "—", x["反問句"]))
	print()

	# ── 契約 §二 表的 B 出口格式 ────────────────────────────────────────────
	print("## 二、契約 §二 表：C / I / R / B 出口")
	print()
	exits_all = exits(10 ** 9, order_u)      # 參考態：池內全問
	exits_none = exits(0, order_u)           # 參考態：池內全降權
	r1_excluded = []
	C, I, R, B = [], [], [], []
	for cid, c in cases.items():
		rec = rows.get(cid, {})
		m = mech[cid]
		v = final[cid]
		codes = rec.get("濾網_規則碼") or []
		exit_all = exits_all[cid]
		exit_none = exits_none[cid]
		b = {"句id": cid, "出口_K全問": exit_all[0], "出口_K零問": exit_none[0],
		     "裁決理由": exit_all[1],
		     "觸發感測器": next((p["感測器"] for p in pool if p["id"] == cid), None),
		     "反問句": next((p["反問句"] for p in pool if p["id"] == cid), None)}
		B.append(b)
		if v["端到端判"] == "限制" or exit_all[0] == "ASK":
			if any(str(x).startswith("R1") for x in codes):
				r1_excluded.append({"句id": cid, "理由": "純度條款：R1 傳聞／轉述不入 C",
				                    "規則碼": codes})
			else:
				C.append({"句id": cid, "原文": c["句子"], "型標": type_tag(m),
				          "出口類別": exit_all[0], "來源層": v["來源"],
				          "票型_adapter": rec.get("濾網_adapter票"),
				          "票型_規則": rec.get("濾網_規則票"), "規則碼": codes,
				          "摺疊_P是": (rec.get("摺疊_三跑") or [{}])[0].get("P是"),
				          "摺疊_裕度": margin_of(rec),
				          "旁聽_裕度": listen.get(cid, {}).get("裕度"),
				          "表五命中": m["表五命中"]})
		if m["機械軸一"] == "主請求":
			I.append({"句id": cid, "原文": c["句子"], "機械框標": m["框架"]})
		if m["機械軸二"] == "材料":
			R.append({"句id": cid, "原文": c["句子"]})
	print("| 供應物 | 件數 | 說明 |")
	print("| --- | --- | --- |")
	print("| **C**（條件） | **%d** | 出口＝執行 或 ASK 者；含型標／出口類別／來源層／票型／P值（歸因鏈全留） |" % len(C))
	print("| ├ 其中型標＝寫作規格 | %d | 由修三 `v2寫作規格形` cue 推導 |"
	      % sum(1 for x in C if x["型標"] == "寫作規格"))
	print("| └ 其中型標＝其他 | %d | **型標詞表未簽，無法機械分型**（個人條件／資源清單缺偵測器） |"
	      % sum(1 for x in C if x["型標"] != "寫作規格"))
	print("| **純度條款排除** | **%d** | R1 傳聞／轉述不入 C |" % len(r1_excluded))
	print("| **I**（意圖載體） | %d | 機械軸一＝主請求者，含機械框標 |" % len(I))
	print("| **R**（場景素材） | %d | 機械軸二＝材料者 |" % len(R))
	print("| **B 出口** | %d | 逐句三分（K 全問／K 零問兩參考態）＋裁決理由＋觸發感測器＋反問句佔位符 |" % len(B))
	print()
	if r1_excluded:
		print("純度條款排除逐句：")
		for x in r1_excluded:
			print("- %s（規則碼 %s）" % (x["句id"], x["規則碼"]))
		print()

	# ── 開發集 gold 對照（僅開發集；已燒卷的 gold＝答案本，執行端不可見）──────
	xtab = None
	if DEV_GOLD.exists():
		g = {}
		for line in DEV_GOLD.read_text(encoding="utf-8").splitlines():
			if line.strip():
				x = json.loads(line)
				g["%s/%s" % (x["row"], x["sid"])] = x["gold軸二"]
		if sum(1 for cid in cases if cid in g) == len(cases) and len(cases) > 0:
			print("## 三、開發集 gold 對照（**非遮盲**；驗收數字仍由聊天端起草）")
			print()
			print("開發集 gold 在 repo 內（`gold_40_dual_v1.jsonl`），§三.1 明訂開發集自由迭代，")
			print("所以這裡出對照表作為「探索交數」的實質內容。")
			print("**兩張已燒卷的 gold＝答案本，由聊天端持有，本檔不碰、也不為那兩卷出對照。**")
			print()
			xtab = {}
			for nm, K in (("K=0（池內全降權，等同現行靜默壓制）", 0),
			              ("K=全部（池內全問）", len(pool))):
				e = exits(K, order_u)
				cell = collections.Counter()
				for cid in cases:
					gold_lim = (g[cid] == "限制")
					cell[(e[cid][0], "gold限制" if gold_lim else "gold非限制")] += 1
				xtab[nm] = {"%s×%s" % k: v for k, v in cell.items()}
				print("### %s" % nm)
				print()
				print("| 出口 | gold 限制 | gold 非限制 | 讀法 |")
				print("| --- | --- | --- | --- |")
				print("| 執行 | **%d** | **%d** | 真收 ／ 誤收 |"
				      % (cell[("執行", "gold限制")], cell[("執行", "gold非限制")]))
				print("| 降權棄答 | **%d** | %d | 漏抓 ／ 正確擋下 |"
				      % (cell[("降權棄答", "gold限制")], cell[("降權棄答", "gold非限制")]))
				print("| ASK | **%d** | **%d** | 可救回的漏抓 ／ 問對了的誤收 |"
				      % (cell[("ASK", "gold限制")], cell[("ASK", "gold非限制")]))
				print()
			print("→ 池內那 %d 句裡，gold 限制 **%d** 句、gold 非限制 **%d** 句。"
			      % (len(pool),
			         sum(1 for p in pool if g.get(p["id"]) == "限制"),
			         sum(1 for p in pool if g.get(p["id"]) != "限制")))
			print("這是 ASK 的上限：問對了最多能救回那 %d 句漏抓、擋下那 %d 句誤收。"
			      % (sum(1 for p in pool if g.get(p["id"]) == "限制"),
			         sum(1 for p in pool if g.get(p["id"]) != "限制")))
			print()
			print("### 池內逐句 × gold（供 K 探索）")
			print()
			print("| 序 | 句 | 感測器 | |裕度| | gold 軸二 |")
			print("| --- | --- | --- | --- | --- |")
			for i, x in enumerate(order_u, 1):
				print("| %d | %s | %s | %.6f | **%s** |"
				      % (i, x["id"], x["感測器"][:1], x["裕度絕對值"], g.get(x["id"], "—")))
			print()

	# ── 刀1 交件：新舊排序並排 ────────────────────────────────────────────────
	print()
	print("## 刀1 新舊排序並排（v4.1 ASK 排序調頭）")
	print()
	print("| 排序 | 定義 |")
	print("| --- | --- |")
	print("| 舊（v4） | `uncertain_first`：全池按 \\|裕度\\| 升冪 |")
	print("| **新（v4.1）** | **感測器一按摺疊 P是 降冪優先；感測器二殿後**（令文 §刀1） |")
	print()
	print("感測器二殿後後的內部排序令文未定——本檔用 \\|裕度\\| 升冪，**是 CC 的選擇不是令文規定**。")
	print()
	g = {}
	if DEV_GOLD.exists():
		for line in DEV_GOLD.read_text(encoding="utf-8").splitlines():
			if line.strip():
				x = json.loads(line)
				g["%s/%s" % (x["row"], x["sid"])] = x["gold軸二"]
	has_gold = bool(g) and all(cid in g for cid in cases)

	print("### 兩序的池內名次對照（前 20 名）")
	print()
	print("| 名次 | 舊序 句（感測器｜\\|裕度\\|） | **新序 句（感測器｜P是 或 \\|裕度\\|）** |")
	print("| --- | --- | --- |")
	for i in range(min(20, len(pool))):
		o, n = order_u[i], order_v41[i]
		def desc(x):
			if x["感測器"].startswith("一"):
				return "%s（一｜P是 %.4f）" % (x["id"], x["摺疊P是"] or -1)
			return "%s（二｜裕度 %.4f）" % (x["id"], x["裕度絕對值"])
		print("| %d | %s（%s｜%.4f） | **%s** |"
		      % (i + 1, o["id"], o["感測器"][:1], o["裕度絕對值"], desc(n)))
	print()

	# ── 刀1-R 交件 ───────────────────────────────────────────────────────────
	print()
	print("## 刀1-R 句型先行排序（2026-10-05 刀1R 重設計令 §一）")
	print()
	print("| 排序 | 定義 |")
	print("| --- | --- |")
	print("| 舊（v4） | 全池按 \\|裕度\\| 升冪 |")
	print("| 刀1（已駁） | 感測器一按摺疊 P是 降冪優先；感測器二殿後 |")
	print("| **刀1-R** | **第一級＝帶請求形特徵者優先；第二級＝\\|裕度\\| 升冪**（令文 §一.1） |")
	print()
	print("刀1-R **沒有**感測器別這一級——令文 §一.1 只寫兩級，所以刀1 的「感測器二殿後」整條撤掉。")
	print()
	print("### 第一級的開火率（這是本刀最該先看的數字）")
	print()
	print("| 特徵 | 入第一級 | 池內命中 | 感一 | 感二 |")
	print("| --- | --- | --- | --- | --- |")
	for fk in RF.FEATURES:
		n1 = sum(1 for p in pool if p["請求形特徵全表"][fk] and p["感測器"].startswith("一"))
		n2 = sum(1 for p in pool if p["請求形特徵全表"][fk] and p["感測器"].startswith("二"))
		print("| `%s` | %s | %d | %d | %d |"
		      % (fk, "**是**" if fk in RF.PRIMARY else "否（僅報）", n1 + n2, n1, n2))
	print("| **聯集（第一級布林值）** | — | **%d ／ %d** | %d | %d |"
	      % (sum(1 for p in pool if p["帶請求形特徵"]), len(pool),
	         sum(1 for p in pool if p["帶請求形特徵"] and p["感測器"].startswith("一")),
	         sum(1 for p in pool if p["帶請求形特徵"] and p["感測器"].startswith("二"))))
	print()
	print("### 池內帶特徵句逐句")
	print()
	print("| 句 | 感測器 | 命中條 | \\|裕度\\| | 原文 |")
	print("| --- | --- | --- | --- | --- |")
	for x in order_v41r:
		if x["帶請求形特徵"]:
			print("| %s | %s | %s | %.6f | %s |"
			      % (x["id"], x["感測器"][:1], "、".join(x["請求形命中條"]),
			         x["裕度絕對值"], cases[x["id"]]["句子"].replace("|", "｜")))
	print()

	if has_gold:
		print("### 救回曲線（開發集 gold，**非遮盲**）")
		print()
		print("救回＝ASK 名單中 gold＝限制 的句數（問對了可回收的漏抓）；")
		print("浪費＝ASK 名單中 gold＝非限制 的句數（問了只是確認它不是限制）。")
		print()
		print("| K | 舊序 救回／浪費 | 刀1 救回／浪費 | **刀1-R 救回／浪費** | 刀1-R−舊 |")
		print("| --- | --- | --- | --- | --- |")
		curve = {}
		for K in [1, 2, 3, 5, 8, 10, 15, 20, 30, len(pool)]:
			if K > len(pool):
				continue
			def sc(od):
				sel = [x["id"] for x in od[:K]]
				hit = sum(1 for i in sel if g.get(i) == "限制")
				return hit, K - hit
			ho, wo = sc(order_u)
			hn, wn = sc(order_v41)
			hr, wr = sc(order_v41r)
			curve[K] = {"old": [ho, wo], "new": [hn, wn], "v41r": [hr, wr]}
			print("| %s | %d／%d | %d／%d | **%d／%d** | **%+d** |"
			      % ("全部（%d）" % K if K == len(pool) else K,
			         ho, wo, hn, wn, hr, wr, hr - ho))
		print()
	else:
		print("### ASK 名單逐 K（本卷 gold＝答案本，執行端不可見，救回由聊天端計算）")
		print()
		curve = None
		print("| K | 舊序 ASK 名單 | 刀1 ASK 名單 | **刀1-R ASK 名單** |")
		print("| --- | --- | --- | --- |")
		for K in [1, 2, 3, 5, 8, 10, 15, 20, 30, len(pool)]:
			if K > len(pool):
				continue
			print("| %s | %s | %s | **%s** |"
			      % ("全部（%d）" % K if K == len(pool) else K,
			         "、".join(x["id"] for x in order_u[:K]),
			         "、".join(x["id"] for x in order_v41[:K]),
			         "、".join(x["id"] for x in order_v41r[:K])))
		print()

	payload = {"label": a.label, "corpus": str(cp.relative_to(ROOT)),
	           "pool_v41_order": order_v41,
	           "pool_v41r_order": order_v41r,
	           "pool_patch": pool_patch,
	           "request_form_provenance": RF.provenance(),
	           "request_form_missing": RF.F_NOTES,
	           "request_form_primary": list(RF.PRIMARY),
	           "request_form_self_audit": RF.self_audit(),
	           "knife1_recall_curve": curve,
	           "knife1_note": "感測器二殿後後的內部排序令文未定，本檔用 |裕度| 升冪，係 CC 選擇",
	           "knife1r_note": "刀1-R 兩級照令文 §一.1；請求形特徵全自機械層凍結碼枚舉，"
	                           "零新增詞（self_audit 須為空）；令文所舉『要求／必須／切忌／"
	                           "條列編號行首』四項在凍結碼中缺或語義反向，見 request_form_missing",
	           "pipeline_tag": a.pipeline_tag,
	           "sensor2": {"listened": len(listen_ids), "veto": sum(
		           1 for cid in listen_ids if listen[cid]["傾向"] == "否"),
	                       "seconds": round(listen_s, 2), "per_sentence": round(
		           listen_s / max(len(listen_ids), 1), 4), "load_seconds": round(load_s, 2),
	                       "readings": listen},
	           "pool_uncertain_first": order_u, "pool_confident_first": order_c,
	           "K_curve_uncertain": {}, "K_curve_confident": {},
	           "C": C, "I": I, "R": R, "B": B, "purity_excluded": r1_excluded,
	           "dev_gold_xtab": xtab,
	           "k_decided": K_DECIDED, "k_pct": a.k_pct,
	           # v4.1 封筆：出口以刀1-R 序為準（PI 裁「刀1-R 採用」）。
	           "exits_at_k": ({k: v for k, v in
	                           ((cid, list(x)) for cid, x in
	                            exits(min(K_DECIDED, len(pool)), order_v41r).items())}
	                          if K_DECIDED is not None else None),
	           "exits_at_k_ordering": "order_v41r（刀1-R 句型先行）",
	           "notes": {"ask_template": TPL,
	                     "ask_template_source": str(ASK_TEMPLATE_SRC.relative_to(ROOT)),
	                     "K": "未選；池序與 K 曲線交聊天端，PI 簽",
	                     "型標": "僅寫作規格可機械推導；其餘標為未供應，不自造分類器"}}
	import collections
	for K in K_GRID:
		for nm, od, tgt in (("K_curve_uncertain", order_u, "K_curve_uncertain"),
		                    ("K_curve_confident", order_c, "K_curve_confident")):
			c = collections.Counter(v[0] for v in exits(K, od).values())
			payload[tgt][str(K if K <= len(pool) else len(pool))] = dict(c)
	p = CS / ("judge_v4_%s.json" % a.label)
	p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
	print("逐句全產物：`%s`" % p.relative_to(ROOT))


if __name__ == "__main__":
	main()
