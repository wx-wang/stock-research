# Investment Agent Workflow v1.3

## Personal Investment Research Agent — MVP Research Workflow

**Workflow Version:** v1.3  
**Framework Source:** Investment Decision Framework v1.1  
**适用市场:** A股、港股  
**目标:** 将个人投资理念转化为 Agent 可以启动、顺序执行、中止、汇总和持续跟踪的研究流程。

本 Workflow 服务于个人投资 Agent MVP，不是基金运营系统，不模拟投资团队，不包含代码、数据库、UI或自动交易设计。

Agent 负责：

- 发现股票研究机会；
- 整理产业、公司、财务、估值与市场信息；
- 构建并检验投资逻辑；
- 识别风险和反方解释；
- 生成 Investment Memo；
- 跟踪投资逻辑并更新建议。

Agent 不负责：

- 自动下单或执行交易；
- 替代投资者承担最终判断责任；
- 预测短期价格或最低点；
- 构建基金管理、团队协作或运营流程。

---

# 1. Workflow Overview

## 1.1 核心决策链

每项完整研究必须围绕以下八阶段核心决策链执行：

> Market Regime  
> ↓  
> Industry Thesis  
> ↓  
> Profit Pool  
> ↓  
> Company Alpha  
> ↓  
> Earnings & Variant Perception  
> ↓  
> Valuation & Liquidity  
> ↓  
> Trend & Timing  
> ↓  
> Portfolio Management

前一阶段的结论构成后一阶段的输入。Agent 不得从股价表现或公司故事直接跳到 Buy / Sell，也不得为了完成报告而绕过中间断裂的因果关系。

在八阶段链条之前，机会发现任务还必须经过三个 Workflow 内部层：

```text
Research Trigger
↓
Market Regime
↓
Opportunity Radar
↓
Granularity Gate
↓
Investment Opportunity Hypothesis
↓
Industry Thesis → Profit Pool → Company Alpha → Earnings & Variant Perception
→ Valuation & Liquidity → Trend & Timing → Portfolio Management
```

`Opportunity Radar`、`Granularity Gate` 和 `Investment Opportunity Hypothesis` 是调度与推理层，不是新的独立 Skill，也不改变八阶段核心投资理念。

## 1.2 完整任务生命周期

> 机会或问题进入  
> ↓  
> Task Intake：理解任务、确认对象、建立 Research Brief  
> ↓  
> Research Readiness Gate：判断是否可以启动  
> ↓  
> Market Regime → Opportunity Radar → Granularity Gate → Investment Opportunity Hypothesis  
> ↓  
> 执行八阶段核心决策链的其余阶段  
> ↓  
> Investment Memo Assembly：只汇总已有结论  
> ↓  
> Human Decision：投资者作出最终决定  
> ↓  
> Monitoring：跟踪事实、假设、催化剂和验证指标  
> ↓  
> 重新运行受影响阶段并更新 Memo

## 1.3 三种任务入口

### A. 指定公司研究

投资者提供股票代码、公司名称或明确标的。

Agent 先确认公司、市场和所属产业，但仍必须从 Market Regime 与 Industry Thesis 开始，不能从公司结论倒推产业逻辑。

### B. 产业机会发现

投资者提供行业、产业主题或观察到的产业变化。

Agent 先运行 Market Regime 和 Opportunity Radar；如果对象过宽，先通过 Granularity Gate 拆分细分方向，再形成 Investment Opportunity Hypothesis。只有通过该内部层，才进入 Industry Thesis、Profit Pool 和后续公司研究。

### C. 已有逻辑更新

投资者提供既有 Investment Memo、持仓标的或新的事实，要求检查逻辑是否变化。

Agent 先进入 Monitoring，定位最早受影响的阶段，再从该阶段向后重新运行，不默认从头重做，也不得覆盖原始判断。

投资者提出的单点问题，例如“估值贵不贵”或“财报是否低于预期”，只决定研究重点，不允许跳过其所依赖的上游结论。若已有有效 Memo，可以复用未发生变化的上游输出；否则运行完整流程。

---

# 2. Research Task Initiation

## 2.1 用户可以提供的输入

一次研究任务可以由以下任一信息启动：

- 股票代码；
- 公司名称；
- 行业或产业主题；
- 已有 Investment Memo；
- 新出现的产业、公司、财务或市场事实；
- 投资者提出的具体问题。

投资者还可以提供：

- 当前是否持有；
- 当前投资状态；
- 已有投资逻辑；
- 最关注的风险；
- 希望验证的关键假设。

除非进入 Portfolio Management，持仓与成本信息不是启动基础研究的必要条件。

## 2.2 Agent 对任务的理解步骤

### Step 1 — 识别研究对象

Agent 必须确认：

- 公司全称；
- 股票代码与交易市场；
- 主营业务；
- 所属产业及产业链位置；
- 若输入为行业，研究边界包含哪些环节。

如果名称、代码或市场存在冲突，必须先 Recheck，不能分析错误对象。

### Step 2 — 识别投资者问题

Agent 将问题改写为一个可以研究和证伪的核心问题，例如：

- 该公司是否正在受益于可持续的产业变化？
- 行业增长的利润是否会流向该公司？
- 当前市场是否低估未来盈利？
- 当前价格是否仍具有足够风险收益比？
- 新事实是否强化或破坏既有投资逻辑？

Agent 不把“这只股票会不会涨”作为有效研究问题，而应转换为价值、预期、重新定价和风险问题。

### Step 3 — 判断任务入口

Agent 将任务确定为：

- 指定公司研究；
- 产业机会发现；
- 已有逻辑更新。

### Step 4 — 确定研究时点

所有结论必须对应明确的 As-of Date。Agent 必须知道研究使用的信息截止到什么时间，避免把不同时间的事实和预期混为一体。

### Step 5 — 识别决策背景

Agent 必须判断本次研究是为了：

- 建立新的观察对象；
- 判断是否可以试仓或买入；
- 复核已有持仓；
- 判断是否加仓、减仓或退出。

如果投资者没有提供持仓信息，Agent 可以完成基础研究，但 Portfolio Recommendation 必须注明“未结合实际持仓约束”。

## 2.3 Research Brief

正式进入研究流程前，Agent 必须形成一份简短的 Research Brief：

| 字段 | 内容 |
|---|---|
| Research Subject | 公司、股票代码或产业主题 |
| Market | A股 / 港股及对应交易市场 |
| As-of Date | 研究信息截止时间 |
| Entry Type | 指定公司 / 产业发现 / 逻辑更新 |
| Investor Question | 投资者原始问题 |
| Research Question | Agent 转换后的可验证问题 |
| Decision Context | Observe / 新建仓判断 / 持仓复核等 |
| Existing Thesis | 投资者已有逻辑，如有 |
| Known Position | 当前持仓状态，如有 |
| Initial Unknowns | 启动前已知的信息缺口 |
| Workflow Route | 完整流程或从既有 Memo 的某阶段继续 |

Research Brief 只定义任务，不预设投资结论。

## 2.4 Research Readiness Gate

### Pass — 进入研究流程

满足以下条件：

- 研究对象或产业边界明确；
- 核心研究问题可以被事实验证；
- As-of Date 明确；
- 任务属于研究、风险分析、Memo 或逻辑跟踪范围；
- 没有阻止研究启动的身份或信息冲突。

### Recheck — 暂不启动

出现以下情况：

- 股票代码、公司名称或市场无法对应；
- 行业范围过宽，无法形成明确问题；
- 投资者问题存在两种以上实质不同的解释；
- 关键既有 Memo 或新事实没有提供；
- 只能回答部分问题，但无法形成完整决策链。

Agent 必须列出缺失信息和最小补充要求。

### Reject — 不进入本 Workflow

出现以下情况：

- 任务要求自动交易或直接下单；
- 任务只要求预测短期价格或最低点；
- 研究对象无法确认且没有合理补充路径；
- 输入不属于股票投资研究或逻辑跟踪范围。

## 2.5 Opportunity Discovery Context

当任务属于“当前有哪些行业、板块或概念值得研究”时，Research Brief 必须额外记录：

| 字段 | 内容 |
|---|---|
| Scan Mode | Snapshot / Rolling Window / Theme Deep Scan |
| Time Window | 7天、30天、90天或任务指定区间 |
| Source Coverage | Tushare、观察者03、IMA、Report CLI、Web Search 的实际覆盖范围 |
| Candidate Granularity | 一级行业、子行业、产业链环节或概念 |
| Subsegment Need | 是否必须先拆分细分方向 |
| Opportunity Type Tag | 仅作描述标签，不作为独立投资流派或自动分类器 |
| Coverage Unknowns | 未能覆盖的时间段、关键词、主题详情和数据缺口 |

