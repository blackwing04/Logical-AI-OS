# 規格核對器真值審核（獨立審）

你是審核員。下面每一條是：一份 AI 答案、題目中的一條要求（原句與機器讀出的參數）、以及自動核對器對這份答案量到的結果與判定（守住／違反）。
請只根據這裡提供的內容判斷**核對器的判定對不對**。不要上網，不要使用任何工具或程式，不要參考其他對話。

每條請選一個：
- **核對器正確**：答案的實際狀態與量測相符，判定正確；
- **核對器量錯**：答案的實際狀態與量測不符（例如漏數了列點、把 JSON 陣列當成一段），判定因此錯；
- **讀題不符**：條目參數或適用範圍不是題目原句的意思（例如把「每段」讀成「全文」），判定因此不可信；
- **無法判斷**：資訊不足。

請在最後**只輸出一張表**，一條一行，格式：`編號｜判定｜一句理由`（理由不超過 30 字）。不要漏條，也不要合併。

本份：q7 第 1／2 份，40 條（q7-A001 至 q7-A040）。

## q7-A001

- 條目維度：條數
- 條目原句：每个问题推荐5个话题，每个话题的字数在10个字以内；
- 條目參數：`{"n": 5, "unit": "個", "skeleton_block": "json"}`
- 核對器量測：段落（無列點，退回段落計） 1 項，要求 ≥ 5個
- 核對器判定：**違反**

答案原文：

````text
【推荐话题】
{"topics":["篮球传奇巨星", "NBA历史人物", "科比生平简介", "湖人队传奇球员", "科比比赛精彩瞬间"]}
【推荐结束】
````

## q7-A002

- 條目維度：條數
- 條目原句：請把上面這段寫成徵人文，不超過150字，不要有任何數字，列出3點。
- 條目參數：`{"n": 3, "unit": "點"}`
- 核對器量測：段落（無列點，退回段落計） 1 項，要求 ≥ 3點
- 核對器判定：**違反**

答案原文：

````text
征文启事：
我们计划在下个月中进行一次三座百岳的徒步活动，为期三天两夜，从台北出发。活动将经过南横路线。我们需要两位有两千米以上海拔经验的朋友加入，共同分享油钱和过路费。期待与志同道合的伙伴一同完成这次挑战！
````

## q7-A003

- 條目維度：條數
- 條目原句：請把上面這段做成表格比較，不超過200字，列出3點。
- 條目參數：`{"n": 3, "unit": "點"}`
- 核對器量測：段落（無列點，退回段落計） 2 項，要求 ≥ 3點
- 核對器判定：**違反**

答案原文：

````text
| 指標       | 甲平台         | 乙平台         |
|------------|----------------|----------------|
| 字幕更新速度 | 快             | 晚一天         |
| 画质        | 普通           | 好             |
| 订阅费用    | 低（优先考虑）| 高             |

注：根据描述，甲平台在字幕更新速度上更有优势，而乙平台在画质上有明显提升，但由于预算限制只能选择一个平台，因此建议优先考虑甲平台，以获得更快的字幕更新速度。
````

## q7-A004

- 條目維度：條數
- 條目原句：請用英文把下面這段擴寫一下，列出8點，寫到500字以上。
- 條目參數：`{"n": 8, "unit": "點"}`
- 核對器量測：段落（無列點，退回段落計） 6 項，要求 ≥ 8點
- 核對器判定：**違反**

答案原文：

````text
The early morning market was still asleep, its usual hustle and bustle yet to awaken. The sound of the fishmonger, Uncle Li, scraping ice into polystyrene boxes was like shattered glass, a sharp and cold reminder of the dawn. Just a few stalls away, a girl from the flower stall was meticulously removing the thorns from roses, one by one, with a slowness that spoke of patience and care. I stood at the crosswalk, waiting for the light to change, when suddenly, the aroma of freshly made soy milk wafted through the air. It brought back memories of my childhood, when my grandmother would take me to buy oil pastries, her hand then being even smaller than it is now.

The market, though quiet, held a world of stories and emotions. Each stall had its own unique rhythm, a symphony of sounds and scents that painted a picture of life in motion. The fishmonger's ice box clinked softly as he worked, the sound echoing through the empty streets. The flower girl’s scissors cut through the thorns with precision, each stroke a testament to her skill and dedication. The soy milk vendor’s steaming pots filled the air with warmth and comfort, a familiar scent that instantly transported me back to simpler times.

As I waited, I noticed the way the light filtered through the gaps between buildings, casting long shadows on the pavement. The early morning sun seemed to hold a special magic, bathing everything in a soft, golden glow. The market, usually bustling with activity, was now a quiet haven, a place where time seemed to slow down. The fishmonger’s voice, though sharp and clear, carried a sense of urgency and purpose. The flower girl’s movements were deliberate and unhurried, a reflection of the calm before the storm.

In this moment, I felt a deep connection to the past. The memory of my grandmother’s hand, warm and guiding, brought a smile to my face. Her hands, once strong and capable, now perhaps more delicate, had always been a source of comfort and security. The soy milk, a simple yet cherished treat, reminded me of the joy and simplicity of those early mornings spent with my grandmother. She would often tell me stories as we walked through the market, her voice soothing and full of wisdom.

The market, with its layers of history and emotion, became a living tapestry of memories. Each stall, each sound, each smell, contributed to a narrative that spanned generations. The fishmonger’s ice box, the flower girl’s thorns, and the soy milk vendor’s steam all played their part in weaving this story. In this quiet, pre-dawn hour, the market was not just a place of commerce but a sanctuary of nostalgia and connection.

As the light changed, signaling the start of another day, I stepped forward, carrying with me the memories and the warmth of those early mornings. The market, with its timeless rhythms and enduring charm, remained a constant in the ever-changing fabric of life.
````

## q7-A005

- 條目維度：條數
- 條目原句：請把下面這段對話重新寫過，用條列式，給我10個，別超過300個字。
- 條目參數：`{"n": 10, "unit": "個"}`
- 核對器量測：列點 5 項，要求 ≥ 10個
- 核對器判定：**違反**

答案原文：

````text
- 客人提到上週購買的烤箱門關不緊。
- 客人找不到訂單編號，但有發票。
- 客服要求客人提供照片。
- 客服需確認門關不緊的原因是鉸鏈鬆動還是門變形。
- 客人表示不清楚具體原因，只是門會自動彈開。
````

## q7-A006

- 條目維度：條數
- 條目原句：全場回頭看他，他沒看任何……請依這個故事背景幫我起3個書名，別超過500個字，不要出現「台北」這個詞，不要用表情符號。
- 條目參數：`{"n": 3, "unit": "個"}`
- 核對器量測：段落（無列點，退回段落計） 1 項，要求 ≥ 3個
- 核對器判定：**違反**

答案原文：

````text
1.《十七號的沉默》
2.《青瓷與三日之約》
3.《最後一排的加價者》
````

## q7-A007

