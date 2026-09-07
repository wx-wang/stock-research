# Investment Agent Skill Specification v1.3

## Personal Investment Agent — Core Research Skills

**Specification Version:** v1.3  
**Framework Source:** Investment Decision Framework v1.1  
**Workflow Source:** Investment Agent Workflow v1.3  
**适用市场:** A股、港股  
**目标:** 将个人投资理念收敛为最少数量、可以独立调用、可以顺序交接并能够持续验证的核心研究 Skill。

本规范不重新设计 Investment Framework，不增加新的投资理念，不涉及数据库、Tool、UI、自动交易或基金管理流程。

---

# 1. Design Conclusion

## 1.1 Skill 数量

第一阶段生成六个核心 Skill：

1. Market & Opportunity Scanner
2. Industry Value Chain Analyzer
3. Company Alpha Analyzer
4. Earnings & Valuation Analyzer
5. Timing & Portfolio Manager
6. Investment Thesis Monitor

六个 Skill 足以覆盖 Investment Decision Framework v1.1，同时避免按照 Workflow Stage 机械拆分。

## 1.2 合并原则

Skill 可以合并相邻的研究能力，但不能合并原有判断门。

例如：

- Market Regime 与 Opportunity Discovery 可以在一个 Skill 中执行，但必须分别输出市场环境判断和机会筛选判断；
- Industry Thesis 与 Profit Pool 可以在一个 Skill 中执行，但必须分别判断“产业是否创造价值”和“价值流向哪里”；
- Earnings & Variant Perception 与 Valuation & Liquidity 可以在一个 Skill 中执行，但必须分别判断“是否存在预期差”和“当前价格是否仍有赔率”；
- Trend & Timing 与 Portfolio Management 可以在一个 Skill 中执行，但必须分别判断“市场是否确认”和“当前应该处于什么投资状态”。

合并后的综合结论不得掩盖内部因果链断裂。

## 1.3 投资理念覆盖

| 投资理念 | 主要承载 Skill | 如何覆盖 |
|---|---|---|
| 产业趋势 | Market & Opportunity Scanner；Industry Value Chain Analyzer | 先识别产业变化，再验证需求、供给、生命周期和价值创造 |
| 基本面 | Industry Value Chain Analyzer；Company Alpha Analyzer；Earnings & Valuation Analyzer | 从产业价值、利润池、公司竞争优势传导至收入、利润和现金流 |
| 预期差 | Earnings & Valuation Analyzer | 比较市场预期、价格隐含预期与自主盈利判断 |
| 趋势确认 | Timing & Portfolio Manager | 用长期、中期和短期价格行为验证市场是否开始重新定价 |
| 仓位管理 | Timing & Portfolio Manager | 将逻辑、置信度、赔率、环境、趋势和流动性转化为投资状态 |
| Catalyst / Timing | 六个 Skill 的内部要求，集中汇总于 Timing & Portfolio Manager | 每一阶段回答为什么是现在，最终判断重定价条件和行动时点 |
| 投资逻辑跟踪 | Investment Thesis Monitor | 比较实际事实与原始假设，定位变化并触发相关 Skill 重跑 |

## 1.4 不独立生成的能力

以下内容不单独生成 Skill：

- **Research Brief：** 由 Workflow 在调用第一个 Skill 前形成；
- **Opportunity Classification：** 不属于 Framework v1.1 的核心理念，不在本阶段增加；
- **Bull Case / Bear Case：** 属于每个 Skill 的内部强制分析；
- **Investment Debate：** 通过 Bull Case、Bear Case、假设和证伪条件实现；
- **Catalyst：** 每个 Skill 内部分析，并由 Timing & Portfolio Manager 汇总；
- **Final Investment Memo：** 由 Workflow 汇总已有 Skill 输出，不产生新的投资判断；
- **数据获取与整理：** 属于 Skill 的输入准备，不作为投资判断 Skill；
- **自动交易：** 不在系统范围内。

---

# 2. Common Skill Contract

## 2.1 Research Context

每次调用必须具有以下研究上下文：

- Research Subject：公司、股票代码、行业或已有投资逻辑；
- Market：A股或港股及对应交易市场；
- As-of Date：信息截止时间；
- Investor Question：投资者提出的问题；
- Decision Context：发现机会、首次研究、持仓复核或逻辑更新；
- Existing Thesis：已有 Investment Thesis，如有；
- Known Position：当前投资状态或持仓信息，如有；
- Upstream Output：上游 Skill 输出，如有；
- Known Unknowns：可能影响结论的信息缺口。

机会发现任务还必须记录：

- Scan Mode：Snapshot / Rolling Window / Theme Deep Scan；
- Time Window：实际搜索起止时间；
- Source Coverage：Tushare、观察者03分页/关键词/详情、IMA、Report CLI、Web Search 的覆盖；
- Candidate Granularity：一级行业、子行业、产业链环节或概念；
- Coverage Unknowns：未访问的时间段、关键词、原文和数据缺口。

## 2.2 信息分类

每个 Skill 必须区分：

- **Fact：** 已确认事实；
- **Change：** 相对历史、市场预期或原始假设发生的变化；
- **Inference：** 基于事实作出的推断；
- **Assumption：** 尚待验证的关键假设；
- **Unknown：** 当前缺失且可能改变结论的信息。

Skill 不得把推断表述为事实，不得以无法验证的叙事替代缺失信息。

## 2.3 统一推理链

每个 Skill 必须遵循：

> 事实  
> ↓  
> 变化  
> ↓  
> 商业影响  
> ↓  
> 盈利影响  
> ↓  
> 市场定价影响

具体要求：

1. **事实：** 当前可以确认什么；
2. **变化：** 相比历史、市场共识或原始预期，什么发生了改变；
3. **商业影响：** 变化如何影响需求、供给、价格、竞争、份额或商业模式；
4. **盈利影响：** 商业变化如何传导至销量、单价、收入、利润率、利润和现金流；
5. **市场定价影响：** 市场是否已经反映，什么可能推动重新定价。

某一环节在当前 Skill 中不构成直接影响时，必须说明原因，不能为完成格式而虚构因果关系。

## 2.4 统一 Required Output

每个 Skill 至少输出：

| 字段 | 要求 |
|---|---|
| Core Conclusion | 直接回答本 Skill 的 Investment Question |
| Supporting Facts | 支持结论的关键已确认事实 |
| Bull Case | 结论成立的最强因果路径 |
| Bear Case | 最有可能推翻结论的反方路径 |
| Key Assumptions | 结论依赖但尚未完全确认的变量 |
| Falsification Conditions | 哪些事实出现时必须承认判断错误 |
| Verification Metrics | 后续跟踪的指标、方向和时间 |
| Catalyst / Timing | 为什么变化现在发生或何时可能被市场认识 |
| Confidence | High / Medium / Low，并说明依据和主要不确定性 |
| Stage Decision | Pass / Recheck / Reject |
| Handoff Package | 传递给下一 Skill 的标准信息 |

每个 Skill 还必须输出自己的专业字段。

## 2.5 Confidence

- **High：** 核心因果链由多项一致证据支持，重要反方解释不能更好地解释事实；
- **Medium：** 方向性证据成立，但关键变量、幅度或时间仍有明显不确定性；
- **Low：** 结论主要依赖假设、单一信号或不完整证据。

Confidence 表示对结论的确信程度，不表示看多程度。负面结论也可以具有 High Confidence。

## 2.6 Stage Decision

### Pass

- 本 Skill 的独立投资问题已被回答；
- 核心因果链有事实支持；
- 输出足以作为下一 Skill 输入；
- 关键风险、假设和证伪条件明确。

### Recheck

- 逻辑可能成立，但关键输入缺失；
- 事实相互冲突；
- 反方解释与当前解释同样合理；
- 尚未达到验证时间；
- 当前只能形成 Low Confidence 判断。

Recheck 必须输出缺失信息、补充方式、等待事件和重新检查条件。