机会发现默认使用 `Rolling Window`，而不是只读取最近一页主题。最近30条只适合快速雷达；产业机会扫描应结合分页时间窗口、关键词搜索和重点主题详情。所有搜索结果按 `topic_id` 或来源唯一标识去重，并报告实际覆盖范围。

---

# 3. Common Stage Contract

八个研究阶段使用同一套内部分析纪律。Bull Case、Bear Case、Key Assumptions、Falsification Conditions、Verification Metrics 和 Catalyst / Timing 均为阶段内部要求，不拆成独立模块。

## 3.1 信息分类

每个阶段必须区分：

- **Fact：** 已确认事实；
- **Inference：** 基于事实作出的推断；
- **Assumption：** 尚待验证的假设；
- **Unknown：** 当前缺失但可能改变结论的信息。

## 3.2 因果推演纪律

每个阶段都必须回答与本阶段相关的因果链：

> 什么发生了变化  
> ↓  
> 如何影响产业或公司  
> ↓  
> 如何影响盈利与现金流  
> ↓  
> 当前市场如何定价  
> ↓  
> 什么会推动重新定价

阶段不得为了形成完整叙事而虚构中间关系。某一影响在本阶段不显著时，应明确说明。

## 3.3 Stage Record

每个阶段必须形成以下记录：

| 字段 | 必须回答的内容 |
|---|---|
| Core Conclusion | 对本阶段核心问题的直接回答 |
| Supporting Facts | 结论依赖的已确认事实 |
| Bull Case | 支持结论成立的最强路径 |
| Bear Case | 最有可能推翻结论的反方路径 |
| Key Assumptions | 尚待验证且决定结论的变量 |
| Falsification Conditions | 哪些事实出现时必须承认判断错误 |
| Verification Metrics | 跟踪指标、预期方向和验证时点 |
| Catalyst / Timing | 为什么变化在现在发生或可能被市场认识 |
| Confidence | High / Medium / Low，并解释主要不确定性 |
| Stage Decision | Pass / Recheck / Reject |
| Handoff Package | 传递给下一阶段的标准信息 |

## 3.4 Confidence 与方向分离

Confidence 表示 Agent 对结论的确信程度，不表示看多程度。

- High Confidence 可以对应负面结论；
- Low Confidence 不应被包装成明确的正面建议；
- 存在决定性 Unknown 时不得给出 High Confidence。

---

# 4. End-to-End Research Workflow

## Stage 1 — Market Regime

### 目标

判断当前市场环境是否支持风险暴露，以及后续估值和仓位判断应处于怎样的风险背景。

### 核心问题

> 当前市场环境是否支持风险资产上涨，以及应承担多大的总体风险？

### 输入

- Research Brief；
- 利率、美元及汇率环境；
- 信用环境；
- 市场资金流向；
- 成交量与市场宽度；
- 主要指数趋势；
- 市场风格与风险偏好变化。

### 执行重点

1. 判断流动性正在改善、稳定还是收缩；
2. 判断风险偏好正在上升、稳定还是下降；
3. 判断当前环境主要影响企业盈利，还是主要影响估值与资金行为；
4. 识别市场状态切换的关键指标；
5. 形成总体风险暴露倾向，但不因此否定产业机会。

### 输出

- Market State；
- Liquidity Direction；
- Risk Appetite Direction；
- Risk Level；
- Recommended Risk Exposure；
- Regime Change Triggers；
- 完整 Stage Record。

### Handoff Package

向 Industry Thesis 提供市场背景；同时保留给 Valuation & Liquidity、Trend & Timing 和 Portfolio Management 使用：

- 当前 Market State；
- 风险等级；
- 流动性方向；
- 估值扩张或收缩压力；
- 风险暴露倾向；
- 状态切换条件。

### Gate

- **Pass：** 市场状态能够被可靠描述，可进入 Industry Thesis；
- **Recheck：** 主要指标严重冲突或处于快速切换期，需要降低置信度，但可以继续基础产业研究；
- **Reject：** 仅当关键数据不可用、无法形成任何可靠市场判断时停止本次完整决策输出。

不利的 Market Regime 本身不是对产业机会的 Reject，而是对后续估值容忍度和仓位的限制。

---

## Internal Layer — Opportunity Radar, Granularity Gate and Investment Opportunity Hypothesis

该层只在机会发现或研究对象过宽时启动；指定公司研究也必须记录其 Investment Trigger，但不必机械重复完整市场扫描。

### 目标

把“市场正在关注什么”转化为“哪个细分方向出现了可验证变化，以及为什么可能产生预期差”。

### 执行顺序

1. **Opportunity Radar：** 使用结构化市场数据、滚动时间窗口、关键词搜索和重点主题详情，形成候选方向队列；
2. **Granularity Gate：** 判断候选是否过宽，若一个行业包含多个利润池，先拆分为不超过3—5个可研究细分方向；
3. **Investment Opportunity Hypothesis：** 对每个细分方向建立“产业变化 → 价值迁移 → 受益环节 → 利润池 → 盈利影响 → 市场定价 → 预期差”的初步假设。

### 机会发现证据链

```text
事实
↓
相对基线的变化
↓
商业影响
↓
可能的盈利/现金流影响
↓
市场当前叙事
↓
Agent 的不同判断
↓
验证指标与催化剂
```

### 必须输出

- Opportunity Candidate；
- Candidate Granularity；
- Investment Trigger 与 Why Now；
- Opportunity Radar Coverage：时间窗口、页数、关键词、去重主题数、详情数；
- Core View：Agent 当前的明确观点；
- Supporting Facts：带来源、日期、口径和基线的数据；
- Value Migration Hypothesis：价值向哪个环节迁移；
- Profit Pool Pre-check：可能获得利润的环节及尚未确认的地方；
- Market View vs Agent View；
- Variant Hypothesis；
- Bull Case / Bear Case；
- Key Assumptions / Falsification Conditions；
- Verification Metrics / Catalyst / Timing；
- Evidence Level：Radar Only / Narrative Extracted / Cross-Validated；
- Missing Inputs；
- Stage Decision；
- Handoff Package。

### Granularity Gate

- **通过：** 研究对象已经足够具体，或至少一个细分方向具备独立的变化、商业路径和验证指标；
- **需要复核—细分层级：** 一级行业或概念内部存在多个利润池，尚未完成拆分；
- **需要复核—数据缺口：** 细分方向可能成立，但缺少决定性事实或详情内容；
- **不通过—当前范围：** 在完成合理细分后，所有候选方向都没有实质变化或商业传导路径。

一级行业不能因为总体表现弱、估值不便宜或最新主题较少而直接被排除；必须先判断是否存在尚未覆盖的细分方向。

### Handoff Package

只将通过 Granularity Gate 且至少形成初步机会假设的细分方向交给 Industry Thesis。下游必须把该假设当作待验证输入，不得当作已确认的产业结论。

---

## Stage 2 — Industry Thesis

### 目标

判断未来3—5年是否存在能够创造新增价值的产业变化，以及变化是否正在当前阶段发生。

### 核心问题

> 未来3—5年，什么产业变化会创造新增价值？

### 输入

- Research Brief；
- Market Regime 的市场背景；
- Opportunity Radar / Granularity Gate / Investment Opportunity Hypothesis Handoff Package；
- 已确认的候选细分方向和来源覆盖记录；
- 技术、成本、政策、消费和应用场景变化；
- 需求规模、增速和渗透率；
- 供给、产能、资源和进入条件；
- 产业生命周期；
- 市场当前对产业的主流认知。

### 执行重点

1. 识别需求增长的真实来源；
2. 判断供给是否容易增加，是否存在瓶颈和议价权；
3. 判断产业处于萌芽、渗透、高增长、成熟还是衰退阶段；
4. 区分结构性变化与短期波动；
5. 回答为什么变化在当前阶段发生；
6. 明确产业逻辑如何可能传导到收入、利润和现金流。

### 输出

- One-Sentence Industry Thesis；
- Demand Drivers；
- Supply Constraints；
- Lifecycle Stage；
- Industry Value Creation Mechanism；
- Growth Duration；
- Why Now；
- Industry Risks；
- 完整 Stage Record。

### Handoff Package

向 Profit Pool 提供：

- 产业趋势与变化方向；
- 核心需求驱动；
- 供给约束；
- 生命周期与预期持续时间；
- 可能创造的新增价值；
- 关键催化剂；
- 产业风险、证伪条件和验证指标。

### Gate

