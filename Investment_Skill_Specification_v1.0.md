# Investment Skill Specification v1.0

## Investment Agent Core Capability Specification

**Specification Version:** v1.0  
**Framework Source:** Investment Decision Framework v2.0  
**适用市场:** A股、港股  
**目标:** 将优秀主动投资者的研究流程拆解为 Agent 可以顺序执行、相互交接、持续验证的能力模块。

本规范不修改 Investment Decision Framework v2.0 的投资理念，不包含代码、数据库、UI或自动交易设计。

Agent 的职责是发现机会、建立投资逻辑、验证假设、判断风险收益比、提出仓位建议并持续跟踪。最终交易决策由投资者作出。

---

# 1. Specification Scope

## 1.1 核心投资问题

整个 Skill 体系服务于一个核心问题：

> 未来价值增长与当前市场定价之间是否存在值得承担风险的差异？

Agent 必须依次回答：

1. 是否出现值得研究的新变化；
2. 这属于什么类型的投资机会；
3. 当前市场环境如何影响风险暴露；
4. 什么产业变化正在创造价值；
5. 新增价值流向产业链哪个环节；
6. 为什么目标公司能够获得产业利润；
7. 自主盈利判断与市场预期有何差异；
8. 当前价格隐含了什么假设；
9. 为什么市场可能在现在重新定价；
10. 市场是否已开始确认投资逻辑；
11. 当前应处于什么投资状态；
12. 新事实是否强化、弱化或证伪原始逻辑。

## 1.2 核心 Skill

1. Opportunity Screening Skill
2. Opportunity Classification Skill
3. Market Regime Skill
4. Industry Thesis Skill
5. Profit Pool & Competitive Dynamics Skill
6. Company Alpha Skill
7. Earnings & Variant Perception Skill
8. Valuation & Implied Expectation Skill
9. Catalyst & Timing Skill
10. Trend Confirmation Skill
11. Portfolio & Risk Management Skill
12. Monitoring & Review Skill

Investment Debate 是所有 Skill 的内部要求。Final Investment Memo 是全部 Skill 结果的汇总载体，二者均不作为独立 Skill。

---

# 2. Agent Execution Contract

## 2.1 标准因果推演链

每个 Skill 都必须体现以下推演顺序：

> 事实  
> ↓  
> 变化  
> ↓  
> 商业影响  
> ↓  
> 盈利影响  
> ↓  
> 市场定价影响

五个环节的定义：

| 环节 | 必须回答的问题 |
|---|---|
| 事实 | 已经发生或可以验证的客观信息是什么？ |
| 变化 | 相比历史、市场预期或原始假设，什么发生了变化？ |
| 商业影响 | 变化如何影响需求、供给、竞争、份额、价格或商业模式？ |
| 盈利影响 | 商业变化如何传导至销量、单价、收入、利润率、利润或现金流？ |
| 市场定价影响 | 当前价格是否已经反映，什么会推动市场重新定价？ |

Skill 不得从价格表现直接倒推出基本面结论，也不得跳过中间环节，用宏大叙事直接得出盈利或估值结论。

某一环节对当前 Skill 不构成直接影响时，必须明确说明“影响不重大”及原因，不能为了填满链条而虚构因果关系。例如，Market Regime 对企业盈利可能没有直接影响，但会通过流动性、折现率和风险偏好影响市场定价与风险暴露。

## 2.2 输入纪律

进入任何 Skill 的信息必须能够区分：

- **Fact：** 已确认事实；
- **Consensus：** 市场一致预期或主流认知；
- **Inference：** 基于事实作出的推断；
- **Assumption：** 尚待验证的关键假设；
- **Unknown：** 当前缺失但可能影响结论的信息。

关键事实必须具有明确的观察时点。缺少决策关键输入时，Skill 必须输出 Recheck，不得用低质量信息替代。

## 2.3 统一 Output Schema

每个 Skill 必须包含以下字段，同时可以增加本 Skill 专属字段：

| 字段 | 定义 |
|---|---|
| Core Conclusion | 用一句或一段话直接回答该 Skill 的核心投资问题 |
| Bull Case | 支持当前结论成立的最强事实、变化和因果链 |
| Bear Case | 最强反方证据，以及对同一事实的 Alternative Explanation |
| Key Assumptions | 结论成立所依赖、但尚未完全确认的变量 |
| Falsification Conditions | 哪些可观察事实出现时必须承认该环节判断错误 |
| Verification Metrics | 后续跟踪什么指标、方向和时间窗口 |
| Confidence | 对 Core Conclusion 的置信度：High / Medium / Low，并说明依据 |
| Stage Decision | Pass / Recheck / Reject |

### Confidence 语义

- **High：** 核心因果链由多项一致证据支持，关键假设可验证，重要反方解释不能更好地解释事实；
- **Medium：** 方向性证据成立，但关键变量、幅度或时间仍有明显不确定性；
- **Low：** 结论主要依赖假设、单一信号或不完整证据。

Confidence 表示对结论的确信程度，不表示看多程度。Agent 可以对一个负面结论具有 High Confidence。

### Stage Decision 语义

- **Pass：** 本阶段核心问题已被充分回答，输出足以交给下游 Skill；
- **Recheck：** 逻辑可能成立，但存在关键输入缺失、证据冲突或时间尚未验证；
- **Reject：** 本阶段核心因果关系不成立、核心假设已被证伪，或继续向下研究已经没有意义。

Stage Decision 表示是否通过本阶段，不等同于 Buy / Sell。Market Regime 得出高风险环境，仍可因分析完整而 Pass；Trend Confirmation 的 Reject 通常表示拒绝当前入场，而不自动否定长期基本面。

## 2.4 Skill Dependency Graph

> Opportunity Screening  
> ↓  
> Opportunity Classification  
> ↓  
> Market Regime  
> ↓  
> Industry Thesis  
> ↓  
> Profit Pool & Competitive Dynamics  
> ↓  
> Company Alpha  
> ↓  
> Earnings & Variant Perception  
> ↓  
> Valuation & Implied Expectation  
> ↓  
> Catalyst & Timing  
> ↓  
> Trend Confirmation  
> ↓  
> Portfolio & Risk Management  
> ↓  
> Monitoring & Review  
> ↺ 返回发生变化的上游 Skill，并重新运行下游判断