### Reject

- 核心投资逻辑不存在；
- 因果链发生决定性断裂；
- 核心假设已被证伪；
- 继续研究不会增加有效信息。

Reject 必须说明拒绝的是产业、产业链位置、公司、盈利预期差、当前价格还是当前时点。

## 2.7 独立调用规则

每个 Skill 可以单独调用，但独立调用不等于可以忽略依赖关系。

- 如果调用时具有有效的上游输出，Skill 可以直接执行；
- 如果缺少上游结论但用户提供了等价的研究上下文，Skill 可以执行并标记来源；
- 如果缺少决定性上游输入，Skill 必须 Recheck；
- Skill 不得在内部静默重做所有上游研究并假装依赖已经满足；
- 单独调用产生的是该 Skill 范围内的判断，不自动形成完整投资建议。

---

# 3. Skill Dependency Chain

## 3.1 主链

> Market & Opportunity Scanner  
> ↓  
> Industry Value Chain Analyzer  
> ↓  
> Company Alpha Analyzer  
> ↓  
> Earnings & Valuation Analyzer  
> ↓  
> Timing & Portfolio Manager

在 Industry Value Chain Analyzer 之前，机会发现任务还必须经过 Workflow 内部层：

```text
Market & Opportunity Scanner
→ Opportunity Radar
→ Granularity Gate
→ Investment Opportunity Hypothesis
→ Industry Value Chain Analyzer
```

上述三项是现有 Skill 的内部能力和交接记录，不是新的独立 Skill。

Investment Thesis Monitor 位于主链之后：

> 主链输出  
> ↓  
> Investment Memo 由 Workflow 汇总  
> ↓  
> Investment Thesis Monitor  
> ↓  
> 定位发生变化的 Skill  
> ↓  
> 重跑该 Skill 及所有受影响的下游 Skill

## 3.2 条件分支

### 指定公司

Market & Opportunity Scanner 确认市场背景和研究价值后，进入完整主链。

### 指定行业或询问当前行业机会

Market & Opportunity Scanner 先形成候选行业池；Industry Value Chain Analyzer 对候选行业逐一验证，并从受益环节形成候选公司；每家公司分别进入 Company Alpha Analyzer。

### 已有投资逻辑更新

Investment Thesis Monitor 首先被调用，定位最早发生变化的 Skill，再重跑相应下游链路。

---

# 4. Skill 1 — Market & Opportunity Scanner

## Purpose

判断当前市场风险环境，并从产业和公司变化中识别值得进入深度研究的机会。

该 Skill 解决“当前应该研究什么”，不解决“最终应该买什么”。

## Investment Question

> 当前市场环境允许承担多大风险，以及哪些产业或公司正在出现可能尚未被充分定价的价值变化？

内部包含两个不可合并的判断：

1. **Market Regime Judgment：** 当前风险环境是什么；
2. **Opportunity Screening Judgment：** 哪些机会值得进入深度研究。

## Input

### 研究范围

- A股、港股或指定市场；
- 指定公司、指定行业或全行业扫描范围；
- As-of Date；
- Investor Question；
- 已知投资逻辑或观察线索，如有。

### Market Regime 信息

- 利率；
- 美元及汇率环境；
- 信用环境；
- 市场资金流向；
- 成交量；
- 市场宽度；
- 主要指数趋势；
- 市场风格和风险偏好变化。

### Opportunity Signal

- 产业技术、成本、政策、需求和供需变化；
- 公司收入、利润、订单、份额和经营指标变化；
- 行业或公司估值、资金关注和趋势变化；
- 市场主流叙事及可能的认知偏差；
- 新近发生或即将验证的 Catalyst。

## Reasoning Process

### Step 1 — 确认事实

- 识别市场环境和机会线索中的已确认事实；
- 排除单纯传闻、重复信息和只有价格波动的信号；
- 明确信息发生时间和比较基准。

### Step 2 — 识别变化

- 判断流动性和风险偏好正在改善、稳定还是恶化；
- 判断产业或公司信号相对历史和市场预期是否构成实质变化；
- 区分结构变化、周期波动和市场噪声，但不引入独立 Opportunity Classification。

### Step 3 — 判断商业影响

- 初步判断变化是否可能影响需求、供给、价格、竞争、份额或商业模式；
- 对行业机会，识别可能受影响的产业链环节；
- 对指定公司，识别其是否处于变化可能受益的位置。

### Step 4 — 判断盈利影响

- 判断商业变化是否存在传导至收入、利润率、利润或现金流的合理可能；
- 本阶段只建立盈利影响假说，不代替 Earnings & Valuation Analyzer 完成预测。

### Step 5 — 判断市场定价影响

- 判断市场是否已经开始关注；
- 判断变化是否可能尚未被充分认识；
- 判断 Market Regime 对估值和风险暴露的支持或限制；
- 形成 Research Priority，而不是 Buy / Sell。

### Step 6 — 机会召回与粒度判断

- 默认使用 Snapshot + Rolling Window + Keyword Recall + Selected Detail；最近30条只能作为快速雷达；
- 对观察者03使用 `group +topics` 分页、`topic +search` 多关键词和 `topic +detail` 重点补齐；
- 按 topic_id 去重并报告时间窗口、页数、关键词、详情数量和未覆盖范围；
- 判断一级行业或概念是否包含多个利润池；必要时拆成3—5个细分方向；
- 不因宽泛行业的单日跌幅、低热度或单一估值指标直接 Reject 全部细分方向。

### Step 7 — 形成 Investment Opportunity Hypothesis

对每个候选细分方向形成：

```text
产业变化 → 价值迁移 → 受益环节 → 利润池预检
→ 可能的盈利/现金流影响 → Market View → Agent View
→ Variant Hypothesis → 验证指标与催化剂
```

该记录是进入 Industry Value Chain 的待验证输入，不是完成的 Industry Thesis、Company Alpha 或 Buy 结论。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### 专业输出

- **Market State：** 当前市场状态；
- **Liquidity Direction：** 流动性方向；
- **Risk Appetite Direction：** 风险偏好方向；
- **Risk Level：** 当前风险等级；
- **Recommended Risk Exposure：** 风险暴露倾向；
- **Regime Change Triggers：** 市场状态切换条件；
- **Opportunity Candidates：** 候选行业或公司；
- **Trigger Signal：** 每个候选机会的核心变化；
- **Value Change Hypothesis：** 可能的价值创造路径；
- **Possible Earnings Impact：** 初步盈利影响；
- **Preliminary Pricing Status：** 初步判断市场是否可能已定价；
- **Research Priority：** High / Medium / Low；
- **Research Question：** 深度研究必须回答的问题；
- **Recommended Next Route：** 进入哪个行业或公司研究路径。

### 机会发现专业输出补充

- Candidate Granularity；
- Subsegments Considered；
- Opportunity Radar Coverage；
- Core View；
- Supporting Evidence Table；
- Profit Pool Pre-check；
- Market View vs Agent View；
- Variant Hypothesis；
- Evidence Level：Radar Only / Narrative Extracted / Cross-Validated；
- Granularity Decision；
- Recheck Reason 和 Reopen Conditions。

## Decision Rules

### Market Regime Sub-Decision

- 市场环境不利不等于机会 Reject；
- 只要市场状态可以被可靠描述，该子判断可以 Pass，并将风险限制传递给下游；
- 数据严重冲突时 Recheck；
- 关键市场信息无法使用时 Reject 本次风险暴露判断，但产业基础研究仍可继续。

### Opportunity Screening Sub-Decision

#### Pass

- 至少存在一个可验证的新变化；
- 变化到商业和盈利之间存在合理路径；
- 市场可能尚未充分理解；
- 候选机会值得投入 Industry Value Chain 深度研究。

#### Recheck

- 存在线索但变化的真实性、持续性或盈利传导尚不清楚；
- 市场是否已经定价无法判断；
- 保留为 Medium Priority 观察对象。

