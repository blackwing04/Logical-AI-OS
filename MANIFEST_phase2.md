# public_staging 第二階段收裝清單（MANIFEST_phase2）

令：`orders/2026-10-29_公開倉第二階段收裝令.md`（PI 裁 2026-10-29）。**三段制，本輪仍屬第一段（第二次交 staging，回聊天端覆核 `845b64c`，見 §〇）**：CC 建 staging 並 push bridge。公開倉本輪不碰；等聊天端覆核、PI 放行之後另令推送。

| 項 | 值 |
| --- | --- |
| 檔數 | **24**：新寫 18、改寫 5、本檔 1 |
| 疊層基底 | 公開倉 `main@b288d39`（2026-10-29 現場 clone） |
| 界線 | 量測層公開；控制層不公開，依 `orders/2026-10-08_Zenodo_v1.2追加令_公開邊界.md` 與其 2026-10-29 補記 |
| 檔名 | 全 ASCII |
| 自查 | A 語料反查**全查**／B／C／D／D2 控制層反查／W 動作層詞表，見 §四 |

雜湊為 **LF 正規化後 sha256 的前 16 碼**；grade_s* 另附原始位元組的完整 sha256，用來證明與來源逐位元組相同。


## 〇、第二段收裝（回聊天端覆核 `845b64c`）

PI 2026-10-29 裁：公開物只保留「生成後退回一次」「生成時介入」兩個名詞，**不描述任何動作怎麼做**，不列不公開清單的項目。本段照覆核逐檔收：

| 檔 | 收了什麼 |
| --- | --- |
| `README.md`／`.zh-TW.md` | 架構句改為「生成後最多退回一次；自 v1.8 起加入生成時介入」。兩處不公開清單收成一句「所有動作層實作、規則表與門檻」。補記改寫為「只出現兩個動作名稱、不描述怎麼做」。加 gold 標註者一句（照覆核原文）。協定連結改 `docs/protocol/phase2/`。授權表刪 `protocol/`（已併入 `docs/`） |
| `results/phase2/README.md` | 架構第 3–5 點改為「生成後最多退回一次／生成時介入（長度）／條件式條數動作」。不公開句收成一句。JSON 兩條死因改寫成只講結果。M 卷 gold 列加「PI 抽查」 |
| `results/phase2/headline.csv`、`summary.md` | 兩個臂描述的「無生成時控長」改為「無生成時介入」（產生器改字後重產，數字不變） |
| `docs/protocol/phase2/…` | **自頂層 `protocol/phase2/` 搬入**（覆核二.1）；相對連結同步。不公開句收成一句；神諭段改用「生成時介入」；「擬發退回訊息」改「擬發退回」；§8 加「PI 抽查」 |
| `docs/PORTING.md`／`.zh-TW.md` | §6b 改題「生成後退回一次」、§6c 改題「生成時介入」，兩節只留「須自建；做法不公開」與驗收方式。§6c 驗收照覆核原文：S3 型卷上長度／條數落入率與對照臂比較。第一階段 §2c 英文版有一處字面為詞表歸零而換字，語意不變；中文版不需改 |
| `docs/failure_taxonomy.md` | 涉及兩個動作的死因只講結果，不講機制。角色那兩格改用 "role statement" |
| `docs/parts_spec_v2.md` | 長度那列改名「生成時介入（長度）」，條數兩列改名「條數動作」，掛載條件改寫為「條件不公開」；版本表同步改寫 |
| `docs/literature_mapping.md` | §9.3 標題改為「長度控制與受限生成」。兩行舊私有引用已清（覆核二.6）：令文路徑、bib 路徑。待核清單第 1 列 McCoy 改為已結項，與 §四 正文一致 |
| `eval/README.md` | 合成卷核對器的描述改用「numbered or bulleted items／lines」 |
| `eval/complexbench/extract_rule_subset.py`、`obs_coverage.py` | 為詞表歸零，標準庫的計數類別改用 dict 計數；行為不變（重跑：ComplexBench 0／836、obs 145／252 與兩張對照表逐數相同） |

**詞表反查（W 關）**：照覆核 §一 的詞表，比對**內容與檔名**，不分大小寫子字串。

- 本輪 staging 24 檔（含本檔）：**0**。
- 未動的已公開舊檔仍有命中，都是第一階段量測層的一般用法，其中有簽核物件與已發佈於 Zenodo 的報告。逐條清單與語境放在 bridge 交件報告（不入公開倉，免得本檔自己帶出詞表字），請裁。

commit 訊息：bridge 的 commit 不進公開倉。第三段推公開倉時另寫新訊息，屆時同樣過詞表。

