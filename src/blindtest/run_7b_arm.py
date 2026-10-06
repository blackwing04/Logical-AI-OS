# -*- coding: utf-8 -*-
"""盲測對照臂：裸 7B（無框架、無 adapter）。

Qwen2.5-7B-instruct、4-bit NF4 ＋ double quant ＋ fp16、temp 0、N=3，
**二期義務句型儀器**（答案槽 ＋ 首 token P(是) vs P(否)+P(不)），直接判 105 句軸二是否限制。

問句模板直接 `import` 自病三站二期跑批（`run_station2.py`），不重打。
執行端不評分。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import torch

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("H:/Projects/Logical-AI-OS")
SEM = ROOT / "experiments/semantic-station"
BR = ROOT / "laios-bridge"
OUT = ROOT / "experiments/blindtest/outputs"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(SEM / "scripts"))

from run_station2 import PROMPT_TEMPLATE as PROMPT, N_RUNS, FULL_MED, FULL_FRAC
from probe_noise import SEED

MODEL = "E:/AI_models/qwen2.5-7b-instruct"


def model_fingerprint(d: Path):
	out = {}
	for f in sorted(d.glob("*.safetensors")) + sorted(d.glob("config.json")):
		out[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
	return out


def main() -> None:
	ap = argparse.ArgumentParser()
	ap.add_argument("--model-dir", default=MODEL)
	ap.add_argument("--limit", type=int, default=0)
	# 卷路徑接線（2026-10-02 放行令 v2）：卷二換卷必須能指定輸入。
	# **預設值＝卷一路徑**，不給 --corpus 時行為與卷一逐字相同；
	# 判準層（規則／閾值／提示詞／權重）一字未動，這條只是輸入接線。
	ap.add_argument("--corpus", default="data/blindtest/test_sentences_105.jsonl")
	ap.add_argument("--tag", default="full")
	args = ap.parse_args()

	cases = [json.loads(l) for l in
	         (BR / args.corpus).read_text(encoding="utf-8").splitlines()
	         if l.strip()]
	if args.limit:
		cases = cases[:args.limit]

	print("# 盲測對照臂：裸 7B")
	print()
	print("| 項 | 值 |")
	print("| --- | --- |")
	print("| 模型 | `%s` |" % args.model_dir)
	print("| 儀器 | 二期義務句型（答案槽＋首 token 分佈），無框架無 adapter |")
	print("| 句數 | %d |" % len(cases), flush=True)

	fp = model_fingerprint(Path(args.model_dir))
	for k, v in fp.items():
		print("| %s sha256 | `%s` |" % (k, v[:48] + "…"))

	from src.model.loader import load_model
	from src.model.chat_template import format_chat_prompt
	torch.cuda.reset_peak_memory_stats()
	t_load = time.time()
	art = load_model(args.model_dir)
	load_s = time.time() - t_load
	tok, model = art.tokenizer, art.model
	dev = next(model.parameters()).device
	torch.manual_seed(SEED)
	YES = tok.encode("是", add_special_tokens=False)[0]
	NO = tok.encode("否", add_special_tokens=False)[0]
	BU = tok.encode("不", add_special_tokens=False)[0]
	print("| 載入 ／ 記憶體峰值 | %.1f 秒 ／ %.0f MiB |"
	      % (load_s, torch.cuda.max_memory_allocated() / 1024 ** 2))
	print("| 是／否／不 token id | %d ／ %d ／ %d |" % (YES, NO, BU))
	print(flush=True)

	part = (OUT / ("arm7b_partial_%s.jsonl" % args.tag)).open("w", encoding="utf-8")
	rt = (OUT / ("arm7b_runtime_%s.jsonl" % args.tag)).open("w", encoding="utf-8")
	prog = (OUT / ("arm7b_progress_%s.jsonl" % args.tag)).open("w", encoding="utf-8")
	t0, rows = time.time(), []
	for i, c in enumerate(cases, 1):
		body = PROMPT.format(任務=c["任務"], 句子=c["句子"])
		prompt = format_chat_prompt(tok, body)
		ids = tok(prompt, return_tensors="pt").to(dev)
		ta = time.time()
		runs = []
		for _ in range(N_RUNS):
			with torch.no_grad():
				pr = torch.softmax(model(**ids).logits[0, -1, :].float(), dim=-1)
			py, pn, pb = pr[YES].item(), pr[NO].item(), pr[BU].item()
			top = torch.topk(pr, 5)
			runs.append({"P是": py, "P否": pn, "P不": pb, "coverage": py + pn + pb,
			             "判": "限制" if py > pn + pb else "非限制",
			             "top5": [[tok.decode([t]), round(p, 4)]
			                      for t, p in zip(top.indices.tolist(), top.values.tolist())]})
		el_one = time.time() - ta
		stable = len({x["判"] for x in runs}) == 1
		rows.append({**c, "三跑": runs, "穩定": stable,
		             "判": runs[0]["判"] if stable else "**抖動作廢**",
		             "P是": runs[0]["P是"], "coverage": runs[0]["coverage"],
		             "秒": round(el_one, 3)})
		part.write(json.dumps(rows[-1], ensure_ascii=False) + "\n"); part.flush()
		rt.write(json.dumps({"id": c["id"], "prompt_sent": prompt}, ensure_ascii=False) + "\n")
		rt.flush()
		el = time.time() - t0
		prog.write(json.dumps({"n": i, "total": len(cases), "id": c["id"],
		                       "elapsed": round(el, 1),
		                       "eta": round(el / i * (len(cases) - i), 1)},
		                      ensure_ascii=False) + "\n"); prog.flush()
		if i % 20 == 0 or i == len(cases):
			print("  %3d/%d  %.0fs  ETA %.0fs" % (i, len(cases), el, el / i * (len(cases) - i)),
			      flush=True)
	for f in (part, rt, prog):
		f.close()

	cov = sorted(r["coverage"] for r in rows)
	med = cov[len(cov) // 2] if len(cov) % 2 else (cov[len(cov)//2-1]+cov[len(cov)//2])/2
	frac = sum(1 for x in cov if x >= 0.10) / len(cov)
	ok = med >= FULL_MED and frac >= FULL_FRAC
	(OUT / ("arm7b_results_%s.json" % args.tag)).write_text(
		json.dumps({"rows": rows, "model_dir": args.model_dir, "model_sha256": fp,
		            "n_runs": N_RUNS, "seed": SEED, "prompt_template": PROMPT,
		            "yes_id": YES, "no_id": NO, "bu_id": BU,
		            # 配置旗標全欄（2026-10-06 F1規格形豁免與卷七令「CC 三件」）：
		            # 與臂一同補。臂二的旗標少，但「這輪跑的是哪一卷、有沒有 limit」
		            # 同樣必須從 artifact 自己讀得出來，不靠報告的記憶。
		            "config": {"corpus": args.corpus, "tag": args.tag,
		                       "model_dir": args.model_dir, "limit": args.limit,
		                       "argv": sys.argv[1:]},
		            "load_seconds": round(load_s, 2),
		            "mem_MiB": round(torch.cuda.max_memory_allocated() / 1024 ** 2),
		            "gate": {"median_coverage": med, "frac_ge_0.10": frac, "ok": ok},
		            "total_seconds": round(time.time() - t0, 1)},
		           ensure_ascii=False, indent=1), encoding="utf-8")
	sh = [r["id"] for r in rows if not r["穩定"]]
	from collections import Counter
	print()
	print("coverage 中位 %.4f ／ ≥0.10 %.0f%% → **%s**" % (med, 100 * frac, "閘過" if ok else "閘不過"))
	print("三跑判定全同：**%d/%d**；抖動：%s" % (len(rows) - len(sh), len(rows), ", ".join(sh) or "無"))
	print("判定分佈：%s" % dict(Counter(r["判"] for r in rows)))
	print("[完成] %d 句，%.0fs" % (len(rows), time.time() - t0))


if __name__ == "__main__":
	main()