- **Pass：** 存在可验证且能够创造价值的产业变化，因果链和 Why Now 基本成立；
- **Recheck：** 方向可能成立，但需求真实性、供给弹性、持续时间或关键指标尚未确认；
- **Reject：** 不存在实质产业变化，变化无法创造商业价值，或核心产业假设已被证伪。

Industry Thesis Reject 时，停止沿原逻辑继续研究该投资机会。若输入为指定公司，可以形成 Rejection Memo；若输入为产业发现，则停止在该产业中寻找公司。

---

## Stage 3 — Profit Pool

### 目标

判断产业创造的新增价值最终流向产业链哪个环节，以及目标公司所处位置是否可能受益。

### 核心问题

> 行业增长创造的钱最终流向哪里？

### 输入

- Industry Thesis Handoff Package；
- 上游、中游、下游产业链结构；
- 各环节供需、价格和利润率；
- 产能、成本曲线和进入条件；
- 各环节议价权；
- 市场份额和竞争变化；
- 目标公司产业链位置，如已有指定公司。

### 执行重点

1. 描述产业链价值分布；
2. 判断哪个环节最稀缺并拥有定价权；
3. 判断利润率正在向哪里迁移；
4. 判断利润改善是结构性还是周期性；
5. 分析供给扩张和竞争是否会侵蚀利润；
6. 识别最受益与最受损环节；
7. 若任务从行业启动，基于价值流向形成候选公司，而不是先按股价表现选股。

### 输出

- Industry Chain Map；
- Current Profit Pool；
- Profit Migration Direction；
- Pricing Power Holder；
- Beneficiary Segments；
- Disadvantaged Segments；
- Alpha-Producing Position；
- Profit Migration Timing；
- 完整 Stage Record。

### Handoff Package

向 Company Alpha 提供：

- 公司所在环节；
- 该环节获得利润的机制；
- 稀缺性和定价权来源；
- 利润率改善路径；
- 主要竞争和供给风险；
- 最可能的赢家与输家；
- 利润迁移的验证时间和指标。

如果任务从行业启动，同时提供依据上述逻辑形成的候选公司清单。每家公司必须分别进入 Company Alpha，不得共享未经验证的公司结论。

### Gate

- **Pass：** 能明确识别新增价值流向，目标环节具有可解释的利润获取能力；
- **Recheck：** 行业增长成立但利润归属不清，或供给和竞争变化尚未稳定；
- **Reject：** 利润不会流向目标公司所在环节，目标环节缺乏定价权，或属于明确受损方。

Profit Pool Reject 时，停止研究当前公司或当前产业链位置；但可以回到本阶段选择另一个受益环节，而不是修改产业逻辑来迁就原公司。

---

## Stage 4 — Company Alpha

### 目标

判断目标公司是否有能力承接产业利润，并获得超过产业平均水平的价值份额。

### 核心问题

> 为什么产业增长的利润会流向这家公司？

### 输入

- Profit Pool Handoff Package；
- 公司产品、服务、客户和应用场景；
- 收入和利润来源；
- 商业模式；
- 技术、成本、客户、规模和品牌优势证据；
- 市场份额及其变化；
- 主要竞争对手情况；
- 销量、单价、产品结构和利润率变化。

### 执行重点

1. 确认公司在产业链和利润池中的位置；
2. 判断竞争优势是否有经营事实支持；
3. 判断优势是否能够持续，而不是暂时受益于行业景气；
4. 分解收入增长来自市场扩张、份额、销量、单价还是产品结构；
5. 分解利润增长来自收入还是利润率；
6. 与主要竞争对手比较，识别真正的公司 Alpha；
7. 识别公司层面的近期催化剂和证伪条件。

### 输出

- Company Positioning；
- Business Model；
- Company Alpha；
- Competitive Advantage and Durability；
- Growth Engine；
- Revenue Growth Bridge；
- Profit Growth Bridge；
- Relative Competitive Position；
- Company Catalyst；
- Company-Specific Risks；
- 完整 Stage Record。

### Handoff Package

向 Earnings & Variant Perception 提供：

- 公司获得产业利润的具体机制；
- 销量、单价、份额、产品结构和利润率驱动；
- 竞争优势及持续时间假设；
- 相对竞争位置；
- 公司催化剂；
- 公司风险、证伪条件和验证指标。

### Gate

- **Pass：** 公司具有可验证的利润承接能力和至少一项有事实支持的竞争优势；
- **Recheck：** 公司可能受益，但无法区分公司 Alpha 与行业 Beta，或优势持续性尚未验证；
- **Reject：** 公司无法获得产业利润，竞争优势缺少证据，或竞争位置已明显恶化。

Company Alpha Reject 时，停止该公司的深入研究。产业逻辑可以保留，并回到 Profit Pool 选择其他公司。

---

## Stage 5 — Earnings & Variant Perception

### 目标

将产业和公司变化转化为自主盈利判断，并判断市场是否低估了这一变化。

### 核心问题

> 市场是否低估公司未来盈利，以及自己的判断为什么可能比市场更准确？

### 输入

- Industry Thesis、Profit Pool 和 Company Alpha 的 Handoff Package；
- 历史收入、利润率、利润和现金流；
- 销量、单价、份额、产品结构、成本和费用；
- 公司指引和可验证的经营信息；
- 分析师一致预期；
- 市场主流叙事；
- 当前价格可能隐含的预期；
- 关键经营数据和财务验证时间。

### 执行重点

1. 按“需求 → 销量 → 价格 → 收入 → 利润率 → 利润 → 现金流”形成自主推导；
2. 建立 Bull、Base、Bear 三种盈利情景；
3. 区分分析师一致预期、市场主流叙事和价格隐含预期；
4. 明确分歧发生在哪个变量、幅度和时间；
5. 解释市场为什么可能错误，自己为什么可能正确；
6. 主动寻找市场可能正确、自己可能错误的证据；
7. 明确预期差何时被财报或经营数据验证。

### 输出

- Consensus；
- Market Narrative；
- Own Earnings View；
- Bull / Base / Bear Earnings Scenarios；
- Earnings and Cash Flow Bridge；
- Variant Source and Magnitude；
- Why Market May Be Wrong；
- Why Own View May Be Wrong；
- Validation Timeline；
- 完整 Stage Record。

### Handoff Package

向 Valuation & Liquidity 提供：

- 市场预期基准；
- 自主盈利判断及三种情景；
- 预期差来源、幅度和持续时间；
- 盈利与现金流敏感变量；
- 预期差验证时间表；
- 关键催化剂；
- 反方证据、证伪条件和置信度。

### Gate

- **Pass：** 存在对公司价值有实质影响的预期差，且自主判断有产业、公司和经营证据支持；
- **Recheck：** 预期差可能存在，但市场预期基准、差异幅度或兑现时间不清楚；
- **Reject：** 不存在实质预期差，自主判断缺少证据，或盈利与现金流路径被证伪。

Earnings & Variant Perception Reject 时，停止把该公司作为主动投资机会继续推进。好公司但没有预期差，可以保留为 Observe，等待新变化。

---

## Stage 6 — Valuation & Liquidity

### 目标

判断当前价格是否提供足够赔率，以及预期正确时的收益能否补偿判断错误的风险。

### 核心问题

> 好公司现在是否具有好价格？

### 输入

- Earnings & Variant Perception Handoff Package；
- 当前价格、市值和相关估值信息；
- 当前、历史和行业可比估值；
- 盈利增长速度与确定性；
- Market Regime 对流动性和风险偏好的判断；
- 日常成交和价格冲击；
- 计划仓位的进入与退出难度。

### 执行重点

1. 判断当前价格已经反映多少乐观或悲观预期；
2. 将 Bull、Base、Bear 盈利情景映射到合理价值区间；
3. 比较当前估值、历史位置、行业可比和盈利增长匹配度；
4. 计算或描述判断正确时的潜在上涨空间；
5. 描述判断错误时的下行风险；
6. 判断风险收益比是否具有吸引力；
7. 判断成交和流动性是否支持预期仓位进入和退出；
8. 识别估值重估所需催化剂。

### 输出

- Current Valuation Status；
- Priced-In Expectations；
- Bull / Base / Bear Value Range；
- Upside；
- Downside；
- Risk Reward；
- Liquidity Constraint；
- Re-rating Conditions；
- 完整 Stage Record。

### Handoff Package

向 Trend & Timing 提供：

- 当前价格与合理价值区间的关系；
- 上涨与下跌情景；
- 风险收益比；
- 市场已经定价和尚未定价的部分；
- 流动性约束；
- 估值重估条件和催化剂；
- 估值证伪条件。

