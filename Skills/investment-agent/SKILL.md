---
name: investment-agent
description: Orchestrate the user's personal A-share and Hong Kong stock Investment Agent workflow across market scanning, industry value chains, company alpha, earnings and valuation, timing and portfolio state, and thesis monitoring. Use when the user asks to apply their Investment Decision Framework, run an end-to-end stock or industry study, find current industry opportunities, decide a research-level investment state, or update an existing thesis. Do not use for generic stock questions that do not request this framework, automatic trading, or fund operations.
---

# Investment Agent v2.0

调度已安装的投资研究 Skill，不独立创造投资结论。保持投资者规定的流程、闸门和最终决策权。Opportunity Radar、Granularity Gate、Investment Opportunity Hypothesis 是调度与 Scanner 内部能力，不是独立 Skill。

## 始终读取

- [Evidence, Gates and Handoff Contract](references/evidence-and-gates.md)：公共证据、因果链、闸门、停止/重路由和交接规则。
- [Data Source Routing](references/data-source-routing.md)：数据源优先级、证据能力边界和调用预算。

## 按任务条件读取

- 形成阶段报告、完整 Memo、候选比较或逻辑更新时，读取 [Presentation Contract](references/presentation-contract.md)。
- 行业机会发现读取 [Sector Discovery Process](references/sector-discovery-process.md)。
- 完整行业研究读取 [Industry Research Process](references/industry-research-process.md)。
- 完整个股研究读取 [Stock Research Process](references/stock-research-process.md)。
- 涉及行业、利润池或公司研究的行业前置阶段时，读取 [Industry Six-Question Framework](references/industry-six-question-framework.md)。

不假设存在特定数据连接。只使用用户提供或当前环境已授权的数据；关键数据缺失时保留缺口并返回需要复核。

## 入口模式

### 行业机会发现

用户询问“哪些行业值得关注、寻找板块或潜在机会”时，执行10步发现链：

```text
任务启动 → Research Trigger → Market Regime → Opportunity Radar
→ Granularity Gate → Investment Opportunity Hypothesis
→ Industry Thesis → Profit Pool → Research Gate → 行业候选池
```

发现阶段只加载 Market & Opportunity Scanner 和 Industry Value Chain Analyzer；不得调用 Company Alpha、Earnings & Valuation 或 Timing & Portfolio。输出3—5个细分方向及证据等级和Research Gate，不推荐股票。

### 完整个股研究

用户提供公司或代码并要求完整投资判断时，先确认代码、上市市场、截至日期、投资问题、已有仓位、已有逻辑和数据缺口，再执行投资者规定的9阶段链。

### 聚焦问题

用户只问公司Alpha、财报、盈利预期、估值、时点或仓位时，从最早缺失的前置阶段开始。输出标为阶段备忘录，列明已完成/未完成阶段、最大可支持结论和下一路由；不得包装成完整Investment Memo。

### 逻辑更新

已有Memo、持仓逻辑或新事实需要更新时，从 Investment Thesis Monitor 开始：读取旧基线，识别最早受影响阶段，只重跑该阶段及受影响的下游阶段，保留旧Memo和事件前预期。

### 独立财报分析

只分析季度、半年或年度财报时，Financial Statement Analyzer 可以单独运行，输出“财报分析报告（辅助证据输出）”。它不完成投资阶段、不返回阶段闸门、估值或投资状态。

## Skill 路由

- [Financial Statement Analyzer](../investment-financial-statement-analysis/SKILL.md)：财报事实与变化的辅助证据包。
- [Market & Opportunity Scanner](../investment-market-opportunity-scanner/SKILL.md)：市场环境、机会雷达与颗粒度。
- [Industry Value Chain Analyzer](../investment-industry-value-chain/SKILL.md)：产业趋势、周期、价值链和利润池。
- [Company Alpha Analyzer](../investment-company-alpha/SKILL.md)：公司能否捕获已验证利润池。
- [Earnings & Valuation Analyzer](../investment-earnings-valuation/SKILL.md)：独立盈利、预期差、隐含预期、估值与流动性。
- [Timing & Portfolio Manager](../investment-timing-portfolio/SKILL.md)：趋势确认、时点与组合状态。
- [Investment Thesis Monitor](../investment-thesis-monitor/SKILL.md)：基于旧基线追踪逻辑变化。

## 投资者规定的9阶段个股链