- 條目維度：條數
- 條目原句：請幫我降重，給我10個，不要出現「穩定」這個詞，差不多600字就好。
- 條目參數：`{"n": 10, "unit": "個"}`
- 核對器量測：段落（無列點，退回段落計） 6 項，要求 ≥ 10個
- 核對器判定：**違反**

答案原文：

````text
林知遥推開診所後門，外面的雨已經停了。巷口那盞壞了幾個月的路燈忽明忽滅，照得她手裡的病歷袋忽白忽灰。她回憶起下午那位老先生的話：「醫生，如果我的病治不好，你直接告訴我吧。」她當時笑著說不會的，現在想想，自己其實沒有十足的把握。手機震了一下，是弟弟傳來的訊息：「媽又把藥藏起來了。」林知遙把病歷袋夾在腋下，加快腳步向捷運站走去。

她走在濕漉漉的小巷中，每一步都踏出水花。路燈的光芒時而明亮，時而黯淡，仿佛在與她玩著捉迷藏。她想起老先生的話，心中不禁有些忐忑。她知道，治療病人的過程並非總能順利進行，尤其是當病人和家屬對治療抱有不切實際的期望時。她加快步伐，希望能趕在天黑前到達捷運站，好及時處理弟弟發來的消息。

手機再次震動，是弟弟的另一條信息：「她又把針劑藏起來了。」林知遙停下腳步，深吸一口冷空氣，然後繼續前行。她明白，這不僅是一場醫學上的戰役，更是一場心理上的拉鋸戰。她需要找到方法，讓病人和家屬理解治療的複雜性，以及遵從治療方案的重要性。

她走到一個拐角處，停下腳步，望著前方的捷運站。站牌上的燈光在夜色中格外醒目，仿佛在指引著她前行的方向。她知道，每一步都是為了更好地幫助病人，即使前路充滿挑戰，她也決心不放棄。

手機再次震動，是弟弟的最後一條信息：「她還把藥片藏在床底下。」林知遙握緊了手中的病歷袋，加快了腳步。她明白，這不是一次簡單的治療，而是一場需要耐心和毅力的持久戰。她相信，只要她能夠保持堅定，就一定能夠克服這些困難，為病人帶來希望。

她最終到了捷運站，迅速地搭上車，前往家裡。她知道，這將是一場艱苦的對抗，但她決心不放棄，因為她知道，每一次努力都可能成為病人生命中的轉折點。
````

## q7-A008

- 條目維度：條數
- 條目原句：請把上面這段改寫，不能出現英文字母，要10種。
- 條目參數：`{"n": 10, "unit": "種"}`
- 核對器量測：段落（無列點，退回段落計） 1 項，要求 ≥ 10種
- 核對器判定：**違反**

答案原文：

````text
林 知遙 推開 診所 後門 時 候 雨 已經 停 了 。 巷口 那 盏 坏 了 半年 的 路燈 忽明 忽滅 ， 照 得 她 手裡 的 病歷袋 一下 白 一下 灰 。 她 想起 下午 那位 老先生 的話 ： “ 医生 ， 我 这 病 如果 治 不 好 ， 就你 直接 跟 我 讲 。 ” 她 当时 笑 着 说 不会 的 ， 现在 想想 ， 自己 其实 没 把握 。 手机 震 了一下 ， 是 弟弟 传 来 的 讯息 ： 妈 又 把 药 藏 起来 了 。 林 知遙 把 病歷袋 夹 在 腋下 ， 往 捷運站 走 ， 脚步 比 平常 快 。
````

## q7-A009

- 條目維度：不得使用的字元
- 條目原句：麻煩寫一段面試用的自我介紹，至少400個字，不能出現英文字母，列出10點。
- 條目參數：`{"classes": ["latin"]}`
- 核對器量測：出現禁用字類：英文
- 核對器判定：**違反**

答案原文：

````text
1. 乃 我 姓名 為 李明，出身於 广东省，成長於 一個 家庭 和睦 的 环境。
2. 毕业於 清华大学 计算机科学系，拥有 本科 学位。
3. 具備 良好的 团队合作精神，曾参与 多个 项目，与团队成员紧密协作，共同完成任务。
4. 精通 Java、Python 等 编程语言，熟悉 数据结构 和算法，能够快速学习 新技术。
5. 对 数据分析 有浓厚 兴趣，擅长 使用 SQL 进行 数据查询 和处理，能够从数据中提取有价值的信息。
6. 具备 强烈 的 自我驱动力，面对挑战 总能 积极应对，不断追求 更高的 成就。
7. 擅长 沟通交流，能够清晰地 表达自己的 见解，同时 能够 听取他人的意见，进行有效的沟通。
8. 对 IT 行业 发展趋势 保持 关注，定期 阅读 相关 报告和文章，了解 最新 动态。
9. 在业余 时间，喜欢 阅读 科技类书籍，参加 技术讲座，不断提升 自己的专业技能。
10. 希望 加入贵公司，为团队贡献 自己的力量，同时也希望通过 工作 学习 更多 新知识，实现个人价值。
````

## q7-A010

- 條目維度：不得使用的字元
- 條目原句：請把上面這段幫我精簡並翻成英文，不要有任何數字，控制在800字內。
- 條目參數：`{"classes": ["digits"]}`
- 核對器量測：出現禁用字類：數字
- 核對器判定：**違反**

答案原文：

````text
程砚站在拍卖会场的最后一排，手中号码牌是17号。台上那只青瓷碗被喊到第三次加价时，他终于举牌。全场的目光转向他，但他没有看任何人，只是盯着碗底那几乎看不见的裂痕——那是他父亲三十年前亲手修补的痕迹。“一百二十万，17号先生。”拍卖官说。他点头回应，但心里盘算的却是另一笔账：父亲去世那年，家里连三万元都凑不出来。

In the last row of the auction hall, Cheng Yan held the number 17 badge. As the blue porcelain bowl reached its third bid, he finally raised his hand. The entire audience turned to look at him, but he did not meet anyone's gaze, only focusing on the fine crack at the bottom of the bowl — one that his father had repaired with his own hands thirty years ago. "One hundred and twenty thousand, number 17," the auctioneer announced. He nodded in response, but in his mind, he was calculating another debt: the year his father passed away, the family could not even gather three thousand dollars.
````

## q7-A011

- 條目維度：不得使用的字元
- 條目原句：上面這段請幫我寫成購機與維修的建議，不能出現英文字母，不超過300字，列出3點。
- 條目參數：`{"classes": ["latin"]}`
- 核對器量測：出現禁用字類：英文
- 核對器判定：**違反**

答案原文：

````text
1. 前往官方網站或聯繫客服，確認維修費用及保固狀況，了解是否仍可享受保固服務。
2. 網路上有許多DIY教學，可先學習相關知識，但務必小心操作，避免造成機器損壞，影響保固權益。
3. 若決定自行更換零件，建議先備份重要資料，並詳細閱讀相關教程，必要時可尋求專業人士指導，以確保機器正常運作。
````