### Gate

- **Pass：** 当前价格仍存在未充分反映的预期差，且风险收益比和流动性支持继续判断行动时点；
- **Recheck：** 公司价值可能增长，但当前赔率一般、价格接近合理区间或流动性存在不确定性；
- **Reject：** 当前价格已充分反映甚至透支 Bull Case，风险收益比不足，或流动性无法支持合理进入和退出。

Valuation Reject 不否定公司质量，但停止当前买入逻辑。标的可以保留为 Observe，等待价格、盈利或预期发生变化。

---

## Stage 7 — Trend & Timing

### 目标

判断基本面逻辑是否开始获得市场确认，以及当前是否是合适的观察、试仓、买入、加仓或退出时点。

### 核心问题

> 市场是否开始认可投资逻辑？

### 输入

- 完整基本面决策链；
- Valuation & Liquidity Handoff Package；
- 各阶段 Catalyst / Timing；
- 长期年线、季线和价格结构；
- 中期60日趋势、高低点和相对强弱；
- 短期成交、突破和回踩；
- 催化剂前后的价格和成交反应；
- 当前投资状态，如有。

### 执行重点

1. 判断长期价格结构是否支持；
2. 判断中期趋势正在改善、稳定还是恶化；
3. 判断短期突破、成交和回踩是否提供确认；
4. 判断市场是否开始交易产业、盈利或预期差逻辑；
5. 比较基本面催化剂与价格行为是否一致；
6. 形成可观察的 Entry、Add、Reduce 和 Exit Conditions；
7. 不用技术信号替代或重写基本面结论。

### 输出

- Long-Term Trend Status；
- Medium-Term Trend Status；
- Short-Term Confirmation；
- Fundamental–Price Alignment；
- Current Timing State；
- Observe Condition；
- Trial Position Condition；
- Entry Condition；
- Add Condition；
- Reduce Condition；
- Exit Condition；
- 完整 Stage Record。

### Handoff Package

向 Portfolio Management 提供：

- 趋势阶段；
- 市场是否开始确认投资逻辑；
- 催化剂与价格反应是否一致；
- 当前适合的行动状态；
- Entry、Add、Reduce 和 Exit Conditions；
- 趋势失效条件和置信度。

### Gate

- **Pass：** 趋势与基本面方向一致，市场开始确认逻辑，并存在明确行动条件；
- **Recheck：** 基本面成立但趋势尚未确认，或长、中、短周期信号冲突；
- **Reject：** 当前趋势明显否定行动时点、关键利好后价格持续负面反应，或预设退出条件已经触发。

Trend Reject 通常只否定当前行动时点，不自动否定长期基本面。结论进入 Observe；若趋势异常可能反映未知基本面变化，则返回最早可能受影响的阶段 Recheck。

---

## Stage 8 — Portfolio Management

### 目标

把逻辑强度、确定性、预期差、风险收益比、市场环境、趋势和流动性转化为投资状态与仓位方向建议。

### 核心问题

> 当判断正确时应该承担多少风险；当判断错误时如何限制损失？

### 输入

- 前七个阶段的 Core Conclusion、Confidence 和 Stage Decision；
- Market Regime 的风险等级和暴露倾向；
- Earnings & Variant Perception 的预期差及验证时间；
- Valuation & Liquidity 的 Upside、Downside、Risk Reward 和流动性约束；
- Trend & Timing 的行动条件；
- 当前持仓状态与投资者风险边界，如有。

### 执行重点

1. 检查产业—利润池—公司—盈利—定价因果链是否完整；
2. 汇总各阶段关键假设和证伪条件；
3. 判断预期差、赔率和趋势确认强度；
4. 判断 Market Regime 与流动性对风险暴露的限制；
5. 明确跨阶段冲突及其决策优先级，不用平均分掩盖矛盾；
6. 形成 Observe、Trial Position、Buy、Hold、Add、Reduce 或 Sell 建议；
7. 预先定义状态升级、降级和退出条件。

### 输出

- Recommended State；
- Position Direction；
- Position Rationale；
- Supporting Evidence；
- Main Risks；
- Upgrade Conditions；
- Downgrade Conditions；
- Exit Conditions；
- Unresolved Conflicts；
- Human Decision Required；
- 完整 Stage Record。

### 状态定义

- **Observe：** 逻辑值得跟踪，但预期差、估值、催化剂或趋势未满足行动条件；
- **Trial Position：** 核心逻辑初步成立且赔率具有吸引力，但部分假设或趋势仍需验证；
- **Buy：** 产业、利润池、公司、盈利预期差和估值形成闭环，催化剂或趋势支持行动；
- **Hold：** 逻辑仍然成立，关键指标符合预期，预期差尚未完全兑现；
- **Add：** 新证据强化预定义关键假设，且风险收益比仍然合理；
- **Reduce：** 逻辑边际弱化、估值透支、趋势走弱或风险收益比下降；
- **Sell：** 核心假设被证伪、盈利路径破坏、赔率消失或出现不可接受的新风险。

### Gate

- **Pass：** 能形成有完整依据的投资状态和仓位方向，包括有充分依据的 Observe、Reduce 或 Sell；
- **Recheck：** 关键阶段仍为 Recheck、存在未解决冲突，或缺少形成仓位建议的投资者约束；
- **Reject：** 核心因果链已经断裂或证伪，当前不得增加风险，建议只能是 Observe、Reduce 或 Sell。

Portfolio Management 只提供研究建议，不执行交易。任何 Buy、Add、Reduce 或 Sell 都必须进入 Human Decision。

---

# 5. Information Handoff Design

## 5.1 主信息流

| 来源阶段 | 传递的核心信息 | 接收阶段 | 接收阶段使用方式 |
|---|---|---|---|
| Market Regime | 市场状态、流动性、风险等级、风险暴露倾向 | Industry Thesis | 作为产业研究背景，不决定产业成立与否 |
| Opportunity Radar / Granularity Gate / Investment Opportunity Hypothesis | 候选细分方向、触发事实、覆盖范围、初步观点、价值迁移假设、市场叙事、预期差假设、证据等级和数据缺口 | Industry Thesis | 验证产业变化和 Profit Pool，不把初步假设当作事实 |
| Industry Thesis | 产业趋势、驱动、供给、生命周期、风险、验证指标 | Profit Pool | 判断新增价值在产业链中的流向 |
| Profit Pool | 价值分布、稀缺环节、定价权、赢家与输家 | Company Alpha | 判断目标公司是否处于受益位置 |
| Company Alpha | 商业模式、竞争优势、增长引擎、公司风险 | Earnings & Variant Perception | 将产业和公司变化映射到盈利 |
| Earnings & Variant Perception | Consensus、Own View、预期差、情景和验证时间 | Valuation & Liquidity | 判断当前价格反映多少预期及赔率 |
| Valuation & Liquidity | 价值区间、上下行、风险收益比、流动性约束 | Trend & Timing | 在赔率成立的前提下判断行动时点 |
| Trend & Timing | 趋势状态、市场确认、行动与退出条件 | Portfolio Management | 将研究结论转换为投资状态和仓位方向 |
| Portfolio Management | 状态、仓位依据、升级、降级和退出条件 | Investment Memo | 形成最终研究建议并交给投资者 |

## 5.2 跨阶段保留信息

不是所有信息只传给紧邻的下一阶段。以下信息必须贯穿后续流程：

- Market Regime 传递给 Valuation、Trend 和 Portfolio；
- 每个阶段的 Bull Case 与 Bear Case 汇总到最终 Investment Debate；
- 每个阶段的 Key Assumptions、Falsification Conditions 和 Verification Metrics 传递给 Monitoring；
- 每个阶段的 Catalyst / Timing 汇总成最终 Why Now；
- 所有 Recheck、Reject 和 Unknown 必须原样传递，不得在下游消失；
- 上游 Confidence 限制下游结论强度，下游不能无新证据地提高上游置信度。

## 5.3 信息冲突处理

当阶段之间出现冲突时：

1. 明确冲突是什么；
2. 定位最早出现因果断裂的阶段；
3. 将该阶段设为 Recheck；
4. 重新检查该阶段输入和 Alternative Explanation；
5. 重跑该阶段及受影响的下游阶段；
6. 冲突未解决前，不得给出高强度仓位建议。

例如：

- Industry Thesis 很强，但 Profit Pool 不流向目标环节：停止目标公司研究；
- Company Alpha 很强，但不存在预期差：保持 Observe，而不是强行寻找买点；
- 基本面成立，但估值透支：停止当前买入逻辑，等待赔率变化；
- 基本面与估值成立，但趋势未确认：Observe 或 Trial Position；
- 趋势强，但基本面因果链断裂：不得以趋势绕过 Reject。

