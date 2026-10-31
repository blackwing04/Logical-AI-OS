# MANIFEST — Part II 可重現包（v2.0.1）

| 項 | 值 |
| --- | --- |
| 依據 | PI 2026-10-31 裁：放，要給別人可審核 |
| 範圍 | 每題結果表、合成卷題目與各臂答案全文、公開題庫各臂答案全文（只以題號對應） |
| 界線（不變） | 控制層不入；語料原文不入（Multi-IF／ComplexBench 題目只留題號，WildChat 與 LMSYS 不入）；gold 檔不入 |
| 雜湊 | sha256（LF 正規化後的位元組）前 16 碼 |

## 一、逐檔清單

| 檔 | sha256 | 來源 | 去語料方式 | 界線判定／改了什麼 |
| --- | --- | --- | --- | --- |
| `results/phase2/per_item/s1_items.csv` | `304768f95a1bf47c` | S1 評分檔（聊天端 grade_s1.py 輸出）＋結果檔答案重判 | 無語料；限制以 (type, param) 出現 | 公開：逐題判定；限制欄即 S1 的限制清單（gold 的題目規格），已開獎卷，依 PI 裁公開 |
| `results/phase2/per_item/s2_items.csv` | `bfc9ab4dd11458d5` | S2 評分檔＋重判；開發臂 v1.7／oracle 以同一核對器重判 | 同上 | 同上 |
| `results/phase2/per_item/s3_items.csv` | `a62dc58cf843b2ef` | S3 評分檔＋重判 | 同上 | 同上 |
| `results/phase2/per_item/multiif_zh_items.csv` | `2a8c901c5b58ec07` | 官方 Multi-IF 檢查器輸出（mif_scores） | 只留題號、dataset key、instruction id；不收 kwargs（含題目用詞） | 公開：官方判定 |
| `results/phase2/per_item/complexbench_rule_items.csv` | `fa71da7e24452d5e` | 官方 con_rule.py 輸出（cb_scores）＋只記不動臂讀題紀錄經公開 rule_mapping 重算 | 只留 main_id／point_id／kind／dims；不收規則字串與評分題文 | 公開：官方判定與讀題覆蓋；讀題只給四類結果，不給讀出內容 |
| `results/phase2/per_item/stats_paired.csv` | `c395b5b02c21719d` | stats_paired.py 對上列逐題檔的輸出 | 無語料 | 公開 |
| `results/phase2/per_item/stats_paired.py` | `801a478d010e45f1` | 新寫（標準庫） | 無語料 | 公開：統計方法 |
| `results/phase2/per_item/reading_variants.csv` | `fe741b9c02a9bdda` | 讀題變體回歸各欄紀錄（v1.10 重算、v1.11 候選、v1.11 凍結） | 只留各型命中數；不收變體改寫稿 | 公開：覆蓋率數字 |
| `data/phase2/README.md` | `2b1b5a74e838b7ed` | 新寫 | 無語料 | 公開 |
| `data/phase2/synthetic/s1_items.jsonl` | `10e14b6ddf40a889` | S1 題目 orig／final（甲類聊天端原創；乙類執行端依論壇題目撰寫，**執行方聲明原創，無法機械核查**）＋模型實際讀到的文字 | 不收乙類板名／日期／題目；不收哨兵題 | 公開：本專案原創，CC BY 4.0 |
| `data/phase2/synthetic/s2_items.jsonl` | `9ef869134b22fef3` | S2 題目，同上 | 同上 | 同上 |
| `data/phase2/synthetic/s3_items.jsonl` | `a02e5364482725bb` | S3 題目，同上 | 同上 | 同上 |
| `data/phase2/synthetic/s1_answers_3b.jsonl` | `c4739cd5fbdd35eb` | S1 3B 四臂答案全文（結果檔 answer 欄） | 只收 answer／answer_kind；不收任何控制層欄位；退回回聲遮罩（§三） | 公開：模型輸出；**research use only（Qwen Research License）**，不入 CC BY |
| `data/phase2/synthetic/s1_answers_7b.jsonl` | `9fb1b574aca8255f` | S1 7B 三臂答案全文 | 同上 | 公開：模型輸出，CC BY 4.0 |
| `data/phase2/synthetic/s2_answers_3b.jsonl` | `53402d58839759e2` | S2 3B 四臂答案全文（含開發臂 v1.7、oracle） | 同上 | 同 S1 3B |
| `data/phase2/synthetic/s2_answers_7b.jsonl` | `bfc20b2bbbe52849` | S2 7B 三臂答案全文（含只記不動臂） | 同上 | 同 S1 7B |
| `data/phase2/synthetic/s3_answers_3b.jsonl` | `9c7db089bd85bed0` | S3 3B 三臂答案全文 | 同上 | 同 S1 3B |
| `data/phase2/synthetic/s3_answers_7b.jsonl` | `04aaa7fb358616a7` | S3 7B 兩臂答案全文 | 同上 | 同 S1 7B |
| `data/phase2/public_benchmarks/multiif_zh_answers_3b.jsonl` | `2f2f1948433f79c4` | Multi-IF zh 3B 兩臂答案全文 | 不含題目；答案中重述 Multi-IF 題目 ≥40 字的段落遮罩；退回回聲遮罩（§三） | 同 S1 3B；以題號對應 |
| `data/phase2/public_benchmarks/multiif_zh_answers_7b.jsonl` | `92dffc1b177d68b8` | Multi-IF zh 7B 兩臂答案全文 | 同上 | 同 S1 7B；以題號對應 |
| `data/phase2/public_benchmarks/complexbench_rule_answers_3b.jsonl` | `30536c7ca721ab81` | ComplexBench 純規則子集 3B 兩臂答案全文 | 不含題目；答案引用題目的段落照生成原樣（題庫 MIT）；退回回聲遮罩（§三） | 同 S1 3B；以題號對應 |
| `data/phase2/public_benchmarks/complexbench_rule_answers_7b.jsonl` | `398087f0a5d25528` | ComplexBench 純規則子集 7B 兩臂答案全文 | 同上 | 同 S1 7B；以題號對應 |
| `data/phase2/public_benchmarks/extract_multiif_zh_turn1.py` | `49b45b53200cf0e7` | 新寫（標準庫）；實跑產出與 Phase II 用檔逐位元組相同 | 不含資料 | 公開：取題方法 |
| `README.md` | `308e31b128b0b611`（原 `5ad2dfbc66bb19a7`） | 公開倉現檔 | — | 目錄表加兩列；「不在本倉」改寫 Part II 一項；復現性加一條；授權表加 `data/`，3B 答案檔除外（research use only） |
| `results/phase2/per_type.csv` | `aa8d4b1404572016`（原 `0c62ba373849bb36`） | 公開倉現檔 | — | **更正**：S1 person_first 分母 17→15、term_req 27→22（四臂各一列，共 8 格；通過數不變），見 §四 |
| `README.zh-TW.md` | `7fd8ff796fdc4a35`（原 `c308e67c16994041`） | 公開倉現檔 | — | 同上（中文） |
| `results/phase2/README.md` | `c6bcf961205f8dbf`（原 `013cf4b8e62675bb`） | 公開倉現檔 | — | 開頭「只有彙總數字」改寫；ComplexBench 取樣一條改寫（區間只涵蓋題目抽樣）；新增逐題結果一節（欄位、口徑、與報告各節對應） |
| `eval/README.md` | `42269932a6de1974`（原 `69c1d0bb29e3f7df`） | 公開倉現檔 | — | 「不包含」一段改寫：答案與逐條判定已公開，gold 檔與題庫題目仍不含。上游授權表 ComplexBench 一格**更正**為 MIT（倉內 `LICENSE`；原寫 Data CC BY 4.0, code MIT） |