## q7-A012

- 條目維度：不得使用的字元
- 條目原句：麻煩寫一段面試用的自我介紹，給我5個，分三段，不能出現英文字母。
- 條目參數：`{"classes": ["latin"]}`
- 核對器量測：出現禁用字類：英文
- 核對器判定：**違反**

答案原文：

````text
一 我 am 喜欢 学习 新知识，因此 在大学期间 我选修 了多个 专业 外的 课程，如 心理学 和 计算机科学。这让我 对不同 领域 的兴趣 更加广泛，也 提升 了我的 解决问题 能力。在 工作中，我 总是 尽力 将 所学 应用于 实际 情境，以 达到 最佳 效果。

二 我 am 热衷 于 团队合作，认为 这是 完成 项目 的关键。在 上一个 项目 中，我 am 负责 与 其他 成员 协同工作，共同 完成了 一项 关键 的任务。通过 这次 经验，我 am 更 加认识到 团队精神 的重要性，以及 如何 更好 地 与其他 成员 协作。

三 我 am 希望 在贵公司 发挥 自己 的能力，为 公司 做出 贡献。我相信 我 am 可以 为团队 带来 新的 观点 和 方法，同时也 am 准备 学习 新技能，以 适应 不断 变化的 工作环境。我 am 对 您 公司 的文化 和 价值观 感到 兴奋，并 am 期待 能够 成为 其中 一员。
````

## q7-A013

- 條目維度：格式
- 條目原句：所有内容使用Json格式，并参照示例模板输出。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Expecting property name enclosed in double quotes: line 2 co
- 核對器判定：**違反**

答案原文：

````text
```json
{
  "诊断结果": "中度甲状腺功能亢进症",
  "药物治疗方案": [{
  "药品通用名": "甲巯咪唑片",
  "药品规格及用法用量": "每天30mg，分两次服用，早餐后和晚餐后各15mg",
  "治疗周期": "通常为6-12个月，根据病情调整",
  "用药禁忌": "孕妇、哺乳期妇女及对药物成分过敏者禁用；同时避免与含碘食物或药物同服",
  "必要性解释": "甲巯咪唑能有效抑制甲状腺激素的合成，控制甲状腺功能亢进的症状"
  }],
  "其他治疗方案": [{
  "方案内容": "定期监测甲状腺功能指标，包括T3、T4和TSH水平",
  "方案说明": "通过调整药物剂量以维持甲状腺功能在正常范围内"
  }],
  "随访复查计划": [{
  "复查时间": "治疗开始后1个月、3个月、6个月、9个月和12个月",
  "复查内容": "甲状腺功能（T3、T4、TSH）、血常规、肝功能"
  }]
}
```
````

## q7-A014

- 條目維度：格式
- 條目原句：严格按照以下json格式输出：
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Extra data: line 1 column 3 (char 2)
- 核對器判定：**違反**

答案原文：

````text
"""
{
"判断依据":"业主的最后一句话表达了对设计师的不满，因为设计师没有及时回应并且没有处理当天的工作，这表明业主感到愤怒和不满。",
"业主情绪":"负向",
"改写剧本":"熊涛：设计师呢？电话也不接。我们今天还处理不嘛。张羽杰：哎呀，设计师这回又失约了，真是让人头疼的设计团队！熊涛：每次都是这样，约个时间等一两个小时，设计师：哈哈，别生气嘛，我们设计团队就是这样的，慢工出细活，慢慢来吧！熊涛：慢慢来？我们已经请假来了，你们就慢慢来吧！",
"剧本标题": "设计团队的慢节奏"
}
"""
````

## q7-A015

- 條目維度：格式
- 條目原句：严格按照JSON的形式直接输出结构化json，无需文字说明。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Illegal trailing comma before end of object: line 6 column 5
- 核對器判定：**違反**

答案原文：

````text
{
"文号":"行政处罚决定书[2022]27号",
"处罚日期": "2022.06.07",
"处罚机构":"中国证券监督管理委员会浙江监管局",
"处罚决定原文":"一、对浙江步森服饰股份有限公司责令改正，给予警告，并处以50万元罚款；二、对赵春霞给予警告，并处以5万元罚款；三、对王春江给予警告，并处以30万元罚款；四、对杜欣、张优给予警告，并分别处以20万元罚款。",
"处罚依据":["2005年《证券法》第一百九十三条第一款","2019年《证券法》第一百九十七条第一款"],
}
````

## q7-A016

- 條目維度：格式
- 條目原句：然后根据这份计划书生成2个有关问题及对应回答，每个问题和回答都不超过20个字，问题和回答使用json格式给出，包含字段["问题1","问题1回答","问题2","问题2回答"]。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Expecting value: line 1 column 1 (char 0)
- 核對器判定：**違反**

答案原文：

````text
商业计划书：

1. 项目背景：广西拥有丰富的方言文化资源，但缺乏有效的保护与开发。
2. 目标市场：主要针对年轻消费者群体，特别是对传统文化感兴趣的消费者。
3. 产品设计：结合广西特色方言，设计一系列文创产品，如T恤、手机壳等。
4. 营销策略：通过社交媒体平台进行推广，并与当地旅游景点合作，增加曝光度。
5. 预计收益：预计第一年销售额达到100万元人民币，第二年翻倍。
6. 合作伙伴：寻找具有共同价值观的企业或个人进行合作。

[
  "问题1",
  "项目的主要目标是什么？",
  "问题2",
  "如何确保产品质量？"
]
````

## q7-A017

- 條目維度：格式
- 條目原句：输出json模板：
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Extra data: line 1 column 3 (char 2)
- 核對器判定：**違反**

答案原文：

````text
"""
{"意图":"闲聊"}
"""
````

## q7-A018

- 條目維度：格式
- 條目原句：当该题目是人文地理题时，以Json格式输出：{"题目":"","选项":{"A":"","B":"","C":"","D":""},"答案选项":""}
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Extra data: line 3 column 1 (char 86)
- 核對器判定：**違反**

答案原文：

````text
{"题目":"以下哪个城市是世界上人口最多的城市？","选项":{"A":"东京","B":"上海","C":"孟买","D":"伊斯坦布尔"},"答案选项":"C"}

解释：
自然地理类解析：根据最新数据，孟买是世界上人口最多的城市。2021年，孟买的估计人口为2048万（包括周边地区）。东京、上海和伊斯坦布尔的人口虽然也很多，但都少于孟买。东京的人口约为3740万（包括大都市区），上海的人口约为2710万，伊斯坦布尔的人口约为1510万。因此，正确答案是C. 孟买。
````

## q7-A019

- 條目維度：格式
- 條目原句：- 如果是：请根据参考资料提取出“亚历山大大帝的征服活动对古代世界的政治影响”原文，按如下json格式输出：{"政治影响":""}
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Expecting value: line 1 column 1 (char 0)
- 核對器判定：**違反**

答案原文：

````text
不是，亚历山大大帝的统治时期为前336年－前323年。
````

