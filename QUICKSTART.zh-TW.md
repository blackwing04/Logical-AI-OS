[English](QUICKSTART.md) | 繁體中文

# 快速上手

本倉能跑什麼：每件事一行指令，附上它印出來的結果。

下列每一行指令都在 2026-10-31 實跑過：全新虛擬環境、全新 clone 的 tag `v2.0.1-repro`
（Windows 11，Git Bash）。實跑兩次，Python 3.13.0 與 3.13.9 各一次，兩次輸出相同。輸出照印出的原樣貼上。

```bash
git clone https://github.com/blackwing04/Logical-AI-OS.git
cd Logical-AI-OS
python -m venv .venv
source .venv/bin/activate        # Windows：.venv\Scripts\activate（cmd／PowerShell），source .venv/Scripts/activate（Git Bash）
```

所有指令都在倉的根目錄下執行。macOS 上把 `sha256sum` 換成 `shasum -a 256`。

## 一、辨識零件跑你自己的句子

**它做什麼。**跑 v4.5 判定鏈（機械層，零模型呼叫）。它把一段中文請求切成句與子句，每一句在兩軸上貼標：

- **軸一**，是不是請求：`主請求`、`空框請求`、`隱性需求`、`非請求`；
- **軸二**，對答案而言它是什麼：`限制`（答案的限制）、`材料`（待處理的材料）、`無`（這句本身就是請求）。

另外印出：

- 每個子句的**框架**，它決定表五（限制線索表）進不進場；
- 開火的**表五線索**，各附來源表。

**安裝。**只要 Python；辨識零件只用標準庫。

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

**關於這個範例。**

- 範例請求是為本文寫的，不來自任何語料。
- 一句有多個子句時，每個子句列一個框架。
- `不要超過五點` 沒有開火：「N 點」不在表五裡。這是辨識零件的真實行為，照原樣呈現。

**更多細節。**`--file request.txt` 從檔案讀請求。`--json` 每句印一行完整紀錄：兩軸各是哪一條規則開火、逐子句的訊號、該句在整篇請求裡的地位。

**讓它跑得起來的東西。**兩個小模組把公開的鏈補齊：

- [`src/mechanical/canon_v3/`](src/mechanical/canon_v3/)：表五線索偵測器與它的表；
- [`src/mechanical/classifier.py`](src/mechanical/classifier.py)：權重與路由對照。

兩者都是內部檔的公開副本或節錄，處理紀錄見 [`PUBLIC_NOTES.zh-TW.md`](PUBLIC_NOTES.zh-TW.md) 第七節。

**結果怎麼核過。**拿公開的 S1–S3 題目所有文字欄（4,482 句）比對，這條鏈的輸出與內部版逐位元組相同。

**規則在哪裡讀。**

- 規則順序在 [`src/mechanical/rules_v2.py`](src/mechanical/rules_v2.py)；
- 軸一規則在 [`src/mechanical/pipeline_v2.py`](src/mechanical/pipeline_v2.py)，軸二框架在 [`src/mechanical/reorder_v2.py`](src/mechanical/reorder_v2.py)；
- 簽核詞表在 [`src/mechanical/lexicon_v2.py`](src/mechanical/lexicon_v2.py)、[`src/mechanical/signed_tables/`](src/mechanical/signed_tables/) 與 [`src/mechanical/canon_v3/lexicon.py`](src/mechanical/canon_v3/lexicon.py)；
- 封筆時的旗標見 [`manifest/v45_manifest.md`](manifest/v45_manifest.md)。

## 二、重算第二部分的配對統計

**它做什麼。**讀 `results/phase2/per_item/` 的逐題 CSV，為 Part II 報告裡每一組臂對比重算
不一致題的 McNemar 精確檢定與差值的 bootstrap 95% 區間，並在同目錄寫出 `stats_paired.csv`。

**安裝。**只要 Python；腳本只用標準庫。

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

