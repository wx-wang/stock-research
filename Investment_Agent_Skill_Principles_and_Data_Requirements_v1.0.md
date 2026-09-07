# Investment Agent Skill Principles & Data Requirements v1.0

## 1. Scope

本文件定义六个投资研究 Skill 和一个调度 Skill 的共同原则与数据契约。

当前版本只说明需要什么数据、数据必须具有什么属性以及缺失时如何处理，不绑定任何数据供应商、API、Tool、数据库或自动交易能力。

## 2. Skill Set

1. Market & Opportunity Scanner
2. Industry Value Chain Analyzer
3. Company Alpha Analyzer
4. Earnings & Valuation Analyzer
5. Timing & Portfolio Manager
6. Investment Thesis Monitor
7. Investment Agent：负责调度以上 Skill，不创造新的投资结论

## 3. Non-Negotiable Investment Principles

### 3.1 研究顺序

> 市场环境与机会变化  
> ↓  
> 产业趋势与利润池  
> ↓  
> 公司 Alpha  
> ↓  
> 盈利、预期差、估值与赔率  
> ↓  
> 趋势确认与投资状态  
> ↓  
> 投资逻辑持续跟踪

不得从股价、热门概念或公司故事直接倒推完整投资结论。

### 3.2 统一因果链

每个 Skill 必须遵循：

> 事实 → 变化 → 商业影响 → 盈利影响 → 市场定价影响

不得跳过中间环节。某一影响不重大时应明确说明，不能虚构因果关系。

### 3.3 事实与判断分离

所有输入和输出必须区分：

- Fact：已确认事实；
- Change：相对历史、市场预期或原假设的变化；
- Inference：基于事实作出的推断；
- Assumption：尚待验证的关键假设；
- Unknown：缺失且可能改变结论的信息。

### 3.4 正反论证

每个 Skill 都必须输出：

- Core Conclusion；
- Bull Case；
- Bear Case；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Confidence；
- Stage Decision；
- Handoff Package。

### 3.5 判断门

- **Pass：** 核心问题得到回答，因果链有事实支持，足以传给下游；
- **Recheck：** 逻辑可能成立，但缺少关键数据、证据冲突或尚未达到验证时间；
- **Reject：** 核心因果链不成立或关键假设已被证伪。

Reject 必须说明否定的是产业、产业链位置、公司、预期差、当前价格还是当前时点。

### 3.6 投资边界

- Market Regime 影响风险暴露，不决定产业机会；
- Catalyst 推动重新定价，不替代投资逻辑；
- Trend 验证市场认知，不证明基本面；
- 好公司不等于好投资；
- 价格下跌本身不是加仓理由；
- Skill 只输出研究建议，不执行交易；
- 最终投资决策由投资者作出。

## 4. Common Data Contract

### 4.1 每项数据必须携带

- Data Item：数据或事实内容；
- Subject：对应市场、行业或公司；
- Observation Period：数据对应期间；
- As-of Date：研究可使用信息的截止日期；
- Publication Time：公开时间，如适用；
- Comparison Basis：同比、环比、历史、市场预期或原始假设；
- Evidence Type：Fact / Consensus / Inference / Assumption / Unknown；
- Source Identification：来源名称或材料标识，暂不规定获取方式；
- Reliability Note：数据口径、修订、缺失或冲突说明。

### 4.2 时点原则

- 禁止使用 As-of Date 之后的信息支持此前判断；
- 财务数据必须标明报告期和公布时间；
- 行业数据必须标明频率和观察期；
- 市场预期必须标明形成时间；
- 价格、估值、成交和趋势必须使用同一或可比时点；
- 原始 Memo 与后续更新必须保留各自的 As-of Date。

### 4.3 缺失数据处理

- 决策关键数据缺失时输出 Recheck；
- 明确 Missing Inputs、重要性、补充方式和重新检查条件；
- 不得用无法核验的数字填充；
- 不得把行业平均值静默替代公司数据；
- 不得把单一分析师观点等同于市场一致预期；
- 如果只能形成方向性判断，必须降低 Confidence。

## 5. Data Requirements by Skill

## 5.1 Market & Opportunity Scanner

### Minimum Data

- 扫描市场和范围；
- As-of Date；
- 利率、美元/汇率、信用环境方向；
- 指数、成交量、市场宽度、资金与风格变化；
- 产业技术、成本、政策、需求或供需变化；
- 公司收入、利润、订单、份额或经营变化线索；
- 行业或公司估值与趋势变化；
- 每项变化的历史或预期比较基准。

### Decision-Critical Data

- 至少一个可验证的新变化；
- 变化可能影响商业价值和盈利的初步路径；
- 市场是否可能尚未充分理解；
- 候选机会的验证指标和时间。

### Output Data Package

- Market State、Risk Level、Recommended Risk Exposure；
- Candidate Industries / Companies；
- Trigger Signal、Value Change Hypothesis；
- Research Priority、Research Question；
- Regime Change Triggers。

## 5.2 Industry Value Chain Analyzer

### Minimum Data

- 候选行业和核心变化；
- 需求规模、增速、渗透率和驱动；
- 供给、产能、库存、资源和进入条件；
- 技术、成本、政策和应用变化；
- 产业生命周期；
- 上中下游结构；
- 各环节价格、成本、利润率和资本投入；
- 各环节市场份额、主要参与者和竞争变化；
- 市场当前产业叙事。

### Decision-Critical Data