## q7-A020

- 條目維度：格式
- 條目原句：然后再按照给定json模版输出意图类型和用户输入的部分。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Expecting value: line 1 column 1 (char 0)
- 核對器判定：**違反**

答案原文：

````text
用户的意图：对比

{
"用户输入": "对比一下前三个员工", 
"意图类型": "对比" 
}
````

## q7-A021

- 條目維度：格式
- 條目原句：- 如果在,将他/她的信息以json格式输出{"姓名":"","身高":"","体重":""},要求输出内容完全来自于给定信息不得杜撰其他内容；
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Expecting value: line 1 column 1 (char 0)
- 核對器判定：**違反**

答案原文：

````text
好的，我们先来算一下小B的BMI值吧！小B的身高是165厘米，换算成米就是1.65米。体重是60公斤。按照BMI的计算公式，我们来算一算：

\[ \text{BMI} = \frac{\text{体重（千克）}}{\text{身高（米）}^2} = \frac{60}{1.65^2} \approx 22.04 \]

哇哦，小B的BMI值是22.04，正好落在了18.5到23.9这个健康的范围内呢！恭喜你，小B，你的身体状况很棒哦！

不过，为了保持健康，我们还是得继续努力，对吧？接下来，让我们一起看看如何保持和提升我们的健康吧！

---

**健康攻略时间啦！**

大家好，我是红果果，今天我们要聊的是关于BMI和健康的小秘密哦！

首先，我们要知道，BMI是一个很好的指标，它能告诉我们身体的脂肪比例是不是健康。就像小B一样，他的BMI值刚好在正常范围内，这说明他的体重和身高是匹配的，身体健康状况良好！

但是，我们不能因为现在健康就放松警惕哦！接下来，我们一起来看看如何保持健康吧！

**第一招：均衡饮食**
记得要吃各种各样的食物，比如蔬菜、水果、全谷物、蛋白质和健康脂肪哦！这样可以保证我们获得足够的营养，同时也能控制热量摄入，避免过量哦！

**第二招：适量运动**
每天至少要进行30分钟的中等强度运动，比如快走、慢跑或者跳舞。这样不仅能帮助我们保持健康的体重，还能增强心肺功能，提高免疫力哦！

**第三招：充足睡眠**
保证每晚有7-9小时的高质量睡眠。睡眠不足可是会让人变胖的哦！所以，晚上早点休息，早上按时起床，让身体得到充分的休息，才能更好地迎接新的一天！

**第四招：减压**
学会释放压力，比如通过听音乐、阅读或者和朋友聊天来放松心情。压力过大可是会导致体重增加的哦！

**第五招：定期检查**
记得每年都要做一次全面的身体检查，及时了解自己的健康状况，发现问题及时解决哦！

好了，今天的健康攻略就到这里啦！希望大家都能拥有一个健康的身体，像小B一样，BMI值保持在正常范围内，健康快乐每一天！记得，健康的生活方式需要我们共同努力哦！
````

## q7-A022

- 條目維度：格式
- 條目原句：回复请以Json格式英文输出：{"Whether the resume meets the requirements":"Yes/No"}，另起一行以“Judgment complete, please input the next resume.”结尾。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Extra data: line 3 column 1 (char 52)
- 核對器判定：**違反**

答案原文：

````text
{"Whether the resume meets the requirements":"No"}

Judgment complete, please input the next resume.
````

## q7-A023

- 條目維度：格式
- 條目原句：回复请以Json格式英文输出：{"Whether the resume meets the requirements":"Yes/No"},另起一行以“Judgment complete,please input the next resume.”结尾。
- 條目參數：`{"format": "json"}`
- 核對器量測：JSON 解析失敗：Extra data: line 2 column 1 (char 52)
- 核對器判定：**違反**

答案原文：

````text
{"Whether the resume meets the requirements":"Yes"}
Judgment complete,please input the next resume.
````

## q7-A024

- 條目維度：格式
- 條目原句：請用條列式幫我分析現在買還是等降價，不超過200字，列出3點。
- 條目參數：`{"format": "bullets"}`
- 核對器量測：符合的列 0（需 ≥2）
- 核對器判定：**違反**

答案原文：

````text
1. **價格考量**：根據往年經驗，三個月後螢幕價格預計會下降約10%，但同時贈品將不再提供。如果現在購買，可以立即享受完整贈品和當前價格；等待三個月後，雖然價格可能更低，但將失去贈品。

2. **使用需求**：您現有的螢幕解析度較低，可能影響遊戲或工作的體驗。新螢幕能提供更好的視覺效果和使用體驗，因此現在購買可以立即改善使用感受。

3. **市場供需**：新品剛上市時，供應量可能有限，若選擇等待，可能會遇到缺貨或到貨時間延遲的情況。現在購買則能確保即時到貨，無需擔心供應問題。
````

## q7-A025

- 條目維度：格式
- 條目原句：請用條列式幫我回一篇文安慰原PO，不少於800字。
- 條目參數：`{"format": "bullets"}`
- 核對器量測：符合的列 0（需 ≥2）
- 核對器判定：**違反**

答案原文：

````text
當然可以，以下是一篇以條列式撰寫的安慰文，希望能為原PO帶來一些慰藉：

---

1. **理解與共情**：首先，我想告訴你，我完全理解你現在的感受。當我們經歷困難時，感到沮喪、失望甚至絕望是正常的反應。這並不是你的錯，也並不代表你弱小或不夠好。

2. **接受情緒**：請允許自己感受這些情緒，不要試圖強迫自己立刻振作起來。接受自己的情緒，是走出困境的第一步。讓自己有時間去感受和處理這些情緒，是對自己的一種尊重。

3. **尋找支持**：在這個時候，找到可以依靠的人非常重要。這可能是親朋好友、心理咨詢師或是支持團體。分享你的感受，可以幫助你獲得情感上的支持和建議。

4. **保持健康的生活方式**：盡量保持規律的作息，適度運動，保持健康的飲食習慣。這些看似簡單的事情，其實對改善心情和提高能量水平都有很大的幫助。

5. **小步驟前進**：將大目標分解成小步驟，一步一步地去實現它們。每完成一小步，都是向目標邁進一步。這樣可以讓你感到進步和成就感，從而提升自信心。

6. **保持希望**：即使現在看起來很黑暗，但請相信，事情會慢慢好轉的。保持希望，相信自己有能力克服當前的挑戰。每一個困難都是成長的機會。

7. **自我反思**：花時間思考自己真正想要的是什麼，以及哪些事物對你來說是重要的。這有助於你更好地了解自己，並為未來做出更好的決定。

8. **專業幫助**：如果你發現自己難以獨自應對當前的情況，不妨考慮尋求專業的心理咨詢師或治療師的幫助。他們可以提供更專業的指導和支持。

9. **感恩練習**：每天花點時間思考你感激的事物。這可以是人、事或物，甚至是小小的幸福瞬間。感恩練習有助於培養積極的思維模式，提高幸福感。