Opportunity Screening 只负责从大量候选中发现值得研究的变化，不构成深度研究。通过筛选后，Opportunity Classification 必须在任何深度研究前完成。

## 2.5 Opportunity Type Routing

Opportunity Classification 不允许跳过其他核心 Skill，而是决定各 Skill 的分析重点。

| Opportunity Type | 研究主线 | 重点验证 |
|---|---|---|
| Structural Growth | 产业扩张 → 公司份额与盈利增长 → 重新定价 | 渗透率、成长持续性、利润池、公司竞争优势 |
| Cyclical Recovery | 供需变化 → 价格反转 → 盈利与估值修复 | 库存、产能退出、价格、成本曲线、盈利弹性 |
| Value Re-rating | 错误定价 → 认知修正 → 估值提升 | 隐含预期、错误定价原因、修正催化剂 |
| Special Situation | 特定事件 → 商业或资产价值变化 → 市场重估 | 事件真实性、影响路径、发生时间与失败风险 |

---

# 3. Opportunity Screening Skill

## Skill Purpose

从大量公司或市场变化中识别值得投入深度研究资源的候选机会。

该 Skill 解决的是“是否值得研究”，而不是“是否值得买入”。

## Framework Mapping

- Framework §3 Opportunity Screening
- 同时承接 Framework §1 First Principles 对“未来价值增长与当前市场定价差异”的总要求

## Required Input

- 候选公司或候选产业的基本身份信息；
- Industry Signal：技术、政策、供需、消费变化；
- Business Signal：收入、利润、份额或经营指标变化；
- Market Signal：估值、资金关注、成交或趋势变化；
- 变化发生的时间及与历史状态的对比；
- 已知市场叙事和明显风险；
- 人工输入的观察名单或研究线索，如有。

## Reasoning Process

1. **事实：** 识别可验证的新信号，排除传闻和重复信息；
2. **变化：** 判断信号相对历史、市场预期或此前状态是否构成实质变化；
3. **商业影响：** 建立变化可能影响需求、供给、竞争、份额或商业模式的初步路径；
4. **盈利影响：** 判断是否存在传导至收入、利润率、利润或现金流的合理可能；
5. **市场定价影响：** 判断市场是否开始关注，以及当前定价可能仍存在研究空间。

本阶段只要求建立可研究的因果假说，不要求完成盈利预测或估值结论。

## Output Schema

- **Core Conclusion：** 是否值得进入深度研究，以及最重要的变化是什么；
- **Bull Case：** 该信号可能形成投资机会的最强路径；
- **Bear Case：** 信号可能只是噪声、一次性波动或被错误解释的原因；
- **Key Assumptions：** 从信号传导到商业和盈利变化所依赖的假设；
- **Falsification Conditions：** 哪些初步事实会直接否定研究价值；
- **Verification Metrics：** 下一步需要补充和验证的指标；
- **Confidence：** 对“值得研究”这一判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Research Priority：** High / Medium / Low；
- **Trigger Signal：** 触发筛选的核心信号；
- **Research Question：** 深度研究必须回答的首要问题。

## Decision Rules

### Pass

- 至少存在一个可验证、具有实质性的变化；
- 变化到商业和盈利影响之间存在合理路径；
- 信息增量可能尚未被市场充分理解；
- Research Priority 为 High。

### Recheck

- 存在潜在线索，但事实强度、持续性或盈利传导尚不清楚；
- 多个信号相互冲突；
- Research Priority 为 Medium，需要等待或补充信息。

### Reject

- 没有实质变化，只有价格波动或市场噪声；
- 变化无法合理传导至商业价值或盈利；
- 核心信息明显失真、过时或不可验证；
- Research Priority 为 Low，不进入当前深度研究队列。

## Skill Dependency

- **输入来自：** 市场、产业和公司层面的原始研究线索，以及投资者主动提出的候选对象；
- **输出给：** Opportunity Classification Skill；
- **后续反馈：** Monitoring & Review 发现的新事实，也可以重新触发本 Skill 对新机会进行筛选。

---

# 4. Opportunity Classification Skill

## Skill Purpose

判断候选机会属于哪一种主要投资类型，从而确定后续研究的主因果链和分析重点。

该 Skill 防止 Agent 用同一种研究逻辑分析所有股票。

## Framework Mapping

- Framework §2 Investment Opportunity Classification
- Type A Structural Growth
- Type B Cyclical Recovery
- Type C Value Re-rating
- Type D Special Situation

## Required Input

- Opportunity Screening 的全部输出；
- 触发机会的核心事实和变化；
- 公司主要盈利来源；
- 所处产业的增长、供需和生命周期概况；
- 当前估值或错误定价的初步线索；
- 已知事件、政策、改革、并购或资产变化；
- 市场当前对该机会的主流叙事。

## Reasoning Process

1. **事实：** 确认机会由产业扩张、周期拐点、认知修正还是特殊事件触发；
2. **变化：** 判断主要变量正在发生结构变化、周期变化、定价变化或事件变化；
3. **商业影响：** 为四类机会分别建立对业务、供需或资产价值的影响路径；
4. **盈利影响：** 判断收益主要来自持续增长、盈利修复、估值重估还是事件兑现；
5. **市场定价影响：** 明确市场需要修正的核心预期及可能的重定价机制。

如果多种类型同时存在，必须选出主类型；次类型只能作为补充，不能用来模糊主要收益来源。

## Output Schema

- **Core Conclusion：** 主要 Opportunity Type 及一句话分类理由；
- **Bull Case：** 该分类能够解释价值创造和重新定价的证据；
- **Bear Case：** 其他类型或非投资性解释为何可能更合理；
- **Key Assumptions：** 分类成立依赖的关键变量；
- **Falsification Conditions：** 哪些事实会迫使 Agent 重新分类；
- **Verification Metrics：** 用于确认类型的后续指标；
- **Confidence：** 对分类结论的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Opportunity Type：** Structural Growth / Cyclical Recovery / Value Re-rating / Special Situation；
- **Secondary Type：** 如存在，说明其作用但不得替代主类型；
- **Investment Logic：** 该类型对应的核心收益链；
- **Required Analysis Path：** 后续 Skill 的重点变量和验证顺序。