必要时明确标注：`Recheck—Subsegment`、`Recheck—Data` 或 `Recheck—Variant`。

#### Reject

- 没有实质变化；
- 只有股价、成交或题材信号；
- 变化无法合理传导到商业价值和盈利；
- 信息明显失真、过时或不可验证。

`Reject—Current Scope` 只能在合理拆分主要细分方向后使用；它拒绝当前扫描范围，不代表宽泛行业的所有细分方向或未来催化剂均失效。

## Dependency

- **输入来自：** Workflow Research Context、投资者提供的公司或产业线索，以及当前市场与产业事实；
- **输出给：** Industry Value Chain Analyzer；
- **跨阶段输出：** Market State、Risk Level 和 Recommended Risk Exposure 同时传递给 Earnings & Valuation Analyzer 及 Timing & Portfolio Manager；
- **可被触发：** Investment Thesis Monitor 在 Market Regime 或机会信号发生变化时重新调用。

---

# 5. Skill 2 — Industry Value Chain Analyzer

## Purpose

判断产业是否正在创造新增价值、所处生命周期，以及新增价值最终流向产业链哪个环节。

该 Skill 把“产业有机会”和“钱流向哪里”放在同一能力中，但必须保留两个内部判断门。

## Investment Question

> 未来3—5年是否存在可持续的产业价值变化，这些价值最终会流向哪里？

内部包含：

1. **Industry Thesis Judgment：** 产业是否创造价值；
2. **Profit Pool Judgment：** 价值由哪个环节获取。

## Input

- Market & Opportunity Scanner 的 Handoff Package；
- Market State 和 Risk Level；
- 候选行业及核心变化；
- 技术、成本、政策、消费和应用场景变化；
- 行业需求、供给、渗透率和生命周期；
- 上游、中游、下游产业链结构；
- 各环节价格、产能、成本、收入和利润率；
- 市场份额、主要参与者和新进入者；
- 各环节的稀缺性、议价权和竞争变化；
- 市场当前对产业的主流认知；
- 指定公司在产业链中的位置，如有。

## Reasoning Process

### Step 1 — 确认事实

- 确认需求、供给、技术、成本、政策、渗透率和生命周期状态；
- 描述产业链结构、关键参与者、价格、成本、产能和利润率；
- 确认当前市场主流产业叙事。

### Step 2 — 识别变化

- 判断产业变化是长期价值创造还是短期扰动；
- 判断需求、供给、产业阶段和竞争格局发生了什么变化；
- 识别稀缺性、定价权、利润率和份额正在向哪里迁移；
- 回答为什么变化在当前阶段发生。

### Step 3 — 判断商业影响

- 判断变化如何影响行业规模、产品价格、供给格局和商业价值；
- 判断上中下游哪个环节能够捕获新增价值；
- 判断哪些环节会被成本、竞争或替代挤压；
- 识别最可能的产业赢家和输家。

### Step 4 — 判断盈利影响

- 推导受益环节的收入、利润率和盈利方向；
- 判断利润改善是结构性还是周期性；
- 判断供给扩张是否会快速侵蚀利润；
- 确定后续公司盈利分析需要关注的关键变量。

### Step 5 — 判断市场定价影响

- 判断市场是否仍在按旧产业结构或旧利润池定价；
- 判断利润迁移何时可能被经营数据或财务结果验证；
- 识别产业与利润池层面的 Catalyst；
- 形成最值得进入 Company Alpha 分析的公司类型或候选公司。

### Step 6 — 细分行业与利润池预检

- 对宽泛或异质行业先拆分主要子行业和产业链环节；
- 对每个细分方向分别测试“产业变化 → 价值迁移 → 利润池 → 定价权 → 盈利影响”；
- 明确哪些细分方向被验证、被推迟或被拒绝，以及拒绝原因；
- 不用一级行业平均涨跌或报告热度替代利润池判断。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### 专业输出

- **Industry Thesis：** 一句话产业价值判断；
- **Industry Thesis Decision：** Pass / Recheck / Reject；
- **Demand Drivers：** 需求增长来源；
- **Supply Constraints：** 供给限制；
- **Lifecycle Stage：** 萌芽 / 渗透 / 高增长 / 成熟 / 衰退；
- **Value Creation Mechanism：** 产业创造新增价值的机制；
- **Growth Duration：** 预期持续时间；
- **Industry Chain Map：** 上中下游价值链；
- **Current Profit Pool：** 当前利润池位置；
- **Profit Migration Direction：** 利润迁移方向；
- **Profit Pool Decision：** Pass / Recheck / Reject；
- **Pricing Power Holder：** 拥有定价权的环节；
- **Beneficiary Segments：** 最受益环节；
- **Disadvantaged Segments：** 最受损环节；
- **Winner Characteristics：** 赢家应具备的特征；
- **Candidate Companies：** 基于价值流向形成的候选公司，如适用；
- **Profit Migration Timing：** 利润迁移验证时间。

### 细分与证据补充输出

- Candidate Granularity；
- Subsegments Considered；
- Segment-Level Industry Thesis；
- Segment-Level Profit-Pool Hypothesis；
- Profit-Pool Evidence Table；
- Market View vs Agent View；
- Evidence Level；
- Coverage Unknowns；
- Recheck Reason。

## Decision Rules

### Industry Thesis Judgment

#### Pass

- 存在可验证的需求、供给或产业结构变化；
- 变化能够创造新增商业价值；
- 具有合理持续时间；
- 为什么是现在有事实支持。

#### Recheck

- 产业方向可能成立，但需求真实性、供给弹性或持续时间不清；
- 关键产业指标尚未到达验证时点。

#### Reject

- 不存在实质产业变化；
- 变化无法形成商业价值；
- 核心产业假设已被事实否定。

### Profit Pool Judgment

#### Pass

- 能明确识别新增价值流向；
- 目标环节具有稀缺性、定价权或利润率改善；
- 竞争不会立即消除优势。

#### Recheck

- 行业价值增长成立，但利润归属尚不清楚；
- 供给扩张、成本曲线或竞争反应存在重大不确定性。

#### Reject

- 价值不流向目标环节；
- 目标环节缺乏定价权；
- 利润改善完全来自不可持续因素；
- 指定公司所在位置属于明确受损方。

### 综合 Stage Decision

- 两个子判断均 Pass，综合结果才能 Pass；
- 任一子判断 Recheck，综合结果通常为 Recheck；
- Industry Thesis Reject 时停止原产业逻辑；
- Industry Thesis Pass 但 Profit Pool Reject 时，只否定当前环节或公司，可以重新选择受益环节。
- 对宽泛行业，只有 Granularity、Industry Thesis 和 Profit Pool 均通过，才允许输出行业机会 Pass；`Reject—Current Scope` 不等于否定所有未覆盖的细分方向。

## Dependency

- **输入来自：** Market & Opportunity Scanner；
- **输出给：** Company Alpha Analyzer；
- **行业扫描分支：** 对多个候选行业逐一执行，并将通过的行业及候选公司交给 Company Alpha Analyzer；
- **可被触发：** Investment Thesis Monitor 在产业数据、政策、供需、产能或竞争格局变化时重新调用。

---

# 6. Skill 3 — Company Alpha Analyzer

## Purpose

判断目标公司是否能够承接产业价值，并获得超过产业平均水平的利润。

## Investment Question

> 为什么产业创造的价值会流向这家公司，而不是竞争对手？

## Input

- Industry Value Chain Analyzer 的 Handoff Package；
- Industry Thesis 与 Profit Pool 子判断；
- 公司在产业链中的位置；
- 产品、服务、客户和应用场景；
- 收入和利润来源；
- 商业模式；
- 技术、成本、客户、规模和品牌优势证据；
- 市场份额及其变化；
- 主要竞争对手；
- 销量、单价、产品结构、利润率和现金流变化；
- 公司层面的近期 Catalyst；
- 市场对公司竞争优势的主流认知。