重寫出的 `stats_paired.csv` 與倉內版逐位元組相同。（Windows 上 `core.autocrlf=true` 時，
`git status` 仍會把它標成已修改，原因只是換行符。）

**對 README。**

| README 數字 | 對應上方哪一行 |
| --- | --- |
| S3 全部限制皆守率 3B 39.3 → 53.8%、7B 51.3 → 68.4% | `S3 3B v1.8`、`S3 7B v1.8` |
| ComplexBench 條過 3B 57.1 → 60.3%、7B 63.9 → 69.0% | `rule level` |
| Multi-IF 中文 −1.8／−1.3 點 | `Multi-IF zh` |

腳本檔頭記了與 Part II 報告的兩處已知差異：

- 報告的區間用了一個沒記下的 seed，所以區間端點最多差 0.8 點。
- 有兩格差值差 0.1，因為報告是拿四捨五入後的百分比相減。

## 三、用我們的腳本評你自己的回答

**它做什麼。**用官方檢查器、照 Part II 的同一種呼叫方式，為一個模型在兩個公開題庫上的回答評分：

- ComplexBench 純規則子集：209 題、252 條規則；
- Multi-IF 中文第一輪：454 題。

**回答檔格式。**一個系統一個 JSON Lines 檔，每題一行：

```json
{"key": "CB0001", "answer": "..."}
```

- **ComplexBench 的 key** 是 `CB` 加上 `data_final.json` 的 `main_id` 補零到四位；用它的 `instruction` 欄生成回答。
- **Multi-IF 的 key** 是 `MIF001` 到 `MIF454`，由下方的抽取腳本編號；用它的 `prompt` 欄生成回答。
- **比較多個系統。**`--responses 名稱=路徑` 可重複給，每個名稱成為輸出的一欄。

範例裡，用 [`data/phase2/`](data/phase2/) 的裸 Qwen2.5-7B 回答代替「你的回答」，
這樣輸出可以拿來對已公開的數字。一行轉換挑出該臂，並把 `item` 改名為 `key`。

### 三之一、ComplexBench

**安裝。**只要 Python；`con_rule.py` 與腳本都只用標準庫。

