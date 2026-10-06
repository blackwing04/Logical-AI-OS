# 文獻對照總表

**用途**：把專案各主張／零件與最接近的前作對起來，一列一件。
**這是合併表，不新寫評價**——每列的「關係」欄照各輪結論原樣搬，不在此處重新判斷。

| 令／筆記 | 日期 | 本表涵蓋 |
| --- | --- | --- |
| `2026-10-07_文獻補查與總表落檔令.md` §二 | 2026-10-07 | 本表（8/31 欠件補齊） |

**關係欄的五個值**：
`對得上`（原典明確主張該事）／`借名`（原典沒講到該用法，只是名詞借用）／
`已有前作`（查重結論：概念非首創）／`部分重疊`（元件有前作、組合未見同形）／
`未找到`（五組關鍵詞內零命中，須附關鍵詞與庫）。
另有 `出處待核`：前作存在但本輪未能核到完整出處，**不編**。

---

## 一、辨識線零件（引用支持）

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 軸一「主請求」＝使用者要系統做的那件事 | Austin, J. L. (1962) *How to Do Things with Words*, Lect. VIII–IX；Searle, J. R. (1969) *Speech Acts*（directives） | **對得上** | `reports/2026-10-06_文獻之旅_report.md` A1 |
| 軸一「隱性需求」（規則 5 自己收掉） | Searle, J. R. (1975) "Indirect Speech Acts", *Syntax and Semantics 3*, pp. 59–82 | **對得上** | 同上 A1 |
| F4 功能層「Form≠Function」（疑問形不必然推主請求） | Austin (1962) 言外之力不由形式唯一決定 | **對得上** | 同上 A1 |
| 軸一「空框請求」 | （無） | **借名**／實為無文獻支持——Austin、Searle 皆無「請求形式齊備但缺內容槽」此範疇 | 同上 A1 |
| 五框（主請求框／自陳情境／描述框／引述框／過去敘事框） | Fillmore, C. J. (1982) "Frame Semantics"；Fillmore (1985) *Quaderni di Semantica* 6(2):222–254 | **借名**——我方的「框」是偵測器訊號合取的閘條件，無 frame elements、無 frame-to-frame relations | 同上 A2 |
| 「句型層先定意義、詞表只在對的域內開工」（軸二重排令核心） | Goldberg, A. E. (1995) *Constructions*, Ch. 1–2 | **對得上（僅此優先序）**；構式本體不對得上 | 同上 A2 |
| 人稱偵測器「沒掛人」、F3 祈使隱含人稱＝你、主語繼承 | Li, C. N. & Thompson, S. A. (1981) *Mandarin Chinese: A Functional Reference Grammar*, Ch. 4／14／15 | **對得上但實作偏離**——原典支持主語省略（零代詞），不支持把非人主語歸入同格 | 同上 A3 |
| 刀2 量詞白名單＝物件量詞、明文排除度量單位 | Chao, Y.-R. (1968) *A Grammar of Spoken Chinese*；Her, O.-S. & Hsieh, C.-T. (2010) *Language and Linguistics* 11(3):527–551（sortal vs measural） | **對得上（對得很緊）** | 同上 A4 |
| 守側哨兵（整篇 gold 全無限制，抓偽陽性） | Ribeiro, M. T. et al. (2020) "Beyond Accuracy: Behavioral Testing of NLP Models with CheckList", ACL 2020 — **MFT** | **對得上（限 MFT）**；INV／DIR 未實作 | 同上 A5 |
| 「對抗抽樣」這個說法 | Gardner, M. et al. (2020) "Evaluating Models' Local Decision Boundaries via Contrast Sets", Findings of EMNLP 2020 | **借名**——contrast set 要求同一樣本最小編輯且標籤翻面；哨兵是整篇新樣本 | 同上 A5 |
| bootstrap 求兩臂差的 95% 區間、「含零→不宣稱勝」 | Efron, B. (1979) *Ann. Statist.* 7(1):1–26；Koehn, P. (2004) "Statistical Significance Tests for MT Evaluation", EMNLP 2004, pp. 388–395（paired bootstrap） | **對得上**。附記：我方以句重抽，但同篇句子共享任務欄不獨立，應為 cluster bootstrap | 同上 A6 |

