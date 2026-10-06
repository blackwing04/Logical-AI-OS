# -*- coding: utf-8 -*-
"""v4.5 封筆 manifest（2026-10-06 F1規格形豁免與卷七令 §二「過線→封筆 v4.5」）。零呼叫。

**令文要求：manifest 自 import 鏈反查，不憑印象列組件。**

v4.1 的 manifest 就是憑印象列的，漏了 `clause_v2.py` 與 `reorder_v2.py`
（自報於 v4.2 封筆包 §2.2），所以那份封筆雜湊沒蓋住它們。
本檔改成**真的走 import 圖**：從入口檔出發，用 `ast` 解析每個檔的 import，
在專案內遞迴解析成實際路徑，直到收斂。

入口＝兩臂與裁決器的三個 `main()`：
  `run_perf.py`（臂一管線）／`run_7b_arm.py`（臂二）／`judge_v4.py`（裁決器）
另加三個**非 import 可達**但判定會用到的資料面物件（簽核表與 gold），
它們以檔案路徑被讀取、不是 import，所以 import 圖抓不到——**照實分開列**。
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path("H:/Projects/Logical-AI-OS")
CS = ROOT / "experiments/control-station"

ENTRIES = [
	("臂一 管線（丙-1 快檢台）", "experiments/perf-station/run_perf.py"),
	("臂二 裸 7B", "experiments/blindtest/scripts/run_7b_arm.py"),
	("裁決器 v4.1 排序", "experiments/control-station/judge_v4.py"),
]

# import 圖搜尋路徑（與各入口的 sys.path 設定一致）
SEARCH = [
	"experiments/perf-station", "experiments/mechanical-v2",
	"experiments/semantic-station/scripts", "experiments/blindtest/scripts",
	"experiments/control-station", "experiments/composite-classifier/src",
	"laios-bridge/reports/attachments/2026-09-24_框架消費b路",
	"scripts", "tools", ".",
]

# import 圖抓不到的（以路徑讀取的資料面物件）——**照實分開列，不混進 import 鏈**
BY_PATH = [
	("刀2 簽核表（detectors 讀）", "experiments/mechanical-v2/signed_tables/knife2_one_classifier.json"),
	("F4 功能層表（pipeline_v2 讀）", "experiments/mechanical-v2/signed_tables/function_layer.json"),
	("F5 註冊表（classifier 讀）", "experiments/mechanical-v2/signed_tables/lexicon_registry.json"),
	("正典切分器（卷檔產生）", "tools/split_sentences.py"),
]

# 外部套件／標準庫前綴，不入 manifest
SKIP = ("torch", "transformers", "numpy", "pandas", "json", "re", "sys", "os",
        "pathlib", "argparse", "time", "hashlib", "collections", "itertools",
        "importlib", "difflib", "statistics", "ast", "contextlib", "random",
        "functools", "math", "typing", "datetime", "warnings", "copy", "bisect",
        "textwrap", "unicodedata", "subprocess", "shutil", "glob", "io", "csv")


def resolve(mod: str) -> Path | None:
	"""模組名 → 專案內實際路徑；找不到（外部套件）回 None。"""
	top = mod.split(".")[0]
	if top in SKIP:
		return None
	rel = mod.replace(".", "/")
	for d in SEARCH:
		for cand in (ROOT / d / (rel + ".py"), ROOT / d / rel / "__init__.py"):
			if cand.exists():
				return cand
	return None


def imports_of(p: Path) -> set[str]:
	try:
		tree = ast.parse(p.read_text(encoding="utf-8"))
	except Exception:
		return set()
	out = set()
	for n in ast.walk(tree):
		if isinstance(n, ast.Import):
			for a in n.names:
				out.add(a.name)
		elif isinstance(n, ast.ImportFrom):
			if n.level == 0 and n.module:
				out.add(n.module)
	return out


def main():
	print("# v4.5 封筆 manifest（**自 import 鏈反查**）")
	print()
	print("配置＝v4.4 ＋ **F2 描述框掛同一張寫作規格形豁免表** ＋ **刀1-C 改按族比**。")
	print("「無第一人稱」這個代理住在 F1 與 F2 兩處，v4.4 只補了 F1；本代補齊第二處。")
	print()
	print("取法同 v4.4：`ast` 從三個入口遞迴解析 import 至收斂——**走出來的，不是回想的**。")
	print("對照基準是 v4.4 的 31 組件清單，所以「改」欄答的是**本代動了哪幾個檔**。")
	print()
	seen: dict[Path, set[str]] = {}
	frontier = []
	for nm, e in ENTRIES:
		p = ROOT / e
		seen[p] = {"入口：%s" % nm}
		frontier.append(p)
	while frontier:
		cur = frontier.pop()
		for m in sorted(imports_of(cur)):
			r = resolve(m)
			if r is None:
				continue
			r = r.resolve()
			if r not in seen:
				seen[r] = set()
				frontier.append(r)
			seen[r].add("%s ← %s" % (m, cur.name))

	rows = []
	for p in sorted(seen, key=lambda x: str(x)):
		b = p.read_bytes().replace(b"\r\n", b"\n")
		rows.append({"檔": str(p.relative_to(ROOT)).replace(chr(92), "/"),
		             "sha256": hashlib.sha256(b).hexdigest(), "位元": len(b),
		             "被誰 import": sorted(seen[p])[:3], "來源": "import 鏈"})
	for nm, f in BY_PATH:
		rel = f
		if any(r["檔"] == rel for r in rows):
			continue
		b = (ROOT / f).read_bytes().replace(b"\r\n", b"\n")
		rows.append({"檔": rel, "sha256": hashlib.sha256(b).hexdigest(),
		             "位元": len(b), "被誰 import": ["（以路徑讀取）%s" % nm],
		             "來源": "路徑讀取"})

	# v4.2 的 manifest json 是扁平 dict{檔: {...}}；v4.4 起改成 {"rows": [...]}。
	# 兩種格式都讀——第一版我只寫了 v4.2 那種，結果 31 個組件全被標成「新列」、
	# 「本代有變」顯示 0，等於比對沒做。照實記：**是輸出看起來不對才抓到的**。
	prev = {}
	try:
		d = json.loads((CS / "v44_manifest.json").read_text(encoding="utf-8"))
		src = d["rows"] if isinstance(d, dict) and "rows" in d else None
		if src is not None:
			prev = {r["檔"].replace(chr(92), "/"): r["sha256"] for r in src}
		else:
			prev = {k.replace(chr(92), "/"): v["sha256"] for k, v in d.items()}
	except Exception:
		pass

	print("| # | 檔 | 來源 | sha256（前16） | 位元 | 對 v4.4 |")
	print("| --- | --- | --- | --- | --- | --- |")
	cnt = {"同": 0, "改": 0, "新列": 0}
	for i, r in enumerate(rows, 1):
		h = r["sha256"]
		o = prev.get(r["檔"])
		tag = "同" if o == h else ("改" if o else "新列")
		cnt[tag] += 1
		print("| %d | `%s` | %s | `%s` | %d | %s |"
		      % (i, r["檔"], r["來源"], h[:16], r["位元"],
		         tag if tag == "同" else "**%s**" % tag))
		r["對v43"] = tag
	print()
	print("| 項 | 值 |")
	print("| --- | --- |")
	print("| **組件數** | **%d**（import 鏈 %d ＋ 路徑讀取 %d） |"
	      % (len(rows), sum(1 for r in rows if r["來源"] == "import 鏈"),
	         sum(1 for r in rows if r["來源"] == "路徑讀取")))
	print("| 與 v4.4 相同 | **%d** |" % cnt["同"])
	print("| 本代有變 | **%d** |" % cnt["改"])
	print("| v4.4 未列（本代新進 import 鏈） | **%d** |" % cnt["新列"])
	print()
	print("v4.4 走出 31 個；本代 **%d** 個。兩代同一套走法，所以差額是真的組件變動，"
	      % len(rows))
	print("不再是「手列漏了多少」那種雜訊。")
	print()
	print("### 旗標狀態（判定行為的一部分，必須入 manifest）")
	print()
	sys.path.insert(0, str(ROOT / "experiments/mechanical-v2"))
	sys.path.insert(0, str(ROOT / "experiments/composite-classifier/src"))
	import clause_v2 as C
	import detectors as D
	import pipeline_v2 as P
	import reorder_v2 as R
	flags = {"F1_DOC_STATUS": C.F1_DOC_STATUS,
	         "F1_WRITING_SPEC_EXEMPT（本代新增）": C.F1_WRITING_SPEC_EXEMPT,
	         "F1_WS_SCOPE": C.F1_WS_SCOPE,
	         "F2_WS_EXEMPT（本代新增）": R.F2_WS_EXEMPT,
	         "F2_DESCRIPTIVE_NON_FIRST": R.F2_DESCRIPTIVE_NON_FIRST,
	         "F2_SCOPE": R.F2_SCOPE,
	         "F3_IMPERATIVE_YOU": C.F3_IMPERATIVE_YOU,
	         "F4_FUNCTION_LAYER": P.F4_FUNCTION_LAYER,
	         "F4_COMBINE": P.F4_COMBINE,
	         "KNIFE1C_PASTE_SCOPE": C.KNIFE1C_PASTE_SCOPE,
	         "KNIFE1C_AS_FALLBACK": C.KNIFE1C_AS_FALLBACK,
	         "KNIFE2_ONE_CLASSIFIER": D.KNIFE2_ONE_CLASSIFIER,
	         "KNIFE1_AGG_FIX（棄決）": C.KNIFE1_AGG_FIX,
	         "CASE1_POSSESSIVE_EXCEPTION": R.CASE1_POSSESSIVE_EXCEPTION,
	         "CASE2_DEGREE_GUARD": D.CASE2_DEGREE_GUARD,
	         "TIME_INHERIT": C.TIME_INHERIT,
	         "PERSON_INHERIT": C.PERSON_INHERIT}
	print("| 旗標 | 值 |")
	print("| --- | --- |")
	for k, v in flags.items():
		print("| `%s` | **%s** |" % (k, v))
	print()
	(CS / "v45_manifest.json").write_text(
		json.dumps({"rows": rows, "flags": {k: str(v) for k, v in flags.items()},
		            "entries": [e for _n, e in ENTRIES]},
		           ensure_ascii=False, indent=1), encoding="utf-8")
	print("完整 64 位雜湊：`experiments/control-station/v45_manifest.json`")


if __name__ == "__main__":
	main()