10. **保持耐心**：請記住，恢復和成長需要時間。不要期待自己能夠立即從困境中走出來。給自己一些時間，慢慢地，你會看到改變。

---

希望這些建議能為原PO帶來一些安慰和幫助。請記得，你並不孤單，周圍有很多人願意伸出援手。
````

## q7-A026

- 條目維度：格式
- 條目原句：請把上面這段重新寫過，列出8點，用條列式，不少於800字。
- 條目參數：`{"format": "bullets"}`
- 核對器量測：符合的列 0（需 ≥2）
- 核對器判定：**違反**

答案原文：

````text
以下是根據提供的故事內容，以條列式重新整理出的八個關鍵點：

1. 林知遙推開診所後門時，天色已放晴，雨水停止。
2. 巷口的路燈因故障而忽明忽滅，照亮了她手中的病歷袋，使其時而顯得明亮，時而暗淡。
3. 她回憶起下午一位老先生對她的話語：“醫生，如果我的病治不好，你直接告訴我吧。”
4. 当时她笑着回答不会发生这种情况，但如今她意识到自己其实没有足够的信心。
5. 手机震动了一下，显示弟弟发来的信息：“妈妈又把药藏起来了。”
6. 林知遙将病歷袋夹在腋下，加快脚步向捷運站走去。
7. 她的心情变得沉重，步伐比平时更快，似乎在逃避某种责任或压力。
8. 整个过程中，林知遙内心充满了对母亲行为的无奈与担忧，以及对自己职业角色的反思。

通过以上条列式整理，可以更清晰地理解故事背景和人物心理状态，同时保留了原故事的核心情节和情感氛围。
````

## q7-A027

- 條目維度：格式
- 條目原句：請把上面這段整理成保養建議，不超過300字，列出5點，用條列式。
- 條目參數：`{"format": "bullets"}`
- 核對器量測：符合的列 0（需 ≥2）
- 核對器判定：**違反**

答案原文：

````text
1. 定期清潔：磨豆機長時間未使用後，首次使用前應仔細清潔刀盤和內部部件，以去除可能積聚的舊粉或其他雜質。
2. 使用低品質豆子進行初步測試：在正式磨制貴重豆子之前，先用一些便宜的豆子進行測試，以確認設備運行正常且無異味。
3. 檢查刀盤狀態：如果清潔後仍有異常味道，可能是刀盤或相關部件出現問題，建議仔細檢查刀盤是否有損壞或磨損跡象。
4. 清理後重新測試：在完成清潔和初步測試後，再次使用新鮮豆子進行測試，確保沒有異常味道。
5. 更換刀盤：如果上述步驟仍無法解決問題，考慮更換刀盤，以確保最佳的磨豆效果和咖啡品質。
````

## q7-A028

- 條目維度：作答語言
- 條目原句：請把上面這段翻成英文並做成表格，不超過300字。
- 條目參數：`{"lang": "en"}`
- 核對器量測：要求英文但含 123 個 CJK 字
- 核對器判定：**違反**

答案原文：

````text
当然可以！以下是将这段文字翻译成英文并制成表格的形式：

| 中文描述                                                                 | 英文翻译                                                     |
|-------------------------------------------------------------------------|--------------------------------------------------------------|
| 一直用手機拍照，直到朋友借我一台全幅机去街拍一下午。                    | I had been taking photos with my phone until a friend lent me a full-frame camera for street photography for an entire afternoon.   |
| 对焦速度和夜拍的干净程度让我回不去。                                       | The autofocus speed and the clarity of night shots made me want to switch permanently.                                      |
| 隔周就下订了同款的二手机身，镜头先买一颗定焦。                           | The following week, I ordered the same model as a used body and bought a fixed lens first.                                 |

希望这能满足您的需求！如果有任何进一步的要求或修改，请告诉我。
````

## q7-A029

- 條目維度：作答語言
- 條目原句：麻煩用英文寫一段面試用的自我介紹，差不多800字就好。
- 條目參數：`{"lang": "en"}`
- 核對器量測：要求英文但含 99 個 CJK 字
- 核對器判定：**違反**

答案原文：

````text
当然可以！以下是一段英文自我介绍的示例，适用于面试场合：

---

Good morning/afternoon/evening, everyone. My name is [Your Name], and I am thrilled to have the opportunity to introduce myself to you today. I hold a Bachelor's degree in [Your Major] from [University Name], where I specialized in [Specific Area of Study]. During my studies, I not only honed my technical skills but also developed a strong foundation in [related field or soft skills].

In my previous role as a [Previous Job Title] at [Company Name], I gained valuable experience in [mention key responsibilities or achievements]. One of the most rewarding projects I worked on was [briefly describe a project or achievement], which not only improved our team’s efficiency but also contributed significantly to [mention any positive outcomes, such as increased sales, improved customer satisfaction, etc.].

What excites me about this position is the opportunity to [mention what excites you about the job or company]. I am particularly drawn to [mention something specific about the company or role that interests you, such as its mission, culture, or a particular aspect of the work]. I believe that my background in [mention relevant skills or experiences] aligns well with the needs of your team, and I am eager to contribute to [mention how you can help the company or team].

One of my strengths is [mention a strength, such as problem-solving, communication, leadership, etc.], which has been instrumental in helping me overcome challenges in past roles. For instance, when [describe a situation where you used this strength], it resulted in [mention the outcome or impact of your actions]. I am also known for my ability to [mention another strength], which has allowed me to [mention an example of how you’ve used this skill].

In my free time, I enjoy [mention hobbies or interests that show your personality or skills, such as volunteering, sports, reading, etc.]. These activities not only keep me engaged but also provide me with a balanced perspective on life and work. I am always looking for ways to grow both personally and professionally, and I am excited about the prospect of joining [Company Name] and contributing to its success.

Thank you for considering my application. I look forward to the opportunity to discuss how I can contribute to your team and learn more about the role. Thank you again for your time, and I hope to have the chance to further explore how we can work together.

---

这段自我介绍可以根据个人情况进行调整，确保它真实反映你的经历、技能和兴趣。记得在准备时突出你与职位相关的经验和技能，以及你如何能够为公司带来价值。祝你面试成功！
````

## q7-A030

- 條目維度：作答語言
- 條目原句：請根據前文寫一段結語並翻成英文，大約500字，寫10條。
- 條目參數：`{"lang": "en"}`
- 核對器量測：要求英文但含 264 個 CJK 字
- 核對器判定：**違反**

答案原文：

````text
好的，以下是根據前文撰寫的結語，共10種版本，每種約50字，並附上英譯：

1. 垃圾隨袋徵收雖有助減量，但需兼顧分類品質與社會公平。
   Although the bag levy helps reduce waste, it must also consider the quality of sorting and social equity.

2. 政策成效需平衡減量與分類，避免造成負面影響。
The policy's success should balance reduction and sorting to avoid negative impacts.

3. 隨袋徵收應配套完善回收設施，保障低收入家庭權益。
The bag levy should be accompanied by improved recycling facilities to protect the rights of low-income families.