## Decision Rules

### Pass

- 能识别唯一的主收益来源；
- 分类与已知事实、商业影响和盈利路径一致；
- Required Analysis Path 明确，足以指导后续 Skill。

### Recheck

- 两种或以上类型的解释力接近；
- 收益来源尚不清楚；
- 需要等待供需、盈利或事件信息确认主类型。

### Reject

- 不能归入任何一种 Framework 类型；
- 分类只来自题材标签，无法建立商业或盈利路径；
- 候选机会不再具备可研究的投资逻辑。

## Skill Dependency

- **输入来自：** Opportunity Screening Skill；
- **输出给：** Market Regime Skill，并为其后全部 Skill 提供 Opportunity Type 和 Required Analysis Path；
- **反馈关系：** 后续事实与原类型不符时，由 Monitoring & Review 触发重新分类。

---

# 5. Market Regime Skill

## Skill Purpose

判断当前市场环境如何影响风险预算、估值容忍度和仓位暴露。

该 Skill 不决定产业机会是否成立，只决定承担风险的环境是否有利。

## Framework Mapping

- Framework §4 Market Regime Analysis
- Framework §13 Portfolio & Risk Management 中的市场环境要求

## Required Input

- 当前 Opportunity Type 与 Required Analysis Path；
- 利率及其变化方向；
- 美元与相关汇率环境；
- 信用环境；
- 市场资金流向；
- 成交量和市场宽度；
- 市场风格变化；
- 当前风险偏好及其历史对比。

## Reasoning Process

1. **事实：** 汇总流动性、信用、成交、市场宽度和风格数据；
2. **变化：** 判断环境正在改善、稳定还是恶化；
3. **商业影响：** 判断融资条件、需求或经营环境是否受到实质影响；若不显著必须明确说明；
4. **盈利影响：** 评估市场环境是否改变企业盈利假设，或主要只影响折现率与风险偏好；
5. **市场定价影响：** 判断估值扩张或收缩压力，以及适合承担的风险暴露。

## Output Schema

- **Core Conclusion：** 当前 Market Regime 及其对该机会的主要影响；
- **Bull Case：** 支持流动性和风险偏好改善的证据；
- **Bear Case：** 支持环境恶化或相反解释的证据；
- **Key Assumptions：** 市场状态判断依赖的变量；
- **Falsification Conditions：** 哪些变化将迫使 Agent 切换 Regime 判断；
- **Verification Metrics：** 需要持续跟踪的宏观与市场指标；
- **Confidence：** 对 Market Regime 判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Market State：** 当前市场状态；
- **Risk Level：** 当前风险等级；
- **Recommended Risk Exposure：** 风险暴露方向及理由；
- **Regime Change Triggers：** 市场状态切换条件。

## Decision Rules

### Pass

- 主要市场指标能够形成一致或可解释的状态判断；
- 风险等级和风险暴露建议有明确依据；
- 即使市场环境不利，只要结论可靠仍然 Pass，并将风险传递给 Portfolio Skill。

### Recheck

- 流动性、风险偏好和市场宽度信号明显冲突；
- 数据处于快速变化阶段，尚不能确定主要方向；
- 输出只能形成暂时性判断。

### Reject

- 关键市场数据缺失、失真或过时，无法形成可靠环境判断；
- Reject 仅表示本 Skill 结果不可用于仓位决策，不表示产业机会被否定。

## Skill Dependency

- **输入来自：** Opportunity Classification Skill 以及当前市场事实；
- **输出给：** Industry Thesis Skill 作为环境背景，并直接提供给 Valuation、Trend 和 Portfolio Skills；
- **后续更新：** Monitoring & Review 在市场状态切换时触发重新运行。

---

# 6. Industry Thesis Skill

## Skill Purpose

判断未来3—5年是否存在能够创造新增价值的产业变化，以及这一变化为什么现在发生。

## Framework Mapping

- Framework §5 Industry Thesis Analysis
- Framework §1 First Principles 中“企业未来价值是否增长”的要求

## Required Input

- Opportunity Type 与 Required Analysis Path；
- Market Regime 背景；
- 产业需求规模、增速和驱动因素；
- 技术、成本、政策、消费或应用场景变化；
- 产业供给、产能、资源与进入条件；
- 渗透率及产业生命周期信息；
- 当前市场对产业的主流认知；
- 可能推动变化的产业 Catalyst。

## Reasoning Process

1. **事实：** 确认需求、供给、技术、成本、政策与生命周期状态；
2. **变化：** 识别正在发生的结构性、周期性或事件性变化；
3. **商业影响：** 判断变化如何影响行业规模、价格、竞争和价值创造；
4. **盈利影响：** 推导行业收入、利润空间或盈利波动方向；
5. **市场定价影响：** 比较产业现实与市场认知，判断哪些变化可能尚未充分定价。

分析重点必须服从 Opportunity Type：Structural Growth 强调渗透与持续性，Cyclical Recovery 强调供需拐点，Value Re-rating 强调被忽视的产业现实，Special Situation 强调事件的产业背景和影响边界。

## Output Schema

- **Core Conclusion：** 一句话 Industry Thesis；
- **Bull Case：** 产业变化持续并创造价值的证据链；
- **Bear Case：** 需求不成立、供给快速跟进或其他解释；
- **Key Assumptions：** 需求、供给、生命周期和持续时间假设；
- **Falsification Conditions：** 产业逻辑必须被否定的条件；
- **Verification Metrics：** 需求、供给、渗透率、价格等跟踪指标；
- **Confidence：** 对产业逻辑的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Industry Thesis：** 完整产业判断；
- **Growth Driver：** 核心价值增长驱动；
- **Key Variables：** 最关键的产业变量；
- **Catalyst：** 为什么变化在当前阶段发生；
- **Lifecycle：** 当前产业生命周期；
- **Risks：** 主要产业风险。

## Decision Rules

### Pass

