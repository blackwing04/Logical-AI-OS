English | [繁體中文](QUICKSTART.zh-TW.md)

# Quickstart

What you can run from this repository, with one command each and the output it printed.

Every command below was run on 2026-10-31 in a fresh virtual environment on a fresh clone of tag
`v2.0.1-repro` (Windows 11, Git Bash). It was run twice, on Python 3.13.0 and 3.13.9, and both runs
printed the same output. The outputs are pasted as printed.

```bash
git clone https://github.com/blackwing04/Logical-AI-OS.git
cd Logical-AI-OS
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate (cmd / PowerShell), source .venv/Scripts/activate (Git Bash)
```

All commands are run from the repository root. On macOS, use `shasum -a 256` where `sha256sum` appears.

## 1. Run the recognizer on your own sentences

**What it does.** It runs the v4.5 judgement chain (mechanical layer, zero model calls). The chain
splits a Chinese request into sentences and clauses, and labels each sentence on two axes:

- **axis 1**, whether the sentence is a request: `主請求` main request, `空框請求` empty-frame request,
  `隱性需求` implicit need, `非請求` not a request;
- **axis 2**, what it is to the answer: `限制` a constraint on the answer, `材料` material to be
  processed, `無` none (the sentence is the request itself).

It also prints:

- the **frame** of each clause, which decides whether table 5 (the constraint-cue table) is consulted;
- the **table-5 cues** that fired, each with the table it came from.

**Install.** Nothing beyond Python. The recognizer uses the standard library only.

```bash
python src/run_recognizer.py "我下週要跟主管報告這季的業績。請幫我寫一份簡報大綱，不要超過五點，每點三十字以內。可以順便建議一個標題嗎？"
```

```text
s01  我下週要跟主管報告這季的業績。
     axis 1: 非請求   axis 2: 材料   frame: 自陳情境
     table-5 cues: -
s02  請幫我寫一份簡報大綱，不要超過五點，每點三十字以內。
     axis 1: 主請求   axis 2: 限制   frame: 主請求框／過去敘事框／自陳情境
     table-5 cues: 以內 (table5_limiting_head)、三十字 (v2_writing_spec)
s03  可以順便建議一個標題嗎？
     axis 1: 主請求   axis 2: 材料   frame: 描述框／主請求框
     table-5 cues: -
```

**Notes on this example.**

- The request was written for this guide; it is not from any corpus.
- A sentence with several clauses lists one frame per clause.
- `不要超過五點` did not fire: "N points" is outside table 5. That is the recognizer's real behaviour,
  shown as is.

**More detail.** `--file request.txt` reads the request from a file. `--json` prints the full record of
every sentence, one JSON line each: the rule that fired on each axis, per-clause signals and the
sentence's status in the whole request.

**What makes it run.** Two small modules complete the published chain:

- [`src/mechanical/canon_v3/`](src/mechanical/canon_v3/) holds the table-5 cue detector and its tables;
- [`src/mechanical/classifier.py`](src/mechanical/classifier.py) holds the weight and route mapping.

Both are public copies or excerpts of internal files; the record is in
[`PUBLIC_NOTES.md`](PUBLIC_NOTES.md) section 7.

**How the result was checked.** On every text field of the published S1–S3 items (4,482 sentences),
this chain printed byte-identical output to the internal one.

**Where to read the rules.**

- the rule order is in [`src/mechanical/rules_v2.py`](src/mechanical/rules_v2.py);
- the axis-1 rules are in [`src/mechanical/pipeline_v2.py`](src/mechanical/pipeline_v2.py), and the axis-2 frames are in [`src/mechanical/reorder_v2.py`](src/mechanical/reorder_v2.py);
- the signed word lists are in [`src/mechanical/lexicon_v2.py`](src/mechanical/lexicon_v2.py), [`src/mechanical/signed_tables/`](src/mechanical/signed_tables/) and [`src/mechanical/canon_v3/lexicon.py`](src/mechanical/canon_v3/lexicon.py);
- the flags as sealed are in [`manifest/v45_manifest.md`](manifest/v45_manifest.md).

## 2. Recompute the Part II paired statistics

**What it does.** Reads the per-item CSV files in `results/phase2/per_item/` and recomputes, for
every arm comparison in the Part II report, the exact McNemar test on the discordant items and a
bootstrap 95% interval of the difference. It writes `stats_paired.csv` next to them.

**Install.** Nothing beyond Python; the script uses the standard library only.

```bash
python results/phase2/per_item/stats_paired.py
```