---

# 6. Research Gate and Stop Rules

## 6.1 Pass / Recheck / Reject

### Pass

用于以下情况：

- 本阶段核心问题得到直接回答；
- 结论有已确认事实支持；
- 关键因果关系成立；
- 最强 Bear Case 不足以推翻结论；
- 关键假设、证伪条件和验证指标明确；
- 输出足以被下一阶段使用。

Pass 不等于看多，也不等于 Buy。一个明确的负面市场环境或明确的 Sell 结论也可以是高置信度 Pass。

### Recheck

用于以下情况：

- 逻辑可能成立但证据不足；
- 关键输入缺失或过时；
- 事实之间存在未解决冲突；
- 核心变化尚未达到验证时点；
- 反方解释与当前解释同样合理；
- 当前只能形成低置信度判断。

Recheck 必须同时输出：

- 缺少什么；
- 如何补充；
- 等待什么事件或指标；
- 何时重新检查；
- 在此之前允许的最高投资状态。

机会发现任务还必须区分以下三种 Recheck / Reject：

- **Recheck—细分层级：** 当前一级行业或概念过宽，必须先拆分主要利润池；
- **Recheck—数据缺口：** 已有产业变化线索，但缺少来源、基线、盈利传导或验证事件；
- **Reject—当前范围：** 完成合理细分后，当前研究范围内没有任何方向通过机会闸门。

`Reject—当前范围` 不等于否定整个宏观行业或所有未来机会。新细分事实、催化剂或盈利变化出现时，可以重新启动扫描。

### Reject

用于以下情况：

- 核心逻辑不存在；
- 因果链发生决定性断裂；
- 核心假设已经被证伪；
- 即使判断正确也不具备足够赔率；
- 继续研究只会增加叙事，而不会增加有效信息。

Reject 必须同时输出：

- 拒绝发生在哪一阶段；
- 哪项事实或证伪条件触发 Reject；
- Reject 的对象是产业、公司、当前价格还是当前时点；
- 什么新事实出现时可以重新启动研究。

## 6.2 Hard Gate Matrix

| 阶段 | Reject 是否停止当前研究 | Reject 的准确含义 | 后续处理 |
|---|---|---|---|
| Market Regime | 通常否 | 当前无法形成可靠环境判断，或只能限制风险暴露 | 暂停仓位结论；产业基础研究可继续 |
| Industry Thesis | 是 | 产业价值创造逻辑不成立 | 停止原产业逻辑 |
| Profit Pool | 对当前环节或公司是 | 价值不流向目标位置 | 返回利润池选择其他受益环节，或结束 |
| Company Alpha | 对当前公司是 | 公司不能承接产业利润 | 更换候选公司，不能修改产业逻辑迁就原公司 |
| Earnings & Variant Perception | 对主动机会是 | 没有盈利预期差或自主判断无证据 | 转为 Observe，等待新变化 |
| Valuation & Liquidity | 对当前价格是 | 赔率不足或流动性不支持 | 保留公司逻辑，等待价格或盈利变化 |
| Trend & Timing | 对当前行动时点是 | 市场尚未确认或已触发退出条件 | Observe、延后行动或复核基本面 |
| Portfolio Management | 对增加风险是 | 当前不应建立或增加风险暴露 | Observe、Reduce 或 Sell，提交人工决定 |

## 6.3 Research Stop Output

研究在任何 Hard Gate 停止时，不需要强行生成完整正面 Investment Memo，而应生成 Research Stop Memo：

- Research Subject；
- Stop Stage；
- Core Rejection Reason；
- Supporting Facts；
- Failed Assumption or Broken Link；
- Investor Impact；
- Reopen Conditions；
- Verification Metrics；
- Final State：Observe / Reject / Reduce / Sell Recommendation；
- Human Decision Required。

停止研究是有效研究结论，不是任务失败。

---

# 7. Human Judgment Boundary

## 7.1 Agent 可以完成

- 识别并整理公开事实；
- 区分事实、推断、假设和未知信息；
- 比较历史、行业、公司和市场预期；
- 分解销量、单价、收入、利润率、利润和现金流；
- 形成 Bull、Base、Bear 情景；
- 还原产业链、利润池和竞争位置；
- 识别一致预期、主流叙事和可能的价格隐含预期；
- 进行估值、流动性和风险收益分析；
- 检查趋势与基本面是否一致；
- 主动寻找 Bear Case 和 Alternative Explanation；
- 定义假设、证伪条件、验证指标和催化剂；
- 生成 Investment Memo 和 Research Stop Memo；
- 在新事实出现时定位受影响阶段并更新结论。

## 7.2 必须保留人工判断

以下事项可以由 Agent 提供证据和建议，但最终判断必须由投资者承担：

### 长期产业趋势的最终确信

Agent 可以分析需求、供给、技术、政策和生命周期，但产业变化能否持续3—5年，尤其在证据不完整时，需要投资者决定是否接受相关假设。

### 非结构化信息的权重

渠道反馈、产业访谈、市场情绪、产品体验和管理层表达可能相互矛盾。Agent 可以归纳，但投资者决定哪些信息值得信任以及给予多大权重。

### 管理层与竞争优势的定性判断

Agent 可以整理管理层历史行为和经营结果，但对管理层诚信、执行能力、资本配置能力以及竞争优势持续性的最终判断，应保留给投资者。

### 自主判断相对市场预期的可信度

Agent 可以说明差异、证据和验证时间，但投资者必须判断是否愿意用真实资本押注“自己比市场更正确”。

### 概率、赔率与损失承受

Agent 可以给出情景和风险收益比，但投资者决定可接受的下行、等待时间和仓位风险。

### 跨阶段冲突的最终裁决

当基本面、估值、催化剂和趋势无法形成一致结论时，Agent 必须展示冲突，不能替投资者隐藏或强行裁决重大不确定性。

### 最终投资决策

Observe、Trial Position、Buy、Hold、Add、Reduce 和 Sell 均为研究建议。是否执行、何时执行以及实际仓位由投资者决定。

## 7.3 MVP 人工检查点

为了避免把个人 Agent 变成复杂审批系统，只保留以下检查点：

1. **条件性研究检查：** 任一关键阶段 Recheck、证据严重冲突或涉及重要非结构化信息时，由投资者决定继续等待、接受假设还是停止；
2. **最终决策检查：** Investment Memo 完成后，所有仓位和交易相关建议必须由投资者确认；
3. **证伪检查：** Monitoring 触发 Invalidated 或 Sell Recommendation 时，Agent 必须明确提醒，但仍由投资者作出最终交易决定。

当所有阶段均 Pass 时，Agent 可以自动完成研究和 Memo，不需要在每个阶段等待人工批准。

---

# 8. Investment Memo Design

## 8.1 Memo Header

- Research Subject；
- Stock Code and Market；
- Industry；
- As-of Date；
- Investor Question；
- Decision Context；
- Recommended State；
- Overall Confidence。

## 8.1A Opportunity Viewpoint Card

对于产业机会发现或候选行业队列，Memo 在核心叙事前先展示一张简短观点卡：

| 字段 | 内容 |
|---|---|
| 核心观点 | Agent 当前对该机会的明确判断，不使用“值得研究”替代观点 |
| 为什么现在 | 触发事实、时间窗口和催化剂 |
| 数据支撑 | 关键事实、基线、变化、来源和日期 |
| 推导链 | 事实 → 变化 → 商业影响 → 盈利/现金流 → 市场定价 |
| 市场当前认知 | 市场正在交易什么，证据等级是什么 |
| Agent 潜在不同判断 | 哪个变量可能被低估或高估 |
| 主要风险 | 最可能破坏假设的反方路径 |
| 下一步验证 | 指标、事件、验证时间和重跑阶段 |
| 阶段决策 | 通过 / 需要复核 / 不通过及原因标签 |

观点卡只做决策导航，不替代后面的证据链。

## 8.2 Investment Thesis

用一句话回答：

> 什么产业变化，为什么由这家公司获得利润，如何形成盈利预期差，以及为什么现在可能重新定价。

## 8.2A 投资核心叙事

在详细 Decision Dashboard 之前，先用中文展示一条可读的演绎链：

> 现实变化 → 产业变化 → 利润池迁移 → 公司如何获得利润 → 收入/利润/现金流变化 → 市场当前预期 → 当前价格隐含预期 → 催化剂与验证时间 → 趋势确认 → 投资状态