- 存在可验证的需求、供给或产业结构变化；
- 变化具有足够持续性或对当前 Opportunity Type 具有足够影响；
- 能建立产业变化到行业价值和盈利方向的清晰路径；
- “为什么现在”有事实支持。

### Recheck

- 产业方向可能成立，但需求真实性、供给弹性或持续时间不清楚；
- 当前变化仍处于早期，关键指标尚未确认；
- 市场认知与产业事实之间的差异无法可靠判断。

### Reject

- 产业变化不存在或只是短期噪声；
- 需求增长无法形成商业价值；
- 供给无约束地扩张并抵消价值增长；
- 关键产业假设已被事实否定。

## Skill Dependency

- **输入来自：** Opportunity Classification Skill、Market Regime Skill 和产业事实；
- **输出给：** Profit Pool & Competitive Dynamics Skill；
- **横向输出：** Catalyst & Timing Skill 和 Monitoring & Review Skill 使用其关键变量与证伪条件。

---

# 7. Profit Pool & Competitive Dynamics Skill

## Skill Purpose

判断行业创造的新增价值最终流向产业链哪个环节、哪些参与者获益，以及竞争是否会侵蚀利润。

## Framework Mapping

- Framework §6 Profit Pool & Competitive Dynamics

## Required Input

- Industry Thesis 的全部输出；
- Opportunity Type 与研究重点；
- 上游、中游、下游产业链结构；
- 各环节收入、利润率和资本投入特征；
- 供需缺口、产能和成本曲线；
- 价格与议价权信息；
- 市占率及其变化；
- 主要竞争者、新进入者与退出者；
- 技术、规模、品牌、客户或网络效应信息。

## Reasoning Process

1. **事实：** 描述产业链结构、供需、成本、价格、份额和竞争者状态；
2. **变化：** 识别稀缺性、定价权、利润率和市场份额向哪里迁移；
3. **商业影响：** 判断哪些环节能够捕获新增价值，哪些环节被竞争或成本挤压；
4. **盈利影响：** 推导赢家与输家的收入、利润率和盈利弹性；
5. **市场定价影响：** 判断市场是否仍在按旧利润池结构定价，以及利润迁移何时会被识别。

## Output Schema

- **Core Conclusion：** 利润池位置、迁移方向和竞争格局结论；
- **Bull Case：** 目标环节持续获得定价权和利润的证据；
- **Bear Case：** 供给扩张、竞争加剧、替代或其他利润归属解释；
- **Key Assumptions：** 稀缺性、成本曲线、份额和竞争行为假设；
- **Falsification Conditions：** 利润池判断失效的可观察条件；
- **Verification Metrics：** 价格、价差、利润率、产能、份额等指标；
- **Confidence：** 对利润池和竞争判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Profit Pool：** 当前及未来利润主要集中环节；
- **Winner：** 最可能受益的参与者类型；
- **Loser：** 最可能受损或被淘汰的参与者类型；
- **Competitive Advantage：** 维持利润获取的关键竞争优势；
- **Profit Migration Timing：** 利润迁移的验证时间。

## Decision Rules

### Pass

- 能明确识别新增价值流向；
- 目标环节具有可解释的稀缺性、定价权或利润率改善；
- 竞争动态不会立即消除这一优势；
- 盈利影响可以传递给 Company Alpha Skill。

### Recheck

- 行业增长明确，但利润归属尚不稳定；
- 供给扩张速度、成本曲线或竞争反应存在重大不确定性；
- 无法判断当前改善是暂时还是持续。

### Reject

- 行业价值不会流向目标环节；
- 目标环节缺乏定价权且竞争持续恶化；
- 利润改善完全来自不可持续因素；
- 目标公司所在位置属于明确输家。

## Skill Dependency

- **输入来自：** Industry Thesis Skill；
- **输出给：** Company Alpha Skill；
- **横向输出：** Earnings、Valuation 和 Monitoring Skills 使用利润池、成本曲线和份额指标。

---

# 8. Company Alpha Skill

## Skill Purpose

判断目标公司为什么能够比产业平均水平获得更多利润，并将产业机会转化为公司价值增长。

## Framework Mapping

- Framework §7 Company Alpha Analysis

## Required Input

- Industry Thesis 输出；
- Profit Pool & Competitive Dynamics 输出；
- 公司产品、客户、收入来源和商业模式；
- 销量、单价、收入和利润率历史变化；
- 技术、成本、客户、品牌和规模优势证据；
- 市场份额及其变化；
- 主要竞争对手对比；
- 公司治理和执行结果中与竞争优势直接相关的信息。

## Reasoning Process

1. **事实：** 确认公司的产品、客户、商业模式、份额和经营表现；
2. **变化：** 判断公司竞争位置、份额、价格、客户或产品结构是否改善；
3. **商业影响：** 说明公司如何获得产业利润，以及竞争优势能否阻止利润被他人夺走；
4. **盈利影响：** 将优势分解为销量、单价、收入、利润率和现金流影响；
5. **市场定价影响：** 判断市场是否低估了公司承接利润的能力或优势持续时间。

## Output Schema

- **Core Conclusion：** 公司是否具有可验证的 Company Alpha；
- **Bull Case：** 公司获得超额产业利润的最强证据链；
- **Bear Case：** 优势可能被高估、不可持续或由行业 Beta 误解释的原因；
- **Key Assumptions：** 份额、定价、成本、客户和执行能力假设；
- **Falsification Conditions：** 哪些事实说明公司 Alpha 已不存在；
- **Verification Metrics：** 份额、客户、销量、价格、利润率等指标；
- **Confidence：** 对 Company Alpha 判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Company Alpha：** 公司获取超额利润的机制；
- **Growth Engine：** 销量、单价、份额、产品结构或利润率驱动；
- **Competitive Position：** 相对竞争者的位置及变化；
- **Risk：** 最可能破坏公司 Alpha 的风险。

## Decision Rules

### Pass

- 公司在目标利润池中具有明确位置；
- 至少一种竞争优势有经营事实支持；
- 优势能够传导至收入、利润率、利润或现金流；
- 相对竞争者的优势不是纯叙事。

### Recheck

- 公司可能受益，但超额收益与行业 Beta 无法区分；
- 优势存在但持续性、商业化或执行结果尚未验证；
- 关键客户、产品或产能数据不足。