## Reasoning Process

### Step 1 — 确认事实

- 确认公司产品、客户、收入来源、商业模式和产业位置；
- 确认历史经营结果、份额、销量、价格、利润率和现金流；
- 确认竞争优势是否有可观察事实支持。

### Step 2 — 识别变化

- 判断公司份额、客户、产品、价格、成本或竞争位置发生了什么变化；
- 区分公司自身 Alpha 与行业整体 Beta；
- 判断变化是暂时受益还是持续优势强化。

### Step 3 — 判断商业影响

- 解释公司如何承接利润池；
- 判断竞争优势如何阻止利润被竞争者夺走；
- 与主要竞争者比较技术、成本、客户、规模或品牌能力；
- 判断商业模式是否支持持续价值获取。

### Step 4 — 判断盈利影响

- 分解收入增长来自市场扩张、份额、销量、单价或产品结构；
- 分解利润增长来自收入还是利润率；
- 判断盈利是否能够改善现金流；
- 向 Earnings & Valuation Analyzer 输出关键盈利驱动。

### Step 5 — 判断市场定价影响

- 判断市场是否低估公司承接产业利润的能力；
- 判断市场是否高估竞争优势持续时间；
- 识别公司经营变化何时可能通过订单、份额或财报被市场认识。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### 专业输出

- **Company Positioning：** 公司产业链位置；
- **Business Model：** 产品、客户、收入和利润来源；
- **Company Alpha：** 公司获取超额产业利润的机制；
- **Competitive Advantage：** 技术、成本、客户、规模或品牌优势；
- **Advantage Durability：** 优势持续性；
- **Growth Engine：** 增长引擎；
- **Revenue Growth Bridge：** 销量、单价、份额和产品结构；
- **Profit Growth Bridge：** 收入和利润率传导；
- **Relative Competitive Position：** 相对竞争者的位置与变化；
- **Company-Specific Risks：** 可能破坏 Alpha 的风险；
- **Earnings Drivers for Next Stage：** 交给盈利分析的核心变量。

## Decision Rules

### Pass

- 公司处于受益利润池；
- 至少一项竞争优势有经营事实支持；
- 优势能够传导至收入、利润率、利润或现金流；
- 相对竞争者的优势不是纯叙事；
- 关键盈利驱动可以被验证。

### Recheck

- 公司可能受益，但无法区分 Company Alpha 与行业 Beta；
- 优势存在但持续性或商业化尚未验证；
- 客户、产品、份额或成本数据不足；
- 市场和自身对竞争优势的解释力接近。

### Reject

- 公司无法获得产业利润；
- 竞争优势没有事实支持；
- 盈利改善主要来自不可持续或非经营因素；
- 竞争位置正在恶化并触发证伪条件。

Reject 只停止当前公司的研究。Industry Thesis 和 Profit Pool 可以保留，并选择其他候选公司。

## Dependency

- **输入来自：** Industry Value Chain Analyzer；
- **输出给：** Earnings & Valuation Analyzer；
- **多公司比较：** 同一 Industry Value Chain 输出可以分别调用多个 Company Alpha Analyzer 实例；
- **可被触发：** Investment Thesis Monitor 在产品、客户、份额、成本、管理执行或竞争位置变化时重新调用。

---

# 7. Skill 4 — Earnings & Valuation Analyzer

## Purpose

将产业和公司变化转化为自主盈利判断，识别与市场预期之间的差异，并判断当前价格是否提供足够赔率。

该 Skill 同时处理“价值判断”和“价格判断”，但必须保留 Earnings & Variant Gate 与 Valuation & Liquidity Gate。

## Investment Question

> 市场是否低估公司未来盈利，当前价格是否仍未充分反映这一变化，并提供足够风险收益比？

内部包含：

1. **Earnings & Variant Judgment：** 是否存在有证据支持的盈利预期差；
2. **Valuation & Liquidity Judgment：** 当前价格和流动性是否支持投资。

## Input

- Industry Value Chain Analyzer 的产业与利润池输出；
- Company Alpha Analyzer 的 Handoff Package；
- Market & Opportunity Scanner 的 Market State、Risk Level 和流动性背景；
- 公司历史收入、利润率、利润和现金流；
- 销量、单价、份额、产品结构、成本和费用；
- 公司指引及经营信息；
- 分析师一致预期；
- 市场主流叙事；
- 当前价格可能隐含的盈利预期；
- 当前价格、市值和估值信息；
- 历史及行业可比估值；
- 日常成交和预期仓位的进入、退出难度；
- 关键变量的验证时间。

## Reasoning Process

### Step 1 — 确认事实

- 确认历史财务、经营数据、公司指引、当前价格和估值；
- 区分分析师一致预期、市场主流叙事和价格隐含预期；
- 确认流动性和成交条件。

### Step 2 — 识别变化

- 识别需求、销量、价格、份额、成本、产品结构和利润率变化；
- 判断市场盈利预期和估值相对历史发生了什么变化；
- 识别变化的幅度、方向和兑现时间。

### Step 3 — 判断商业影响

- 将 Industry Thesis、Profit Pool 和 Company Alpha 映射到订单、收入来源和竞争位置；
- 判断商业变化能否持续；
- 识别对盈利最敏感的变量。

### Step 4 — 判断盈利影响

按以下顺序推导：

> 需求 → 销量 → 单价 → 收入 → 利润率 → 利润 → 现金流

必须形成：

- Bull Earnings Scenario；
- Base Earnings Scenario；
- Bear Earnings Scenario；
- 自主盈利判断；
- 与市场预期的差异；
- 自己可能判断错误的原因；
- 预期差验证时间表。

### Step 5 — 判断市场定价影响

- 判断当前价格已经反映多少乐观或悲观预期；
- 将 Bull、Base、Bear 盈利情景映射到价值区间；
- 比较当前、历史和同行估值；
- 判断盈利增长能否消化估值；
- 判断 Upside、Downside 和 Risk Reward；
- 判断流动性是否支持预期进入和退出；
- 识别估值重估需要的 Catalyst。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### Earnings & Variant 专业输出

- **Consensus：** 分析师一致预期；
- **Market Narrative：** 市场主流认知；
- **Priced-In Earnings Expectation：** 当前价格可能隐含的盈利假设；
- **Own Earnings View：** 自主盈利判断；
- **Bull / Base / Bear Earnings Scenarios：** 三种盈利情景；
- **Earnings and Cash Flow Bridge：** 盈利与现金流传导；
- **Variant Source：** 预期差来源；
- **Variant Magnitude：** 预期差幅度；
- **Why Market May Be Wrong：** 市场可能错误的原因；
- **Why Own View May Be Wrong：** 自主判断可能错误的原因；
- **Validation Timeline：** 预期差验证时间；
- **Earnings & Variant Decision：** Pass / Recheck / Reject。

### Valuation & Liquidity 专业输出

- **Current Valuation Status：** 当前估值状态；
- **Priced-In Expectations：** 当前价格反映的增长与确定性；
- **Bull / Base / Bear Value Range：** 三种价值情景；
- **Upside：** 判断正确时的潜在上行；
- **Downside：** 判断错误时的潜在下行；
- **Risk Reward：** 风险收益比；
- **Liquidity Constraint：** 流动性限制；
- **Re-rating Conditions：** 重新定价条件；
- **Valuation & Liquidity Decision：** Pass / Recheck / Reject；
- **Reject Scope：** 无预期差 / 当前价格无赔率 / 流动性不支持。

## Decision Rules

### Earnings & Variant Judgment

#### Pass

- 存在对公司价值有实质影响的预期差；
- 自主判断由产业、公司和经营事实推导；
- 能解释市场为什么可能错误；
- 验证变量和时间明确。

#### Recheck

- 自主盈利方向可能正确，但差异幅度不清；
- 市场预期基准无法可靠识别；
- 预期差尚未传导至盈利；
- 验证时间过长或节点不明确。

