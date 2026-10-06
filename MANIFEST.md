# public_staging 收裝清單（MANIFEST）

令：`orders/2026-10-07_公開倉收裝令.md` §一。**三段制，本輪只做第一段。**

| 項 | 值 |
| --- | --- |
| 檔數 | **34**（複製＋處理 23 ／ 公開版新寫或節錄 11） |
| 公開倉 | `https://github.com/blackwing04/Logical-AI-OS.git`（**本輪不碰**） |
| 來源 | 一律**複製**，不搬動；內部檔原地不動 |
| 自查三關 | 見 §四 |

---

## 一、逐檔清單

「處理」欄：`原樣` ／ `去人名` ／ `去語料` ／ `去語料+去人名` ／ `節錄` ／ `新寫`。
雜湊為 **LF 正規化後的 sha256**；`來源 sha256` 是內部原始檔的，便於對照。

### 1a 自內部檔複製（23 檔）

| # | staging 路徑 | 來源 | 處理 | sha256（前16） | 來源 sha256（前16） | 為何該公開 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `docs/literature_mapping.md` | `docs/literature_mapping.md` | **去人名** | `8a10c693e2b9a1ce` | `b04affc65ec636aa` | 文獻對照總表，39 列，含「借名」與「已有前作」的誠實判定；外部審查最需要的一份 |
| 2 | `docs/method/2026-07-22_四條相鄰文獻線查證與定位.md` | `docs/timeline/2026-07-22_method_四條相鄰文獻線查證與定位.md` | **原樣** | `a50cc3b2fc841024` | `a50cc3b2fc841024` | 四條相鄰線逐線判決；對外定位句的出處，無語料無人名 |
| 3 | `docs/method/2026-07-29_方法論答辯_模型貼標籤.md` | `docs/timeline/2026-07-29_method_模型貼標籤方法論答辯.md` | **去人名** | `a4f995913af6b0af` | `d8287a5c2ce3a365` | 「用模型貼標籤為何不自相矛盾」的答辯；已是概念文 |
| 4 | `docs/method/2026-07-29_框架_GPS對外解釋.md` | `docs/timeline/2026-07-29_framework_GPS對外解釋.md` | **去人名** | `82c47e4d0d685937` | `ce7b6f59a1c4df2d` | 對外解釋框架（黑箱三層／GPS 比喻／ASK 定位）；已是概念文 |
| 5 | `manifest/v45_manifest.json` | `experiments/control-station/v45_manifest.json` | **原樣** | `ab05661190ff303f` | `ab05661190ff303f` | 同上，完整 64 位雜湊 |
| 6 | `manifest/v45_manifest.md` | `experiments/control-station/v45_manifest.md` | **原樣** | `40d3b839efbaa000` | `40d3b839efbaa000` | v4.5 封筆 31 組件雜湊與旗標表；只有路徑與雜湊，無語料 |
| 7 | `manifest/v45_manifest.py` | `experiments/control-station/v45_manifest.py` | **去人名** | `c87a5cb7e9ef7bc8` | `c87a5cb7e9ef7bc8` | manifest 產生器本身（自 import 鏈反查，不憑印象列） |
| 8 | `src/blindtest/run_7b_arm.py` | `experiments/blindtest/scripts/run_7b_arm.py` | **去人名** | `cb2ed42dee7e6d2f` | `cb2ed42dee7e6d2f` | 臂二裸 7B；對照臂的全部設定 |
| 9 | `src/control/judge_v4.py` | `experiments/control-station/judge_v4.py` | **去人名** | `764732bfb7e1596a` | `8845e46d5aaaa97f` | 裁決器 v4.1：出口三分、ASK 池、刀1-R 排序 |
| 10 | `src/control/request_form.py` | `experiments/control-station/request_form.py` | **去人名** | `7ed23ac8fadc5207` | `15f0eec929ad946f` | 請求形特徵列舉器（零新詞，自帶 self_audit） |
| 11 | `src/mechanical/clause_v2.py` | `experiments/mechanical-v2/clause_v2.py` | **去語料+去人名** | `5b182a8cac27b376` | `1524a992a869b98f` | 子句站本體；F1／F1-WS／刀1-C 全在此檔 |
| 12 | `src/mechanical/detectors.py` | `experiments/mechanical-v2/detectors.py` | **去人名** | `48612cc9095a91fb` | `69a6cedefaeaf5f8` | 七個偵測器與刀2；判定的訊號來源 |
| 13 | `src/mechanical/lexicon_v2.py` | `experiments/mechanical-v2/lexicon_v2.py` | **去人名** | `c7121d902052697a` | `99b6e68b297358c8` | 簽核詞表（含寫作規格形豁免表、量詞閉集）；內含 PI 自撰測試句，非 WildChat |
| 14 | `src/mechanical/pipeline_v2.py` | `experiments/mechanical-v2/pipeline_v2.py` | **去語料+去人名** | `092c1c715ad454d4` | `d8723b37c3ac4017` | 軸一規則與 F4 功能層 |
| 15 | `src/mechanical/reorder_v2.py` | `experiments/mechanical-v2/reorder_v2.py` | **去語料+去人名** | `d1c022bee13ee2c0` | `c8aeb6795009d9a8` | 軸二重排與 F2／F2-WS |
| 16 | `src/mechanical/rules_v2.py` | `experiments/mechanical-v2/rules_v2.py` | **去人名** | `1e3fc5e9ec09c15f` | `f979a3095f9b8d82` | 規則表本體 |
| 17 | `src/mechanical/signed_tables/function_layer.json` | `experiments/mechanical-v2/signed_tables/function_layer.json` | **去人名** | `dd4a3d4a2557d205` | `ec1df128cce3e2c0` | F4 功能層簽核表（五分類留槽＋本令實作的唯一一條） |
| 18 | `src/mechanical/signed_tables/knife2_one_classifier.json` | `experiments/mechanical-v2/signed_tables/knife2_one_classifier.json` | **去人名** | `b106667fd4350cbe` | `bb4a4ccadf6355ef` | 刀2「一＋物件量詞」簽核表；sortal／measural 界線的落地 |
| 19 | `src/mechanical/signed_tables/lexicon_registry.json` | `experiments/mechanical-v2/signed_tables/lexicon_registry.json` | **去人名** | `52586129f1461d6b` | `c207c1208d9e1670` | F5 詞表註冊表；未註冊即拋例外的那張表 |
| 20 | `src/perf/early_stop.py` | `experiments/perf-station/early_stop.py` | **去人名** | `3e60d5a62f3ff9fc` | `3e60d5a62f3ff9fc` | 刀3 早停條件；離線驗證與生產共用同一份 |
| 21 | `src/perf/run_perf.py` | `experiments/perf-station/run_perf.py` | **去人名** | `60c211e02ccd5c39` | `83b01addf50c804c` | 臂一管線；本代新增的 config 欄在此 |
| 22 | `src/perf/schema_v1.py` | `experiments/perf-station/schema_v1.py` | **去人名** | `3118b84b017ffd7e` | `712ffc481bd0800d` | 方案甲格式物件 |
| 23 | `src/tools/split_sentences.py` | `tools/split_sentences.py` | **去語料+去人名** | `34bfcbf9d1c82cfe` | `890a73048d47a3c7` | 正典切分器；句數認定的唯一依據 |