### Reject

- 公司无法获得产业利润；
- 所谓竞争优势没有事实支持；
- 盈利改善主要来自不可持续或非经营因素；
- 竞争位置正在恶化并触发证伪条件。

## Skill Dependency

- **输入来自：** Industry Thesis Skill、Profit Pool & Competitive Dynamics Skill；
- **输出给：** Earnings & Variant Perception Skill；
- **横向输出：** Catalyst、Valuation 和 Monitoring Skills 使用公司增长引擎与证伪指标。

---

# 9. Earnings & Variant Perception Skill

## Skill Purpose

将产业和公司变化转化为自主盈利判断，并识别其与市场预期之间的盈利差、叙事差和时间差。

## Framework Mapping

- Framework §8 Earnings & Variant Perception
- Framework §1 First Principles 中“未来变化是否超过市场预期”的要求

## Required Input

- Opportunity Type；
- Industry Thesis、Profit Pool 和 Company Alpha 的全部输出；
- 公司历史收入、利润率、利润和现金流；
- 销量、单价、产品结构、成本和费用等经营变量；
- 公司指引及可验证的经营信息；
- 分析师一致预期；
- 市场主流叙事；
- 当前价格可能隐含的初步盈利假设；
- 关键变量的预期兑现时间。

## Reasoning Process

1. **事实：** 确认历史财务、经营指标、公司指引和市场一致预期；
2. **变化：** 识别销量、价格、成本、份额、产品结构或利润率的变化；
3. **商业影响：** 将产业和公司变化映射至订单、收入来源和竞争地位；
4. **盈利影响：** 按销量 × 单价推导收入，按收入 × 利润率推导利润，并检查现金流方向；
5. **市场定价影响：** 比较 Consensus 与 Own View，识别 Earnings Gap、Narrative Gap 和 Time Gap，以及市场修正路径。

必须明确回答：市场认为 X，自己的判断是 Y，为什么自己可能正确是 Z。

## Output Schema

- **Core Conclusion：** 是否存在可投资的 Variant Perception；
- **Bull Case：** 自主盈利判断超过市场预期的完整证据链；
- **Bear Case：** 市场可能正确、自己可能错误以及 Alternative Explanation；
- **Key Assumptions：** 销量、价格、利润率、持续时间和兑现时间假设；
- **Falsification Conditions：** 哪些经营或财务结果会否定自主判断；
- **Verification Metrics：** 用于验证盈利和预期差的指标；
- **Confidence：** 对 Own View 和 Variant 的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Consensus：** 市场一致预期与主流叙事；
- **Own View：** 自主盈利判断；
- **Earnings Gap：** 盈利预测差；
- **Narrative Gap：** 市场认知差；
- **Time Gap：** 兑现时间差；
- **Evidence：** 支持差异判断的关键证据；
- **Validation Timeline：** 预期差验证时间表。

## Decision Rules

### Pass

- 至少存在一个对价值或定价有实质影响的预期差；
- 自主判断能够由产业、公司和经营事实推导；
- 能解释市场为什么可能错误；
- 验证变量和时间窗口明确。

### Recheck

- 自主盈利方向可能正确，但差异幅度不明确；
- 市场 Consensus 本身无法可靠识别；
- Narrative Gap 存在但尚未传导至盈利；
- Time Gap 太长或缺少验证节点。

### Reject

- 自主判断与市场预期没有实质差异；
- Own View 主要来自主观乐观而非证据；
- 盈利推导与现金流或经营事实明显矛盾；
- 核心预期差已经被证伪。

## Skill Dependency

- **输入来自：** Industry Thesis、Profit Pool & Competitive Dynamics、Company Alpha Skills 及市场预期信息；
- **输出给：** Valuation & Implied Expectation Skill；
- **横向输出：** Catalyst & Timing 和 Monitoring & Review 使用其 Validation Timeline。

---

# 10. Valuation & Implied Expectation Skill

## Skill Purpose

判断当前价格隐含了怎样的收入、利润率和增长持续时间假设，并比较这些假设与现实发生概率。

该 Skill 解决“好公司是否已经被价格充分反映”和“当前赔率是否值得承担风险”。

## Framework Mapping

- Framework §9 Valuation & Implied Expectation
- Framework §1 First Principles 中“当前市场如何定价”和“价格是否提供足够赔率”的要求

## Required Input

- 当前价格、股本、市值及与估值相关的资本结构信息；
- 历史财务和当前经营数据；
- Earnings & Variant Perception 输出；
- 市场一致预期；
- 当前估值及必要的历史和可比信息；
- Market Regime 对流动性和风险偏好的判断；
- 标的成交与流动性信息；
- Opportunity Type 与相应收益逻辑。

## Reasoning Process

1. **事实：** 确认当前价格、估值、盈利和市场预期；
2. **变化：** 判断估值、盈利预期和风险偏好相对历史发生的变化；
3. **商业影响：** 明确当前估值需要公司实现怎样的业务表现；
4. **盈利影响：** 反推价格隐含的收入增长、利润率和增长持续时间；
5. **市场定价影响：** 比较 Market Implied Expectation 与 Reality Probability，判断上涨、下跌空间和风险收益比。

不得以“PE高”或“PE低”直接得出结论。

## Output Schema

- **Core Conclusion：** 当前价格是否低估、合理反映或透支未来变化；
- **Bull Case：** 现实结果超过隐含预期的路径；
- **Bear Case：** 隐含预期过高、估值收缩或其他定价解释；
- **Key Assumptions：** 估值所依赖的增长、利润率、持续时间和风险偏好假设；
- **Falsification Conditions：** 哪些事实会使当前估值结论失效；
- **Verification Metrics：** 价格、估值和隐含假设的跟踪指标；
- **Confidence：** 对隐含预期和赔率判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Valuation：** 当前估值状态；
- **Implied Expectation：** 当前价格隐含的核心经营假设；
- **Reality Probability：** 自主判断对隐含假设实现概率的评估；
- **Upside：** 判断正确时的潜在上行空间及条件；
- **Downside：** 判断错误时的潜在下行风险及条件；
- **Risk Reward：** 风险收益比结论；
- **Liquidity Constraint：** 流动性对估值和仓位的限制。