每个环节必须标注内部证据类型：Fact、Change、Inference、Assumption、Hypothesis、Decision 或 Unknown。最终面向投资者的报告使用中文标签和中文解释，英文只保留为首次出现时的辅助说明或内部字段。

## 8.3 Decision Chain

用一张表汇总八个阶段：

| Stage | Core Conclusion | Confidence | Decision | Key Handoff |
|---|---|---|---|---|
| Market Regime |  |  | Pass / Recheck / Reject |  |
| Industry Thesis |  |  | Pass / Recheck / Reject |  |
| Profit Pool |  |  | Pass / Recheck / Reject |  |
| Company Alpha |  |  | Pass / Recheck / Reject |  |
| Earnings & Variant Perception |  |  | Pass / Recheck / Reject |  |
| Valuation & Liquidity |  |  | Pass / Recheck / Reject |  |
| Trend & Timing |  |  | Pass / Recheck / Reject |  |
| Portfolio Management |  |  | Pass / Recheck / Reject |  |

## 8.4 Value Creation Chain

> 产业变化  
> ↓  
> 利润池迁移  
> ↓  
> 公司获得利润  
> ↓  
> 收入、利润和现金流变化  
> ↓  
> 预期差  
> ↓  
> 估值或价格重新定价

任何断裂环节必须显式标记。

## 8.5 Bull Case

汇总各阶段最强支持证据，形成从产业到重新定价的完整正向路径。

## 8.6 Bear Case

汇总以下风险：

- 产业需求风险；
- 供给和利润池风险；
- Company Alpha 失效风险；
- 盈利和现金流风险；
- 市场预期判断错误；
- 估值与流动性风险；
- Catalyst 失败或延迟；
- 趋势未确认或反向变化。

必须包含能够解释同一事实的最强 Alternative Explanation。

## 8.7 Key Assumptions

逐项列出：

- 假设内容；
- 当前证据；
- 预期路径；
- 需要验证的时间；
- 如果错误会影响哪个阶段。

## 8.8 Falsification Conditions

明确：

- 哪些事实意味着逻辑弱化；
- 哪些事实意味着核心逻辑失效；
- 对应 Reduce 或 Sell Recommendation 的条件。

## 8.9 Verification Metrics

按阶段列出：

- 指标；
- 当前状态；
- 预期方向；
- 验证时间；
- 数据变化对应的逻辑影响。

## 8.10 Catalyst / Timing

必须回答：

- 最近发生了什么新变化；
- 变化如何影响产业、公司、盈利或市场认知；
- 市场是否已经定价；
- 什么事件可能推动重新评估；
- 预计在什么时间窗口发生；
- 如何判断催化剂兑现或失败。

## 8.10A Catalyst Priority

不能只罗列事件，必须对最重要的催化剂排序。每个催化剂至少包含：

- 事件；
- 影响变量；
- 预计时间窗口；
- 重要性；
- 当前证据置信度；
- 超预期时的影响；
- 低于预期或失败时的影响；
- 下一次验证时间。

产品发布、新闻或管理层表述只有在可能改变盈利、估值或市场认知时，才可以被列为催化剂。

## 8.11 Valuation & Risk Reward

- Current Valuation；
- Priced-In Expectations；
- Bull / Base / Bear Value Range；
- Upside；
- Downside；
- Risk Reward；
- Liquidity Constraint。

## 8.12 Trend Confirmation

- 长期趋势；
- 中期趋势；
- 短期确认；
- 基本面与价格是否一致；
- Entry / Add / Reduce / Exit Conditions。

## 8.13 Portfolio Recommendation

- Recommended State；
- Position Direction；
- Position Rationale；
- Upgrade Conditions；
- Downgrade Conditions；
- Exit Conditions；
- Unresolved Conflicts；
- Human Decision Required。

## 8.13A Opportunity Ranking and Investment Mistake Analysis

当研究任务同时包含多个候选机会时，Portfolio Management 在现有输出中增加 `Candidate Comparison Record`，比较：

- 产业趋势；
- 利润池位置；
- 公司 Alpha 及其持续性；
- 预期差；
- 盈利可见度；
- 估值/风险收益比；
- 催化剂与时点；
- 趋势确认；
- 流动性；
- 组合匹配度；
- 机会成本。

如果是单一股票研究，或缺少足够同口径候选数据，必须写明“机会排序：未评估”，不得强行给出市场排名。

最终 Memo 还必须回答：

> 如果当前判断错了，最可能先错在哪里？

记录最可能的错误路径、受影响的阶段、领先指标、影响和应对方式。将“投资逻辑错误”与“逻辑正确但兑现速度慢于价格预期”区分开来，不虚构精确概率。

## 8.14 Monitoring Plan

- 需要持续跟踪的关键假设；
- 强制更新事件；
- 下一次验证时间；
- 需要重新运行的阶段；
- 当前 Thesis Status。

---

# 9. Investment Thesis Monitoring Workflow

## 9.1 监控目标

Monitoring 不重新发明投资逻辑，而是比较原始预期与实际事实，判断投资逻辑是否变化。

## 9.2 监控触发方式

出现以下事件时启动更新：

- 关键产业数据公布；
- 公司财报或业绩预告；
- 产品、价格、订单、库存或产能重大变化；
- 政策或竞争格局变化；
- 预定 Catalyst 发生或逾期未发生；
- 股价和成交与基本面判断明显冲突；
- 关键假设接近 Falsification Condition；
- 投资者主动要求复核。

## 9.3 更新步骤

1. 读取原始 Investment Memo；
2. 找出本次新增事实；
3. 比较原始预期与实际变化；
4. 判断差异是正常波动还是逻辑变化；
5. 定位最早受影响的研究阶段；
6. 重新运行该阶段；
7. 顺序重跑所有受影响的下游阶段；
8. 更新 Investment Memo 和 Portfolio Recommendation；
9. 将结果交给投资者作最终决定。

## 9.4 Thesis Status

- **Strengthened：** 新证据强化关键假设；
- **Unchanged：** 事实基本符合原始路径；
- **Weakened：** 关键指标低于预期，但尚未证伪；
- **Invalidated：** 核心假设或因果链已经被破坏。

## 9.5 状态与动作映射

| Thesis Status | Workflow Action | Portfolio Implication |
|---|---|---|
| Strengthened | 更新假设和验证指标，重跑估值、趋势和仓位阶段 | 可考虑 Hold 或 Add，但必须重新检查赔率 |
| Unchanged | 保持原逻辑，更新事实和下一验证时间 | 通常维持原状态 |
| Weakened | 将受影响阶段设为 Recheck，补充信息并降低置信度 | 通常不加仓，可考虑 Reduce |
| Invalidated | 将最早断裂阶段设为 Reject，重跑下游 | 输出 Reduce 或 Sell Recommendation，等待人工决定 |

## 9.6 跟踪纪律

- 保留原始假设和原始验证时间，不事后移动目标；
- 同时记录支持与反对原逻辑的新事实；
- 价格下跌本身不构成加仓理由；
- 加仓必须同时满足逻辑强化和赔率合理；
- 核心逻辑被证伪时必须输出 Invalidated；
- 新 Memo 必须说明“什么发生了变化”，而不是只给出新结论。

---

# 10. MVP Operating Rules

## 10.1 最小完整研究

一个研究任务只有满足以下条件，才可以输出完整 Portfolio Recommendation：

- Research Brief 已确认；
- 八个阶段均已运行；
- 所有关键 Recheck 和 Reject 已显式保留；
- Investment Thesis 可以沿价值创造链回溯；
- Bull Case 与 Bear Case 均有事实支持；
- Key Assumptions、Falsification Conditions 和 Verification Metrics 已定义；
- Catalyst / Timing、估值赔率和趋势确认已回答；
- 已明确需要投资者决定的事项。

## 10.2 Agent 不得做出的行为

- 从股票涨幅倒推产业逻辑；
- 因公司优秀而忽略价格；
- 因行业增长而假定公司必然受益；
- 因观点与市场不同而假定市场错误；
- 只寻找支持证据；
- 用趋势信号绕过基本面 Reject；
- 在证据不足时输出确定性结论；
- 修改证伪条件来维护原判断；
- 把仓位建议转化为自动交易。

## 10.3 Workflow 完成条件

一次任务在以下任一状态下完成：

### Completed — Full Memo

完成八阶段研究，输出完整 Investment Memo 和人工决策事项。

### Completed — Recheck Memo

逻辑可能成立但存在关键不确定性，输出缺失信息、验证事件、最高允许状态和重新检查条件。

### Completed — Research Stop Memo

Hard Gate 触发 Reject，输出停止原因和重新启动条件。

### Entered Monitoring