---

## 一、逐檔清單

處理欄的值：`新寫`（公開版新寫，不是內部某檔的複製）、`改寫`（以公開倉現檔為底增修）、`衍生`（自內部檔抽出公開部分，路徑參數化）、`原樣`。

### 1a 令文第 1 項：`results/phase2/`（去語料彙總表）

| 檔 | 處理 | sha16 | 來源 | 界線判定 |
| --- | --- | --- | --- | --- |
| `results/phase2/README.md` | 新寫 | `013cf4b8e62675bb` | 各卷開獎報告與交件（下列） | 只寫指標定義、狀態標籤、口徑限定與負結果；不含題目、答案或逐篇紀錄 |
| `results/phase2/summary.md` | 新寫（由 CSV 產生） | `1cd8d351d8157d9d` | 同下四個 CSV | 同上 |
| `results/phase2/headline.csv` | 新寫 | `aacdc492fb7d3885` | 見表下 | 只含各臂分數 |
| `results/phase2/deltas.csv` | 新寫 | `efc7ee6e24ff3690` | 見表下 | 只含改善／變差與逐條修好／弄壞的計數 |
| `results/phase2/per_type.csv` | 新寫 | `0c62ba373849bb36` | 見表下 | 只含逐型通過計數；Multi-IF 的列以官方 instruction id 命名（題庫結構名，不是題目文字） |
| `results/phase2/triggers_coverage.csv` | 新寫 | `ace51d821c1c68ca` | 見表下 | 只含觸發率與讀題命中計數 |

**數字來源**：

| 卷 | 來源 |
| --- | --- |
| M1 | `reports/2026-10-11_M站第一卷開獎報告.md`；附件 `gold_m1.jsonl` 重數 97／111／115 |
| M2 | `2026-10-17_三臂v1.1開獎報告.md`、`2026-10-17_三臂v1.2開獎報告.md` |
| M3 | `2026-10-18_M站第三卷開獎報告.md` |
| S1 | `2026-10-19_合成卷S1開獎報告.md` |
| S2 | `2026-10-19_S2開獎報告.md`、`2026-10-19_S2_v1.7與神諭開獎紀錄.md`（CC 已重算一致）、`attachments/2026-10-19_S2gold/s2_grade.json`（sha16 `d51b5c1b001a996b`）、`2026-10-19_合成卷S2五臂交件.md` |
| S3 | `2026-10-22_S3開獎報告.md`、`2026-10-22_合成卷S3五臂交件.md` |
| Multi-IF | develop `experiments/m-station/outputs/mif_scores.json`（sha16 `7958044e7d820bcb`） |
| ComplexBench | develop `outputs/cb_scores.json`（sha16 `c6f1b1cf31494eaa`） |
| 讀題命中 | `2026-10-25_讀題變體回歸集交件.md`、`2026-10-29_v1.11收尾與ComplexBench盲打交件.md`、`2026-10-25_最後一發三門檻.md`、`attachments/2026-10-23_小模型讀題小測/index.jsonl`（R0 列） |

產生器在 scratchpad，不入倉。

**本輪才從 artifact 算出、先前報告沒出現過的數**（請聊天端過目）：

| 數 | 值 | 算自 |
| --- | --- | --- |
| ComplexBench 題層全過翻轉 | 3B 改善 26／變差 14；7B 22／7 | `cb_scores.json` |
| Multi-IF 7B 題層翻轉 | 5／11（草稿只用了 3B 的 5／13） | `mif_scores.json` |
| Multi-IF 指令層修好／弄壞 | 3B 9／17、7B 10／12 | `mif_scores.json` |
| Multi-IF 逐 instruction id 通過 | 全表 | `mif_scores.json` |
| S2 的 A0／A1′ 逐型通過 | 全表 | `s2_grade.json`（A1 為只記臂，已排除） |

M1 的 3B／7B 分子 97／111 以 gold 檔重數，與開獎報告的百分比一致。

### 1b 令文第 2 項：`docs/protocol/phase2/`（覆核二.1 自頂層搬入）

| 檔 | 處理 | sha16 | 來源 | 界線判定 |
| --- | --- | --- | --- | --- |
| `docs/protocol/phase2/evaluation_protocol_phase2.md` | 新寫（英文） | `51e4c5dec6518450` | `orders/2026-10-18_合成卷制度v2令.md`、`2026-10-19_S2卷令.md`、`2026-10-19_v1.7最小修令.md`、`2026-10-22_L1小修與S3正式卷令.md`、`2026-10-25_最後一發三門檻令.md`、`2026-10-29_v1.11型別覆蓋令.md`、`reports/2026-10-22_子彈盤點.md` | 制度條款可公開（同第一階段盲測制度說明的處理）。內容含：門檻沿革**全部**列出（40→70、改驗 Multi-IF、≤41 在候選不過線後改為幻抽率）、偷看一次與影響上限、停工線中途改線、制度沒有解決的四件事。**不含**讀題樣式、模板、門檻值本身。gold 一律不附 |