```text
S1            3B v1.3 vs bare                      n=117  46.2 ->  51.3 ( +5.1)  up/down 12/6   p=0.2379  CI [-1.7, +12.0]
S1            7B v1.3 vs bare                      n=117  47.0 ->  46.2 ( -0.9)  up/down 10/11  p=1.0000  CI [-8.5, +6.8]
S2            3B v1.6 vs bare                      n=117  40.2 ->  41.9 ( +1.7)  up/down  4/2   p=0.6875  CI [-2.6, +6.0]
S2            7B v1.6 (retry arm) vs bare          n=117  48.7 ->  47.9 ( -0.9)  up/down  6/7   p=1.0000  CI [-6.8, +5.1]
S2            3B v1.7 vs bare                      n=117  40.2 ->  47.0 ( +6.8)  up/down 11/3   p=0.0574  CI [+0.9, +12.8]
S2            3B oracle vs bare                    n=117  40.2 ->  51.3 (+11.1)  up/down 15/2   p=0.0023  CI [+4.3, +17.9]
S3            3B v1.8 vs bare                      n=117  39.3 ->  53.8 (+14.5)  up/down 21/4   p=0.0009  CI [+6.8, +22.2]
S3            3B v1.7 vs bare                      n=117  39.3 ->  48.7 ( +9.4)  up/down 14/3   p=0.0127  CI [+3.4, +16.2]
S3            7B v1.8 vs bare                      n=117  51.3 ->  68.4 (+17.1)  up/down 23/3   p=0.0001  CI [+9.4, +24.8]
Multi-IF zh   3B v1.9 vs bare                      n=454  57.7 ->  55.9 ( -1.8)  up/down  5/13  p=0.0963  CI [-3.5, +0.0]
Multi-IF zh   7B v1.9 vs bare                      n=454  65.0 ->  63.7 ( -1.3)  up/down  5/11  p=0.2101  CI [-3.1, +0.4]
ComplexBench  3B v1.11 vs bare, prompt level       n=209  52.2 ->  57.9 ( +5.7)  up/down 26/14  p=0.0807  CI [+0.0, +12.0]
ComplexBench  7B v1.11 vs bare, prompt level       n=209  58.9 ->  66.0 ( +7.2)  up/down 22/7   p=0.0081  CI [+2.4, +12.4]
ComplexBench  3B v1.11 vs bare, mappable subset    n=188  56.4 ->  63.8 ( +7.4)  up/down 28/14  p=0.0436  CI [+0.5, +14.4]
ComplexBench  7B v1.11 vs bare, mappable subset    n=188  60.6 ->  70.7 (+10.1)  up/down 26/7   p=0.0013  CI [+4.3, +16.0]
ComplexBench  3B v1.11 vs bare, rule level         n=252  57.1 ->  60.3 ( +3.2)  up/down 30/22  p=0.3317  CI [-2.4, +8.7]
ComplexBench  7B v1.11 vs bare, rule level         n=252  63.9 ->  69.0 ( +5.2)  up/down 27/14  p=0.0596  CI [+0.4, +10.3]
```

The rewritten `stats_paired.csv` was byte-identical to the committed one. (On Windows with
`core.autocrlf=true`, `git status` still shows it as modified, because of line endings only.)

**Against the README.**

| README figure | Line above |
| --- | --- |
| S3 all-constraints-kept 3B 39.3 → 53.8%, 7B 51.3 → 68.4% | `S3 3B v1.8`, `S3 7B v1.8` |
| ComplexBench rule passes 3B 57.1 → 60.3%, 7B 63.9 → 69.0% | `rule level` |
| Multi-IF zh −1.8 / −1.3 points | `Multi-IF zh` |

The script's header records two known differences from the Part II report:

- The report's intervals used a seed that was not recorded, so their ends differ by up to 0.8 points.
- Two deltas differ by 0.1, because the report subtracted rounded percentages.

## 3. Score your own answers with our scripts

**What it does.** It scores a model's answers on two public benchmarks with the official checkers,
called the same way as in Part II:

- the ComplexBench rule-only subset: 252 rules over 209 prompts;
- the Multi-IF Chinese turn-1 items: 454 prompts.

**Answer file format.** Use one JSON Lines file per system, one line per prompt:

```json
{"key": "CB0001", "answer": "..."}
```

- **ComplexBench keys** are `CB` plus the zero-padded `main_id` of `data_final.json`. Generate from its `instruction` field.
- **Multi-IF keys** are `MIF001` to `MIF454`, assigned by the extraction script below. Generate from its `prompt` field.
- **Comparing systems.** `--responses NAME=PATH` can be repeated; each NAME becomes one column of the output.

In the examples, the bare Qwen2.5-7B answers from [`data/phase2/`](data/phase2/) stand in for
your answers, so the output can be checked against the published numbers. A one-line conversion
selects that arm and renames `item` to `key`.