投资者决定继续观察或持有后，Memo 成为后续 Monitoring 的基准。

Workflow 的成功标准不是每次产生 Buy，而是 Agent 能够忠实地区分：

- 没有投资逻辑；
- 有逻辑但证据不足；
- 有基本面但没有预期差；
- 有预期差但赔率不足；
- 逻辑与赔率成立但时点未到；
- 逻辑、赔率和时点形成闭环；
- 原有逻辑已经弱化或失效。

---

# 11. Workflow Definition

Investment Agent Workflow v1.1 的核心是：

> 用 Market Regime 定义风险背景；  
> 用 Industry Thesis 判断价值从哪里产生；  
> 用 Profit Pool 判断价值流向哪里；  
> 用 Company Alpha 判断谁能获得价值；  
> 用 Earnings & Variant Perception 判断市场错在哪里；  
> 用 Valuation & Liquidity 判断赔率是否足够；  
> 用 Trend & Timing 判断市场是否开始重新定价；  
> 用 Portfolio Management 表达判断强度；  
> 用 Monitoring 持续验证投资逻辑。

它不是股票分析模板，也不是自动交易系统。它是一条可启动、可执行、可中止、可回溯、可更新，并始终保留投资者最终决定权的个人投资研究流程。

---

# 12. v1.1 Enhancement Contract

本节是对前述 v1.0 流程的规范性增强。若本节与前文存在差异，以 v1.1 Enhancement Contract 为准。它不增加 Skill，不改变八阶段核心决策链，也不改变“产业趋势 + 基本面 + 预期差 + 趋势确认 + 仓位管理”的投资理念。

## 12.1 Research Trigger Layer（前置层，不是 Skill）

正式执行八阶段链之前，Research Brief 必须补充一个轻量级投资机会触发记录。触发来源可以是用户指定公司、行业扫描、财报、政策、产业数据、价格行为或已有逻辑更新；如果没有外部事件，必须明确标记为 `User-specified`，不得事后编造催化剂。

```text
Investment Trigger
Trigger Type: User-specified / Event-driven / Industry-scan / Thesis-update
Trigger Event: 最近发生了什么变化
Why Now: 为什么现在值得关注
Affected Variables: 影响哪些需求、供给、价格、份额、成本或流动性变量
Potential Beneficiaries: 可能受益的产业链环节与公司
Initial Research Hypothesis: 首要需要验证的投资假设
Market Awareness: Unknown / Emerging / Widely-recognized
```

Trigger 只提出研究假设，不直接产生投资结论。若 Trigger Event 无法被事实验证，Research Readiness 为 Recheck。

## 12.2 Shared Decision Records（跨阶段共享记录）

为避免每个阶段重复生成相互矛盾的叙事，Workflow 维护四个随阶段更新的共享记录。

### Narrative Record

```text
Current Market Narrative
Potential Narrative Shift
Narrative Gap
Required Evidence
Narrative Risk
```

Industry Thesis 首次建立 Narrative Record；Company Alpha 解释公司如何承载叙事；Earnings & Variant Perception 用经营数据验证；Trend & Timing 判断市场是否开始认可。

### Expectation Record

```text
Market View
Agent View
Variant Source
Evidence
Invalidation
```

该记录必须区分市场当前相信什么、Agent 的独立判断是什么，以及两者差异来自哪个可验证变量。

### Scenario Valuation Record

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

估值不能只输出“便宜/昂贵”，必须说明价格隐含的盈利与估值假设。没有足够数据时输出 Recheck，不得虚构精确目标价。

### Portfolio and Sell Record

```text
Portfolio Context: Known / Unknown
Current Exposure
New Exposure
Risk Factor Contribution
Position State
Sell Type: Thesis Invalidated / Valuation Exhaustion / Trend Failure
Required Action
```

没有持仓、成本、最大回撤和集中度信息时，Portfolio Context 必须标记 Unknown，不输出个性化仓位比例。

## 12.3 八阶段增强映射

| 阶段 | v1.1 强制增强 |
|---|---|
| Market Regime | 在流动性、风险偏好、指数趋势基础上承接 Investment Trigger，并判断市场是否允许承担 Beta |
| Industry Thesis | 增加 Current Market Narrative、Potential Narrative Shift、需求/供给/瓶颈/生命周期判断 |
| Profit Pool | 明确需求增长是否超过有效供给，识别最稀缺环节和盈利弹性变量 |
| Company Alpha | 增加“公司如何赚钱”、收入/利润驱动树和同行比较 |
| Earnings & Variant Perception | 强制输出 Market View、Agent View、Variant Source、独立盈利判断和 Invalidation |
| Valuation & Liquidity | 增加 Bull/Base/Bear 情景估值、隐含预期、上行/下行、分红回购、现金、债务、汇率和流动性 |
| Trend & Timing | 增加 Why Now、催化剂是否已定价、关键平台/均线/突破/失败确认 |
| Portfolio Management | 增加 Portfolio Context、Observe → Trial → Core → Reduce → Exit 状态机及三类 Sell Logic |

Catalyst 不独立成 Skill。它由 Trigger、Narrative、Earnings 和 Trend 的时间条件共同构成。

## 12.4 盈利与赔率门槛

进入 Trial 或 Buy 状态前，必须回答：

1. 产业变化通过什么经营变量影响收入；
2. 收入变化如何影响利润率、EPS 或自由现金流；
3. Market View 与 Agent View 的差异是什么；
4. 当前价格隐含了什么预期；
5. Bull/Base/Bear 的上行、下行和确定性如何；
6. 预期差消失或证伪时如何退出。

缺少其中任一决定性答案时，最高状态为 Observe / Recheck。

机会发现任务在进入 Industry Thesis 前还必须通过内部前置门槛：

1. 已说明 Opportunity Radar 的时间窗口和来源覆盖；
2. 已判断研究对象是否需要细分；
3. 已形成至少一个“观点—数据—推导—验证”的 Investment Opportunity Hypothesis；
4. 已给出 Profit Pool Pre-check，或明确标记 Unknown；
5. 若上述信息缺失，返回 `Recheck—Subsegment` 或 `Recheck—Data`，不得把“值得研究”直接写成行业结论。

## 12.5 Position State Machine

```text
Research Pass
  → Observe
  → Trial
  → Core
  → Reduce
  → Exit
```

- `Research Pass`：研究链可继续，不等于可以买入；
- `Observe`：逻辑有吸引力，但赔率、趋势或组合信息不足；
- `Trial`：基本面、预期差和最低限度的市场确认成立；
- `Core`：证据持续强化、赔率仍合理、趋势和组合风险匹配；
- `Reduce`：赔率下降、组合风险过高、趋势恶化或证据弱化；
- `Exit`：逻辑证伪、估值耗尽且无新增预期，或趋势失败伴随风险收益比恶化。

价格下跌本身不是加仓理由；新增证据、确定性和赔率改善才是加仓依据。

## 12.6 Sell Decision Framework

### Thesis Invalidated

产业需求、利润池流向、公司竞争优势或核心盈利假设被证伪。默认动作是 Exit / Reject。

### Valuation Exhaustion

逻辑仍成立，但市场已经充分定价，预期差和风险收益比消失。默认动作是 Reduce / Hold，除非新的盈利上修足以支持更高估值。

### Trend Failure

逻辑可能仍成立，但市场长期不认可、关键平台突破失败或趋势结构破坏。默认动作是 Recheck / Reduce；单日波动不能单独触发 Exit。

每个 Sell Type 都必须输出 Evidence、Confidence、Required Action 和重新进入条件。

## 12.7 Monitoring and Review Loop

Investment Thesis Monitor 除了跟踪事实，还必须记录：

- 原始假设与当前实际值；
- 偏差对收入、利润、现金流和估值的影响；
- Narrative 是否强化、未变、弱化或失效；
- Position State 是否变化；
- 本次新信息是否触发下游 Skill 重跑；
- 错误归因：产业判断、公司 Alpha、盈利预测、估值、时点或仓位。

长期复盘统计不属于单只股票的交易指令，但应支持按 20—30 个决策样本分析胜率、赔率、最大回撤、趋势失败率和仓位错误。

## 12.8 v1.1 Acceptance Criteria

一份完整研究必须能够回答：

1. 为什么研究这个机会；
2. 现实变化是什么；
3. 产业价值和利润池如何变化；
4. 为什么利润流向这家公司；
5. 市场当前如何理解它；
6. Agent 与市场的差异是什么；
7. 当前价格隐含什么预期；
8. Bull/Base/Bear 的赔率如何；
9. 为什么是现在；
10. 什么条件下从 Observe 转 Trial 或 Core；
11. 什么情况下 Reduce 或 Exit；
12. 下一次验证哪些指标，以及信息变化触发哪个 Skill 重跑。