## Decision Rules

### Pass

- 能够识别当前价格隐含的关键经营假设；
- 自主判断与隐含预期之间存在可解释差异；
- 上下行情景能够对应清晰的基本面条件；
- 风险收益比足以支持继续判断行动时点。

### Recheck

- 隐含假设无法可靠反推；
- 盈利和估值对少数变量过度敏感；
- 上下行空间接近或流动性造成显著不确定性；
- 需要等待价格或盈利信息变化。

### Reject

- 当前价格已经反映或超过 Bull Case；
- 即使自主盈利判断正确，潜在收益仍不足以补偿下行风险；
- 流动性使预期仓位无法合理进入或退出；
- 核心估值假设已被事实证伪。

## Skill Dependency

- **输入来自：** Earnings & Variant Perception Skill、Market Regime Skill 和市场价格信息；
- **输出给：** Catalyst & Timing Skill；
- **横向输出：** Portfolio & Risk Management 和 Monitoring & Review 使用其上下行情景和隐含假设。

---

# 11. Catalyst & Timing Skill

## Skill Purpose

回答“为什么是现在”，识别什么事件或变化可能推动市场从当前认知转向新的定价。

Catalyst 不是投资逻辑，只是推动市场重新定价的机制。

## Framework Mapping

- Framework §10 Catalyst & Timing
- Framework §1 First Principles 中“为什么市场会重新定价”的要求

## Required Input

- Opportunity Type；
- Industry Thesis、Company Alpha、Earnings & Variant Perception 和 Valuation 输出；
- 产品、订单、财报、政策和竞争变化；
- 市场认知及其近期变化；
- 预期差 Validation Timeline；
- 事件发生概率、可能时间和已知前置指标；
- 当前价格是否已提前反映事件。

## Reasoning Process

1. **事实：** 确认可观察事件、经营变化或市场认知变化；
2. **变化：** 判断催化剂相对原预期带来了什么新信息；
3. **商业影响：** 判断催化剂是否真正改变需求、供给、竞争或公司经营；
4. **盈利影响：** 评估催化剂是否改变盈利路径，或只是让市场更早认识既有价值；
5. **市场定价影响：** 说明催化剂如何、何时推动市场重新定价，以及是否已被提前交易。

必须区分：

- **Business Catalyst：** 改变企业价值或盈利；
- **Recognition Catalyst：** 不改变价值，但推动市场认识价值。

## Output Schema

- **Core Conclusion：** 当前是否存在足以解释“为什么是现在”的 Catalyst；
- **Bull Case：** 催化剂发生并推动重定价的证据链；
- **Bear Case：** 催化剂不发生、影响有限、延迟或已被定价的解释；
- **Key Assumptions：** 事件发生、影响强度和市场反应假设；
- **Falsification Conditions：** 哪些事实说明催化剂失效；
- **Verification Metrics：** 前置指标、事件节点和市场反应指标；
- **Confidence：** 对催化剂及其时间判断的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Why Now：** 当前行动时点的核心理由；
- **Catalyst：** 具体重定价催化剂；
- **Catalyst Type：** Business Catalyst / Recognition Catalyst；
- **Expected Timing：** 预期发生及验证窗口；
- **Pricing Status：** 未定价 / 部分定价 / 可能充分定价。

## Decision Rules

### Pass

- 存在具体、可观察且与投资逻辑相关的催化剂；
- 影响路径和预期时间明确；
- 催化剂尚未被市场充分定价；
- 催化剂即使延迟，也不会自动破坏基本面逻辑，除非时间本身是核心假设。

### Recheck

- 长期逻辑成立，但缺少近期重新定价机制；
- 催化剂存在但时间、发生概率或影响不清楚；
- 市场是否提前定价无法判断。

### Reject

- 所谓催化剂与商业、盈利或认知修正无关；
- 催化剂已经发生且被充分定价；
- 投资机会只剩事件想象，没有基本面和预期差支撑；
- 关键催化剂失败并同时证伪核心逻辑。

## Skill Dependency

- **输入来自：** Industry、Company Alpha、Earnings & Variant Perception、Valuation Skills；
- **输出给：** Trend Confirmation Skill；
- **横向输出：** Portfolio & Risk Management 和 Monitoring & Review 使用 Why Now、Expected Timing 和失效条件。

---

# 12. Trend Confirmation Skill

## Skill Purpose

判断市场是否开始认可投资逻辑，并为观察、入场、加仓和退出提供价格与成交层面的确认条件。

该 Skill 不预测最低点，不用趋势替代基本面。

## Framework Mapping

- Framework §11 Trend Confirmation

## Required Input

- 已完成的基本面投资逻辑；
- Catalyst & Timing 输出；
- 长周期价格趋势；
- 中期趋势及其改善或恶化状态；
- 短期成交、突破和回踩信息；
- 相对市场或相关标的的强弱变化；
- 催化剂发生前后的价格和成交反应；
- 当前持仓状态，如有。

## Reasoning Process

1. **事实：** 描述价格、成交、突破、回踩和相对强弱；
2. **变化：** 判断趋势从弱到强、从强到弱，还是保持原状态；
3. **商业影响：** 趋势通常不改变商业价值；必须明确它是在验证市场认知，而非证明业务本身；
4. **盈利影响：** 检查趋势变化是否与盈利信息同步，避免把纯资金波动误判为盈利变化；
5. **市场定价影响：** 判断市场是否开始交易预期差，并形成 Entry、Add 和 Exit 条件。

## Output Schema

- **Core Conclusion：** 当前趋势是否确认、尚未确认或否定当前行动时点；
- **Bull Case：** 价格和成交支持市场开始认可逻辑的证据；
- **Bear Case：** 趋势可能是假突破、纯流动性驱动或与基本面冲突的解释；
- **Key Assumptions：** 趋势信号与重定价过程相关的假设；
- **Falsification Conditions：** 哪些价格和成交行为使趋势判断失效；
- **Verification Metrics：** 长、中、短周期跟踪指标；
- **Confidence：** 对趋势状态的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Trend Status：** 当前长期、中期和短期趋势状态；
- **Entry Condition：** 入场所需条件；
- **Add Condition：** 加仓所需条件；
- **Exit Condition：** 趋势层面的退出条件；
- **Fundamental Alignment：** 趋势与基本面、催化剂是否一致。