### 1c 令文第 3 項：`eval/`

| 檔 | 處理 | sha16 | 來源（develop） | 界線判定 |
| --- | --- | --- | --- | --- |
| `eval/README.md` | 新寫 | `69c1d0bb29e3f7df` | — | 說明、上游來源與授權、重現核對結果 |
| `eval/multi_if/score_multi_if.py` | 衍生 | `ee65442980482c48` | `experiments/multi_if/score_multi_if.py`（sha16 `3af8d586542625d1`） | 呼叫官方檢查器的 glue。路徑改成參數，不 vendor 上游檔（改附固定 commit 與 sha256 讓人自取） |
| `eval/complexbench/extract_rule_subset.py` | 衍生 | `5a51ff639503bb7d` | `experiments/complexbench/build_cb.py`（`a2270822b6884c49`）的子集抽取段 | 只讀官方 `data_final.json` 的規則欄 |
| `eval/complexbench/rule_mapping.py` | 衍生 | `abb93674f0957937` | `experiments/complexbench/read_cb.py`（`f7aeb12bcb86756c`）的 `gold_of`／`match` | **`main()` 未收**：它會呼叫讀題實作（控制層）。收錄的兩個函式只處理官方規則字串與已記錄的讀出，不含讀題樣式 |
| `eval/complexbench/score_complexbench.py` | 衍生 | `eae331e32a57e646` | `experiments/complexbench/score_cb.py`（`567da9e07be2309b`） | 呼叫官方 `con_rule.py` 的 glue，並寫明「評測對象＝整篇回覆」的口徑差 |
| `eval/complexbench/obs_coverage.py` | 衍生 | `66d6cbef3218a42a` | `experiments/complexbench/obs_cb.py`（`5293867ad207e868`）的統計段 | **重建讀題那段未收**（它會呼叫讀題實作，屬控制層）。改為讀已記錄的讀出檔；讀出檔本身不公開 |
| `eval/synthetic/grade_s1.py` | **原樣** | `bdbd9e9377d3682e` | bridge `reports/attachments/2026-10-19_S1gold/grade_s1.py`；原始 sha256 `07dd8448d50d7b6ae63572c4f8fc3e44e35d157cb46ffe5aac6b1d441684a4b2` | 聊天端獨立核對器，令文明列可公開。含聊天端沙箱路徑 `/home/claude/...`（無人名），照原樣不改，以保逐位元組可核 |
| `eval/synthetic/grade_s2.py` | **原樣** | `a4edaad80f034f95` | `2026-10-19_S2gold/grade_s2.py`；原始 sha256 `58a75f814855ba6a48694625fa27e1117fc1b3acc4a28f7db4f0544133303196` | 同上 |
| `eval/synthetic/grade_s3.py` | **原樣** | `5603f0ed9dd24113` | `2026-10-22_S3gold/grade_s3.py`；原始 sha256 `b1e5e9ab00c9150f3c546b2bd66c66cccf78fdc949bfa055a2ec1cd42b50b3ea` | 同上 |

**重現核對**：三支可獨立跑的腳本都在私有回覆上重跑過，與交件評分檔比對：

| 腳本 | 差異 |
| --- | --- |
| Multi-IF | 0／1816 組 |
| ComplexBench | 0／836 組 |
| obs 覆蓋率 | 145／252 與兩張對照表逐數相同 |

### 1d 令文第 4–8 項：`docs/` 與 README