# 13. v1.2 Opportunity, Evidence and Presentation Contract

v1.2 不增加 Skill，也不改变八阶段核心决策链；它把“为什么关注、为什么是它、市场错在哪里、为什么现在、为什么放入组合”补进现有 Workflow 的前置层、阶段内部字段和汇总层。

## 13.1 Research Trigger and Candidate Queue

每次研究先建立 `Investment Trigger`，记录现实变化、重要性、受影响变量、潜在受益产业链、初始假设和 Market Awareness。若任务来自“当前有哪些行业值得投资”，先由 Market & Opportunity Scanner 形成候选产业/公司队列；若任务直接给定股票，也必须记录触发原因，不能把股票名称本身当作触发器。

## 13.2 Workflow-Level Candidate Comparison

当一个触发器产生两个或以上候选者时，在进入 Portfolio Management 前建立 `Candidate Comparison Record`。比较维度至少包括：Industry Thesis Strength、Profit Pool Position、Company Alpha、Variant Strength、Earnings Visibility、Valuation/Risk Reward、Catalyst/Timing、Trend Confirmation、Liquidity、Portfolio Fit、Opportunity Cost 和 Unknowns。

Candidate Comparison 是 Workflow 层的相对排序记录，不是新 Skill、自动打分器或自动买入规则。单一股票任务若没有可比候选，明确标注 `Comparison: Not Assessed`，不得编造相对排名。

## 13.3 Industry Cycle Position

Industry Thesis 必须标注行业当前所处阶段：

`Technology Breakthrough → Capital Investment → Commercial Validation → Profit Release → Mature Competition`。

同时回答距离利润释放还有多远、当前验证指标是什么、哪些事实会证明阶段判断错误。周期阶段是对 Why Now 和估值兑现速度的约束，不是新的投资理念。

## 13.4 Evidence Chain and Decision-First Memo

所有关键结论使用统一证据标签：

`Fact`（可引用事实）、`Change`（相对基线的变化）、`Inference`（由事实推导的判断）、`Assumption`（估值或盈利模型假设）、`Hypothesis`（待验证投资命题）、`Decision`（阶段或仓位状态）、`Unknown`（尚未验证）。

最终 Memo 先展示 Decision Dashboard，再展示 Evidence Chain。每个关键变量至少保留：最新值、比较基线、变化、商业影响、盈利/现金流影响、市场定价影响、来源和日期、下一次验证时间。事实、推导、假设和不确定性必须分开写，禁止把推断写成事实。

## 13.5 Market Expectation Decomposition

Earnings & Variant Perception 必须分别拆解：

- Short term：未来 1—2 个季度；
- Medium term：未来 1—2 年；
- Long term：未来 3—5 年。

每个周期同时记录 Market View、Agent View、Variant Source、Evidence 和 Invalidation。若不存在可验证的公开共识，使用 `Forecast Range` 或 `Implied Expectation`，不得把单一研报观点称为市场共识。

## 13.6 Implied Expectation and Opportunity Cost

Valuation & Liquidity 必须反推当前价格隐含的收入、利润率、现金流、增长期限或估值倍数，并与 Agent 的 Base Case 对照，明确差异来自哪个变量。Portfolio Management 必须记录组合现有暴露、新增暴露、风险因子贡献和替代机会；信息不足时标记 `Not Assessed`，不伪造机会排序。

## 13.7 Thesis Evolution Log

每次新信息更新必须追加 Thesis Evolution Log：日期、原始假设、预期指标、实际结果、解释、Strengthened/Unchanged/Weakened/Invalidated 状态变化和触发重跑的 Skill。更新后的 Memo 不能删除原始基线。

## 13.8 v1.2 Acceptance Criteria

完整研究必须能够清楚回答：

1. 为什么关注这个机会，现实变化是什么；
2. 产业处于哪个周期阶段，利润池如何迁移；
3. 为什么是这家公司，竞争者为何不能轻易复制；
4. 市场在短、中、长期分别预期什么，Agent 的预期差在哪里；
5. 当前价格隐含了什么，Bull/Base/Bear 的赔率如何；
6. 为什么现在，催化剂和趋势证据是什么；
7. 与候选机会相比为什么排序更高或更低；
8. 放入组合增加什么暴露，机会成本是什么；
9. 什么事实会强化、削弱或证伪原始逻辑；
10. 最终结论中哪些是事实、哪些是推导、哪些仍是 Unknown。

## 13.9 v1.2 Presentation and Decision Enhancements

本次增强不新增 Skill，也不改变八阶段核心决策链：

1. **中文投资者呈现：** 内部保留稳定英文键名，最终 Memo 将阶段、状态、证据类型和解释性文字转换为中文；
2. **投资核心叙事：** Memo 开头先展示“现实变化 → 产业变化 → 利润池 → 公司受益 → 盈利 → 市场预期 → 隐含预期 → 催化剂 → 趋势 → 状态”；
3. **Alpha Durability：** Company Alpha 增加优势持续性、复制难度、侵蚀机制和验证指标；
4. **Catalyst Priority：** Timing & Portfolio 对催化剂按影响变量、时间、重要性和验证结果排序；
5. **Conditional Opportunity Ranking：** 只有存在多个候选和同口径数据时才进行机会排序，否则写“机会排序：未评估”；
6. **Investment Mistake Analysis：** 每份完整 Memo 指出最可能的错误路径，并区分逻辑失效、估值透支、兑现延迟和市场不认可。

这些是已有阶段的内部字段与呈现要求，不构成新的投资理念、Skill 或自动交易规则。

# 14. v1.3 Opportunity Recall and Hypothesis Contract

v1.3 针对机会扫描试跑中的两个问题收敛 Workflow：最近主题覆盖不足，以及“值得研究”没有转化为明确的可验证投资观点。v1.3 不增加独立 Skill，不改变八阶段核心决策链。

## 14.1 多源机会召回

机会发现默认使用 `Rolling Window`：

1. `group +topics` 读取最近主题，并使用 `next_end_time` 分页，按 `topic_id` 去重；
2. 对指定主题使用 `topic +search` 多关键词召回；由于该接口没有翻页，使用近义词和相关词合并结果；
3. 只对高相关主题调用 `topic +detail`；
4. 结构化数据先由 Tushare 取得，知识星球、IMA、Report CLI 和 Web Search 作为定向证据包；
5. 报告必须写明时间窗口、页数、关键词、去重主题数、详情数和未覆盖范围。

推荐默认范围：短期催化剂使用7—30天，产业趋势使用30—90天；最近30条仅作为快速 Snapshot，不得作为机会发现的唯一覆盖。

## 14.2 证据等级

所有非结构化来源必须标注：

- `Radar Only`：主题标题、列表或热度，仅说明市场关注；
- `Narrative Extracted`：已读取主题正文、研报摘要或机构观点；
- `Cross-Validated`：已与 Tushare、公司公告、政府/协会或其他一手来源交叉验证。

Radar Only 不得直接支撑 Industry Thesis Pass、Profit Pool Pass 或 Earnings Pass。

## 14.3 细分闸门与假设形成

一级行业、宽泛概念或混合主题必须先进行 Granularity Gate。若内部存在不同需求、供给和利润池，最多先拆分为3—5个可研究方向。只有至少一个细分方向形成以下链条，才可进入 Industry Thesis：

```text
产业变化 → 价值迁移 → 受益环节 → 利润池假设 → 盈利影响假设 → 市场定价差异 → 验证指标
```

此处形成的是 `Investment Opportunity Hypothesis`，不是最终产业结论、公司结论或 Buy 信号。

## 14.4 观点—数据呈现

每个候选方向必须先给出“核心观点”，然后提供支持该观点的事实、基线、变化、推导、关键假设、证伪条件和下一次验证。不得以“板块上涨”“研报很多”或“行业长期空间大”单独构成观点。

## 14.5 v1.3 验收标准

机会扫描完成后必须能够回答：

1. 扫描覆盖了多长时间、哪些来源和哪些关键词；
2. 当前对象是否需要拆分为细分方向；
3. 每个候选的核心观点是什么；
4. 哪些是事实，哪些是推断，哪些仍是待验证假设；
5. 利润池可能位于哪个环节，为什么；
6. 市场当前认知与 Agent 判断差异在哪里；
7. 哪个数据或事件会强化、削弱或证伪该假设；
8. 当前应当通过、复核还是在当前范围停止，而不是笼统排除整个一级行业。