**取得題庫。**用 [thu-coai/ComplexBench](https://github.com/thu-coai/ComplexBench)，釘在 commit
`749f4575d5dc981182ecaebb8c292b2a61213cf3`（MIT）：

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

兩個雜湊都與 Part II 所用的檔相同。

**建純規則子集。**

```bash
python eval/complexbench/extract_rule_subset.py --data bench/complexbench/data_final.json --out bench/complexbench/pure_rules.jsonl
```

```text
rules: 252, instructions: 209
kinds: {'length': 77, 'keyword': 51, 'Json': 42, 'forbidden_word': 28, 'startswith': 24, 'endswith': 19, 'length_word': 7, 'constraint_punc': 3, 'modek_keyword': 1}
```

**準備範例回答，然後評分。**

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

裸 7B 臂的公開值：條過 63.9%、題過 58.9%、可映射子集 60.6%。252 條逐條判定與
`results/phase2/per_item/complexbench_rule_items.csv` 全部相同。

**輸出欄位。**

- `cb_scores.json` 每一列有 `key`、`rules`、`arms`。
  - `rules[]` 有 `point_id`、`rule`、`kind`、`dep`、`dep_on_llm`、`mappable`。
  - `arms.名稱` 有：
    - `pass[]`：每條一個；`null` 表示 `con_rule.py` 判不了，計為未過；
    - `all_pass`；
    - `mappable_all_pass`。
- 印出的表：
  - 「mappable」是本專案讀得到的型別的規則；
  - 「minus LLM-dependent」去掉依賴點須由 LLM 判的規則。

**與官方流程的一處差異。**官方流程先請 GPT-4 抽出受評片段；這裡整篇回答都是受評對象，
且每條規則獨立判、不看它的依賴點。細節見 `score_complexbench.py` 檔頭。

### 三之二、Multi-IF（中文，第一輪）

**安裝。**官方 `metrics.py` 需要 [`requirements.txt`](requirements.txt) 裡的套件（Part II 所用版本），
外加兩個 NLTK 資料包：

```bash
python -m pip install -q -r requirements.txt
python -m nltk.downloader -q punkt punkt_tab
```

**取得題庫與官方檢查器。**資料用 [facebook/Multi-IF](https://huggingface.co/datasets/facebook/Multi-IF)
的 revision `0ab97ce0b45c7f57772e8ba2ac1616f4b00bd3aa`（CC BY-NC 2.0）；`ifeval.py` 與 `metrics.py` 用
[facebookresearch/Multi-IF](https://github.com/facebookresearch/Multi-IF) 的 commit
`1cdb53ed18499ad729e0766e5d3099dd5344406f`（Apache-2.0）：

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

**抽出 454 題中文第一輪。**

```bash
python data/phase2/public_benchmarks/extract_multiif_zh_turn1.py --csv bench/multi_if/multiIF_20241018.csv --out bench/multi_if/zh_turn1.jsonl
```

```text
454 prompts written; output sha256 946f8fcbbbe42f67791c57604f76bab8e5a878bf0062c0b4e47637c27cf62330 (matches Phase II)
```

**準備範例回答，然後評分。**

```bash
python -c "import json; src='data/phase2/public_benchmarks/multiif_zh_answers_7b.jsonl'; out=open('my_mif_answers.jsonl','w',encoding='utf-8'); [out.write(json.dumps({'key': r['item'], 'answer': r['answer']}, ensure_ascii=False) + '\n') for r in map(json.loads, open(src, encoding='utf-8')) if r['arm'] == 'A0']"
python eval/multi_if/score_multi_if.py --vendor-dir bench/multi_if --questions bench/multi_if/zh_turn1.jsonl --responses mine=my_mif_answers.jsonl --out mif_scores.json
```

```text
mine: questions all-pass strict 292/454 (64.3%); instructions strict 432/610 (70.8%)
```

**為什麼是 292，不是公開的 295（65.0%）。**有些公開的 Multi-IF 回答照指令要求重述了題目。
題目不是我們能轉散布的，所以那些片段換成了 `[benchmark prompt text redacted, N chars]`，
見 [`data/phase2/README.md`](data/phase2/README.md)。公開的判定是在原文上算的。

**影響有多大。**我們把兩個題庫的四臂全部重評：

- **Multi-IF：**1,816 份題 × 臂回答中有 24 份判定改變，每一份都含佔位符。
- **ComplexBench：**836 份中有 1 份改變，同樣含佔位符。
- **其餘**與逐題檔完全相同。

你自己的回答沒有佔位符，不受此影響。

**輸出欄位。**

- `mif_scores.json` 每一列有 `key`、`instruction_id_list`、`our_types`、`arms`。
  - `our_types` 是每條指令在本專案的型別；`null` 表示不在我們的 11 型內。
  - `arms.名稱` 有 `strict[]`、`loose[]`、`all_strict`、`all_loose`、`mappable_all_strict`。
- `results/phase2/` 的主指標是每題的 `all_strict`。

## 這個倉**不能**做什麼

- **不能重跑架構。**會改變模型回答的那一層不在本倉：讀出限制、規則核對、退回、生成時介入。
  所以不能重跑 S1–S3、Multi-IF、ComplexBench 的架構臂，也不能把架構套到你自己的模型上。
  能做的是**評分**（第三節）與**審核**除 M1–M3 外每一個 Part II 公開數字（第二節，加上 `data/phase2/` 的答案）。
- **不能跑合成卷核對器。**`eval/synthetic/grade_s1.py`–`grade_s3.py` 讀的是聊天端的 gold 檔，那些不公開；
  公開它們是為了讓核對邏輯可讀。
- **不能跑 `eval/complexbench/obs_coverage.py`。**它需要架構的讀題紀錄。
- **不能復現辨識零件的七卷盲考。**句子檔來自 WildChat，不轉散布。第一節可以拿同一個辨識零件跑你自己的句子。