## 二、辨識線三件原創候選（查重）

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 軸二「限制／材料」相對任務本體的子句級標註 | Zverev, E. et al. (2025) ICLR 2025, arXiv:2403.06833（SEP）；Wallace, E. et al. (2024) arXiv:2404.13208（Instruction Hierarchy）；AGENTIF (2025) arXiv:2505.16944（Task／Context／Constraint 三分）；FollowBench arXiv:2310.20410；StructFlowBench arXiv:2502.14494 | **已有前作** | `reports/2026-10-06_文獻之旅_report.md` B1 |
| 外部機械層＋小模型做 AI 行為治理（不改權重） | Rebedea, T. et al. (2023) "NeMo Guardrails", EMNLP 2023 Demo, arXiv:2310.10501；Coucke, A. et al. (2018) "Snips Voice Platform", arXiv:1805.10190（確定性層先跑、抽不到才跑機率層）；PL-Guard arXiv:2608.15673；Llama Guard 級聯 arXiv:2512.19011 | **已有前作** | 同上 B2 |
| 研究流程元層：聊天端持 gold、執行端盲跑、人類只裁決 | Roelofs, R. et al. (2019) NeurIPS 2019（Kaggle public/private 切分）；Chen, W., SSRN 7555178（hidden-test 外部評分器）；Auditing Games for Sandbagging arXiv:2512.07810（設計期可見／執行期盲）；Autonomous Research Agents survey arXiv:2608.05179（creator 與 evaluator 不得共享 context） | **部分重疊** | 同上 B3 |

## 三、ASK 閘門與規則否決（2026-10-07 補查）

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 缺槽／低信心走 ASK（封閉 schema 側） | Jurafsky & Martin, *SLP3* Ch. 24（α/β/γ 三門檻：拒識／明確確認／隱式確認／直接接受）；AAAI SS-03-06 (2003) Clarification in Spoken Dialogue Systems；Padmakumar & Thomason (2020) arXiv:2006.05456 | **已有前作**（教科書級成熟） | `reports/2026-10-07_文獻補查_report.md` §一條1(a) |
| 「規則層判低信心→強制問」（開放領域側） | Chow, C. K. (1970) *IEEE Trans. IT* 16(1):41–46（reject option）；Madras, D. et al. (2018) NeurIPS 2018（learning to defer）；Verma & Nalisnick (2022) arXiv:2202.03673；A Vision for Abstention in LLMs, TechRxiv 10.36227/techrxiv.175682660.02761872（外部驗證層可為規則引擎） | **已有前作** | 同上 §一條1(b) |
| 「開放領域＋三槽由 `B=f(I,C,R)` 決定＋ASK 內建規格化管線」此一組合 | W5H2 七欄意圖分解（arXiv:2606.22916）；保守規格化「不填不移未知槽 ?」（arXiv:2609.22213、arXiv:2512.00329）；Structured Intent Canonicalization（arXiv:2602.18922） | **部分重疊**——元件全有前作，組合未見同形 | 同上 §一條1(c) |
| T1 規則否決 T3 模型輸出（規則壓模型） | Katz, G. (2020) "Guarded Deep Learning using Scenario-Based Modeling", MODELSWARD 2020, arXiv:2006.03863（**override rules**）；續篇 arXiv:2301.08114；Alshiekh, M. et al. (2018) "Safe Reinforcement Learning via Shielding", AAAI 2018, arXiv:1708.08611（**shield**，只在不安全時糾正） | **已有前作** | 同上 §一條2 |
| 低信心轉出（降權棄答／轉人工）＋信心分層 | Chow (1970)；Madras et al. (2018)；conformal 免訓練轉交 arXiv:2509.12573；神經符號驗證層 PL-Guard arXiv:2608.15673、SMT 合規 arXiv:2601.06181、VFR-LLM arXiv:2606.27281 | **已有前作** | 同上 §一條2 |