| 檔 | 處理 | sha16（公開倉現檔） | 來源 | 界線判定 |
| --- | --- | --- | --- | --- |
| `docs/parts_spec_v2.md` | 新寫（英文） | `8e0ac58c10644c3b` | bridge `docs/零件規格表.md` @ `013a25d`（sha16 `47b84ea940bed5b1`） | 數值照抄並去私有路徑。**去掉所有動作層實作描述**；動作只以「生成後退回一次」「生成時介入」兩個名稱出現，條數相關列稱「條數動作」。版本表只留一行高階描述 |
| `docs/failure_taxonomy.md` | 新寫（英文） | `6131a2124c4dd30a` | `reports/2026-10-18_失敗解剖報告.md`（sha16 `8f7273e12d55b8e1`）；死因出處見表下 | **去篇號、去引文**（原檔的人名替換例、聲稱含某詞的例、角色自介例一律改寫成抽象描述）。**去偵測門檻與退回措辭**（照抄比、拒答後重做的訊息句等）。只留「有沒有可機械核的形狀」 |
| `docs/literature_mapping.md` | 改寫 | `b17d2031a707e80e`（`3f936121791e5fff`） | 公開倉現檔＋develop `docs/literature_mapping.md` §九（`ba0baf2`，sha16 `d9ee900427167ce7`）＋待核 9–11 | 純增 46 行。§九的兩處私有引用已改寫：令文路徑、內部導入評估報告路徑 |
| `docs/PORTING.md` | 改寫 | `f643802167fb861a`（`bb3a043f4d15ca7a`） | 公開倉現檔＋新 §6 | §6 只寫「須自建的三塊」及各自的驗收方式，不給實作 |
| `docs/PORTING.zh-TW.md` | 改寫 | `db1ac30895679606`（`1b73cfb48ed87adb`） | 同上中文版 | 與英文段落一一對應 |
| `README.md` | 改寫 | `0e1d416398a8637c`（`bcec837395a2cab9`） | 公開倉現檔 | 新增 Part II 摘要一節（DOI 佔位）；目錄表加五列；「不在本倉」補第二階段項目；收裝規矩補 2026-10-29 補記；復現性補一條；授權表加 `eval/`、`protocol/` |
| `README.zh-TW.md` | 改寫 | `e0f2f9dc716a574b`（`e67bed802699ec99`） | 同上中文版 | 同上，段落一一對應 |
| `MANIFEST_phase2.md` | 新寫 | — | — | 本檔 |

失敗型錄 B 部分的死因出處：

- 方向讀反、材料誤觸、訊息漏限制：`orders/2026-10-19_v1.6修與重做一致性小測令.md`、`reports/2026-10-19_S2開獎報告.md`、`2026-10-18_M站第三卷開獎報告.md`。
- 句數讀成條數：`2026-10-23_第一發MultiIF_zh四臂交件.md`。
- 作用域、JSON 提前結束、條數動作改格式、改寫漂移：`2026-10-29_v1.11收尾與ComplexBench盲打交件.md`。

---

## 二、聊天端覆核六件的處置（`845b64c` §二）

| # | 覆核裁定 | 處置 |
| --- | --- | --- |
| 1 | `protocol/phase2/` 併入 `docs/protocol/phase2/` | 已搬；README（中英）、PORTING（中英）、協定內相對連結同步。授權表刪 `protocol/`（`docs/` 已涵蓋，CC BY 4.0） |
| 2 | 授權 `eval/` MIT、protocol CC BY 4.0，同意 | 照寫 |
| 3 | README Part II 照 §一 收，另加 gold 標註者一句 | 已收；英文版照覆核原文加 "Gold in Phase II was labelled by the reviewer session (an LLM), not by a human; the PI spot-checked."，中文版同義。results README 與協定 §8 同步加「PI 抽查」 |
| 4 | 評分腳本採衍生版，同意；MANIFEST 寫明 | 見 §1c（衍生欄與界線判定欄已寫明抽出範圍與未收部分） |
| 5 | 中文列點正則同時在 grade_s* 與控制層，判非外洩，同意 | 不動 |
| 6 | `literature_mapping` 兩行舊私有引用與不一致：順手清 | 已清，見 §〇 |

## 三、請裁：詞表在未動的已公開舊檔的命中

見 §〇末段；逐條清單在 bridge 交件報告。本輪未改這些檔。

---

## 四、自查（push 樹＝公開倉 `b288d39` 工作樹疊上本 staging，共 66 檔）

腳本：develop `experiments/control-station/audit_phase2_staging.py`（零模型呼叫）。原始命中清單逐筆放 bridge `reports/attachments/2026-10-29_公開倉第二階段收裝/audit_stage2.md`（第一次交件的版本為同目錄 `audit_full.md`），不入公開倉。

### A 語料反查（全查，非抽樣）

方法：去空白後取 12 字窗，查是否出現在 push 樹的窗集合。小語料步長 1；兩個原始大庫步長 6，任何 ≥17 字的外洩片段仍必中。