- 产业变化是否创造新增价值；
- 价值增长的持续时间；
- 稀缺环节和定价权；
- 利润池位置及迁移方向；
- 供给扩张和竞争侵蚀风险；
- 产业与利润池验证指标。

### Output Data Package

- Industry Thesis、Lifecycle、Demand Drivers、Supply Constraints；
- Industry Chain Map、Current Profit Pool、Profit Migration；
- Beneficiary / Disadvantaged Segments；
- Winner Characteristics、Candidate Companies；
- Industry Thesis Decision 和 Profit Pool Decision。

## 5.3 Company Alpha Analyzer

### Minimum Data

- 已通过的 Industry Thesis 与 Profit Pool 输出；
- 公司产品、服务、客户、应用场景和产业链位置；
- 分业务收入和利润来源；
- 销量、单价、产品结构、利润率和现金流；
- 市场份额及其变化；
- 技术、成本、客户、规模和品牌优势证据；
- 主要竞争对手及可比经营结果；
- 公司近期经营 Catalyst。

### Decision-Critical Data

- 公司是否位于受益利润池；
- 竞争优势是否有经营事实支持；
- 优势能否传导至收入、利润和现金流；
- 优势持续性；
- Company Alpha 与行业 Beta 的区别。

### Output Data Package

- Company Positioning、Business Model、Company Alpha；
- Competitive Advantage、Advantage Durability；
- Growth Engine、Revenue Bridge、Profit Bridge；
- Relative Competitive Position；
- Earnings Drivers、Company-Specific Risks。

## 5.4 Earnings & Valuation Analyzer

### Minimum Data

- Industry Value Chain 与 Company Alpha 输出；
- 历史收入、利润率、利润、现金流和相关经营数据；
- 销量、单价、份额、产品结构、成本和费用；
- 公司指引；
- 分析师一致预期及其时间；
- 市场主流叙事；
- 当前价格、市值、股本和相关资本结构；
- 当前、历史和行业可比估值；
- 成交与流动性；
- Market State 和风险偏好背景。

### Decision-Critical Data

- Consensus 与 Own View 的可比口径；
- Bull / Base / Bear 盈利情景；
- 需求到现金流的盈利桥；
- 预期差来源、幅度和验证时间；
- 当前价格隐含预期；
- Bull / Base / Bear 价值区间；
- Upside、Downside、Risk Reward；
- 进入和退出的流动性约束。

### Output Data Package

- Consensus、Market Narrative、Own Earnings View；
- Earnings Scenarios、Earnings and Cash Flow Bridge；
- Variant Source、Magnitude、Validation Timeline；
- Current Valuation、Priced-In Expectations；
- Value Range、Upside、Downside、Risk Reward；
- Liquidity Constraint；
- Earnings & Variant Decision、Valuation & Liquidity Decision。

## 5.5 Timing & Portfolio Manager

### Minimum Data

- 前四个主链 Skill 的有效输出；
- 长期年线、季线与价格结构；
- 中期60日趋势、高低点和相对强弱；
- 短期成交、突破和回踩；
- Catalyst 发生前后的价格反应；
- Market State、Risk Level 和流动性；
- 当前持仓、投资状态和投资者风险边界，如有。

### Decision-Critical Data

- 基本面与价格行为是否一致；
- 市场是否开始交易预期差；
- Entry、Add、Reduce、Exit Conditions；
- 逻辑完整度、Confidence 和 Risk Reward；
- 当前持仓与可承受风险。

### Output Data Package

- Long / Medium / Short Trend Status；
- Fundamental–Price Alignment；
- Market Recognition Status；
- Observe / Trial / Entry / Add / Reduce / Exit Conditions；
- Recommended State、Position Direction、Rationale；
- Upgrade、Downgrade、Exit Conditions；
- Human Decision Required。

没有投资者风险边界时，只能给出仓位方向和状态，不应虚构具体仓位比例。

## 5.6 Investment Thesis Monitor

### Mandatory Baseline Data

- 原始或最近一次 Investment Memo；
- 原始 Core Conclusion；
- Supporting Facts；
- Key Assumptions；
- Falsification Conditions；
- Verification Metrics；
- Catalyst / Timing；
- Validation Timeline；
- Recommended State 和状态调整条件。

### New Data

- 新产业、供需、政策或竞争事实；
- 新产品、客户、份额、订单、价格或成本事实；
- 新财报、业绩预告或经营数据；
- 新市场预期、估值、流动性、价格和趋势；
- Catalyst 是否兑现、延迟或失败；
- 投资者新增观察或问题。

### Decision-Critical Data

- Expected vs Actual；
- 受影响的原始假设或证伪条件；
- 最早受影响的 Skill；
- 盈利和市场定价影响；
- 需要重跑的下游链路。

### Output Data Package

- Strengthened / Unchanged / Weakened / Invalidated；
- New Facts、Expected vs Actual；
- Changed Assumptions、Triggered Falsification Conditions；
- Affected Skill、Affected Downstream Chain；
- Updated Earnings / Pricing Implication；
- Updated State Recommendation、Next Review Trigger。

没有基准 Investment Memo 或等价原始逻辑时，不得输出变化状态，必须 Recheck。

## 6. Data Integration Boundary for v1.0

当前 Skill 版本：

- 定义数据类别、口径、时点和缺失处理；
- 接受投资者提供或当前环境已授权取得的数据；
- 不假定任何指定数据供应商；
- 不写 API 调用；
- 不设计数据存储；
- 不生成数据抓取脚本；
- 不因为没有自动数据源而降低研究纪律。

后续数据接入应服务于本数据契约，而不是反过来改变投资逻辑。
