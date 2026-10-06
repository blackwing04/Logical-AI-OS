# v4.5 封筆 manifest（**自 import 鏈反查**）

配置＝v4.4 ＋ **F2 描述框掛同一張寫作規格形豁免表** ＋ **刀1-C 改按族比**。
「無第一人稱」這個代理住在 F1 與 F2 兩處，v4.4 只補了 F1；本代補齊第二處。

取法同 v4.4：`ast` 從三個入口遞迴解析 import 至收斂——**走出來的，不是回想的**。
對照基準是 v4.4 的 31 組件清單，所以「改」欄答的是**本代動了哪幾個檔**。

| # | 檔 | 來源 | sha256（前16） | 位元 | 對 v4.4 |
| --- | --- | --- | --- | --- | --- |
| 1 | `experiments/blindtest/scripts/run_7b_arm.py` | import 鏈 | `cb2ed42dee7e6d2f` | 6755 | 同 |
| 2 | `experiments/composite-classifier/src/classifier.py` | import 鏈 | `7ed901dcd3e278c6` | 15150 | 同 |
| 3 | `experiments/composite-classifier/src/wording.py` | import 鏈 | `43a93a7f6b3775e1` | 8276 | 同 |
| 4 | `experiments/control-station/judge_v4.py` | import 鏈 | `8845e46d5aaaa97f` | 32337 | 同 |
| 5 | `experiments/control-station/request_form.py` | import 鏈 | `15f0eec929ad946f` | 10427 | 同 |
| 6 | `experiments/mechanical-v2/clause_v2.py` | import 鏈 | `1524a992a869b98f` | 29170 | **改** |
| 7 | `experiments/mechanical-v2/detectors.py` | import 鏈 | `69a6cedefaeaf5f8` | 28991 | 同 |
| 8 | `experiments/mechanical-v2/lexicon_v2.py` | import 鏈 | `99b6e68b297358c8` | 34860 | 同 |
| 9 | `experiments/mechanical-v2/pipeline_v2.py` | import 鏈 | `d8723b37c3ac4017` | 8464 | 同 |
| 10 | `experiments/mechanical-v2/reorder_v2.py` | import 鏈 | `c8aeb6795009d9a8` | 10554 | **改** |
| 11 | `experiments/mechanical-v2/rules_v2.py` | import 鏈 | `f979a3095f9b8d82` | 11462 | 同 |
| 12 | `experiments/perf-station/early_stop.py` | import 鏈 | `3e60d5a62f3ff9fc` | 3451 | 同 |
| 13 | `experiments/perf-station/run_perf.py` | import 鏈 | `83b01addf50c804c` | 28862 | 同 |
| 14 | `experiments/perf-station/schema_v1.py` | import 鏈 | `712ffc481bd0800d` | 5402 | 同 |
| 15 | `experiments/semantic-station/scripts/probe_causal.py` | import 鏈 | `3b19b026fc75649b` | 6282 | 同 |
| 16 | `experiments/semantic-station/scripts/probe_noise.py` | import 鏈 | `e82e21bebdc24271` | 4651 | 同 |
| 17 | `experiments/semantic-station/scripts/run_fold.py` | import 鏈 | `b8bb750d03ad0dbd` | 5796 | 同 |
| 18 | `experiments/semantic-station/scripts/run_station.py` | import 鏈 | `b6ca26fa3d273199` | 5641 | 同 |
| 19 | `experiments/semantic-station/scripts/run_station2.py` | import 鏈 | `0167072dc7579e62` | 7692 | 同 |
| 20 | `laios-bridge/reports/attachments/2026-09-24_框架消費b路/adjudicator_v3b.py` | import 鏈 | `3777470fb3c277ba` | 1275 | 同 |
| 21 | `scripts/canon_v3/modeling.py` | import 鏈 | `e75067d2aa5452c5` | 1677 | 同 |
| 22 | `scripts/canon_v3/prompts.py` | import 鏈 | `bc2558da42f91235` | 5582 | 同 |
| 23 | `src/generation/stop_tokens.py` | import 鏈 | `b7d3161dd301de92` | 374 | 同 |
| 24 | `src/model/base.py` | import 鏈 | `d36527ca9a4b03bb` | 722 | 同 |
| 25 | `src/model/chat_template.py` | import 鏈 | `df33089c77b59764` | 731 | 同 |
| 26 | `src/model/hf_backend.py` | import 鏈 | `047291b12beecfde` | 2416 | 同 |
| 27 | `src/model/loader.py` | import 鏈 | `212f07a9b94cda97` | 2673 | 同 |
| 28 | `experiments/mechanical-v2/signed_tables/knife2_one_classifier.json` | 路徑讀取 | `bb4a4ccadf6355ef` | 2413 | 同 |
| 29 | `experiments/mechanical-v2/signed_tables/function_layer.json` | 路徑讀取 | `ec1df128cce3e2c0` | 1877 | 同 |
| 30 | `experiments/mechanical-v2/signed_tables/lexicon_registry.json` | 路徑讀取 | `c207c1208d9e1670` | 1892 | 同 |
| 31 | `tools/split_sentences.py` | 路徑讀取 | `890a73048d47a3c7` | 16650 | **改** |

| 項 | 值 |
| --- | --- |
| **組件數** | **31**（import 鏈 27 ＋ 路徑讀取 4） |
| 與 v4.4 相同 | **28** |
| 本代有變 | **3** |
| v4.4 未列（本代新進 import 鏈） | **0** |

v4.4 走出 31 個；本代 **31** 個。兩代同一套走法，所以差額是真的組件變動，
不再是「手列漏了多少」那種雜訊。

### 旗標狀態（判定行為的一部分，必須入 manifest）

| 旗標 | 值 |
| --- | --- |
| `F1_DOC_STATUS` | **True** |
| `F1_WRITING_SPEC_EXEMPT（本代新增）` | **True** |
| `F1_WS_SCOPE` | **sentence** |
| `F2_WS_EXEMPT（本代新增）` | **True** |
| `F2_DESCRIPTIVE_NON_FIRST` | **True** |
| `F2_SCOPE` | **sentence** |
| `F3_IMPERATIVE_YOU` | **True** |
| `F4_FUNCTION_LAYER` | **True** |
| `F4_COMBINE` | **and** |
| `KNIFE1C_PASTE_SCOPE` | **True** |
| `KNIFE1C_AS_FALLBACK` | **True** |
| `KNIFE2_ONE_CLASSIFIER` | **True** |
| `KNIFE1_AGG_FIX（棄決）` | **False** |
| `CASE1_POSSESSIVE_EXCEPTION` | **True** |
| `CASE2_DEGREE_GUARD` | **True** |
| `TIME_INHERIT` | **False** |
| `PERSON_INHERIT` | **False** |

完整 64 位雜湊：`experiments/control-station/v45_manifest.json`