## 二、自驗（對既有交件，不符即停）

| 項 | 結果 |
| --- | --- |
| S1–S3 逐條判定 | 19 個評分臂以各卷核對器重判結果檔答案，逐題逐條與聊天端評分檔**全部相同**；各臂全守數與 `headline.csv` 相同 |
| S2 開發臂 | v1.7 55／117、oracle 60／117，與 2026-10-29 交件重判數相同 |
| 模型實際讀到的文字 | 與 final 去換行後逐字相同、各臂一致；只差換行者 S1 0、S2 17、S3 18 題 |
| Multi-IF | 四臂答案字數與官方評分檔記錄逐題相同；全過 262／254／295／289；觸發 36／35 |
| ComplexBench | 四臂答案字數逐題相同；觸發 102／89；讀題命中 145／252；讀到且裸臂未過→轉過 26/46（3B）、24/41（7B），未讀到 1/35、0/25 |
| 讀題變體 | 八欄各建置的命中與幻抽總數、五欄各型命中，與 2026-10-29 交件表逐數相同；v1.11 凍結原版 320／51、V2 301／52 |
| 配對統計 | up／down 17 組、p 值（報告列出的 11 組）與報告相同；bootstrap 區間端點因報告未記 seed，5 組差 0.4–0.8 點 |
| Multi-IF 取題腳本 | 以 HF 釘定 revision 的 CSV（sha256 與建卷紀錄相同）實跑，產出與 Phase II 用檔逐位元組相同 |

## 三、遮罩紀錄

過／不過判定照原文結果，不動（逐題表未改）。遮罩只在答案檔，標記內 N＝被換掉的字元數。不撤筆。

### 3a 答案抄進退回訊息：`[retry-prompt echo redacted, N chars]`（20 塊、20 題臂）