| 語料 | 項 | 字元 |
| --- | ---: | ---: |
| 第一階段七卷（候選、句子檔） | 135,415 | 4,642,324 |
| M1–M3 卷 | 9,808 | 3,768,703 |
| S1–S3 卷（orig／final、manifest、改寫、池） | 5,934 | 512,112 |
| Multi-IF zh＋變體 V1–V5／X1／X5 | 11,535 | 660,585 |
| ComplexBench `data_final` 等 | 23,369 | 5,436,577 |
| 全部模型答案（develop results 檔） | 91,944 | 13,337,931 |
| LMSYS-Chat-1M，language＝Chinese 全部輪次 | 65,414 | 6,494,310 |
| WildChat 來源 parquet 全部輪次 | 733,605 | 235,800,167 |

**判讀**：

- 命中本輪新檔的中文窗共 8 個，全是通用字串：表格分隔線、正則字元集 `[一二三四五六七八九十]`、`transformers模型`。
- 英文與程式碼窗另做連續覆蓋分析。新檔中 ≥30 字元的連續重疊段全部屬於下列類型：
  - 一般英文措辭（WildChat 英文對話裡也有的句段）
  - Python 樣板碼
  - Multi-IF 官方 instruction id
  - 論文標題
  - DOI 與 GitHub 網址
- **沒有任何語料內容外洩。**

### B 人名／第三方帳號

7 筆：6 筆在第一階段已公開的 `MANIFEST.md`，1 筆在本檔 §四；全是聲明文列舉類別時的字面，例如「Reddit 字樣」。其他新檔 **0**。

### C 憑證

**0**。

### D 公開邊界（第一階段舊樣式＋第二階段新樣式：動作層、讀題實作與 ASK 決策值的內部名稱）

共 28 筆，逐筆人判：

- 本輪新檔的命中全是「X 屬控制層、不公開」一類的**聲明句**。
- 其餘是已公開舊檔中、第一階段已判讀放行的同一批：`row_confidence 0.85`、`judge_v4` 的模組名、`run_perf.py` 的 v4.5 機械層函式名、`split_sentences.py` 的近重複區間。
- **無操作層外洩。**

### D2 控制層原始檔反查（本輪新增）

**來源**：控制層原始檔 33 檔、字串常值 9,142 筆。涵蓋讀題、退回、生成時介入、機械層、忠實度各模組，以及 `config/` 的全部設定檔。逐檔清單在 bridge 附件的稽核全文。

**結果**：

| 項 | 筆數 | 內容 |
| --- | ---: | --- |
| 整條常值（≥8 字元）出現在 push 樹 | 75 | 型別名（`term_required`、`forbidden_charset` 等，屬公開的型別分類）、欄位名（記錄檔的欄位）、一般英文字、markdown 表格線、短正則字元集、第一階段已公開的路徑字串 |
| 12 字窗 | 604 | 同上類型，加上 §二.5 的列點正則 |

**沒有任何讀題樣式、退回模板句、門檻值或處理器邏輯出現在 push 樹。**

### W 動作層詞表（第二段新增，覆核 `845b64c` §一）

比對 push 樹的內容與檔名，不分大小寫子字串：

- 本輪 staging 24 檔：**0**。
- 未動的已公開舊檔：39 筆，見 §三。
- PDF 為二進位，未掃文字層；其正文即 `report_v1.2.md`，已掃。

### 令文嚴禁項逐條

| 嚴禁項 | 結果 |
| --- | --- |
| 規則表／簽核樣式／所有動作層實作／B 閘與抽取確定度決策碼 | 未收；D2 反查 0 實質命中 |
| 任何語料原文 | 未收；A 全查無外洩 |
| gold 檔 | 未收；grade_s* 只含讀 gold 的程式，不含 gold |
| `orders/` | 未收。新檔只在本 MANIFEST 以檔名引用（與第一階段 MANIFEST 同做法）；`literature_mapping` §九原有的令文路徑已改寫 |
| 含真實帳號或人名的筆記 | 未收；B 關新檔 0 |
| 憑證 | C 關 0 |
| 非 ASCII 檔名 | 0 |

## 五、第三段（放行後）要做的

依第一階段慣例：

1. 推前 fetch，核遠端 HEAD 仍是 `b288d39`。
2. 核 staging 與聊天端覆核過的 commit 逐位元組相同。
3. 以 `write_public_manifest.py` 重產 `manifest/public_manifest.{json,md}`（第二階段新增檔要入表）。
4. 再跑一次 README／PORTING 英中對應檢查。本輪已在 push 樹上跑過：README、PUBLIC_NOTES、PORTING 三對**全過**。中途抓到中文版正文的「第二部分」「第二條線」被檢查器正規化成數字 2，是偵測器的假訊號；已把正文改為與英文同形的「Part II」「這一階段」。
5. 新 commit 推公開倉，不 force。
6. 推完自遠端重新 clone 核對；最後刪 bridge `public_staging/`。