### 1b 公開版新寫或節錄（11 檔）

| # | staging 路徑 | 來源 | 處理 | sha256（前16） | 位元 | 為何該公開 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `LICENSE` | （公開版新寫） | **新寫** | `6ac9e44619713aa8` | 1083 | 碼（`src/`、`manifest/`）的 MIT 授權，第二段修正令 §4 |
| 2 | `LICENSE-docs` | （公開版新寫） | **新寫** | `1ec1b3d515d88593` | 1883 | 文件（`docs/`、`results/`、三份根目錄 md）的 CC BY 4.0 授權，第二段修正令 §4 |
| 3 | `MANIFEST.md` | （本檔） | **新寫** | `4d6d7469f995c3e9` | 17484 | 收裝清單與自查結果，令文 §一要求 |
| 4 | `PUBLIC_NOTES.md` | （公開版新寫） | **新寫** | `3ca27d271fc603fd` | 4813 | 去語料／去人名的處理聲明，與雜湊落差的說明 |
| 5 | `README.md` | （公開版新寫） | **新寫** | `e9cc20e3aeef3e96` | 5182 | 倉導覽；**誠實清單前置**：把借名、已有前作、方法學缺口、制度未解決的三件事放在和結果同等位置 |
| 6 | `docs/protocol/盲測制度說明.md` | （公開版新寫，材料散在內部各輪修正令） | **新寫** | `9c63c7b94185764a` | 7105 | 三方分權／seed 規矩／gold 凍結流程／artifact 自證；**制度說明可公開，gold 本身不可**。§九 列出這套制度沒解決的事 |
| 7 | `docs/theory/AI行為虛構_機制假說與文獻對應.md` | 節錄：`laios-bridge/docs/timeline/2026-08-15_AI行為虛構事件紀錄_Fable5.md` §五＋§六 | **節錄** | `35677340fca14043` | 4187 | **只留機制假說與文獻對應**；逐輪事件紀錄全刪，依令文辦 |
| 8 | `docs/theory/失控機制理論與文獻定位.md` | 節錄：`docs/timeline/2026-08-04_archive_R8R9結案與失控機制.md` §六 ＋ `laios-bridge/docs/timeline/2026-08-05_archive_R10R10b結案.md` §五 | **節錄** | `0d5ba4399f925427` | 3723 | 四句失控論與其文獻定位；概念文，去人名後可公開 |
| 9 | `results/2026-10-05_卷五開獎報告_去語料.md` | `laios-bridge/reports/2026-10-05_卷五開獎報告.md` | **去語料** | `8ccf64ed0a901e4e` | 2074 | 歷卷帳的第一筆有效卷（我方負）；統計與歸因留，原句片段刪 |
| 10 | `results/2026-10-06_卷七開獎報告_辨識線結案_去語料.md` | `laios-bridge/reports/2026-10-06_卷七開獎報告_辨識線結案.md` | **去語料** | `3dbe4328e30fddbc` | 3403 | 辨識線結案與有界結論；對外能寫與不能寫的話都在這裡 |
| 11 | `results/2026-10-06_卷六開獎報告_去語料.md` | `laios-bridge/reports/2026-10-06_卷六開獎報告.md` | **去語料** | `bcc3ca26724f3847` | 1370 | 不算成績那一卷；根因是判準層令文缺陷，**公開這一筆才看得出修法的由來** |