## 四、失控理論定位（2026-08-05）

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 四句論之「目的忠實 × 覆蓋邊緣」（目的論方法：從訓練目標推導失效） | McCoy, R. T. et al. "Embers of Autoregression: Understanding Large Language Models Through the Problem They are Trained to Solve", **arXiv:2309.13638**；筆記記為 PNAS 2024 期刊版 | **最近近親**（筆記原判）。**PNAS 2024 卷期／DOI：出處待核**（本輪五組檢索未核到，不編） | `docs/timeline/2026-08-05_archive_R10R10b結案.md` §五 |
| 零件「模式檢索」 | shortcut learning（筆記未指定具體篇目） | **出處待核**（筆記只給領域名） | 同上 §五 |
| 零件「無因果層」＝有能力無理解 | Dennett（筆記未指定具體著作） | **出處待核**（筆記只給作者名） | 同上 §五 |
| 零件「無警報」＝二元計分激勵瞎猜 | Kalai, A. T., Nachum, O., Vempala, S. S., Zhang, E. (2025) "Why Language Models Hallucinate", **arXiv:2509.04664** | **對得上**（核到原文：訓練與評測獎勵猜測而非承認不確定） | 同上 §五 |
| say-do gap 的測量面（言行不一致普遍存在） | Xu, R. et al. (2025) "Large Language Models Often Say One Thing and Do Another", ICLR 2025, **arXiv:2503.07003**（WDCT，言行不一致約 30%，且**只對齊一側對另一側影響小且不可預測**）；**arXiv:2604.28031**「Models Recall What They Violate」（DRIFTBENCH，KBV 率 8–99%）；Cartagena & Teixeira (2026) "Mind the GAP", **arXiv:2602.16943**（文字拒絕不遷移工具層） | **已有前作（測量面）**。筆記原判：「測量極多，解釋多停於獎勵層」 | 同上 §五 |
| PI 獨有三項：①「取消連接」一步 ②四因子整合為一條失效方程 ③介入性證據（temp=0 單變因翻轉） | 文獻全預設「連接存在而壞」；WDCT 的「對齊言不動行」被筆記記為此論之實證預言 | **部分重疊**（筆記原判：非獨一份；「有測量有局部歸因、缺機制層完整故事」） | 同上 §五 |

## 五、誠信對照（2026-08-15）

**注意**：原筆記 §六 **不在倉內**（`data/record/2026-08-15/2026-08-15.md` 只有四節，無誠信對照）。
以下三列依 `orders/2026-10-07_文獻補查與總表落檔令.md` §二 的摘述填入，出處由 CC 本輪補齊。

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 模型的自述理由不等於其真實決定過程 | Turpin, M., Michael, J., Perez, E., Bowman, S. R. (2023) "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting", **NeurIPS 2023, arXiv:2305.04388** | **對得上** | 令文 §二 摘述（**原筆記 2026-08-15 §六 未在倉內找到**） |
| 內部機制可被外部工具部分追溯 | Anthropic (2025) "On the Biology of a Large Language Model", **transformer-circuits.pub/2025/attribution-graphs/biology.html**（attribution graphs／circuit tracing，cross-layer transcoder 約 3000 萬特徵） | **對得上** | 同上 |
| 自述與機制分離的人類對照（左右腦分裂病人的事後合理化） | Gazzaniga, M. S.（筆記未指定具體著作） | **出處待核**（筆記只給作者名） | 同上 |
| 「規則知悉不阻斷執行」（知道規則但照樣違反） | 筆記原判：**無直接文獻**。本輪補到最接近者＝DRIFTBENCH 的 KBV（knows-but-violates）**arXiv:2604.28031**，但那是測量而非機制 | **部分重疊**（測量面有前作、機制面筆記判無） | 同上 |