| 卷 | 題 | 臂 | N |
| --- | --- | --- | ---: |
| S2 | Q007 | B1 | 14 |
| S2 | Q028 | B1 | 8 |
| S2 | Q007 | B1_v1.7 | 15 |
| S2 | Q010 | B1_v1.7 | 9 |
| S2 | Q010 | B_oracle | 9 |
| S2 | Q044 | B_oracle | 14 |
| S2 | Q050 | B_oracle | 38 |
| S2 | Q093 | B_oracle | 28 |
| S3 | Q015 | B1 | 19 |
| S3 | Q047 | B1 | 12 |
| S3 | Q060 | B1 | 8 |
| S3 | Q083 | B1 | 13 |
| S3 | Q093 | B1 | 20 |
| S3 | Q015 | B2 | 19 |
| S3 | Q060 | B2 | 8 |
| S3 | Q093 | B2 | 14 |
| S3 | Q019 | A1 | 9 |
| Multi-IF zh | MIF323 | B1 | 10 |
| ComplexBench | CB0053 | B1 | 118 |
| ComplexBench | CB0507 | B1 | 14 |

### 3b Multi-IF 答案重述題目：`[benchmark prompt text redacted, N chars]`（43 段；A0 7、A1 7、B0 14、B1 15）

| 題 | 臂 | N |
| --- | --- | ---: |
| MIF071 | A0 | 45 |
| MIF071 | A1 | 45 |
| MIF072 | A0 | 49 |
| MIF072 | A1 | 49 |
| MIF072 | B0 | 49 |
| MIF072 | B1 | 49 |
| MIF075 | B0 | 41 |
| MIF075 | B1 | 41 |
| MIF078 | B0 | 42 |
| MIF078 | B1 | 42 |
| MIF079 | B0 | 52 |
| MIF079 | B1 | 52 |
| MIF102 | A0 | 43 |
| MIF102 | A1 | 43 |
| MIF102 | B0 | 44 |
| MIF102 | B1 | 44 |
| MIF103 | B0 | 45 |
| MIF103 | B1 | 45 |
| MIF106 | B0 | 51 |
| MIF106 | B1 | 51 |
| MIF138 | B0 | 41 |
| MIF138 | B0 | 41 |
| MIF138 | B1 | 41 |
| MIF138 | B1 | 41 |
| MIF156 | B0 | 51 |
| MIF233 | A0 | 66 |
| MIF233 | A1 | 66 |
| MIF234 | B0 | 60 |
| MIF234 | B1 | 60 |
| MIF254 | B0 | 58 |
| MIF254 | B1 | 58 |
| MIF278 | A0 | 40 |
| MIF278 | A1 | 40 |
| MIF278 | B0 | 68 |
| MIF278 | B1 | 68 |
| MIF279 | A0 | 63 |
| MIF279 | A1 | 63 |
| MIF286 | B1 | 43 |
| MIF314 | B0 | 50 |
| MIF314 | B1 | 50 |
| MIF322 | B1 | 73 |
| MIF436 | A0 | 90 |
| MIF436 | A1 | 90 |

ComplexBench 答案引用題目者保留（題庫倉 MIT）。

## 四、更正紀錄

| 檔 | 更正 | 原因 |
| --- | --- | --- |
| `results/phase2/per_type.csv` | S1 `person_first` 四列分母 17→15；`term_req` 四列分母 27→22；通過數不變 | 評分器對「譯成英文」的 16 題先丟掉與英文衝突的限制；第二階段此表自開獎報告手抄，分母未扣。由本輪逐題表核出；報告正文未引用這兩格 |
| `eval/README.md` 上游授權表 | ComplexBench：Data CC BY 4.0, code MIT → MIT | 以題庫倉實際標示（倉內 `LICENSE`、GitHub 授權欄）為準 |

## 五、自查

範圍：本輪 staging 全部檔。零模型呼叫。

| 關 | 結果 |
| --- | --- |
| K 欄位白名單 | 21 個資料檔，白名單外欄位 0；`answer_kind` 只有 deliver／ask／refuse |
| A 禁區語料反查（全查） | 第一階段七卷、M1–M3 卷、WildChat 全輪次、LMSYS-Chat-1M 中文全輪次、develop 其他結果檔、Multi-IF 題目與變體、ComplexBench `data_final.json`。合成卷題目檔對全部禁區語料：≥40 字元連續段 **0**。遮罩後 Multi-IF 答案對 Multi-IF 題目：≥40 字元連續段 **0**。答案檔與公開語料的其餘重疊都是模型常見寫法（樣板碼、信件套語、表格分隔線）；ComplexBench 答案引用題目者照生成原樣保留 |
| R 答案抄進退回訊息 | 遮罩後 **0** |
| J 生成時介入的固定字串 | 架構臂共有、裸臂全無的字串只有模型被退回後的回應口吻，無插入字串 |
| W 動作層詞表 | 文件與腳本 **0**；答案中 37 筆為一般英文字與一個中文複合詞，列白名單（逐字清單在交件報告，不入本檔），白名單外 **0** |
| B 人名／帳號 | 文件與腳本 0；答案中的電子郵件樣式全是模型虛構的範例聯絡方式 |
| C 憑證 | 0 |
| D 公開邊界 | 文件命中全是既有、已判讀的句子與本表的邊界聲明；資料檔 0 |
| D2 控制層原始檔反查 | 命中的整條常值都是一般字與型別名（language、structure、markdown、型別碼等） |
| 英中對應 | README／PUBLIC_NOTES／PORTING 三對全過 |