#### Reject

- 自主判断与市场预期没有实质差异；
- Own View 缺少证据；
- 盈利推导与现金流或经营事实矛盾；
- 核心预期差已经被证伪。

### Valuation & Liquidity Judgment

#### Pass

- 当前价格仍未充分反映自主盈利判断；
- 上下行情景能够对应明确基本面条件；
- Risk Reward 足以支持进入 Timing 判断；
- 流动性支持合理进入和退出。

#### Recheck

- 公司价值可能增长，但当前价格接近合理区间；
- 估值对少数变量过度敏感；
- 上下行接近或流动性存在不确定性；
- 需要等待价格、盈利或预期变化。

#### Reject

- 当前价格已经反映或超过 Bull Case；
- 判断正确时的收益仍不足以补偿下行；
- 流动性不支持合理进入和退出；
- 核心估值假设已被证伪。

### 综合 Stage Decision

- 两个子判断均 Pass，综合结果才能 Pass；
- 任一子判断 Recheck，综合结果通常为 Recheck；
- Earnings & Variant Reject 表示不存在当前主动投资优势，可转为 Observe；
- Earnings & Variant Pass 但 Valuation Reject 表示公司逻辑成立、当前价格无机会，应等待赔率变化。

## Dependency

- **输入来自：** Company Alpha Analyzer，并同时使用 Industry Value Chain 和 Market Scanner 的相关输出；
- **输出给：** Timing & Portfolio Manager；
- **独立调用：** 若用户只问估值，必须具有有效的 Industry、Company Alpha 和 Earnings 上游结论，否则 Recheck；
- **可被触发：** Investment Thesis Monitor 在财报、订单、价格、成本、市场预期、估值或流动性变化时重新调用。

---

# 8. Skill 5 — Timing & Portfolio Manager

## Purpose

判断市场是否开始确认投资逻辑，并把逻辑强度、确定性、赔率、市场环境、趋势和流动性转化为投资状态与仓位方向建议。

该 Skill 不预测最低点，不执行交易。

## Investment Question

> 基本面逻辑是否开始获得市场确认，当前应处于什么投资状态，并承担多大方向性的风险？

内部包含：

1. **Trend & Timing Judgment：** 当前是否是合适行动时点；
2. **Portfolio Judgment：** 当前状态和仓位方向应如何表达判断强度。

## Input

- Market & Opportunity Scanner 的 Market State、Risk Level 和 Recommended Risk Exposure；
- Industry Value Chain Analyzer 的产业、利润池、风险和 Catalyst；
- Company Alpha Analyzer 的公司竞争优势、增长引擎和证伪条件；
- Earnings & Valuation Analyzer 的预期差、价值区间、Upside、Downside、Risk Reward 和 Liquidity Constraint；
- 长期年线、季线和价格结构；
- 中期60日趋势、高低点和相对强弱；
- 短期成交、突破和回踩；
- Catalyst 前后的价格和成交反应；
- 当前投资状态、持仓和投资者风险边界，如有。

## Reasoning Process

### Step 1 — 确认事实

- 汇总上游投资逻辑、关键假设、证伪条件和风险收益比；
- 确认长期、中期、短期价格与成交事实；
- 确认当前 Market Regime、流动性和持仓背景。

### Step 2 — 识别变化

- 判断趋势从弱到强、从强到弱或保持原状态；
- 判断 Catalyst 后价格反应是否与基本面一致；
- 判断投资逻辑、赔率和市场环境相对上次决策发生了什么变化。

### Step 3 — 判断商业影响

- 趋势本身通常不改变商业价值，必须明确它只验证市场认知；
- 若价格行为与基本面持续冲突，识别是否可能存在尚未发现的商业变化；
- 不允许由股价反推 Company Alpha。

### Step 4 — 判断盈利影响

- 检查趋势和 Catalyst 是否与 Earnings Validation Timeline 一致；
- 判断市场是在交易真实盈利变化，还是纯粹交易流动性和风险偏好；
- 保留盈利判断的独立性。

### Step 5 — 判断市场定价和投资状态

- 判断市场是否开始交易预期差；
- 形成 Observe、Trial Position、Buy、Hold、Add、Reduce 或 Sell；
- 将逻辑完整度、置信度、Risk Reward、Market Regime、趋势和流动性转化为仓位方向；
- 明确状态升级、降级和退出条件；
- 将所有交易相关结论提交投资者最终决定。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### Trend & Timing 专业输出

- **Long-Term Trend Status：** 长期趋势；
- **Medium-Term Trend Status：** 中期趋势；
- **Short-Term Confirmation：** 短期成交、突破和回踩；
- **Fundamental–Price Alignment：** 基本面与市场行为是否一致；
- **Market Recognition Status：** 市场是否开始交易投资逻辑；
- **Observe Condition：** 观察条件；
- **Trial Position Condition：** 试仓条件；
- **Entry Condition：** 买入条件；
- **Add Condition：** 加仓条件；
- **Reduce Condition：** 减仓条件；
- **Exit Condition：** 退出条件；
- **Trend & Timing Decision：** Pass / Recheck / Reject。

### Portfolio 专业输出

- **Recommended State：** Observe / Trial Position / Buy / Hold / Add / Reduce / Sell；
- **Position Direction：** 仓位方向；
- **Position Rationale：** 为什么该状态合理；
- **Supporting Evidence：** 支持该状态的核心证据；
- **Main Risks：** 当前最重要风险；
- **Upgrade Conditions：** 提高投资状态的条件；
- **Downgrade Conditions：** 降低投资状态的条件；
- **Portfolio Exit Conditions：** 仓位层面退出条件；
- **Unresolved Conflicts：** 未解决的跨 Skill 冲突；
- **Human Decision Required：** 必须由投资者判断的事项；
- **Portfolio Decision：** Pass / Recheck / Reject。

## Decision Rules

### Trend & Timing Judgment

#### Pass

- 长期或中期趋势与基本面逻辑一致；
- Catalyst 后的价格与成交反应支持重新定价；
- Entry 或 Add 条件能够客观描述。

#### Recheck

- 基本面成立但趋势尚未确认；
- 长、中、短周期信号冲突；
- Catalyst 后的市场反应不明确；
- 通常对应 Observe 或 Trial Position。

#### Reject

- 当前趋势显著恶化并触发预设 Exit Condition；
- 市场对关键利好持续负面反应；
- 当前行动时点被否定。

Trend Reject 不自动否定基本面。如果异常可能来自未知基本面变化，应触发相关上游 Skill Recheck。

### Portfolio Judgment

#### Pass

- 核心产业—公司—盈利—定价因果链完整；
- 当前状态与 Risk Reward、Market Regime、趋势和流动性一致；
- 升级、降级和退出条件明确。

Pass 可以对应有充分依据的 Observe、Buy、Hold、Add、Reduce 或 Sell。

#### Recheck

- 关键上游 Skill 为 Recheck；
- 基本面、估值和趋势存在未解决冲突；
- 缺少形成仓位方向所需的持仓或风险边界；
- 不得给出高强度仓位建议。

#### Reject

- 决定性上游结论为 Reject；
- Risk Reward 不支持持仓；
- 核心证伪条件已触发；
- 当前不得建立或增加风险，建议只能是 Observe、Reduce 或 Sell。

### 综合 Stage Decision

- 两个子判断都能够形成可靠结论时，综合结果可以 Pass；
- 基本面和估值成立但趋势未确认时，综合结果可以 Recheck，状态为 Observe 或 Trial Position；
- 当前行动时点 Reject 不等于永久否定公司；
- 所有交易相关输出都只是建议，必须保留 Human Decision Required。

## Dependency

