[English](README.md) | 繁體中文

# Logical AI OS — 公開收裝

[![DOI, this version](https://zenodo.org/badge/DOI/10.5281/zenodo.23226740.svg)](https://doi.org/10.5281/zenodo.23226740)
[![DOI, all versions](https://zenodo.org/badge/DOI/10.5281/zenodo.23226739.svg)](https://doi.org/10.5281/zenodo.23226739)
[![prior work: LoRA line, software](https://zenodo.org/badge/DOI/10.5281/zenodo.17848554.svg)](https://doi.org/10.5281/zenodo.17848554)
[![prior work: LoRA line, preprint](https://zenodo.org/badge/DOI/10.5281/zenodo.17848305.svg)](https://doi.org/10.5281/zenodo.17848305)

以邏輯映射取代參數窮舉的一次實作嘗試。行為公式 `B = f(I, C, R)`，驗證公式 `M = i × e`。

本倉是**辨識線結案後的公開收裝**：把一條做完、有結論、結論有界的研究線
連同它的碼、判準表、文獻定位與評測制度一起放出來。

## 這條線做了什麼、結果是什麼

目標是：用一個**外部機械層**（零模型呼叫的語言學判準）加一個**小模型**（3B），
在開放領域的使用者請求上，把「對答案的限制」與「待處理的材料」分開；
缺口不猜，走 ASK 回問。

七卷盲測、三方分權評測、兩臂對照（本系統 vs 裸 7B）。**結論是有界的**：

- **不能宣稱「外部框架 ＋ 3B ≥ 裸 7B」。** 兩次有效卷一勝一負，勝的那卷
  bootstrap 95% 區間含零。
- **能宣稱的穩定差異（兩卷同向）**：守側哨兵上框架 0/10、1/7，裸 7B 4/10、5/7
  ——裸模型會把小說文案與截斷自述判成限制，框架不會；兩者的偽陽性型態不同。
- **兩條路徑的共同天花板**：無字面形狀的語義限制（要求改變措辭風格、語氣、
  詞彙層級一類），兩邊都抓不到。

詳見 [`results/`](results/)。

## 誠實清單（先讀這個）

這份收裝刻意把**不利的判定**放在和結果同等的位置：

- [`docs/literature_mapping.md`](docs/literature_mapping.md) — 39 列文獻對照總表。
  每一列都標了關係：`對得上`／**`借名`**／**`已有前作`**／`部分重疊`／`出處待核`。
  其中：
  - 三件候選原創，查重結果是 **兩件「已有前作」、一件「部分重疊」**；
  - 五框的「框架」一詞是**借名**（與 Fillmore 的 frame 不是同一構造物）；
  - 「對抗抽樣」是**借名**（哨兵對應 MFT，不是 contrast set）；
  - 「空框請求」**無文獻支持**，不掛在言語行為論底下；
  - bootstrap 的重抽單位有方法學缺口（以句重抽，但同篇句子不獨立）。
- [`docs/protocol/blind-test-protocol.md`](docs/protocol/blind-test-protocol.md) §9 —
  這套評測制度**沒有解決的三件事**。

## 目錄

| 路徑 | 內容 |
| --- | --- |
| [`docs/literature_mapping.md`](docs/literature_mapping.md) | 文獻對照總表（我方零件 vs 最近前作 vs 關係 vs 來源） |
| [`docs/method/`](docs/method/) | 四條相鄰文獻線的逐線判決、方法論答辯、對外解釋框架 |
| [`docs/theory/`](docs/theory/) | 失控機制理論與文獻定位；AI 行為虛構的機制假說與文獻對應 |
| [`docs/protocol/`](docs/protocol/) | 盲測制度（三方分權、seed 規矩、gold 凍結流程、artifact 自證） |
| [`docs/PORTING.md`](docs/PORTING.md) | 把這套量測層移植到另一種語言時：什麼原樣可用、什麼必須重建、什麼必須重新簽核 |
| [`results/`](results/) | 卷五／卷六／卷七開獎報告（去語料版） |
| [`src/`](src/) | v4.5 判定鏈：機械層、控制層、效能站、對照臂、切分器 |
| [`src/mechanical/signed_tables/`](src/mechanical/signed_tables/) | 簽核詞表（量詞分類器、功能層、詞表註冊表） |
| [`manifest/`](manifest/) | v4.5 封筆 manifest：31 組件的 sha256 與旗標表 |
| [`papers/`](papers/) | 技術報告（Zenodo 存放）：PDF、Markdown 正文、中文摘要、bib，附雜湊 |

## 公開範圍與不公開的東西

**不在本倉**，而且是刻意的：

- **七卷的句子檔與任何原始語料衍生內容**。測試語料源自 WildChat，
  含真實使用者對話；本倉不重新散布任何使用者原句。
- **所有答案本（gold）**。公開答案本等於作廢這些卷。
- 各輪修正令與進度檔（內部工作流）。
- 任何憑證。

### 收裝規矩：公開線與不公開線

本專案的公開範圍自 2026-10-08 起是一條**制度線**，不是逐次判斷：

| | 內容 |
| --- | --- |
| **公開線＝量測層** | 辨識零件（碼、判準表）、評測協定、失控理論、文獻對照、各卷去語料結案報告 |
| **不公開線＝操作層** | 行為公式的閘接法、驗證公式的計算定義與閾值、控制層、誠信協定設計，以及尚未結案的病灶處置 |

不公開項**不出現在本倉、也不出現在任何對外文本**；其設計稿只留在內部工作倉。
需要存證時走雜湊承諾的形式——**內容封存、本倉只放雜湊**，如同
[`COMMITMENT_2026-09-24.md`](COMMITMENT_2026-09-24.md)。

這條線的理由寫在這裡而不是藏著：**量測層可以被外人檢查，操作層被檢查前先要有
能被檢查的量測層。** 先放可驗的那一半，是順序問題，不是保留。

**凡是從內部檔去語料／去人名而來的檔，檔頭都寫明處理方式**；
逐檔逐處的刪改紀錄在 [`PUBLIC_NOTES.md`](PUBLIC_NOTES.md)。

## 復現性的誠實邊界

碼與判準表都在，但**語料不在**，所以本倉**不能逐位元組復現**七卷的數字。
可以復現的是：

- 判定鏈在**你自己的**句子上的行為（`src/` 可直接跑）；
- 簽核表與旗標的完整狀態（`manifest/`）；
- 每一個結論的歸因鏈（`results/` 的拆帳）。

`manifest/` 裡的雜湊是**內部原始檔**的雜湊，與本倉的去語料版**不相符**；
原因與對照方式見 [`PUBLIC_NOTES.md`](PUBLIC_NOTES.md) §三。這是去語料的必然代價，
不是紀錄錯誤。

## 授權與引用

**雙授權，依路徑分管**：

| 路徑 | 授權 | 檔 |
| --- | --- | --- |
| [`src/`](src/)、[`manifest/`](manifest/) | **MIT** | [`LICENSE`](LICENSE) |
| [`docs/`](docs/)、[`results/`](results/)、[`papers/`](papers/)、`README.md`、`PUBLIC_NOTES.md`、`MANIFEST.md` | **CC BY 4.0** | [`LICENSE-docs`](LICENSE-docs) |

論文（Zenodo）側為 **CC BY**。

**不在任何授權範圍內**：測試語料。它源自 WildChat，授權由該資料集自身規範；
本倉未重新散布其中任何內容（見 [`PUBLIC_NOTES.md`](PUBLIC_NOTES.md)）。

### 引用

**作者：Joe Yuan。** 那是本專案的對外筆名，不是法定姓名，引用請用這個名字。
[`PUBLIC_NOTES.md`](PUBLIC_NOTES.md) §1b 所述的去人名規矩管的是內部代稱與第三方，
**不管這個筆名**。

技術報告已在 Zenodo 發布。引用句照 Zenodo 給的（APA）：

> Yuan, J. (2026). Logical AI OS, Measurement Layer: An External Mechanical Extractor of Answer Constraints — Protocol, Failure Theory, and Bounded Results from Seven Blind Rounds (Version v1.2). Zenodo. https://doi.org/10.5281/zenodo.23226740

**兩個 DOI，不可互換。** 要引用**所有版本**用 [10.5281/zenodo.23226739](https://doi.org/10.5281/zenodo.23226739)——它永久指向最新版；
要引用**本版**用 [10.5281/zenodo.23226740](https://doi.org/10.5281/zenodo.23226740)。
若你的論點依賴的是 v1.2 當時的那組數字，用版本 DOI。

存放檔在 [`papers/zenodo_v1.2/`](papers/zenodo_v1.2/)，附雜湊；該處的 PDF 與
已發布的那一份逐位元組相同，而
[`papers/zenodo_v1.2/CHECKSUMS.md`](papers/zenodo_v1.2/CHECKSUMS.md)
寫明那四個檔裡**哪些在存放裡、哪些不在**。

若要引用本專案，請**連同 [`docs/literature_mapping.md`](docs/literature_mapping.md) 一起引**——
那張表列出每個零件的最近前作與關係（含三件「借名」與兩件「已有前作」），
**它才是這條線的誠實位置**。單引結論而不引那張表，會讓讀者誤以為零件是新的。

本專案更早的一條線（3B 的 LoRA 微調）另行存放於
[10.5281/zenodo.17848554](https://doi.org/10.5281/zenodo.17848554) 與
[10.5281/zenodo.17848305](https://doi.org/10.5281/zenodo.17848305)；
本倉的工作不依賴它。