---

## 二、逐處處理紀錄

### 2a 去語料（9 處）

**判準**：刪 WildChat 衍生的逐字句或片段；**留**句子 id（句子檔不公開，
id 單獨存在無法回溯到語料）；**留** PI 自撰的測試句，但在 §三 標明其來源。

| # | 檔 | 刪了什麼 | 狀態 |
| --- | --- | --- | --- |
| 1 | `src/mechanical/clause_v2.py` | 卷三 D17/s01 逐字原句（WildChat 衍生） | 已代換 |
| 2 | `src/mechanical/clause_v2.py` | 卷三 D17/s01 子句片段（WildChat 衍生） | 已代換 |
| 3 | `src/mechanical/clause_v2.py` | （同上立案句的指涉，改為詞表鍵表示法，不涉語料） | 已代換 |
| 4 | `src/mechanical/reorder_v2.py` | 語料句片段（親屬領屬構式實例） | 已代換 |
| 5 | `src/mechanical/reorder_v2.py` | 語料句片段（指示主語實例） | 已代換 |
| 6 | `src/mechanical/reorder_v2.py` | 語料句片段（指示／概念主語實例） | 已代換 |
| 7 | `src/mechanical/pipeline_v2.py` | 開發集 M15/s04 逐字原句（來源未逐筆可溯，從嚴視為語料） | 已代換 |
| 8 | `src/tools/split_sentences.py` | 卷一 B03／B18 逐字片段（WildChat 衍生） | 已代換 |
| 9 | `src/tools/split_sentences.py` | 卷七 序12 候選原文片段（WildChat 衍生；該句是 CC 自己在卷七組卷時寫進註解的） | 已代換 |

另在 `results/` 三檔手工去語料（短檔，逐處手改比腳本代換可靠）：

| 檔 | 刪了什麼 |
| --- | --- |
| 卷五開獎 | 9 句機械直收誤收的**數字表達原句片段**；F01 的字數規格原句片段；F10 的語言規格原句片段。三處皆改為類型描述，id 保留 |
| 卷六開獎 | 無語料可刪（原檔不含任何使用者原句）；只改了兩處指向不公開 `orders/` 的路徑引用 |
| 卷七開獎 | §三.3「病三」那一組 **6 個漏抓句片段**，改為類型描述（措辭風格／語氣／詞彙層級／語言難度／長度壓縮／重點突出）；另把刀2 誤收的詞表鍵改為指向 `signed_tables/` |