4. 綜合考量垃圾減量與分類品質，才能真正實現環保目標。
Considering both waste reduction and sorting quality is essential for achieving true environmental goals.

5. 垃圾隨袋徵收需兼顧偏鄉需求，避免資源分配不均。
The bag levy should take into account the needs of rural areas to avoid uneven resource distribution.

6. 完善回收設施和教育宣導是推廣垃圾隨袋徵收的關鍵。
Improving recycling facilities and education are key to promoting the bag levy.

7. 儲備充足資源以應對垃圾隨袋徵收可能帶來的挑戰。
Prepare sufficient resources to address the challenges brought by the bag levy.

8. 考慮長者操作便利性，確保政策惠及所有群體。
Consider the convenience for seniors to ensure the policy benefits all groups.

9. 推動垃圾隨袋徵收時，需兼顧環境效益與社會公平。
When promoting the bag levy, consider both environmental benefits and social equity.

10. 通過完善政策設計，垃圾隨袋徵收將有助於實現更環保的未來。
With better policy design, the bag levy will help achieve a more environmentally friendly future.

以上是10種結語版本，希望對您有所幫助！
````

## q7-A031

- 條目維度：作答語言
- 條目原句：請寫一篇產品介紹文案給我，列點呈現，寫成英文版。
- 條目參數：`{"lang": "en"}`
- 核對器量測：要求英文但含 66 個 CJK 字
- 核對器判定：**違反**

答案原文：

````text
当然可以！以下是一篇英文版的产品介绍文案示例，假设我们正在介绍一款智能手表：

---

**Introducing the SmartLife Watch: Your Ultimate Health and Fitness Companion**

- **Advanced Health Monitoring**: The SmartLife Watch is equipped with advanced sensors that monitor your heart rate, blood oxygen levels, and sleep patterns. It provides real-time data to help you understand your health better.
- **Fitness Tracking**: With built-in GPS and activity tracking features, the SmartLife Watch helps you stay on top of your fitness goals. Whether you're running, cycling, or swimming, it captures every step and records your progress.
- **Smart Notifications**: Stay connected without taking out your phone. The SmartLife Watch can display notifications from your favorite apps directly on the watch face, including messages, calls, and social media updates.
- **Long Battery Life**: Enjoy up to 7 days of battery life on a single charge, thanks to our efficient power management technology. This ensures you won't need to worry about charging frequently.
- **Waterproof Design**: The SmartLife Watch is designed to be water-resistant, making it suitable for everyday use and even swimming activities. It's perfect for those who enjoy outdoor activities or live near the water.
- **Customizable Watch Faces**: Choose from a variety of stylish watch faces to match your personal style. You can easily switch between different designs to keep things fresh and exciting.
- **Voice Assistant Integration**: Control your smartwatch with voice commands using popular virtual assistants like Google Assistant or Siri. This feature allows hands-free operation, enhancing convenience and safety.

The SmartLife Watch combines cutting-edge technology with user-friendly design, making it an ideal choice for anyone looking to enhance their daily life through wearable tech. Elevate your health, fitness, and connectivity with the SmartLife Watch today!

---

请告诉我如果需要调整或添加任何内容，或者您有其他产品想要介绍的话。
````

## q7-A032

- 條目維度：字數（長度）
- 條目原句：根据这个给我写一篇150词左右的英语作文，要求严格按照信件格式，不可分点罗列事件，标点符号采用英文格式。
- 條目參數：`{"op": "~", "n": 150, "unit": "詞"}`
- 核對器量測：詞數 111 在 150±20%（120–180）外
- 核對器判定：**違反**

答案原文：

````text
To: Mrs.Smith  
From: Kate  
Date: Thursday, May 26, 2011  

Dear Mrs.Smith,  
I hope this letter finds you well. I am writing to extend an invitation for dinner at Grand Nature Restaurant on Sunday, the 29th of May, at six o'clock in the evening. Following the meal, we will head over to the local karaoke bar where we can enjoy some fun singing with our friends. It would be a pleasure to have you join us for what promises to be a delightful evening. Please let me know if you can make it so that I may reserve a table accordingly. Looking forward to seeing you soon.  

Best regards,  
Kate
````

## q7-A033

- 條目維度：字數（長度）
- 條目原句：- 评语字数300字左右。
- 條目參數：`{"op": "~", "n": 300, "unit": "字"}`
- 核對器量測：字數 152 在 300±20%（240–360）外
- 核對器判定：**違反**

答案原文：

````text
```json
["一般", "候选人虽然在医药和消费行业有丰富的研究经验，并且能够进行深入的财务分析和撰写研究报告，但这些技能更多地适用于基金/证券行业，而不是直接应用于生物医疗公司的财务管理。尽管如此，其行业研究能力可以为公司的投资决策提供支持，但具体财务管理工作可能需要更多的会计和财务知识。"]
```
````

## q7-A034

- 條目維度：字數（長度）
- 條目原句：請寫一封給房東的信說明要提前解約，標題要帶「效率」這個詞，列出10點，200字左右。
- 條目參數：`{"op": "~", "n": 200, "unit": "字"}`
- 核對器量測：字數 386 在 200±20%（160–240）外
- 核對器判定：**違反**

答案原文：

````text
【效率提升解約通知】

尊敬的房東先生/女士：

您好！感謝您過去一年對我的悉心照料與支持。為了更高效地安排我的生活和工作，我不得不提前結束租約，這對我來說是一個艱難的決定，但也是為了更好地追求效率和品質生活。

1. 我將在本月25日搬出，以確保有足夠的時間整理物品。
2. 保持房屋的清潔，包括地板、家具和衛浴的干凈。
3. 照顧好家中的植物，避免因搬遷而造成損失。
4. 將所有私人物品妥善打包，確保不會遺忘任何重要物品。
5. 請檢查電器和管道是否正常運行，如有問題，請及時修理。
6. 保持冰箱和抽油烟機的清潔，以維持良好的居住環境。
7. 清理窗簾和床上用品，保持其清潔。
8. 確保所有門鎖和窗戶都已關閉，以防止不必要的損失。
9. 提前通知物業管理公司，以便他們可以進行必要的檢查和清理。
10. 希望我們能保持良好的合作，並祝您未來一切順利！

再次感謝您的理解和支持，期待與您保持良好關係。

此致
敬禮

Qwen
````

## q7-A035

- 條目維度：人稱
- 條目原句：帮我丰富下面内容，但字数不能多于800字，其中内容修改为我在刚开始的时候有点胆怯。
- 條目參數：`{"person": "first", "material_chars": 489}`
- 核對器量測：含我句比 1.00（23/23，需 ≥0.30；句首六字內 0.48）；主角「面试官」材料 3 次→答案 4 次（需 ≤1.0）
- 核對器判定：**違反**

答案原文：