## Decision Rules

### Pass

- 长期或中期趋势与基本面逻辑方向一致；
- 催化剂后的价格和成交反应支持重新定价；
- Entry 或 Add 条件可以被客观描述。

### Recheck

- 基本面逻辑成立，但趋势尚未确认；
- 长、中、短周期信号冲突；
- 突破缺少成交支持或催化剂后的市场反应不明确；
- 输出通常对应 Observe 或 Trial Position。

### Reject

- 趋势显著恶化并触发预设 Exit Condition；
- 市场对关键利好持续出现负面反应；
- 当前行动时点被否定。

Trend Reject 只否定当前入场或持仓时点。若同时出现基本面证伪，则必须将信息反馈给相关上游 Skill。

## Skill Dependency

- **输入来自：** Catalyst & Timing Skill、Market Regime Skill、完整基本面逻辑和市场交易事实；
- **输出给：** Portfolio & Risk Management Skill；
- **反馈关系：** 趋势与基本面持续冲突时，将异常交给 Monitoring & Review 调查。

---

# 13. Portfolio & Risk Management Skill

## Skill Purpose

将投资逻辑强度、确定性、风险收益比、市场环境、流动性和趋势确认转换为研究层面的投资状态与仓位建议。

仓位是判断强度的表达，但该 Skill 不执行交易。

## Framework Mapping

- Framework §13 Portfolio & Risk Management
- Framework §1 First Principles 中“当前价格是否提供足够赔率”的要求

## Required Input

- 前十个 Skills 的 Core Conclusion、Confidence 和 Stage Decision；
- Opportunity Type；
- Market Regime 与推荐风险暴露；
- Earnings Variant 的强度和验证时间；
- Valuation 的 Upside、Downside、Risk Reward 和流动性约束；
- Catalyst 的发生概率与时间；
- Trend 的 Entry、Add 和 Exit Conditions；
- 当前持仓状态和成本，如有；
- 投资者已经明确的仓位和风险边界。

## Reasoning Process

1. **事实：** 汇总各 Skill 已确认结论、风险和当前持仓事实；
2. **变化：** 判断投资逻辑、市场环境、赔率和趋势相对上次决策发生了什么变化；
3. **商业影响：** 检查产业和公司价值创造链是否完整；
4. **盈利影响：** 判断预期差强度、兑现概率及下行情景；
5. **市场定价影响：** 综合估值、催化剂、趋势和流动性，决定 Observe、Trial Position、Buy、Hold、Add、Reduce 或 Sell。

不得用单一分数机械替代冲突判断。存在冲突时，必须明确哪项证据具有更高决策重要性及原因。

## Output Schema

- **Core Conclusion：** 当前投资状态及建议仓位方向；
- **Bull Case：** 支持承担或增加风险的完整证据链；
- **Bear Case：** 可能导致损失的最强路径和 Alternative Explanation；
- **Key Assumptions：** 仓位建议依赖的关键假设；
- **Falsification Conditions：** 必须减仓或退出的条件；
- **Verification Metrics：** 决定状态升级或降级的指标；
- **Confidence：** 对当前状态和仓位方向的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **State：** Observe / Trial Position / Buy / Hold / Add / Reduce / Sell；
- **Position Rationale：** 为什么该状态与判断强度匹配；
- **Upgrade Conditions：** 提高投资状态或仓位的条件；
- **Downgrade Conditions：** 降低投资状态或仓位的条件；
- **Exit Conditions：** 退出条件；
- **Unresolved Conflicts：** 尚未解决的跨 Skill 冲突。

## Decision Rules

### Pass

- 核心产业—公司—盈利—定价因果链完整；
- 各 Skill 的关键结论不存在未解释的致命冲突；
- 当前状态与风险收益比、市场环境、趋势和流动性一致；
- 能明确说明仓位升级、降级和退出条件。

Pass 可以对应 Buy、Hold、Add，也可以对应有充分依据的 Observe、Reduce 或 Sell。

### Recheck

- 关键 Skill 为 Recheck；
- 基本面、估值、催化剂和趋势之间存在尚未解决的冲突；
- 缺少投资者风险边界或当前持仓信息；
- 通常不得给出高强度仓位建议。

### Reject

- 一个或多个决定性基本面 Skill 为 Reject；
- 风险收益比无法支持持仓；
- 关键证伪条件已经触发；
- 当前状态只能是 Observe 或 Sell，不得继续增加风险。

## Skill Dependency

- **输入来自：** 前十个 Skills 以及投资者明确的风险边界；
- **输出给：** Final Investment Memo 和 Monitoring & Review Skill；
- **权限边界：** 输出研究层面的状态与仓位建议，不生成或执行交易指令。

---

# 14. Monitoring & Review Skill

## Skill Purpose

持续比较实际事实与原始投资逻辑，判断逻辑是 Strengthened、Unchanged、Weakened 还是 Invalidated，并触发必要的重新研究。

该 Skill 使投资研究形成闭环，而不是一次性结论。

## Framework Mapping

- Framework §14 Monitoring Loop
- Framework §12 Investment Debate
- Framework §15 Final Investment Memo 中的 Verification Metrics

## Required Input

- 初始及最近一次 Final Investment Memo；
- 十二个 Skills 的历史 Core Conclusion、Key Assumptions、Falsification Conditions 和 Verification Metrics；
- 原始 Validation Timeline 与 Catalyst Expected Timing；
- 新发生的产业、竞争、公司、盈利、估值、催化剂和趋势事实；
- 当前市场预期和价格变化；
- 当前投资状态及仓位建议；
- 上次 Review 后的实际变化。

## Reasoning Process

1. **事实：** 记录新事实，不先判断其利多或利空；
2. **变化：** 比较实际结果与原始预期、关键假设和验证时间表；
3. **商业影响：** 判断偏差是否改变需求、供给、利润池、竞争位置或公司增长引擎；
4. **盈利影响：** 判断盈利和现金流路径是否需要调整；
5. **市场定价影响：** 判断预期差、隐含预期、催化剂和趋势是否变化，并更新投资状态。