## 六、F2 對照（2026-09-05）

**注意**：原筆記 §三 **不在倉內**（`data/record/` 下無 2026-09-05 目錄）。arXiv 號由 CC 本輪自核。

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| F2 對照用的 H3／H4 假設 | Sheshadri, A., Hughes, J., Michael, J., Mallen, A., Jose, A., Janus, Roger, F. (2025) "Why Do Some Language Models Fake Alignment While Others Don't?", **arXiv:2506.18032**。**H3＝Terminal Goal Guarding**（因內在不喜歡目標被改而順從，與後果無關）；**H4＝Low Coherence Alignment Faking**（出於其他原因偽裝，順從行為對情境措辭敏感）。另 H1＝Rater Sycophancy、H2＝Instrumental Goal Guarding | **對得上（H1–H4 已核到原文）**；**Fig 12／13 出處待核**（抓到的 v1 全文段落只到 Fig 11，附錄自 Fig 18 起） | 令文 §二 摘述（**原筆記 2026-09-05 §三 未在倉內找到**）＋CC 本輪自核 |

## 七、probe 的 OOD 泛化（2026-08-31）

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| A1 線性探針錨定集 LPO 88.3% → 新考卷 70.0%，落差 18.3 點（教材擴充後收到 15.0，未消除） | Belinkov, Y. (2022) "Probing Classifiers: Promises, Shortcomings, and Advances", *Computational Linguistics* 48(1):207–219（`aclanthology.org/2022.cl-1.7`）；具體泛化失敗實證見 "False Sense of Security: Why Probing-based Malicious Input Detection Fails to Generalize", arXiv:2509.03888；另 "Probing Classifiers are Unreliable for Concept Removal and Detection", NeurIPS 2022 | **對得上**（筆記原判：「本站數字是該現象在中文限制語義上的一個實例，**不是新發現**」） | `data/record/2026-08-31/2026-08-31.md:223`（文獻對照補格）。**注**：筆記原文**未給出處**，上列出處為 CC 本輪補齊；令文「40 資料集先例」一語，CC 讀為我方 40 句新考卷，**讀法待核** |

## 八、四條相鄰線逐線判決（2026-07-22，**該檔在倉內，非遺失**）

來源：`docs/timeline/2026-07-22_method_四條相鄰文獻線查證與定位.md`（63 行，已 commit）。
2026-10-07 令文誤記此檔遺失；本輪補查（§三各列）在不知其存在下獨立重做，結論逐條收斂。
下列各列**照該檔原文搬**，不重新判斷。

