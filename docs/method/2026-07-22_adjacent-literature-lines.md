# 四條相鄰文獻線查證與定位修正(2026-07-22)

起因:外部 AI 主張「你的研究與這四條線差不多且他們更完整」。查證判決:
「更完整」成立(各自格子內),「差不多」不成立(組合格無人佔)。

## 逐線判決

### 1. AI Control(Redwood Research)
- 實況:威脅模型=蓄意破壞(intentional subversion)。red/blue team、
  後門、共謀、sandbagging、audit budget。ICML oral 2024 起,UK AISI
  ControlArena 等完整生態。
- 與本研究:哲學近親(外部協定/不信任模型內部/trusted-untrusted 分層/
  defer),問題不同(malice vs incapability+輸入劣化)。
- 可借:safety/usefulness tradeoff 數學、audit budget 概念(ASK 成本帳)、
  Factor(T,U) 之 factored cognition(原子分解的正式近親)、
  「結構化判準優於整體判斷」(TraceGuard,與原子化哲學同構,安全側獨立收斂)。
- 論文用法:motivation 引(外部化控制之安全論證)+related work 區隔威脅模型。

### 2. Selective prediction / Abstention / Conformal
- 實況:極成熟。Wen et al. 2025 survey、conformal abstention 具
  finite-sample 保證(participation + conditional correctness)、2026 仍活躍。
- 邊界:abstention 動作止於「不答/IDK/輸出集合」;ASK=棄權後的下一步
  (指出缺的槽+針對性提問),文獻中屬不同能力。
- 可借(重要):conformal calibration → row_confidence 閾值(現 0.85 任意
  鎖死)升級為有覆蓋率保證之校準閾值。OOD 站後執行。
- 論文用法:ASK 閘門的閾值理論工具+related work(棄權 vs 追問之區隔)。

### 3. Guardrails 系統(NeMo/Guardrails AI/Llama Guard)
- 實況:內容政策+格式驗證層。無 I/C 分離、無槽位完整性、無缺資訊追問。
- 可借:validator 工程模式(與 JSON 合約形似)、規則庫維護經驗(規則爆炸)。
- 論文用法:related work 一段,區隔「政策驗證 vs 輸入規格化+決策框架」。

### 4. TOD / Slot filling(最實的一條)
- 實況:「缺必要槽→問」為 1990s 起標配(ATIS/DST/MultiWOZ/
  mixed-initiative)。此機制非本研究發明。
- 差異:TOD=每領域手工封閉 schema;本研究=領域通用功能分解(I/C/R),
  公式錨定,開放領域,小模型原子判斷實作,可審計紀律。
- 新前線(2025-2026,證明賽道活+提供對照組):Ambig-SWE(SWE-Bench
  歧義變體,偵測/提問/利用三步)、CLARITI(reward-driven clarification)、
  DiscoBench(搜尋 agent 的 clarification-aware)、information-gain clarifier
  (ICML 2026)、MIRA-Math(typed atomic hints——與槽位理論神似,收藏)。
- 論文義務:**TOD 必引,不引必死**。定位句式:「缺槽即問的機制承自 TOD;
  本研究將其從封閉 schema 推廣至公式錨定之領域通用槽位」。

## 7/13 主張窄化(自我校準)

原句「低信心→ASK 閘門為 CIDM 生態普遍缺席」易被誤讀為「無人做 clarification」。
修正版:**clarification 為活躍領域;缺席的是「輸入規格化管線內建+
行為公式錨定+缺槽觸發」之組合格。** 對外表述一律用窄版。

## 總定位句(對外可用)

各零件皆有成熟鄰居(control 之外部協定、abstention 之閾值理論、
TOD 之缺槽即問、guardrails 之驗證工程);貢獻在組合與錨定:
公式驅動之領域通用規格化+ASK,以小模型原子判斷實作,全程可審計。

## 行動清單

1. related work 四段,按上列判決寫,TOD 為首要
2. conformal 校準入 OOD 後待辦(閾值升級)
3. AI Control 的 audit budget/tradeoff 框架讀後評估借用
4. 新前線五篇入文獻資料夾,Ambig-SWE 可為未來對照 benchmark 候選
5. 對外主張一律用窄版組合格表述