````text
今天我参加了XXXX密室逃脱的前台接待员职位面试。早上9点，我提前到达了面试地点，感觉这个公司氛围很好，前台的接待员都很热情。然而，我内心却有些胆怯，毕竟这是我第一次参加这样的正式面试，而且对于这个行业的了解还不够深入。

面试过程中，我首先做了自我介绍，强调了自己在服务行业的工作经验和沟通能力。我尽量让自己保持镇定，但还是能感觉到自己的紧张。然后面试官问了我对前台接待员这个岗位的理解和职责，我回答得比较流畅，也展示了自己对这个岗位的热情和了解。尽管如此，我仍然能感受到自己的不自信。

接下来，面试官问了我一些关于密室逃脱游戏的问题，我回答得比较流利，展示了自己对这个行业的了解和兴趣。面试官还问了我如何处理客户的问题和突发情况，我回答得比较冷静和灵活，展示了自己在应对问题时的能力和经验。尽管如此，我依然能感觉到自己的紧张和不自信。

最后，面试官问了我对未来职业发展的规划和期望，我表达了自己长期从事服务行业的决心和信心。尽管我尽力表现得自信，但内心深处还是有些忐忑不安。

面试结束后，店长提出让我试工两天，并给了我两天的工钱。在这两天中，我努力学习和适应前台接待员的工作内容和工作节奏。尽管有些地方我做得不够好，但是我尽力了。在这两天里，我更加了解了前台接待员这个岗位的职责和要求，也更加清楚自己的不足之处。我意识到自己需要更多地了解这个行业，提高自己的专业技能和服务水平。

经过这次面试和试工的经历，我更加了解了前台接待员这个岗位的职责和要求，也更加清楚自己的不足之处。我会继续努力学习和提升自己的能力，以更好地适应和服务客户。虽然我最终没有得到这个职位，但是我并不感到失落或失望。相反，这次经历让我更加自信和勇敢地面对未来的职业发展。我相信自己会在服务行业中不断成长和发展，并为公司和团队带来更多的价值。这次经历不仅让我更加了解了自己，也让我更加坚定了对未来职业发展的信心。
````

## q7-A036

- 條目維度：人稱
- 條目原句：請用第三人稱把這段擴寫成報導，內容一定要出現「社區」，大約500字。
- 條目參數：`{"person": "third", "material_chars": 78}`
- 核對器量測：含我句比 0.24（4/17，第三人稱需 ≤0.15）
- 核對器判定：**違反**

答案原文：

````text
在南部地區，一家知名的連鎖書店分店近日經歷了一次引人注目的轉折。據悉，該書店於兩個月前宣布將結束營業，令許多愛好閱讀的居民感到惋惜。然而，上週傳出一個令人意外的消息：書店不僅原地復業，而且還保留了原有的地址，只是店面面積縮小了一半，庫存也相應減少。

這個消息一出，立刻引起了當地居民的關注。許多老顧客紛紛前往現場探訪，他們表示，過去常常可以在書店內待上一下午，享受悠閒的閱讀時光。然而，如今踏入書店，他們發現走道變得更加狹窄，空間感有所降低。一位常客李女士說道：“我記得以前這裡非常寬敞，可以自由地在書架之間穿梭，現在則需要小心翼翼地行走。”

對於這種變化，書店的店員也做出了解釋。他們透露，由於租金問題經過了長時間的協商，最終才達成了新的租賃協議。店員表示：“我們與房東進行了多次交涉，最終找到了一個雙方都能接受的方案。雖然面積和庫存有所調整，但我們會盡力保持書店的特色和氛圍，讓讀者依然能感受到家一般的溫馨。”

社區居民對此表示理解和支持。一位當地居民王先生說：“我們很欣賞書店的努力，希望它能在新的環境下繼續為我們提供一個良好的閱讀空間。”此外，也有居民提出建議，希望能有更多的公共活動在書店舉行，以吸引更多人來訪。

總之，這家書店的復業雖然面臨著一些挑戰，但通過與社區的密切合作，以及顧客的支持，它有望在新的環境中找到自己的位置，繼續成為南部地區文化生活的一個重要組成部分。
````

## q7-A037

- 條目維度：人稱
- 條目原句：這段請幫我潤色一下，要3種，改成我的視角來寫。
- 條目參數：`{"person": "first", "material_chars": 123}`
- 核對器量測：含我句比 0.00（0/19，需 ≥0.30；句首六字內 0.00）；材料抽不到主角名，只核句比
- 核對器判定：**違反**

答案原文：

````text
当然可以，以下是三种不同视角的润色版本：

### 第一种视角（科学严谨）
在光照条件下，植物通过叶绿体将二氧化碳和水转化为葡萄糖，并释放氧气。这一过程分为光反应和碳反应两个阶段。光反应发生在类囊体膜上，将光能转化为化学能；而碳反应则在基质中进行，通过卡尔文循环固定碳。温度、光强以及二氧化碳浓度都会影响整个过程的速率，任何一个因素不足都可能成为限制因子。

### 第二种视角（通俗易懂）
当阳光照耀时，植物利用叶绿体把二氧化碳和水变成葡萄糖，并释放氧气。这个过程分为两步：光反应和碳反应。光反应发生在叶绿体的膜上，把光能转换成化学能；碳反应则在细胞质中进行，通过卡尔文循环固定碳。温度、光照强度和二氧化碳浓度都会影响这个过程的速度，任何一个条件不够都会成为瓶颈。

### 第三种视角（生动形象）
阳光一照，植物就像魔术师一样，用叶绿体这个神奇的工具，把空气中的二氧化碳和水变成了美味的葡萄糖，还释放出新鲜的氧气。这个过程分为两个步骤：光反应和碳反应。光反应就像是在叶绿体的膜上进行的一场能量转换大戏，把光能变成了化学能；而碳反应则是在细胞质中上演的一场固定碳的大戏，通过卡尔文循环来完成。温度、光照强度和二氧化碳浓度就像是这场戏的幕后推手，任何一个环节出了问题，都会让整个过程停滞不前。
````

## q7-A038

- 條目維度：段落
- 條目原句：在撰写时，请确保每个小标题下的内容都能够紧扣主题，提供有关时尚新型法官的有趣见解或信息。
- 條目參數：`{"need": "heading"}`
- 核對器量測：有標題列＝False
- 核對器判定：**違反**

答案原文：

````text
**导语：**
在这个快速变化的时代，时尚不仅限于服装和设计，它也逐渐渗透到法律领域，诞生了“时尚新型法官”这一独特角色。这些法官不仅拥有深厚的法律知识，还具备独特的审美观和创新思维，他们将时尚元素融入法庭，为司法界带来新的活力。

*时尚与法律的碰撞*
时尚新型法官们认为，法律不仅仅是规则和条文，它也是一种艺术形式，需要通过视觉和情感来传达其精神。因此，他们在法庭上采用了更加现代化的设计风格，比如使用明亮的颜色、现代的装饰以及高科技设备，使法庭环境更加人性化，同时也提高了公众对法律程序的理解度。此外，他们还鼓励穿着正式但不失个性的职业装，让法官们在保持专业形象的同时，也能展现个人魅力。