### 3a. ComplexBench

**Install.** Nothing beyond Python. `con_rule.py` and the scripts use the standard library only.

**Get the benchmark.** Use [thu-coai/ComplexBench](https://github.com/thu-coai/ComplexBench), pinned to commit
`749f4575d5dc981182ecaebb8c292b2a61213cf3` (MIT):

```bash
mkdir -p bench/complexbench
curl -sL -o bench/complexbench/data_final.json https://raw.githubusercontent.com/thu-coai/ComplexBench/749f4575d5dc981182ecaebb8c292b2a61213cf3/data/data_final.json
curl -sL -o bench/complexbench/con_rule.py https://raw.githubusercontent.com/thu-coai/ComplexBench/749f4575d5dc981182ecaebb8c292b2a61213cf3/evaluation/con_rule.py
sha256sum bench/complexbench/data_final.json bench/complexbench/con_rule.py
```

```text
df28e64563efda2ff4c7436d7b8244975352549055949c2ce1005766047c7b09 *bench/complexbench/data_final.json
eb9b539b3ffeae79c82fea6d7b10aab571af726de3f22fe02b114c30ffa59d50 *bench/complexbench/con_rule.py
```

Both hashes are those of the files used in Part II.

**Build the rule-only subset.**

```bash
python eval/complexbench/extract_rule_subset.py --data bench/complexbench/data_final.json --out bench/complexbench/pure_rules.jsonl
```

```text
rules: 252, instructions: 209
kinds: {'length': 77, 'keyword': 51, 'Json': 42, 'forbidden_word': 28, 'startswith': 24, 'endswith': 19, 'length_word': 7, 'constraint_punc': 3, 'modek_keyword': 1}
```

**Example answers, then score.**

```bash
python -c "import json; src='data/phase2/public_benchmarks/complexbench_rule_answers_7b.jsonl'; out=open('my_cb_answers.jsonl','w',encoding='utf-8'); [out.write(json.dumps({'key': r['item'], 'answer': r['answer']}, ensure_ascii=False) + '\n') for r in map(json.loads, open(src, encoding='utf-8')) if r['arm'] == 'A0']"
python eval/complexbench/score_complexbench.py --con-rule bench/complexbench/con_rule.py --rules bench/complexbench/pure_rules.jsonl --responses mine=my_cb_answers.jsonl --out cb_scores.json
```

```text
questions: 209; con_rule sha256: eb9b539b3ffeae79c82fea6d7b10aab571af726de3f22fe02b114c30ffa59d50
| column | mine rules | mine questions |
| --- | ---: | ---: |
| all rules | 161/252 (63.9%) | 123/209 (58.9%) |
| mappable subset | 133/208 (63.9%) | 114/188 (60.6%) |
| all rules, minus LLM-dependent | 137/216 (63.4%) | 101/175 (57.7%) |
| mappable, minus LLM-dependent | 110/176 (62.5%) | 93/158 (58.9%) |
```

The bare 7B arm's published values are 63.9% of rules, 58.9% of prompts and 60.6% of the mappable
subset. All 252 per-rule verdicts are the same as `results/phase2/per_item/complexbench_rule_items.csv`.

**Output fields.**

- Each row of `cb_scores.json` holds `key`, `rules` and `arms`.
  - `rules[]` holds `point_id`, `rule`, `kind`, `dep`, `dep_on_llm` and `mappable`.
  - `arms.NAME` holds:
    - `pass[]`: one per rule; `null` means `con_rule.py` could not judge it, and it counts as not passed;
    - `all_pass`;
    - `mappable_all_pass`.
- Printed table:
  - "mappable" means rules of a type this project reads;
  - "minus LLM-dependent" drops rules whose dependency is an LLM-judged point.

**One difference from the official pipeline.** The official pipeline first asks GPT-4 to extract the
evaluated span. Here the whole answer is judged, and each rule is judged independently of its
dependencies. The file header of `score_complexbench.py` gives the details.

### 3b. Multi-IF (Chinese, turn 1)

**Install.** The official `metrics.py` needs the packages in [`requirements.txt`](requirements.txt), at the
versions Part II used, plus two NLTK data packages:

```bash
python -m pip install -q -r requirements.txt
python -m nltk.downloader -q punkt punkt_tab
```

**Get the benchmark and the official checker.** Use the
[facebook/Multi-IF](https://huggingface.co/datasets/facebook/Multi-IF) data at revision
`0ab97ce0b45c7f57772e8ba2ac1616f4b00bd3aa` (CC BY-NC 2.0), and `ifeval.py` and `metrics.py` from
[facebookresearch/Multi-IF](https://github.com/facebookresearch/Multi-IF) at commit
`1cdb53ed18499ad729e0766e5d3099dd5344406f` (Apache-2.0):

```bash
mkdir -p bench/multi_if
curl -sL -o bench/multi_if/multiIF_20241018.csv https://huggingface.co/datasets/facebook/Multi-IF/resolve/0ab97ce0b45c7f57772e8ba2ac1616f4b00bd3aa/multiIF_20241018.csv
curl -sL -o bench/multi_if/ifeval.py https://raw.githubusercontent.com/facebookresearch/Multi-IF/1cdb53ed18499ad729e0766e5d3099dd5344406f/ifeval.py
curl -sL -o bench/multi_if/metrics.py https://raw.githubusercontent.com/facebookresearch/Multi-IF/1cdb53ed18499ad729e0766e5d3099dd5344406f/metrics.py
sha256sum bench/multi_if/multiIF_20241018.csv bench/multi_if/ifeval.py bench/multi_if/metrics.py
```

```text
6c588af031fe67b17c535b9ba0ccc14a1b9d77b4faf88c294f83aaa5a3000018 *bench/multi_if/multiIF_20241018.csv
61a56d4510a0b8cbacc511d50d4707d20ff72e521d02e29a2898dec69a5507b2 *bench/multi_if/ifeval.py
3aa15edc8e5f6d2f92abe0ec7ae12e9568ed6aadd1f82efc7805808fef76dc2b *bench/multi_if/metrics.py
```

**Extract the 454 Chinese turn-1 items.**

```bash
python data/phase2/public_benchmarks/extract_multiif_zh_turn1.py --csv bench/multi_if/multiIF_20241018.csv --out bench/multi_if/zh_turn1.jsonl
```

```text
454 prompts written; output sha256 946f8fcbbbe42f67791c57604f76bab8e5a878bf0062c0b4e47637c27cf62330 (matches Phase II)
```

**Example answers, then score.**

```bash
python -c "import json; src='data/phase2/public_benchmarks/multiif_zh_answers_7b.jsonl'; out=open('my_mif_answers.jsonl','w',encoding='utf-8'); [out.write(json.dumps({'key': r['item'], 'answer': r['answer']}, ensure_ascii=False) + '\n') for r in map(json.loads, open(src, encoding='utf-8')) if r['arm'] == 'A0']"
python eval/multi_if/score_multi_if.py --vendor-dir bench/multi_if --questions bench/multi_if/zh_turn1.jsonl --responses mine=my_mif_answers.jsonl --out mif_scores.json
```

```text
mine: questions all-pass strict 292/454 (64.3%); instructions strict 432/610 (70.8%)
```

**Why this is 292 and not the published 295 (65.0%).** Some published Multi-IF answers repeat the
prompt, because the instruction asks them to. Those spans are replaced by
`[benchmark prompt text redacted, N chars]`, since the prompts are not ours to redistribute; see
[`data/phase2/README.md`](data/phase2/README.md). The published verdicts were computed on the
original text.

**Size of the effect.** We rescored all four arms of both benchmarks:

- **Multi-IF:** 24 of the 1,816 item × arm answers changed verdict, and every one contains a placeholder.
- **ComplexBench:** 1 of the 836 changed, and it also contains a placeholder.
- **Everything else** matched the per-item files exactly.

Your own answers carry no placeholders, so this does not apply to them.

**Output fields.**

- Each row of `mif_scores.json` holds `key`, `instruction_id_list`, `our_types` and `arms`.
  - `our_types` is this project's type for each instruction; `null` means it is outside our 11 types.
  - `arms.NAME` holds `strict[]`, `loose[]`, `all_strict`, `all_loose` and `mappable_all_strict`.
- The headline metric in `results/phase2/` is `all_strict` per question.

## What this repository cannot do

- **It cannot rerun the architecture.** The layer that changes the model's answers is not here: reading the constraints, the
  rule check, the retry and the generation-time intervention. So you cannot rerun the architecture arms of
  S1–S3, Multi-IF or ComplexBench, or apply the architecture to your own model. What you can do is
  **score** answers (section 3) and **audit** every published Part II number except M1–M3
  (section 2, plus the answers in `data/phase2/`).
- **It cannot run the synthetic-paper checkers.** `eval/synthetic/grade_s1.py`–`grade_s3.py` read the
  reviewer's gold files, which are not public. They are published so that the checking logic can be read.
- **It cannot run `eval/complexbench/obs_coverage.py`.** It needs the architecture's reading records.
- **It cannot reproduce the recognizer's seven blind rounds.** The sentence files come from WildChat and are not
  redistributed. Section 1 runs the same recognizer on your own sentences.