Monitoring 不直接重写原始逻辑。它必须指出哪个 Skill 的哪项假设发生变化，并触发该 Skill 重新运行。

## Output Schema

- **Core Conclusion：** 当前 Investment Thesis 状态及最重要变化；
- **Bull Case：** 新事实强化逻辑的证据；
- **Bear Case：** 新事实弱化逻辑或 Alternative Explanation；
- **Key Assumptions：** 仍然有效、已改变和待验证的假设；
- **Falsification Conditions：** 已接近或已经触发的证伪条件；
- **Verification Metrics：** 指标实际值、预期值、差异及下一观察时间；
- **Confidence：** 对更新后逻辑状态的置信度；
- **Stage Decision：** Pass / Recheck / Reject；
- **Thesis Status：** Strengthened / Unchanged / Weakened / Invalidated；
- **Changed Facts：** 自上次判断以来的新事实；
- **Affected Skills：** 必须重新运行的上游 Skills；
- **Updated State Recommendation：** 更新后的投资状态建议；
- **Next Review Trigger：** 下次强制复核的事件或指标。

## Decision Rules

### Pass

- Thesis Status 为 Strengthened 或 Unchanged；
- 新事实与核心因果链一致；
- 未触发关键证伪条件；
- 当前投资状态仍有充分依据。

### Recheck

- Thesis Status 为 Weakened，但尚不能确认逻辑失效；
- 新事实与原判断冲突，需要重新运行一个或多个上游 Skill；
- 关键 Catalyst 延迟或指标偏离，但原因尚未确认。

### Reject

- Thesis Status 为 Invalidated；
- 一个或多个核心假设被事实证伪；
- 原始价值创造链、预期差或重新定价逻辑已经断裂；
- 必须把结果传给 Portfolio & Risk Management，重新形成 Reduce 或 Sell 建议。

## Skill Dependency

- **输入来自：** 全部 Skills、Final Investment Memo 和后续新事实；
- **输出给：** 受影响的上游 Skill 重新运行，并最终返回 Portfolio & Risk Management Skill；
- **闭环：** 更新后的 Portfolio 结论进入新的 Final Investment Memo，成为下一轮 Monitoring 基准。

---

# 15. Final Investment Memo Assembly

Final Investment Memo 不是独立分析 Skill。它只能汇总已经完成的 Skill 输出，不得创造上游分析中不存在的新结论。

必须包含：

## Investment Thesis

用一句话表达：

> 什么事实发生了变化，如何影响产业和公司盈利，市场当前错在哪里，为什么现在可能重新定价。

## Opportunity Type

- 主 Opportunity Type；
- 对应 Required Analysis Path。

## Why Now

- Catalyst；
- Expected Timing；
- Pricing Status；
- Trend Confirmation。

## Value Creation Chain

> 产业变化  
> ↓  
> 利润池与竞争格局  
> ↓  
> 公司 Alpha  
> ↓  
> 盈利与预期差  
> ↓  
> 当前价格隐含预期  
> ↓  
> Catalyst 与重新定价

## Investment Debate

- Bull Case；
- Bear Case；
- Alternative Explanation；
- Key Assumptions；
- Falsification Conditions。

## Verification

- Verification Metrics；
- Validation Timeline；
- Next Review Trigger。

## Decision

- State；
- Position Rationale；
- Confidence；
- Upgrade Conditions；
- Downgrade Conditions；
- Exit Conditions。

如果任一关键 Skill 为 Recheck 或 Reject，Final Investment Memo 必须显式保留，不得在汇总时被平均、隐藏或改写为确定性结论。

---

# 16. System-Level Decision Rules

## 16.1 Research Continuation

- Screening Pass 后必须完成 Opportunity Classification；
- Classification Pass 后才进入深度研究；
- 上游核心因果 Skill Reject 时，停止沿原逻辑继续向下论证；
- Recheck 可以进入有限的下一步分析，但必须携带缺失信息和不确定性；
- Agent 不得为了完成 Memo 而把 Recheck 自动升级为 Pass。

## 16.2 Cross-Skill Conflict

当 Skill 之间发生冲突时：

1. 明确冲突事实，而不是简单取平均；
2. 判断冲突发生在产业、公司、盈利、定价、催化剂还是趋势层；
3. 回到最早出现断裂的 Skill；
4. 重做该 Skill 及其所有受影响的下游 Skill；
5. 在冲突未解决前降低 Confidence，并将 Stage Decision 设为 Recheck。

## 16.3 Fundamental and Market Signal Boundary

- Market Regime 影响风险暴露，不决定产业机会；
- Catalyst 推动重新定价，不替代投资逻辑；
- Trend Confirmation 验证市场认知，不证明公司基本面；
- 价格下跌本身不是加仓理由；
- 价格上涨本身不是投资逻辑正确的证明。

## 16.4 Human Decision Boundary

Agent 可以：

- 提出 Observe、Trial Position、Buy、Hold、Add、Reduce、Sell；
- 说明仓位方向、风险和调整条件；
- 在新事实出现时更新建议。

Agent 不可以：

- 自动下单；
- 生成未经投资者确认的交易指令；
- 因趋势信号绕过基本面研究；
- 在信息不足时伪造确定性。

---

# 17. Definition of a Successful Skill System

Investment Skill Specification v1.0 的成功标准不是能生成一篇完整的股票分析报告，而是：

1. 每个 Skill 只解决一个明确的投资问题；
2. 每个结论都能沿“事实—变化—商业影响—盈利影响—市场定价影响”回溯；
3. 上游输出能够成为下游输入；
4. Bull Case 与 Bear Case 在每个阶段同时存在；
5. 关键假设、证伪条件和验证指标可以持续跟踪；
6. Agent 能区分机会不存在、证据不足和时点未到；
7. Agent 能把新事实反馈到正确的 Skill，而不是整体重写叙事；
8. 最终状态和仓位建议能够解释其依据，但不触发自动交易。

这套体系的本质是：

> 把主动投资者脑中的研究判断，拆成可执行、可交接、可证伪、可更新的能力模块。