| 阶段 | 核心问题 | Skill | 结果 |
|---|---|---|---|
| 1 市场环境 | 当前市场是否支持风险暴露 | Scanner（Regime） | 通过/需要复核 |
| 2 产业趋势 | 未来3—5年产业价值是否变化 | Industry Value Chain | 通过/需要复核/不通过 |
| 3 利润池 | 价值最终流向哪个环节 | Industry Value Chain | 通过/需要复核/不通过 |
| 4 公司Alpha | 为什么利润流向该公司 | Company Alpha | 通过/需要复核/不通过 |
| 5 盈利与预期差 | 市场预期与Agent差异 | Earnings & Valuation | 通过/需要复核/不通过 |
| 6 估值与流动性 | 价格隐含什么、赔率如何 | Earnings & Valuation | 通过/需要复核/不通过 |
| 7 催化与趋势 | 为什么是现在、是否重新定价 | Timing & Portfolio | 通过/需要复核/不通过 |
| 8 组合与仓位 | 是否适合当前组合 | Timing & Portfolio | 观察/试仓评估/买入评估/持有/加仓/减仓/卖出 |
| 9 逻辑跟踪 | 原始假设是否被验证 | Thesis Monitor | 强化/未变/减弱/失效 |

阶段7—8同属 Timing & Portfolio，不增加Skill。近期财报在阶段5内由 Financial Statement Analyzer 先形成带日期证据包，不构成“阶段4.5”。

## 投资者规定的12步行业链

```text
Research Trigger → Market Regime → Opportunity Radar → Granularity Gate
→ Investment Opportunity Hypothesis → Industry Thesis → Industry Cycle
→ Value Chain & Profit Pool → Competitive Dynamics → Market View vs Agent View
→ Catalyst / Verification → Beneficiary Candidates
```

步骤1—5由Scanner执行；步骤6—12由Industry Value Chain执行。六问是步骤4—11的覆盖层，不新增阶段、Skill或闸门。Scanner形成粗扫和深研顺序，Industry Value Chain完成深读与约束闭环；Q3不预判Company Alpha，Q6不预判公司估值。

宽泛行业未覆盖主要细分环节前不得整体Reject，使用 `Recheck—Subsegment`。行业Pass只允许进入公司研究，不等于买入。

## 前置条件与最大结论

- 市场环境问题：Scanner可单独运行。
- 行业吸引力或利润池：需要Scanner上下文，再运行Industry Value Chain。
- 公司竞争优势：需要有效行业和利润池结论。
- 盈利或估值：需要有效行业、利润池和公司Alpha结论。
- 买入、加仓、减仓或卖出评估：需要全部有效上游输出后才能运行Timing & Portfolio。

缺少前置条件时补跑，或明确返回需要复核；不得让窄问题绕过投资链。

## 财报支持路由

- 独立财报分析先确认上市主体和代码，最大结论限于经营变化、盈利质量、会计风险和验证需要。
- 完整公司研究中，近期财报对盈利判断重要时，在阶段5刷新证据包。
- Company Alpha只把证据包用于分部经济和同行经营比较，Alpha结论仍由Company Alpha负责。
- 新财报触发更新时，Thesis Monitor是入口；Financial Statement Analyzer提取相对旧基线的变化。

## 调度纪律

所有阶段遵守 [Evidence, Gates and Handoff Contract](references/evidence-and-gates.md)：认可与充分定价分开、行业Beta与公司Alpha分开、负结论可以高置信通过、估值不通过只否定当前价格、趋势不通过只否定当前时点。（INV-01/04/05/17/18）

多候选研究对每个候选保留同一因果链，再在工作流层建立一次比较，不新增Skill或评分。没有有效候选集时写“机会排序：未评估”。

数据证据包已经带日期且研究截止日未变化时，下游不重复拉取；只有验证窗口、定义或受影响假设变化时才刷新。

## Memo 组装

需要成文时必须读取 [Presentation Contract](references/presentation-contract.md)。完整公司Memo只有在9阶段完成，或所有必要阶段已有明确Recheck/Reject记录时才能组装；阶段输出必须标为阶段备忘录。完整Memo综合现有结论，不补造缺失字段。

最终报告使用中文，保留来源、日期、口径、计算、冲突、Unknown和需要投资者判断的事项。研究中止时输出停止记录，说明最先失败环节、否定范围和重新开启条件。

## 红线

- 不增加机会分类体系、额外阶段、六问Skill或自动评分。
- 不使用七层推演、数值评分卡、贝叶斯合成或数值化护城河分替代因果链。（INV-26）
- 不把Financial Statement Analyzer当作投资阶段或独立投资判断。（INV-23）
- 不执行交易、不生成订单、不虚构仓位或精确比例。（INV-25）
- 不在缺少候选比较时声称“最优”“最景气”或“核心Alpha”。（INV-06）
- 最终投资决策由投资者完成。