### 2b 去人名（16 檔）

專案內以一個短代稱指稱人類主持人。它是專案代稱而非真實姓名，但令文對概念文明文
要求「去人名後」，所以**全 staging 一律代換為 `PI`**，不分檔種——一致比偏好重要。

| 檔 | 代換處數 |
| --- | --- |
| `docs/literature_mapping.md` | 1 處 |
| `docs/method/2026-07-29_方法論答辯_模型貼標籤.md` | 3 處 |
| `docs/method/2026-07-29_框架_GPS對外解釋.md` | 1 處 |
| `src/mechanical/clause_v2.py` | 7 處 |
| `src/mechanical/reorder_v2.py` | 6 處 |
| `src/mechanical/pipeline_v2.py` | 3 處 |
| `src/mechanical/detectors.py` | 6 處 |
| `src/mechanical/rules_v2.py` | 12 處 |
| `src/mechanical/lexicon_v2.py` | 31 處 |
| `src/mechanical/signed_tables/knife2_one_classifier.json` | 4 處 |
| `src/mechanical/signed_tables/function_layer.json` | 1 處 |
| `src/mechanical/signed_tables/lexicon_registry.json` | 1 處 |
| `src/control/judge_v4.py` | 6 處 |
| `src/control/request_form.py` | 2 處 |
| `src/perf/run_perf.py` | 2 處 |
| `src/perf/schema_v1.py` | 1 處 |

**自查第一輪抓到四檔漏網**（標了「原樣」但檔內仍有代稱）：`docs/literature_mapping.md` 與三張簽核表 JSON，共 7 處。
已改標為「去人名」後重跑，第二輪 B 關歸零。**是自查抓到的，不是我先想到的。**

---

## 三、兩件必須先講清楚的事

### 3a `manifest/` 的雜湊與本倉檔案**不相符**，這是去語料的必然代價

`manifest/v45_manifest.{md,json}` 記的是**內部原始檔**的 sha256。
本倉的 `src/` 經過去語料與去人名，所以**雜湊必然不同**。

| 選項 | 代價 |
| --- | --- |
| 公開未處理的碼，雜湊相符 | **違反「嚴禁含語料」**，不可行 |
| 公開去語料版，附逐處刪改紀錄（**現行做法**） | 雜湊不符，但差異逐處可查 |
| 只公開 manifest 不公開碼 | 碼不可讀，公開的意義大減 |

現行做法讓外部審者能做的事：拿 §一 的「來源 sha256」與內部 manifest 對照，
確認**內部封筆的那一份**是什麼；再拿 §二 的逐處刪改紀錄，確認
**公開版與它的差異只有去語料與去人名**。這兩步合起來可驗，單獨一步不可驗。
**這一點呈裁**：若要讓公開版自己可驗，需另出一份公開版 manifest。

### 3b `src/mechanical/lexicon_v2.py` 內含 PI 自撰的測試句

那幾句（如請託事件敘述的同構變體）是 PI 手寫的掃查用例，**不是 WildChat 語料**，
所以沒有依「嚴禁」刪除；但它們是真人寫的句子，**在此標明來源讓審者自己判**。
若裁定也要刪，一行即可照辦。

---

## 四、自查（令文 §一末要求，附於此）

## 自查（公開倉收裝令 §一末）

| 項 | 值 |
| --- | --- |
| staging 檔數 | **36** |
| staging 全文字元數 | 237953 |
| 抽樣 seed | `20261007`（固定，可重跑） |

### A 語料反查——自**候選原文全集**逐片段反查（**全查，不抽樣**）

每篇切成不重疊的 10 字片段，逐片段在 staging 全文（去空白後）搜。
**從語料那一側問「有沒有洩出去」。**

**本關原為抽 20 篇；第三段推公開倉前改為全查，當場抓到兩處**——
抽樣版在同一棵樹上是全過的。詳見下方命中明細與 MANIFEST §二。