- **输入来自：** Market & Opportunity Scanner、Industry Value Chain Analyzer、Company Alpha Analyzer、Earnings & Valuation Analyzer；
- **输出给：** Workflow 汇总 Investment Memo，并成为 Investment Thesis Monitor 的基准输入；
- **独立调用：** 若用户直接询问“现在能不能买”或“可以买多少”，必须具有有效上游投资逻辑，否则 Recheck；
- **可被触发：** Investment Thesis Monitor 在趋势、Catalyst、Risk Reward 或 Market Regime 变化时重新调用。

---

# 9. Skill 6 — Investment Thesis Monitor

## Purpose

持续比较实际事实与原始投资逻辑，判断逻辑是 Strengthened、Unchanged、Weakened 还是 Invalidated，并触发受影响 Skill 重新运行。

该 Skill 是独立长期跟踪能力，不重新发明投资逻辑，也不覆盖原始假设。

## Investment Question

> 新事实如何改变原始投资逻辑，最早影响了哪个判断环节，当前投资状态是否需要更新？

## Input

- 原始或最近一次 Investment Memo；
- 五个主链 Skill 的 Core Conclusion；
- 原始 Supporting Facts；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Earnings Validation Timeline；
- 当前 Recommended State 和状态调整条件；
- 新出现的产业、竞争、公司、财务、估值、Catalyst、趋势或市场事实；
- 当前价格和市场预期变化；
- 当前投资状态和投资者新增问题。

没有原始 Investment Memo 或等价的基准投资逻辑时，本 Skill 不得生成“变化判断”，必须 Recheck 并要求先建立基准。

## Reasoning Process

### Step 1 — 确认新事实

- 记录自上次 Memo 以来的新事实；
- 不先把新事实分类为利多或利空；
- 确认发生时间和信息可靠性。

### Step 2 — 比较变化

- 原始判断是什么；
- 原本预期在当前时点看到什么；
- 实际发生了什么；
- 差异来自正常波动、时间延迟还是逻辑变化；
- 哪个 Key Assumption、Falsification Condition 或 Verification Metric 被影响。

### Step 3 — 判断商业影响

- 新事实是否改变产业需求、供给、生命周期或利润池；
- 是否改变公司竞争优势、客户、份额、价格或商业模式；
- 定位最早受到影响的 Skill。

### Step 4 — 判断盈利影响

- 新事实是否改变销量、单价、收入、利润率、利润或现金流；
- Own Earnings View 和 Variant 是否需要调整；
- 原 Validation Timeline 是否仍然有效。

### Step 5 — 判断市场定价和状态影响

- 当前价格隐含预期是否变化；
- Catalyst 是否兑现、失败或延迟；
- 趋势是否确认或否定新事实；
- Risk Reward 和 Recommended State 是否需要变化；
- 触发最早受影响 Skill 及其全部下游 Skill 重跑。

## Required Output

### 统一输出

- Core Conclusion；
- Supporting Facts；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### 专业输出

- **Thesis Status：** Strengthened / Unchanged / Weakened / Invalidated；
- **New Facts：** 新发生事实；
- **Expected vs Actual：** 原预期与实际变化；
- **Changed Assumptions：** 被强化、弱化或证伪的假设；
- **Triggered Falsification Conditions：** 已触发的证伪条件；
- **Affected Skill：** 最早受影响的 Skill；
- **Affected Downstream Chain：** 需要重跑的下游 Skill；
- **Updated Earnings Implication：** 盈利影响；
- **Updated Pricing Implication：** 市场定价影响；
- **Updated State Recommendation：** 更新后的投资状态方向；
- **Next Review Trigger：** 下一次强制复核事件；
- **Human Decision Required：** 需要投资者判断的事项。

## Decision Rules

### Pass

- Thesis Status 为 Strengthened 或 Unchanged；
- 新事实与核心因果链一致；
- 没有触发关键证伪条件；
- 当前状态仍有充分依据。

### Recheck

- Thesis Status 为 Weakened；
- 新事实与原判断冲突，但尚不能确认逻辑失效；
- Catalyst 延迟或指标偏离，但原因尚未确认；
- 必须重跑一个或多个受影响 Skill。

### Reject

- Thesis Status 为 Invalidated；
- 一个或多个核心假设已被证伪；
- 产业、利润池、Company Alpha、盈利预期差或重新定价逻辑发生决定性断裂；
- 必须触发 Timing & Portfolio Manager 形成 Reduce 或 Sell 建议。

## Dependency

- **输入来自：** Workflow 汇总的 Investment Memo，以及全部五个主链 Skill 的历史输出；
- **输出给：** 最早受影响的 Skill；
- **回流方式：** 重跑受影响 Skill 以及它后面的所有 Skill，最后重新调用 Timing & Portfolio Manager；
- **终点：** Workflow 汇总 Updated Investment Memo，作为下一次 Monitoring 的新基准；
- **权限边界：** 输出更新建议，不自动执行 Reduce 或 Sell。

---

# 10. Invocation Routes

## 10.1 当前有哪些行业值得研究

> Market & Opportunity Scanner  
> ↓  
> 候选行业池  
> ↓  
> Industry Value Chain Analyzer 对候选行业逐一验证  
> ↓  
> 形成通过产业逻辑和利润池判断的行业  
> ↓  
> 如需具体股票，进入 Company Alpha Analyzer

输出区分：

- 值得关注的行业；
- 值得深度研究的行业；
- 产业逻辑成立但利润池不清的行业；
- 已经存在候选公司的产业机会。

行业层面 Pass 不直接等于股票 Buy。

## 10.2 分析指定股票

> Market & Opportunity Scanner  
> ↓  
> Industry Value Chain Analyzer  
> ↓  
> Company Alpha Analyzer  
> ↓  
> Earnings & Valuation Analyzer  
> ↓  
> Timing & Portfolio Manager

## 10.3 比较同一行业的多家公司

共享一次 Market & Opportunity Scanner 和 Industry Value Chain Analyzer 输出；每家公司分别运行：

> Company Alpha Analyzer  
> ↓  
> Earnings & Valuation Analyzer  
> ↓  
> Timing & Portfolio Manager

不得因为公司属于同一行业而共享 Company Alpha、预期差或估值结论。

## 10.4 判断估值贵不贵

如果存在有效的 Industry Value Chain 和 Company Alpha 输出，可以单独调用 Earnings & Valuation Analyzer。

如果上游逻辑不存在或已过期，必须从相应上游 Skill 开始，不能只看估值倍数。

## 10.5 判断现在能否买入或加仓

必须具有前四个主链 Skill 的有效输出，再调用 Timing & Portfolio Manager。

没有完整基本面和赔率结论时，不得仅凭趋势输出 Buy 或 Add。

## 10.6 更新已有投资逻辑

> Investment Thesis Monitor  
> ↓  
> 定位最早受影响 Skill  
> ↓  
> 重跑该 Skill 及下游  
> ↓  
> Timing & Portfolio Manager 更新状态

---

# 11. Scenario Coverage

| 用户场景 | 首次调用 | 后续路径 | 主要输出 |
|---|---|---|---|
| 当前有哪些行业值得研究 | Market & Opportunity Scanner | Industry Value Chain Analyzer | 候选行业、产业逻辑和利润池 |
| 从某产业寻找股票 | Market & Opportunity Scanner | Industry Value Chain → Company Alpha | 受益环节和候选公司 |
| 完整分析一家公司 | Market & Opportunity Scanner | 完整主链 | 完整研究结论和投资状态 |
| 判断公司竞争优势 | Company Alpha Analyzer | 必要时补齐 Industry Value Chain | Company Alpha及其持续性 |
| 判断业绩是否可能超预期 | Earnings & Valuation Analyzer | 必要时补齐上游 | Own View、预期差和验证时间 |
| 判断股票贵不贵 | Earnings & Valuation Analyzer | 必要时补齐盈利和上游 | 价值区间、Upside、Downside、Risk Reward |
| 判断现在能否买入 | Timing & Portfolio Manager | 必须使用完整上游结论 | Observe / Trial / Buy等状态 |
| 判断已有持仓是否加减仓 | Investment Thesis Monitor | 受影响 Skill → Timing & Portfolio | Updated State Recommendation |
| 财报后更新投资逻辑 | Investment Thesis Monitor | Earnings & Valuation → Timing & Portfolio | Strengthened / Weakened等 |
| 政策或产业数据变化 | Investment Thesis Monitor | Industry Value Chain及下游 | 更新后的产业和公司结论 |
| 股价与基本面明显冲突 | Investment Thesis Monitor | 定位原因，必要时回到上游 | Recheck、Reduce或Sell建议 |
| 生成 Investment Memo | Workflow 汇总 | 不调用独立 Memo Skill | 汇总所有已有 Skill 输出 |