| 我方主張／零件 | 最近前作（作者／年／出處） | 關係 | 來源筆記 |
| --- | --- | --- | --- |
| 外部協定／不信任模型內部／trusted-untrusted 分層／defer | **AI Control**（Redwood Research 線；ICML oral 2024 起，UK AISI ControlArena 等）。該檔記的可借項：safety/usefulness tradeoff 數學、audit budget（對應 ASK 成本帳）、**Factor(T,U)** 的 factored cognition、TraceGuard 的「結構化判準優於整體判斷」 | **哲學近親，問題不同**（malice vs incapability＋輸入劣化）→ 論文用法：motivation 引＋related work 區隔威脅模型 | `docs/timeline/2026-07-22_method_四條相鄰文獻線查證與定位.md` §1。**2026-10-07 補**：Factor(T,U)＝arXiv:2512.02157（本輪 10/6 B3 獨立撞到同一篇）；另加 Auditing Games for Sandbagging arXiv:2512.07810 |
| ASK 閘門的閾值理論工具 | **Selective prediction／Abstention／Conformal**（Wen et al. 2025 survey；conformal abstention 具 finite-sample 保證：participation＋conditional correctness） | **極成熟**。邊界：**abstention 動作止於「不答／IDK／輸出集合」；ASK＝棄權後的下一步（指出缺的槽＋針對性提問），文獻中屬不同能力** | 同上 §2（此措辭比 2026-10-07 本輪的「拒答不回問」更鋒利，總表採該檔說法） |
| `row_confidence` 閾值（現 0.85） | conformal calibration（有覆蓋率保證之校準閾值） | **可借，未結**——該檔記「現 0.85 任意鎖死」，應升級；註明「OOD 站後執行」 | 同上 §2「可借（重要）」 |
| 外部層做內容政策與格式驗證 | **Guardrails 系統**（NeMo／Guardrails AI／Llama Guard） | **各自更完整但格子不同**——該檔判：**無 I／C 分離、無槽位完整性、無缺資訊追問**。可借 validator 工程模式與規則庫維護經驗（規則爆炸） | 同上 §3 |
| 缺必要槽→問 | **TOD／Slot filling**：1990s 起標配（ATIS／DST／MultiWOZ／mixed-initiative） | **已有前作**——該檔原文「**此機制非本研究發明**」。定位句式：「缺槽即問的機制承自 TOD；本研究將其從封閉 schema 推廣至公式錨定之領域通用槽位」。**論文義務：TOD 必引，不引必死** | 同上 §4 |
| （對照組候選，該檔收藏） | **Ambig-SWE**（SWE-Bench 歧義變體：偵測／提問／利用三步）、**CLARITI**（reward-driven clarification）、**DiscoBench**（搜尋 agent 的 clarification-aware）、**information-gain clarifier**（ICML 2026）、**MIRA-Math**（typed atomic hints，與槽位理論神似） | **新前線（2025–2026）**，證明賽道活＋提供對照組 | 同上 §4。**注**：2026-10-07 本輪五組關鍵詞**一篇都沒命中**（詞偏 TOD／abstention／canonicalization，未打 benchmark 名稱），此列照 7/22 原檔填，非本輪找到 |
| 7/13 原主張「低信心→ASK 閘門為 CIDM 生態普遍缺席」 | — | **已自我窄化**：該檔明定「clarification 為活躍領域；缺席的是『**輸入規格化管線內建＋行為公式錨定＋缺槽觸發**』之組合格。對外表述一律用窄版」 | 同上 §「7/13 主張窄化」。**7/13 原檔未在倉內找到**，但其主張已被 7/22 原文引述並修正 |
| 總定位句（對外可用） | 各零件皆有成熟鄰居（control 之外部協定、abstention 之閾值理論、TOD 之缺槽即問、guardrails 之驗證工程） | **貢獻在組合與錨定**：公式驅動之領域通用規格化＋ASK，以小模型原子判斷實作，全程可審計 | 同上「總定位句」 |

---

## 附：待核清單（不編，等核）

| # | 待核項 | 狀態 |
| --- | --- | --- |
| 1 | McCoy et al., Embers of Autoregression 的 **PNAS 2024 卷期／DOI** | arXiv:2309.13638 已確認；期刊版未核到 |
| 2 | shortcut learning 的具體篇目 | 筆記只給領域名 |
| 3 | Dennett 的具體著作 | 筆記只給作者名 |
| 4 | Gazzaniga 的具體著作 | 筆記只給作者名 |
| 5 | arXiv:2506.18032 的 **Fig 12／13** | H1–H4 已核到；兩圖未核到 |
| 6 | 「40 資料集先例」的所指 | CC 讀為我方 40 句考卷，待更正 |
| 7 | DRIFTBENCH 的身分 | 認為是 arXiv:2604.28031（KBV 8–99% 相符、repo 名相符）；**另有同名近似論文 arXiv:2602.02455（主題不同）**，請覆核 |
| 8 | 2026-08-15 §六、2026-09-05 §三 原筆記 | 不在倉內，總表以令文摘述填入 |

bib 全文：`laios-bridge/reports/attachments/2026-10-06_文獻之旅/bib.txt`