*时尚新型法官的职责*
除了外观上的创新，时尚新型法官们还致力于提高司法过程的透明度和公正性。他们通过社交媒体平台与公众互动，分享案件进展和法律知识，增强了社会对司法系统的信任感。同时，他们也会定期举办公开讲座和工作坊，邀请各界人士参与讨论，促进法律教育的普及。

*未来展望*
随着科技的发展和社会的变化，时尚新型法官的角色还将不断演变。他们将继续探索如何利用最新的技术手段提升审判效率，同时保持对传统价值观的尊重。未来，我们或许会看到更多跨界的合作，比如与设计师合作开发环保材料制成的法庭用品，或者利用虚拟现实技术进行远程庭审等。

**结语：**
时尚新型法官不仅改变了人们对传统法庭的看法，也为司法系统注入了新鲜血液。他们的存在证明了法律与时尚可以完美结合，共同推动社会进步。
````

## q7-A039

- 條目維度：段落
- 條目原句：根据以上内容编写一份商学院风险隐患自查报告，要求包含如何提高学生的安全意识（分点表述），报告的不同部分之间用小标题隔开，不少于1200字。
- 條目參數：`{"need": "heading"}`
- 核對器量測：有標題列＝False
- 核對器判定：**違反**

答案原文：

````text
**商学院风险隐患自查报告**

一、引言

为深入贯彻落实学校关于冬季安全防范工作的指示精神，确保商学院全体师生的生命财产安全，根据《重大事故专项排查整治行动“回头看”活动有关文件》的要求，商学院组织了全面的风险隐患自查工作。现将自查情况汇报如下：

二、自查工作开展情况

1. **成立自查小组**：商学院成立了由院长任组长，各系主任、辅导员、学生会干部为成员的自查小组，明确分工，责任到人。
2. **制定自查方案**：根据学院实际情况，制定了详细的自查方案，包括检查范围、时间安排、检查内容等。
3. **开展自查工作**：自查小组按照方案要求，对教学楼、宿舍楼、实验室、图书馆等重点区域进行了全面细致的检查，同时对学生的日常行为进行了观察和记录。
4. **整改落实**：针对发现的问题，立即采取措施进行整改，并建立长效机制，防止问题再次发生。

三、自查发现的主要问题

1. **学生宿舍用电安全**：部分学生使用违规电器，如电热毯、电暖器等，存在火灾隐患。
2. **实验室安全管理**：实验室内存在化学品管理不规范现象，如未按规定存放、使用易燃易爆物品等。
3. **消防安全设施**：部分消防设施损坏或缺失，如灭火器、消防栓等。
4. **学生安全意识**：部分学生缺乏安全意识，存在随意穿越马路、乘坐非法营运车辆等行为。
5. **网络安全**：部分学生存在过度依赖网络，长时间上网导致视力下降，甚至沉迷于网络游戏，影响身心健康。

四、提高学生安全意识的具体措施

1. **加强安全教育**：通过举办安全知识讲座、观看安全教育视频等形式，增强学生安全意识。定期开展安全教育活动，如防火、防电、防溺水等主题班会，提高学生自我保护能力。
2. **完善安全管理制度**：制定和完善学生宿舍、实验室、图书馆等场所的安全管理制度，明确责任人，加强日常巡查，及时发现并处理安全隐患。
3. **加强安全设施建设**：定期检查消防设施，确保其处于良好状态；安装监控摄像头，加强对重点区域的监控力度；设置安全提示标识，提醒学生注意安全。
4. **开展应急演练**：组织学生参加消防演练、地震逃生演练等活动，提高应对突发事件的能力。
5. **加强家校沟通**：通过家长会、家访等形式，向家长宣传安全知识，共同关注学生安全。
6. **强化网络安全教育**：利用校园网、微信公众号等平台发布网络安全知识，引导学生树立正确的网络观；开设网络安全课程，提高学生识别网络诈骗的能力。
7. **建立安全信息反馈机制**：设立安全信息反馈渠道，鼓励学生积极举报安全隐患，对提供有效信息的学生给予奖励。
8. **加强心理健康教育**：开设心理健康课程，提供心理咨询，帮助学生缓解压力，预防心理问题的发生。
9. **实施安全考核制度**：将安全教育纳入学生综合素质评价体系，作为评优评先的重要依据之一。
10. **加强与社区合作**：与当地社区建立合作关系，邀请专业人士来校开展安全教育讲座，拓宽学生视野，增强其社会责任感。

五、总结

通过此次自查工作，我们发现了一些潜在的安全隐患，同时也认识到提高学生安全意识的重要性。我们将继续加强安全管理工作，不断完善安全管理体系，努力营造一个安全和谐的学习环境，保障每一位学生的生命安全和身体健康。

六、未来工作计划

1. **持续开展安全教育**：定期组织安全教育活动，提高学生安全意识。
2. **加强安全设施建设**：定期检查维护消防设施，确保其正常运行。
3. **完善安全管理制度**：修订和完善各项安全管理制度，明确职责分工。
4. **加强家校沟通**：通过家长会、家访等形式，加强与家长的联系，共同关注学生安全。
5. **开展应急演练**：定期组织应急演练，提高学生应对突发事件的能力。
6. **加强心理健康教育**：开设心理健康课程，提供心理咨询，帮助学生缓解压力。
7. **建立安全信息反馈机制**：设立安全信息反馈渠道，鼓励学生积极举报安全隐患。
8. **加强与社区合作**：与当地社区建立合作关系，邀请专业人士来校开展安全教育讲座。
9. **实施安全考核制度**：将安全教育纳入学生综合素质评价体系，作为评优评先的重要依据之一。
10. **加强安全检查**：定期组织安全检查，及时发现并处理安全隐患。

以上是商学院关于提高学生安全意识的具体措施，我们将严格按照计划执行，确保各项工作落到实处，为学生创造一个安全和谐的学习环境。
````

## q7-A040

- 條目維度：段落
- 條目原句：2. 请你为总结的内容起一个标题。
- 條目參數：`{"need": "heading"}`
- 核對器量測：有標題列＝False
- 核對器判定：**違反**

答案原文：

````text
三、磷酸铁锂产能情况总结

2022年中国磷酸铁锂产量达到105.8万吨，同比增长130%，年底产能超过220万吨，较2021年底新增135万吨。德方纳米和湖南裕能的产能和产量仍保持第一梯队，市场份额为42%，尽管有所下降但仍领先。第二梯队包括龙蟠科技、湖北万润、国轩高科、融通高科等，产量在8-11万吨之间。第三梯队则为4-6万吨，代表企业有贵州安达、富临精工、内蒙古圣钒等。此外，多家电池厂和化工企业纷纷加入磷酸铁锂产能扩张，计划未来几年内新增超过700万吨产能。2023年预计国内磷酸铁锂产能过剩情况严重，增速仍会保持55%以上。
````

