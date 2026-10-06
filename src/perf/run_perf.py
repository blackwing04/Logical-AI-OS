# -*- coding: utf-8 -*-
"""效能站：主臂管線的效能線（2026-10-02 工程站開工令 P0）。

**本檔是感知站 v1.0（d98d908 的 run_main_arm.py）的副本加效能刀。**
凍結件留在 `experiments/blindtest/scripts/run_main_arm.py` **一字不動**——
代際體檢要用它原樣重跑，效能站不能把它改掉。

每把刀獨立開關、預設全關（全關時行為與凍結件逐字相同）：
  `--n-runs N`   刀1：三跑合議改單跑。預設 0＝沿用凍結值（N_RUNS=3）。
                 前提已實測：卷一＋卷二 125 句的摺疊三跑 P 值**逐位元相同**、
                 判定不穩 0 句，故三跑對判定零資訊增量。
  刀4            機械層前濾短路——**凍結件本來就有**（轄區只收機械判「材料」句），
                 不是本站新增；實測卷二 99 句只有 62 句進模型、卷一 105 句只有 69 句。
                 本站照實記為「既有，非本次貢獻」，不冒領。

**P0 期間 F1 動了就是 bug**：每刀都對卷一逐句比對凍結件輸出，
判定不得變；浮點層面的 P 值微差逐句列出並附距門檻裕度。

原盲測主臂說明如下。
---
盲測主臂：全配置端到端（凍結配置一字不動）。

接線（凍結令）：機械層 → 轄區（只審機械判「材料」句）→ 感知（base, disable adapter）
→ 雙票濾網（adapter + rules_v2，雙無出場／單無放行帶標記）
→ 摺疊（餵自產分析原文，argmax，coverage 閘）→ 終審 adjudicator_v3b。

`rules_v2.py` 與 `adjudicator_v3b.py` **直接從 bridge 附件載入，不複製不改寫**
（凍結令宣告的雜湊就是那兩個檔的；複製一份等於執行端自己抄了判準層物件）。

逐節中間產物全落盤（同合體站規格）、逐節計時。執行端不評分。
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

import torch

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("H:/Projects/Logical-AI-OS")
SEM = ROOT / "experiments/semantic-station"
MECH = ROOT / "experiments/mechanical-v2"
BR = ROOT / "laios-bridge"
BPATH = BR / "reports/attachments/2026-09-24_框架消費b路"
OUT = ROOT / "experiments/blindtest/outputs"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SEM / "scripts"))
sys.path.insert(0, str(MECH))
sys.path.insert(0, str(ROOT / "experiments/perf-station"))
sys.path.insert(0, str(BPATH))                       # rules_v2 / adjudicator_v3b 原地載入

from probe_causal import PROMPT as P_PROBE, N_RUNS, MAX_NEW
from run_fold import PROMPT as P_FOLD, FULL_MED, FULL_FRAC
from probe_noise import SEED
import schema_v1 as SCH
import early_stop as ES          # 刀3 早停條件（與離線驗證共用同一份）

ADAPTER = "E:/AI_models/lora_output/qwen2.5-3b-instruct/zh-TW/negative-v1"
BASE = "E:/AI_models/qwen2.5-3b-instruct"
FROZEN = {
	"rules_v2.py": "3de646fcb702fbeca61caa7257fd2f72fdbf7d51f7ed01b8e53a58035a53a6b4",
	"adjudicator_v3b.py": "3777470fb3c277bafd31c941973077736b0a55d0de9ea1b752f0390dc6d28dc2",
}


def check_frozen():
	for n, want in FROZEN.items():
		got = hashlib.sha256((BPATH / n).read_bytes().replace(b"\r\n", b"\n")).hexdigest()
		if got != want:
			raise SystemExit("凍結雜湊不符：%s 得 %s，停工回報" % (n, got))
	return True


def mech_layer(cases):
	"""機械層：凍結版子句站，對 105 句跑軸二。"""
	import clause_v2 as C
	import reorder_v2 as R
	import detectors as D
	R.CASE1_POSSESSIVE_EXCEPTION = True
	D.CASE2_DEGREE_GUARD = True
	by_doc = {}
	for c in cases:
		by_doc.setdefault(c["篇"], []).append(c)
	out = {}
	for doc, rows in by_doc.items():
		units = [{"sid": r["id"].split("/")[1], "text": r["句子"]} for r in rows]
		for r, s in zip(rows, C.classify(units)):
			out[r["id"]] = {"機械軸二": s["軸二"], "機械軸一": s["軸一"],
			                "框架": s["框架"], "表五命中": s["表五命中"]}
	return out


def main() -> None:
	ap = argparse.ArgumentParser()
	ap.add_argument("--limit", type=int, default=0)
	# 卷路徑接線（2026-10-02 放行令 v2）：卷二換卷必須能指定輸入。
	# **預設值＝卷一路徑**，不給 --corpus 時行為與卷一逐字相同；
	# 判準層（規則／閾值／提示詞／權重）一字未動，這條只是輸入接線。
	ap.add_argument("--corpus", default="data/blindtest/test_sentences_105.jsonl")
	# 刀1（效能站 P0）：三跑合議改單跑。0＝沿用凍結值，保留開關供體檢切回。
	ap.add_argument("--n-runs", type=int, default=0)
	# 刀2（效能站 P0）：批次推理。0＝關（逐句，與凍結件同路徑）。
	# **前置探針已量到批次會改變生成文本**（8 句中 1 句，left padding 改變
	# 歸約順序→近乎平手的 token 翻 argmax→整段發散），所以本刀的迴歸
	# 必須逐句比到底，判定若變即停工。
	ap.add_argument("--batch", type=int, default=0)
	# 方案甲（PI 2026-10-03 格式凍結簽核令）：輸出規範化。0＝關。
	# 開啟後：感知走 V2 四欄格式、濾網改一次前傳讀判定槽（正則退休）、
	# 摺疊改吃結構化欄位。格式物件在 schema_v1.py。
	ap.add_argument("--schema", action="store_true")
	# 甲-1 保底案：A/B 改回全文照寫（去掉「限20字內」），其餘同方案甲。
	ap.add_argument("--ab-full", action="store_true")
	# 乙案對決（PI 2026-10-03 乙案對決令）：對決的只有濾網站。
	#   frozen-gen  丙-1 原封：凍結版題目＋凍結版讀法（生成＋正則），逐位元組不動
	#   frozen-slot 丙-2 原題＋讀筆尖：題目逐位元組同凍結版，前綴至「第一句:」讀首 token
	#   dedicated   丙-3 專屬填空格：**欄名未經簽核，尚未實作**（見報告）
	ap.add_argument("--filter", choices=("schema-slot", "frozen-gen", "frozen-slot"),
	                default="schema-slot")
	ap.add_argument("--tag", default="full")
	# 刀3 落地（2026-10-05 三裁令 §二①）：生成早停。
	# **做成旗標而不是直接改行為**——舊行為必須保持可重現，
	# 「落地後兩卷迴歸逐句零變動」這道閘才有對照組可比（同一個 binary 跑兩次）。
	# 條件在 early_stop.py，與離線驗證共用同一份程式碼，見該檔檔頭。
	ap.add_argument("--early-stop", action="store_true",
	                help="感知段四欄齊即停、丙-1 濾網段無匹配出現即停（判定零影響，已離線逐句驗證）")
	args = ap.parse_args()
	global N_RUNS
	n_frozen = N_RUNS
	if args.n_runs:
		N_RUNS = args.n_runs

	check_frozen()
	import rules_v2 as RV
	import adjudicator_v3b as ADJ

	# 卷路徑解析：先找 bridge（盲測卷在那裡），找不到再找 repo 根（開發集在 repo 內）。
	# 控制層站要跑開發集 202 句，而那份卷不在 bridge 下。純輸入接線。
	_cp = BR / args.corpus
	if not _cp.exists():
		_cp = ROOT / args.corpus
	cases = [json.loads(l) for l in
	         _cp.read_text(encoding="utf-8").splitlines()
	         if l.strip()]
	print("| 卷檔 | `%s` |" % _cp.relative_to(ROOT))
	print("# 盲測主臂：全配置端到端")
	print()
	print("| 項 | 值 |")
	print("| --- | --- |")
	print("| 測試卷 | %d 句 ／ %d 篇 |" % (len(cases), len({c["篇"] for c in cases})))
	print("| 凍結雜湊核對 | rules_v2 ✓ ／ adjudicator_v3b ✓ |")
	print("| 刀1 三跑→單跑 | N_RUNS %d（凍結值 %d）%s |"
	      % (N_RUNS, n_frozen, "**已開刀**" if N_RUNS != n_frozen else "未開（沿用凍結）"))
	print("| 刀2 批次推理 | %s |"
	      % ("**已開刀**，batch=%d（left padding）" % args.batch if args.batch
	         else "未開（逐句，與凍結件同路徑）"))
	print("| 濾網站（乙案對決） | %s |"
	      % {"schema-slot": "方案甲原案：新格式判定槽",
	         "frozen-gen": "**丙-1 原封**：凍結版題目＋生成＋正則",
	         "frozen-slot": "**丙-2 讀筆尖**：凍結版題目＋前綴至「第一句:」讀首 token"}[args.filter])
	print("| A/B 欄 | %s |"
	      % ("**甲-1 全文照寫**（保底案）" if args.ab_full else "甲-2 短語指認（限20字內）"))
	print("| 方案甲 輸出規範化 | %s |"
	      % ("**已開**（V2 四欄／槽讀濾網／結構化摺疊）" if args.schema
	         else "未開（自由散文，與凍結件同格式）"))
	print("| 刀4 機械層前濾短路 | **凍結件既有**，非本站新增 |")

	t_mech = time.time()
	mech = mech_layer(cases)
	mech_s = time.time() - t_mech
	from collections import Counter
	mc = Counter(mech[c["id"]]["機械軸二"] for c in cases)
	print("| 機械層 | 限制 **%d** ／ 材料 **%d** ／ 無 **%d**（%.2f 秒，零呼叫） |"
	      % (mc["限制"], mc["材料"], mc["無"], mech_s))

	# 轄區：只審機械判「材料」句（凍結令）
	juris = [c for c in cases if mech[c["id"]]["機械軸二"] == "材料"]
	print("| **轄區（機械判材料）** | **%d 句進模組** |" % len(juris))
	if args.limit:
		juris = juris[:args.limit]
	print(flush=True)

	from src.model.loader import load_model
	from src.model.chat_template import format_chat_prompt
	torch.cuda.reset_peak_memory_stats()
	t_load = time.time()
	art = load_model(ADAPTER, base_model_dir=BASE)
	load_s = time.time() - t_load
	tok, model = art.tokenizer, art.model
	dev = next(model.parameters()).device
	torch.manual_seed(SEED)
	YES = tok.encode("是", add_special_tokens=False)[0]
	NO = tok.encode("否", add_special_tokens=False)[0]
	BU = tok.encode("不", add_special_tokens=False)[0]

	def gen(body, cond=None):
		prompt = format_chat_prompt(tok, body)
		ids = tok(prompt, return_tensors="pt").to(dev)
		outs, ntok = [], []
		n_prompt = ids["input_ids"].shape[1]
		for _ in range(N_RUNS):
			# 刀3：早停只在 --early-stop 開啟時生效；關閉時 crit 為 None，
			# generate 的參數集與落地前**逐參數相同**（迴歸閘的對照組要靠這個）。
			crit = ES.make_criteria(tok, n_prompt, cond) if args.early_stop else None
			with torch.no_grad():
				o = model.generate(**ids, max_new_tokens=MAX_NEW, do_sample=False,
				                   temperature=None, top_p=None, top_k=None,
				                   pad_token_id=tok.pad_token_id,
				                   stopping_criteria=crit)
			new = o[0][n_prompt:]
			ntok.append(int(new.shape[0]))
			outs.append(tok.decode(new, skip_special_tokens=True))
		return prompt, outs, ntok

	def dist(body):
		prompt = format_chat_prompt(tok, body)
		ids = tok(prompt, return_tensors="pt").to(dev)
		runs = []
		for _ in range(N_RUNS):
			with torch.no_grad():
				pr = torch.softmax(model(**ids).logits[0, -1, :].float(), dim=-1)
			py, pn, pb = pr[YES].item(), pr[NO].item(), pr[BU].item()
			runs.append({"P是": py, "P否": pn, "P不": pb, "coverage": py + pn + pb,
			             "判": "是" if py > pn + pb else "否"})
		return prompt, runs

	WU = tok.encode("無", add_special_tokens=False)[0]
	YOU = tok.encode("有", add_special_tokens=False)[0]

	def frozen_slot(body):
		"""丙-2：題目逐位元組同凍結版，前綴至「第一句:」讀首 token，免 decode。"""
		prompt = format_chat_prompt(tok, body) + "第一句:"
		ids = tok(prompt, return_tensors="pt").to(dev)
		with torch.no_grad():
			lg = model(**ids).logits[0, -1, :].float()
		top2 = torch.topk(lg, 2)
		return {"筆尖": "無" if int(top2.indices[0]) == WU else "非無",
		        "logits": {"無": float(lg[WU]), "有": float(lg[YOU])},
		        "分差": float(top2.values[0] - top2.values[1]),
		        "top1合法": int(top2.indices[0]) == WU,
		        "top1_token": tok.decode([int(top2.indices[0])]),
		        "prompt": prompt}

	def slot_dist(body, use_adapter):
		"""方案甲③：一次前傳讀判定槽。無生成、無正則。"""
		prompt = format_chat_prompt(tok, body) + SCH.SLOT_PREFIX
		ids = tok(prompt, return_tensors="pt").to(dev)
		ctx = contextlib.nullcontext() if use_adapter else model.disable_adapter()
		with ctx, torch.no_grad():
			lg = model(**ids).logits[0, -1, :].float()
		three = {"是": float(lg[YES]), "否": float(lg[NO]), "不": float(lg[BU])}
		pick = max(three, key=three.get)
		top2 = torch.topk(lg, 2)
		return {"判定槽": pick, "判定槽_logits": three,
		        "判定槽_分差": float(top2.values[0] - top2.values[1]),
		        "判定槽_top1合法": int(top2.indices[0]) in (YES, NO, BU),
		        "prompt": prompt}

	def gen_batch(bodies, use_adapter):
		"""批次生成。left padding（生成必須左填充），跑完還原 padding_side。"""
		prompts = [format_chat_prompt(tok, b) for b in bodies]
		was = tok.padding_side
		tok.padding_side = "left"
		try:
			runs_all = [[] for _ in prompts]
			toks_all = [[] for _ in prompts]
			for _ in range(N_RUNS):
				for st in range(0, len(prompts), args.batch):
					chunk = prompts[st: st + args.batch]
					enc = tok(chunk, return_tensors="pt", padding=True).to(dev)
					ctx = contextlib.nullcontext() if use_adapter else model.disable_adapter()
					with ctx, torch.no_grad():
						o = model.generate(**enc, max_new_tokens=MAX_NEW, do_sample=False,
						                   temperature=None, top_p=None, top_k=None,
						                   pad_token_id=tok.pad_token_id)
					plen = enc["input_ids"].shape[1]
					for k in range(len(chunk)):
						new = o[k][plen:]
						# 去掉尾端 pad（批次裡短句會被補到最長那句的長度）
						keep = new[new != tok.pad_token_id] if tok.pad_token_id is not None else new
						toks_all[st + k].append(int(keep.shape[0]))
						runs_all[st + k].append(tok.decode(new, skip_special_tokens=True))
			return prompts, runs_all, toks_all
		finally:
			tok.padding_side = was

	def dist_batch(bodies):
		"""批次讀分佈。left padding，取每列最後一個非 pad 位置的 logits。"""
		prompts = [format_chat_prompt(tok, b) for b in bodies]
		was = tok.padding_side
		tok.padding_side = "left"
		try:
			out = [[] for _ in prompts]
			for _ in range(N_RUNS):
				for st in range(0, len(prompts), args.batch):
					chunk = prompts[st: st + args.batch]
					enc = tok(chunk, return_tensors="pt", padding=True).to(dev)
					with torch.no_grad():
						lg = model(**enc).logits
					for k in range(len(chunk)):
						pr = torch.softmax(lg[k, -1, :].float(), dim=-1)
						py, pn, pb = pr[YES].item(), pr[NO].item(), pr[BU].item()
						out[st + k].append({"P是": py, "P否": pn, "P不": pb,
						                    "coverage": py + pn + pb,
						                    "判": "是" if py > pn + pb else "否"})
			return prompts, out
		finally:
			tok.padding_side = was

	part = (OUT / ("main_partial_%s.jsonl" % args.tag)).open("w", encoding="utf-8")
	prog = (OUT / ("main_progress_%s.jsonl" % args.tag)).open("w", encoding="utf-8")
	# 牆鐘起點必須在**批次預跑之前**：批次模式下模型呼叫全在預跑裡，
	# 若沿用迴圈的 t0，total_seconds 只量到組裝迴圈，會印成 0s（初版就是這個 bug）。
	t_wall0 = time.time()
	# ── 刀2 批次預跑 ──────────────────────────────────────────────────────
	# 分階段：感知批 → adapter 批 → 規則／閘（CPU）→ 摺疊批（只跑過閘者）→ 終審（CPU）。
	# **判定邏輯一字不動**，只是把模型呼叫從逐句改成成批；
	# 摺疊只對過閘的句子跑，與逐句路徑的工作量一致（不多算雙無出場那幾句）。
	CS, CA, CF = {}, {}, {}
	PH = {"感知秒": 0.0, "adapter秒": 0.0, "摺疊秒": 0.0}
	if args.batch:
		bodies_p = [P_PROBE.format(任務=c["任務"], 句子=c["句子"]) for c in juris]
		ta = time.time()
		pr_s, run_s, tok_s = gen_batch(bodies_p, use_adapter=False)
		PH["感知秒"] = time.time() - ta
		tb = time.time()
		pr_a, run_a, tok_a = gen_batch(bodies_p, use_adapter=True)
		PH["adapter秒"] = time.time() - tb
		for k, c in enumerate(juris):
			CS[c["id"]] = (pr_s[k], run_s[k], tok_s[k])
			CA[c["id"]] = (pr_a[k], run_a[k], tok_a[k])
		# 先算閘，才知道哪些句子要摺疊（與逐句路徑同工作量）
		need = []
		for c in juris:
			base0 = CS[c["id"]][1][0]
			codes = RV.rule_v2(c["句子"], c["任務"], base0)
			av = "無" if re.search(r"第一句[::]?\s*無", RV.norm(CA[c["id"]][1][0])) else "有"
			if not (len([v for v in (av, "無" if codes else "有") if v == "無"]) == 2):
				need.append(c)
		if need:
			bodies_f = [P_FOLD.format(任務=c["任務"], 句子=c["句子"],
			                          分析=CS[c["id"]][1][0]) for c in need]
			tc = time.time()
			pr_f, run_f = dist_batch(bodies_f)
			PH["摺疊秒"] = time.time() - tc
			for k, c in enumerate(need):
				CF[c["id"]] = (pr_f[k], run_f[k])
		print("| 刀2 階段計時 | 感知 %.1fs ／ adapter %.1fs ／ 摺疊 %.1fs（%d 句進摺疊） |"
		      % (PH["感知秒"], PH["adapter秒"], PH["摺疊秒"], len(need)))
		print(flush=True)

	def _share(key):
		"""批次模式下，單句計時＝該階段總秒數均攤；落盤會標 `批次均攤`。"""
		return PH[key] / max(1, len(juris))

	t0, rows = time.time(), []
	for i, c in enumerate(juris, 1):
		rec = {**c, **mech[c["id"]]}
		# --- 感知：base（disable adapter）---
		ta = time.time()
		if args.schema:
			_tpl = SCH.PROMPT_SENSE_FULL if args.ab_full else SCH.PROMPT_SENSE
		else:
			_tpl = P_PROBE
		# 刀4 版面正規化**已拆除**（2026-10-05 刀4裁定與v4.1封筆令 §1：
		# 「驗收未達不收」判例——F1 擺動 17→16 零收斂，作用面與病灶不相交）。
		# 規則 v1 簽核留案於 `layout_norm.py`，與「模板側正規化」併掛 v4.2，
		# **不留旗標、不留墊片**（條款 3b：不養相容墊片，封印靠 git）。
		# 拆除前的證據在 `reports/attachments/2026-10-05_收尾①②/`。
		body_p = _tpl.format(
			任務=c["任務"], 句子=c["句子"])
		if args.batch:
			p_prompt, base_out, base_tok = CS[c["id"]]
			t_sense = _share("感知秒")
		else:
			with model.disable_adapter():
				# 四欄早停**只在方案甲（結構化感知）下掛**；`--schema` 關閉時
				# 感知題目是凍結版 P_PROBE，輸出沒有四欄，掛上去只會是空條件，
				# 還多一層誤觸風險（萬一自由散文裡出現「判定:」字樣）。
				p_prompt, base_out, base_tok = gen(
					body_p, cond=ES.sense_done if args.schema else None)
			t_sense = time.time() - ta
		# --- 濾網票一：adapter ---
		tb = time.time()
		slot = None
		fslot = None
		# 丙-1／丙-2 的濾網題目＝**凍結版 P_PROBE 逐位元組**，與感知的新格式脫鉤。
		# 鐵約束：adapter **題目文本**（＝P_PROBE 模板）逐位元組不動。
		body_frozen = P_PROBE.format(任務=c["任務"], 句子=c["句子"])
		if args.schema and args.filter == "frozen-gen":
			_, ad_out, ad_tok = gen(body_frozen, cond=ES.filter_done)
			t_ad = time.time() - tb
		elif args.schema and args.filter == "frozen-slot":
			fslot = frozen_slot(body_frozen)
			ad_out, ad_tok = [fslot["筆尖"]], [0]
			t_ad = time.time() - tb
		elif args.schema:
			# 方案甲③：濾網一次前傳讀槽，不生成、不掃正則。
			slot = slot_dist(body_p, True)
			ad_out, ad_tok = [slot["判定槽"]], [0]
			t_ad = time.time() - tb
		elif args.batch:
			_, ad_out, ad_tok = CA[c["id"]]
			t_ad = _share("adapter秒")
		else:
			_, ad_out, ad_tok = gen(body_p)
			t_ad = time.time() - tb
		# --- 濾網票二：rules_v2 ---
		tc = time.time()
		codes = RV.rule_v2(c["句子"], c["任務"], base_out[0])
		t_rule = time.time() - tc
		A, B, causal = RV.parse(base_out[0])
		rule_vote = "無" if codes else "有"
		if args.schema and args.filter == "frozen-gen":
			# 丙-1：凍結版讀法，逐位元組同凍結件的正則。
			ad_vote = "無" if re.search(r"第一句[::]?\s*無", RV.norm(ad_out[0])) else "有"
		elif args.schema and args.filter == "frozen-slot":
			# 丙-2：argmax 是「無」才投無票——對應凍結版正則「第一句:無」才算無。
			ad_vote = "無" if fslot["筆尖"] == "無" else "有"
		elif args.schema:
			ad_vote = SCH.adapter_vote(slot["判定槽"])
		else:
			ad_vote = "無" if re.search(r"第一句[::]?\s*無", RV.norm(ad_out[0])) else "有"
		votes = [v for v in (ad_vote, rule_vote) if v == "無"]
		if len(votes) == 2:
			gate, mark = "雙無出場", None
		elif len(votes) == 1:
			gate, mark = "單無放行", "單票疑無（%s）" % ("adapter" if ad_vote == "無" else "rules")
		else:
			gate, mark = "零無放行", None

		rec.update({"感知_prompt": p_prompt, "感知_base三跑": base_out, "感知_token": base_tok,
		            "配對_A": A, "配對_B": B, "配對_因果": causal,
		            "濾網_adapter三跑": ad_out, "濾網_adapter_token": ad_tok,
		            "濾網_adapter票": ad_vote, "濾網_規則票": rule_vote,
		            "濾網_規則碼": codes, "濾網_閘": gate, "標記": mark})
		if fslot is not None:
			rec.update({"濾網_筆尖": fslot["筆尖"], "濾網_筆尖_logits": fslot["logits"],
			            "濾網_筆尖_分差": fslot["分差"],
			            "濾網_筆尖_top1合法": fslot["top1合法"],
			            "濾網_prompt": fslot["prompt"]})
		if args.schema:
			# 感知的槽與格式健檢：只要開了方案甲就記，與濾網站用哪一案無關。
			sl = SCH.parse_slots(base_out[0])
			rec.update({"感知_槽": sl, "感知_格式健檢": SCH.slot_health(sl)})
		if slot is not None:
			# 判定槽只有方案甲原案（schema-slot）才有；丙-1／丙-2 的濾網不讀它。
			rec.update({"濾網_判定槽": slot["判定槽"],
			            "濾網_判定槽_logits": slot["判定槽_logits"],
			            "濾網_判定槽_分差": slot["判定槽_分差"],
			            "濾網_判定槽_top1合法": slot["判定槽_top1合法"],
			            "濾網_prompt": slot["prompt"]})

		if gate == "雙無出場":
			rec.update({"摺疊_判": None, "終審": None, "端到端判": "非限制",
			            "端到端理由": "雙票無，濾網出場",
			            "計時": {"感知秒": round(t_sense, 3), "adapter秒": round(t_ad, 3),
			                     "規則秒": round(t_rule, 4), "摺疊秒": 0.0, "終審秒": 0.0,
			                     "單題合計秒": round(t_sense + t_ad + t_rule, 3)}})
		else:
			td = time.time()
			if args.schema:
				sl = rec["感知_槽"]
				body_f = SCH.PROMPT_FOLD.format(
					任務=c["任務"], 句子=c["句子"],
					判定=sl.get("判定", "無"), 理由=sl.get("理由", "無"),
					A=sl.get("A", "無"), B=sl.get("B", "無"))
			else:
				body_f = P_FOLD.format(任務=c["任務"], 句子=c["句子"], 分析=base_out[0])
			if args.batch:
				f_prompt, fr = CF[c["id"]]
				t_fold = PH["摺疊秒"] / max(1, len(CF))
			else:
				f_prompt, fr = dist(body_f)
				t_fold = time.time() - td
			stable = len({x["判"] for x in fr}) == 1
			fold = fr[0]["判"] if stable else None
			te = time.time()
			adj, adj_why = ADJ.adjudicate(c["句子"], base_out[0])
			t_adj = time.time() - te
			if fold == "是" and mark:
				# 修正一（2026-09-25 最小修正令）：單票疑無句摺疊判「是」→**不升格**。
				# 雙票無（已在上面出場）、零票無（mark is None）行為不變。
				e2e, why = ("非限制（降權候選，標記保留）",
				            "修正一：%s，摺疊是不升格（終審=%s）" % (mark, adj))
			elif fold == "是" and adj == "採信":
				e2e, why = "限制", "摺疊是＋終審採信"
			elif fold == "是":
				e2e, why = "非限制", "摺疊是但終審駁回：%s" % adj_why
			else:
				e2e, why = "非限制", "摺疊否"
			rec.update({"摺疊_prompt": f_prompt, "摺疊_三跑": fr, "摺疊_穩定": stable,
			            "摺疊_判": fold, "摺疊_P是": fr[0]["P是"],
			            "摺疊_coverage": fr[0]["coverage"],
			            "終審": adj, "終審理由": adj_why,
			            "端到端判": e2e, "端到端理由": why,
			            "計時": {"感知秒": round(t_sense, 3), "adapter秒": round(t_ad, 3),
			                     "規則秒": round(t_rule, 4), "摺疊秒": round(t_fold, 3),
			                     "終審秒": round(t_adj, 4),
			                     "單題合計秒": round(t_sense + t_ad + t_rule + t_fold + t_adj, 3)}})
		rows.append(rec)
		part.write(json.dumps(rec, ensure_ascii=False) + "\n"); part.flush()
		el = time.time() - t0
		prog.write(json.dumps({"n": i, "total": len(juris), "id": c["id"],
		                       "elapsed": round(el, 1),
		                       "eta": round(el / i * (len(juris) - i), 1)},
		                      ensure_ascii=False) + "\n"); prog.flush()
		if i % 10 == 0 or i == len(juris):
			print("  %3d/%d  %.0fs  ETA %.0fs" % (i, len(juris), el, el / i * (len(juris) - i)),
			      flush=True)
	for f in (part, prog):
		f.close()

	# 端到端全卷判定：機械判限制／無 直接定案，轄區句用模組結果
	final = {}
	for c in cases:
		m = mech[c["id"]]["機械軸二"]
		if m == "限制":
			final[c["id"]] = {"端到端判": "限制", "來源": "機械層定案"}
		elif m == "無":
			final[c["id"]] = {"端到端判": "非限制", "來源": "機械層定案（無）"}
		else:
			r = next((x for x in rows if x["id"] == c["id"]), None)
			final[c["id"]] = ({"端到端判": r["端到端判"], "來源": "模組：" + r["端到端理由"]}
			                  if r else {"端到端判": None, "來源": "未跑（limit）"})

	cov = sorted(r["摺疊_coverage"] for r in rows if r.get("摺疊_coverage") is not None)
	med = (cov[len(cov) // 2] if len(cov) % 2 else (cov[len(cov)//2-1]+cov[len(cov)//2])/2) if cov else None
	frac = (sum(1 for x in cov if x >= 0.10) / len(cov)) if cov else None
	(OUT / ("main_results_%s.json" % args.tag)).write_text(
		json.dumps({"rows": rows, "mech": mech, "final": final, "cases": cases,
		            "adapter": ADAPTER, "base": BASE, "n_runs": N_RUNS, "seed": SEED,
		            "frozen_sha256": FROZEN, "mech_seconds": round(mech_s, 3),
		            # 條款 2：artifact 自證。早停是否開著必須留在檔裡，
		            # 否則日後看到兩份秒數不同的 artifact 無從分辨是配置還是機器。
		            "early_stop": bool(args.early_stop),
		            # ── 配置旗標全欄（2026-10-06 F1規格形豁免與卷七令 §二「CC 三件」）──
		            # **立案於一次真實損害**：卷六兩臂第一次全量跑，我用了預設
		            # `--filter schema-slot`，而封筆件的濾網是 `frozen-gen`。
		            # adapter 讀法一換，「單票疑無」從 70/79 塌到 8/254，
		            # 端到端限制率假性衝到 65.6%。當時 artifact **只記了 adapter／base／
		            # seed／n_runs／early_stop**，沒有一個欄位答得出「這輪用什麼配置跑的」，
		            # 我是靠比對 `濾網_adapter_token`（4 vs 0）才反推出來。
		            # 條款 2 要求 `run_metadata` 必記 `mode`——這就是效能站的等價欄位。
		            "config": {"corpus": args.corpus, "tag": args.tag,
		                       "schema": bool(args.schema), "filter": args.filter,
		                       "ab_full": bool(args.ab_full),
		                       "n_runs_arg": args.n_runs, "n_runs_frozen": n_frozen,
		                       "batch": args.batch, "limit": args.limit,
		                       "early_stop": bool(args.early_stop),
		                       "argv": sys.argv[1:]},
		            # 刀4 已拆除，故不再記 layout_norm 欄位。
		            # 帶 `layout_norm: true` 的 artifact 是拆除前的，見封筆包。
		            "early_stop_sha256": hashlib.sha256(
			            (Path(__file__).resolve().parent / "early_stop.py")
			            .read_bytes().replace(b"\r\n", b"\n")).hexdigest(),
		            "load_seconds": round(load_s, 2),
		            "mem_MiB": round(torch.cuda.max_memory_allocated() / 1024 ** 2),
		            "fold_gate": {"median_coverage": med, "frac_ge_0.10": frac,
		                          "ok": (med >= FULL_MED and frac >= FULL_FRAC) if cov else None},
		            "total_seconds": round(time.time() - t_wall0, 1)},
		           ensure_ascii=False, indent=1), encoding="utf-8")
	print()
	if cov:
		print("摺疊 coverage 中位 %.4f ／ ≥0.10 %.0f%% → %s"
		      % (med, 100 * frac, "閘過" if (med >= FULL_MED and frac >= FULL_FRAC) else "**閘不過**"))
	sh = [r["id"] for r in rows if r.get("摺疊_穩定") is False]
	print("摺疊三跑判定全同：**%d/%d**；抖動：%s"
	      % (sum(1 for r in rows if r.get("摺疊_判")), len([r for r in rows if "摺疊_判" in r]),
	         ", ".join(sh) or "無"))
	print("[完成] 轄區 %d 句，%.0fs" % (len(rows), time.time() - t_wall0))


if __name__ == "__main__":
	main()