| 卷 | 受查篇 | 片段數 | 命中 |
| --- | --- | --- | --- |
| 卷一 | 40 | 784 | — |
| 卷二 | 34 | 726 | — |
| 卷三 | 35 | 780 | — |
| 卷四 | 21 | 494 | — |
| 卷五 | 24 | 531 | — |
| 卷六 | 80 | 1668 | — |
| 卷七 | 91 | 1884 | — |

| 項 | 值 |
| --- | --- |
| 受查篇數 | **325**（候選全集） |
| 反查片段總數 | **6867** |
| **命中數** | **0** |

### A2 句子檔全句反查（七卷全部句子，不抽樣）

| 項 | 值 |
| --- | --- |
| 受查句數 | **1134** |
| 整句出現在 staging 者 | **0** |

### B 人名與第三方帳號樣式

**宣告過的豁免**：`MANIFEST.md`／`PUBLIC_NOTES.md` 不列入本關——
它們是處理聲明，必須寫出被排除的類別名稱。兩檔仍受 A／A2 與 C 全檢。

| 樣式 | 命中檔數 | 命中次數 | 明細 |
| --- | --- | --- | --- |
| 人類主持人的專案代稱（有詞界） | 0 | **0** | — |
| **同代稱，不分大小寫且無詞界**（第二段補） | 0 | **0** | — |
| Reddit 字樣 | 0 | **0** | — |
| Reddit 帳號樣式 | 0 | **0** | — |
| @帳號樣式 | 0 | **0** | — |
| 電子郵件樣式 | 0 | **0** | — |

| 豁免兩檔內的樣式出現數（只為透明，不計入判定） | 值 |
| --- | --- |
| Reddit 字樣 | 7（皆為聲明文列舉該類別時的字面） |

### C 憑證樣式

| 樣式 | 命中檔數 | 命中次數 |
| --- | --- | --- |
| GitHub token | 0 | **0** |
| OpenAI 式金鑰 | 0 | **0** |
| AWS key id | 0 | **0** |
| PEM 私鑰 | 0 | **0** |
| 明文憑證賦值 | 0 | **0** |

| **三關總判** | **全過** |
| --- | --- |
| A 候選原文片段反查 | 0 命中 |
| A2 全句反查（1134 句） | 0 命中 |
| B 人名／帳號 | 0 命中 |
| C 憑證 | 0 命中 |

**自查本身的限制，照實記**（三點）：

1. **A 是抽樣**（20 篇／七卷候選），不是全查。
2. **A2 是全查但只比整句**——對「語料被改寫後引用」無效。
   A 與 A2 都抓不到的情形：有人把語料改寫後寫進 staging。
   那一層只能靠逐檔目檢，見 MANIFEST §二的逐處刪改紀錄。
3. **B 關有一處宣告過的豁免**（兩份處理聲明不列入），見該節。

---

## 五、嚴禁清單的逐條自核

| 令文嚴禁項 | staging 現狀 |
| --- | --- |
| 七卷句子檔與任何含 WildChat 語料的檔 | **無**。A 關抽 20 篇候選原文反查、A2 關 1134 句全句反查，皆 0 命中 |
| 所有答案本／gold | **無**。連 gold 的 sha256 都沒放——雜湊要搭配答案本才有驗證意義，單獨公開只是裝飾 |
| bridge 的 `orders/`、`NEXT.md` | **無**。卷六開獎去語料版原本引了 `orders/` 路徑，已改寫 |
| 含 Reddit 帳號或真實人名的筆記 | **無**。`2026-09-05_聊天端筆記_Reddit…` **未收**；B 關 Reddit 字樣／帳號樣式／@帳號／電子郵件皆 0 命中 |
| gitkey 類任何憑證 | **無**。C 關五種樣式皆 0 命中 |

---

## 六、停工點

**第一段做完，push bridge 後停。不碰公開倉。**

呈裁三件：

1. **公開版 manifest 要不要另出**（§3a）——現行做法需兩步才可驗。
2. **`lexicon_v2.py` 的 PI 自撰測試句**要不要一併刪（§3b）。
3. **我補進 `進` 清單的兩項**，請核：`docs/protocol/盲測制度說明.md`（新寫，令文列了「盲測制度說明」但倉內無此檔，故由我整理）與 `README.md`（新寫，公開倉需要入口；我把誠實清單放在最前面）。