---

# 12. MVP Acceptance Criteria

六个 Skill 只有满足以下条件，才算能够执行 Investment Framework：

1. Market & Opportunity Scanner 能区分市场风险环境和具体机会，不用热点代替价值变化；
2. Industry Value Chain Analyzer 能分别判断产业价值创造与利润池归属；
3. Company Alpha Analyzer 能证明公司为何获得产业利润，而不是只描述公司优点；
4. Earnings & Valuation Analyzer 能把产业和公司变化落到盈利、预期差、当前价格与赔率；
5. Timing & Portfolio Manager 能把趋势作为市场验证，而不是替代基本面，并只输出研究层面的仓位建议；
6. Investment Thesis Monitor 能定位最早发生变化的 Skill，而不是事后重写整套故事；
7. 每个 Skill 都能输出 Bull Case、Bear Case、Key Assumptions、Falsification Conditions、Verification Metrics 和 Catalyst / Timing；
8. Recheck 与 Reject 不会在下游被隐藏；
9. 六个 Skill 可以分别调用，也可以通过 Handoff Package 顺序连接；
10. 最终交易始终由投资者决定。

这套六 Skill 体系覆盖的完整投资逻辑是：

> 发现市场与产业变化  
> ↓  
> 验证产业价值和利润流向  
> ↓  
> 判断公司是否具有 Alpha  
> ↓  
> 推导盈利、预期差、估值和赔率  
> ↓  
> 用趋势确认时点并形成投资状态  
> ↓  
> 持续跟踪事实，强化、弱化或证伪原始逻辑

它是个人 Investment Agent 的最小核心研究能力集合，不是股票分析模板，也不是机构化投资系统。

---

# 13. v1.1 Skill Contract Amendments

本节是对 v1.0 Skill Specification 的规范性增强。它不增加 Skill，不改变六个 Skill 的依赖链；若本节与前文存在差异，以本节为准。

## 13.1 Shared Records

六个 Skill 共享以下记录。记录由上游创建，由下游补充和验证，不允许每个 Skill 独立重写而不保留版本变化。

### Investment Trigger Record

由 Market & Opportunity Scanner 或 Workflow Research Brief 创建：

```text
Trigger Type
Trigger Event
Why Now
Affected Variables
Potential Beneficiaries
Initial Research Hypothesis
Market Awareness
```

Trigger Type 可以是 User-specified、Event-driven、Industry-scan 或 Thesis-update。没有可验证事件时必须标记 User-specified 或 Unknown，不得倒推催化剂。

### Narrative Record

由 Industry Value Chain Analyzer 初建，由 Company Alpha、Earnings & Valuation、Timing & Portfolio 更新：

```text
Current Market Narrative
Potential Narrative Shift
Narrative Gap
Required Evidence
Narrative Risk
```

Narrative 必须由事实、经营指标和盈利传导支撑，不能把主题热度直接当作投资逻辑。

### Expectation Record

由 Earnings & Valuation Analyzer 维护：

```text
Market View
Agent View
Variant Source
Evidence
Invalidation
```

Market View 不是简单引用新闻，而是对市场当前增长、利润、估值和主要风险假设的结构化总结。Agent View 必须给出独立判断和关键变量。

### Scenario Valuation Record

由 Earnings & Valuation Analyzer 创建，Timing & Portfolio 使用：

```text
Scenario: Bull / Base / Bear
Revenue Drivers
Margin Drivers
EPS / FCF
Valuation Method and Multiple
Implied Value Range
Upside / Downside
Confidence
```

如果无法建立合理的自主盈利判断或估值区间，Stage Decision 最高为 Recheck，不得用精确目标价掩盖不确定性。

### Portfolio and Sell Record

由 Timing & Portfolio Manager 创建，Investment Thesis Monitor 更新：

```text
Portfolio Context: Known / Unknown
Current Exposure
New Exposure
Risk Factor Contribution
Position State
Sell Type
Evidence
Required Action
Re-entry Condition
```

## 13.2 Common Reasoning Addendum

每个 Skill 的推理仍必须遵循：

```text
事实 → 变化 → 商业影响 → 盈利影响 → 市场定价影响
```

但 v1.1 进一步要求所有“变化”至少与以下一个基准比较：

- 历史实际值；
- 市场一致预期；
- 股价隐含预期；
- 原始 Investment Thesis 假设。

每个专业输出还必须标注：

- Fact / Inference / Assumption / Unknown；
- 数据截止时间；
- 关键变量的预期方向；
- 如果验证失败，对下游判断的影响。

## 13.3 Six-Skill Amendment Map

### Skill 1 — Market & Opportunity Scanner

新增专业输出：

- Investment Trigger Record；
- Market Awareness；
- Research Priority；
- Value Change Hypothesis；
- 市场是否允许承担 Beta 的判断；
- 进入深度研究的最小验证问题。

它只负责发现和筛选机会，不得因为市场强势或题材热度直接输出 Buy。

### Skill 2 — Industry Value Chain Analyzer

新增专业输出：

- Current Market Narrative；
- Potential Narrative Shift；
- Narrative Gap；
- Demand Growth vs Effective Supply Growth；
- Bottleneck；
- Pricing Power；
- Profit Elasticity Variable；
- Industry Lifecycle；
- Profit Pool Migration；
- Required Evidence。

必须明确：产业增长是否会被扩产、价格战或成本上升吞掉。

### Skill 3 — Company Alpha Analyzer

新增专业输出：

- One-line Business Model；
- Revenue Driver Tree；
- Profit Driver Tree；
- Peer Comparison；
- Share / Price / Cost / Customer / Channel / Technology Advantage；
- Structural vs Temporary Advantage；
- 公司获得产业利润的传导链。

必须回答：为什么是这家公司，而不是同行。

### Skill 4 — Earnings & Valuation Analyzer

新增专业输出：

- Market View；
- Agent View；
- Variant Source；
- Independent Earnings View；
- Consensus / Implied Expectation；
- Scenario Valuation Record；
- Shareholder Return；
- Liquidity / Rate / FX Context；
- Upside / Downside / Risk Reward；
- Invalidation。

必须把产业和公司变化落到收入、利润率、EPS 或自由现金流。没有自主盈利判断、预期差或赔率时，分别输出对应的 Recheck 原因。

### Skill 5 — Timing & Portfolio Manager

新增专业输出：

- Why Now；
- Catalyst Status：未发生 / 正在发生 / 已定价 / 失败；
- Trend Confirmation：长期均线、关键平台、相对强弱、成交量或资金承接；
- Portfolio Context；
- Position State：Observe / Trial / Core / Reduce / Exit；
- Sell Type：Thesis Invalidated / Valuation Exhaustion / Trend Failure；
- Required Action；
- Re-entry Condition。

价格下跌不是自动加仓理由。Trend Failure 不能仅由单日波动触发，必须结合关键价格结构、持续时间和风险收益比判断。

### Skill 6 — Investment Thesis Monitor

新增专业输出：

- 原始假设 vs 当前事实；
- 变量偏差及其对 EPS / FCF / 估值的影响；
- Narrative Status：Strengthened / Unchanged / Weakened / Invalidated；
- Position State 变化；
- Sell Type；
- 触发重跑的 Skill；
- 错误归因：产业、公司、盈利、估值、时点或仓位。

