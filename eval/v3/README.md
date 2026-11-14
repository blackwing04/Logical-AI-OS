# v3 evaluation code

| Folder | What it is |
| --- | --- |
| [`checker/`](checker/) | The standalone rule checker (v1 and v2). Self-contained: Python standard library plus `lemminflect==0.2.3`. Reproduces every published verdict; see its README. |
| [`pack_generators/`](pack_generators/) | The programs that built data pack 3.1, published for provenance. They read internal run files that are not part of this release, so they do not run outside the project; comments are in Chinese. The single local model directory in `v3_pack_s3.py` is replaced by the environment variable `LAIOS_MODEL_DIR`. |
| [`export/`](export/) | The programs that produced this release from the internal run files (items, answers with redactions, annotations, reading exams, pack, per-item verdicts) and the pre-release scan. Published for provenance; like the pack generators they read internal files. |

To recompute a verdict from the published material:

```python
import json, sys
sys.path.insert(0, "eval/v3/checker")
import laios_checker_v2 as lc

items = {(r["bank"], r["id"]): r["items"] for r in map(json.loads, open("data/v3/items/checkable_items.jsonl", encoding="utf-8"))}
row = json.loads(open("data/v3/answers/A0g_s3.jsonl", encoding="utf-8").readline())
print(lc.check_items(items[(row["bank"], row["id"])], row["answer"]))
```

Answers that contain a redaction placeholder will not always reproduce the published verdict,
because the verdicts were computed on the original text; `data/v3/answers/REDACTIONS.csv` lists them.