## 13.4 Gate and State Rules

### Research Pass 不等于 Buy

Pass 只表示当前研究阶段的因果链足以进入下一阶段。只有当上游结论、预期差、赔率、趋势和组合约束同时满足，才允许进入 Trial 或更高状态。

### Portfolio Context Unknown

没有用户持仓、成本、最大回撤和集中度时：

- Portfolio Context = Unknown；
- 不输出个性化仓位比例；
- 只能输出研究级 Position State 和需要补充的信息。

### Sell Type Actions

| Sell Type | 默认动作 |
|---|---|
| Thesis Invalidated | Exit / Reject |
| Valuation Exhaustion | Reduce / Hold |
| Trend Failure | Recheck / Reduce |

每种动作都必须给出证据、置信度和重新进入条件。

## 13.5 Minimum Decision Card

Workflow 汇总 Skill 输出时，必须在完整 Memo 前提供一页式 Decision Card：

```text
Investment Trigger
One-line Thesis
Current Market Narrative
Potential Narrative Shift
Core Variant
Key Earnings Drivers
Bull / Base / Bear Value Range
Why Now
Current Position State
Add Conditions
Reduce / Exit Conditions
Next Verification Date and Metrics
```

Decision Card 只能汇总 Skill 已有结论，不产生新的投资判断。

## 13.6 v1.1 Acceptance Criteria

六个 Skill 的完整链路必须能够回答：

1. 为什么研究这个机会；
2. 市场当前如何理解它；
3. 未来可能如何重新定义它；
4. 产业利润为什么流向这家公司；
5. Agent 与市场的预期差是什么；
6. 当前价格隐含了什么；
7. Bull/Base/Bear 的风险收益比如何；
8. 什么条件下从 Observe 转 Trial 或 Core；
9. 什么条件下 Reduce 或 Exit；
10. 哪些新事实会触发哪个 Skill 重跑。

# 14. v1.2 Skill Amendments

本版本只增强六个既有 Skill 的输入、推理和输出，不新增 Skill。所有 Skill 读取 [Decision Presentation v1.2](</Users/bella/.codex/skills/investment-agent/references/decision-presentation-v1.2.md>)，并以 Evidence Taxonomy 区分事实、变化、推导、假设、假说、决策和 Unknown。

## 14.1 Market & Opportunity Scanner

新增 Investment Trigger、Market Awareness、Industry Cycle 初步假设和候选队列。对“当前哪些行业值得研究”的任务，输出候选池与研究优先级；对单股任务，输出触发器并将相对比较标为 `Not Assessed`。不得把高研究优先级直接转成 Buy。

## 14.2 Industry Value Chain Analyzer

新增 Industry Cycle Position、需求增长与有效供给、瓶颈、定价权、利润弹性、Current Market Narrative、Potential Narrative Shift 和 Required Evidence。输出产业链受益者集合，为后续候选比较提供同口径输入。

## 14.3 Company Alpha Analyzer

新增 Competitive Map：公司、关键竞争者、优势来源、证据、竞争者反制、优势的结构性/暂时性、不可复制原因和利润捕获概率。必须回答“为什么是它而不是竞争者”，并把产业 Beta 与可归因于公司的 Alpha 分开。

## 14.4 Earnings & Valuation Analyzer

新增短期/中期/长期 Market Expectation Decomposition、Market View vs Agent View、Variant Source、Evidence、Invalidation，以及 Implied Expectation Analysis。估值必须反推价格隐含假设，并在 Bull/Base/Bear 与流动性约束下表达，不得将单一公开预测冒充共识。

## 14.5 Timing & Portfolio Manager

新增 Decision Dashboard、Candidate Comparison、Portfolio Context、Opportunity Cost 和三类 Sell Logic：Thesis Invalidated、Valuation Exhaustion、Trend/Recognition Failure。输出状态转移条件和下一次验证条件，不输出自动交易或未经约束的精确仓位。

## 14.6 Investment Thesis Monitor

新增 Thesis Evolution Log 和错误归因。每次更新保留原始基线，比较 Expected vs Actual，记录状态变化、最早受影响的 Skill 和重跑触发器；不得用移动假设来维持原结论。

## 14.7 Common Output Contract

六个 Skill 的关键输出均应包含：Core Conclusion、Bull Case、Bear Case、Key Assumptions、Falsification Conditions、Verification Metrics、Catalyst/Timing、Confidence、Stage Decision，以及本 Skill 的专业输出。最终汇总采用“Decision Dashboard → Evidence Chain → Scenario/Valuation → Conditions → Thesis Evolution”顺序，确保投资者先看到决策重点，再能追溯演绎过程。

## 14.8 v1.2 Presentation and Decision Enhancements

本次增强继续保持六个 Skill，不新增投资理念或独立模块：

1. **中文最终呈现：** Skill 内部继续使用稳定英文键名；最终报告将状态、证据标签、标题和解释性文字转换为中文；
2. **投资核心叙事：** Workflow 汇总前先输出“现实变化 → 产业变化 → 利润池 → 公司受益 → 盈利 → 市场预期 → 隐含预期 → 催化剂 → 趋势 → 状态”；
3. **Alpha Durability：** Company Alpha 增加优势机制、持续性、竞争复制难度、侵蚀条件和验证指标；
4. **Catalyst Priority：** Timing & Portfolio 对催化剂按影响变量、时间窗口、重要性、证据置信度和结果分支排序；
5. **Opportunity Ranking：** 只有存在多个候选与同口径数据时才输出相对排序；单一股票或数据不足时输出“机会排序：未评估”；
6. **Investment Mistake Analysis：** 每份完整 Memo 说明最可能的错误路径、领先指标、影响和应对，区分逻辑失效、估值透支、兑现延迟和市场不认可。

这些要求属于既有 Skill 的内部输出与 Memo 呈现规范，不构成新的 Skill、数据库、交易系统或基金管理流程。

# 15. v1.3 Opportunity Discovery Amendments

## 15.1 不新增 Skill

v1.3 继续保持六个核心 Skill。`Opportunity Radar`、`Granularity Gate` 和 `Investment Opportunity Hypothesis` 是 Workflow 内部能力、数据召回和交接记录，不单独注册为 Skill。

## 15.2 Market & Opportunity Scanner 增强

机会扫描默认采用：

```text
Tushare 结构化快照
→ 观察者03滚动分页
→ 多关键词语义召回
→ 重点主题详情
→ IMA/Report CLI/Web Search 定向补充
→ 交叉验证
```

每个候选必须同时输出：

- 核心观点；
- 支持该观点的事实、基线和变化；
- 商业/盈利/现金流传导；
- 市场当前认知和 Agent View；
- 预期差假设；
- Profit Pool Pre-check；
- 证据等级；
- 证伪条件和验证指标；
- 数据缺口和重开条件。

## 15.3 Granularity Gate

对一级行业、宽泛概念或混合主题：

- 先识别是否存在多个利润池；
- 必要时拆分3—5个细分方向；
- 细分未完成时返回 `Recheck—Subsegment`；
- 所有合理细分均无变化或商业路径时，才返回 `Reject—Current Scope`。

## 15.4 Industry Value Chain 增强

Industry Value Chain Analyzer 必须在行业结论前完成细分层级的利润池预检，明确价值流向、定价权、竞争侵蚀机制和验证时间。它不能把 Scanner 的初步假设当成行业事实，也不能以总市场规模替代利润捕获证据。

## 15.5 投资者呈现

机会发现报告先展示中文 `Opportunity Viewpoint Card`：

```text
核心观点
→ 为什么现在
→ 数据支撑
→ 推导链
→ 市场当前认知
→ Agent 潜在不同判断
→ 利润池预检
→ 主要风险
→ 下一步验证
→ 阶段决策
```

证据标签继续使用事实、变化、推断、关键假设、待验证假设、决策和未知；内部英文键名仅用于实现交接。
