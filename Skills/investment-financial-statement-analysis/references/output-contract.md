# 财报分析输出契约

写作遵循[研究报告写作规范](../../../研究规则/研究报告写作规范.md)。以下是分析内容的覆盖要求，正文按读者问题组织，不直接照抄内部名称与字段。


## 1. 独立《财报分析报告》

按决策相关性组织，不必机械填满无关指标。默认主报告应让读者快速回答“本期发生了什么、为什么重要、是否可持续、下一步看什么”，不承担完整审计展示功能：

1. **报告边界**：对象、代码、市场、报告期、公告日、截止日、数据源、比较口径和最大可支持结论；
2. **本期最重要的财务变化**：3—5项能够改变经营或盈利判断的变化；
3. **最重要的3—5项数据**：最新值、比较基线、变化、商业影响、盈利/现金流影响和下一验证；
4. **收入与经营驱动**：分部、产品、地区、量价、份额、产品结构、季节性；
5. **利润与盈利能力**：毛利、经营利润、归母、扣非、利润率和驱动；
6. **资产负债表与营运资本**：应收、合同资产/负债、存货、预付、应付、资产质量；
7. **现金流、资本开支与自由现金流**：利润现金含量、资本开支性质、融资和分红影响；
8. **费用、研发与投入产出线索**：销售、管理、研发、财务费用以及费用资本化；
9. **会计、审计与治理观察**：审计意见、政策/估计变化、减值、关联交易、担保和或有事项；
10. **异常项目及可能原因**：支持解释、反证、持续性、下一验证；
11. **实际结果与基线比较**：公司指引、明确共识、预测区间和历史基线分别列示；
12. **经营改善或恶化时的财务变化**：仅描述后续经营和财务方向，不给估值或投资状态；
13. **验证指标、数据缺口与人工判断事项**。

以下主张级证据表属于内部研究层，默认写入 `Financial Base Packet`、`research_data/` 或单独的 `Evidence Appendix / Audit Log`，不附在主报告中：

| Claim ID | 原子主张 | 类别 | 证据角色 | 置信度 | 根来源 / Lineage ID | 独立原始证据数 | 冲突或口径限制 | 下一验证 / 证伪 |
|---|---|---|---|---|---|---|---|---|

类别使用 `Fact / Inference-Hypothesis / Market Narrative-Expectation / Valuation View-Model Output`。公司报告数字与 Tushare 对同一报告的复刻属于同一 lineage；两者一致可确认提取无误，但不是两条独立经营证据。管理层解释和指引必须与已报告数字分开分类。

重要结论使用：`事实 / 变化 / 推断 / 关键假设 / 待验证假设 / 未知或数据缺口`。不设置财务健康度评分，也不把“优秀/良好/一般/较差”作为自动决策。

主报告不默认展示上述标签，也不展示 `Claim ID`、证据类型/等级、置信度、Lineage ID、独立来源数量或完整研究过程。只有证据限制足以改变财务判断时，才在对应结论后用一句自然语言说明；例如“订单改善目前仅有管理层口径，尚未在合同负债和收入中得到确认”。

## 主报告的默认精简结构

1. 当前财务判断；
2. 最重要的3—5项变化及其经营含义；
3. 利润与现金流为何不同，经营和投资还需要多少资金；
4. 与公司指引或可识别市场预期的核心差异；
5. 最大风险或不确定性；
6. 下一步最重要的验证指标；
7. 数据来源。

其余分部明细、会计勾稽、异常竞争解释和完整指标表仅在与结论相关时进入正文；否则保留在内部底稿或按需附录。完整报告仍需在后台完成所有必需检查，精简的是表达而不是分析。

独立财报报告仅在可能被误读为投资结论时，用自然语言说明范围。例如：“这些数据有助于判断盈利质量；当前股价是否有吸引力，还需要结合行业前景与估值分析。”不要固定输出“辅助证据输出、最大可支持结论、尚未完成阶段、禁止外推”等流程字段。

## 2. Internal Research Layer / Financial Base Packet

供 `narrative-valuation` 复用，至少包含。它是机器可复用的内部研究层，不等同于用户主报告：

```text
Subject / Ticker / Market
As-of Date / Report Period / Publication Date / Report Type
Currency / Units / Consolidation Scope / Restatement Status
Comparison Basis
Source Coverage
Tushare Endpoint / Parameters / Retrieval Date / Raw Data Path
Claim-Level Evidence Register: Claim Class / Evidence Role / Confidence
Source Lineage: Original Source / Immediate Source / Lineage ID
Independent Original Evidence Count / Same-Lineage Repost Count / Conflicts

Revenue and Segment History
Margin and Profit History
Balance-Sheet and Working-Capital Changes
Cash-Flow and Capital-Expenditure Bridge
Earnings-Quality Reconciliation
Operating Driver Changes
Guidance and Identified Expectation Variance
Peer-Comparable Financial Evidence
Accounting / Audit / Governance Observations
Material Anomalies and Competing Explanations
One-Off versus Recurring Items
Verification Metrics and Dates
Falsification-Relevant Evidence
Unknowns / Definition Caveats / Source Conflicts
Normalized Attributable Profit
Normalized Profit Adjustments and Reliability Range
Maintenance versus Growth Capital Expenditure
Working-Capital Requirement
Shareholder-Distributable Cash Flow / FCFE Bridge
Negative-Cash-Flow Diagnosis: Growth Investment / Timing / One-Off / Structural
Current and Terminal Cash-Conversion Path / Timing / Verification Drivers
Net Cash or Net Debt / Minority Interests
Potential Dilution / Fully Diluted Shares
Recommended Valuation Basis: Cash Flow / Profit with Cash Conversion / Revenue-Unit-Economics Pressure Test
C0 or E0 Basis / Unit / Reliability Range
Sell-Side Forecast Set: `report_rc` Broker / Report Date / Forecast Year / Metric / Sample Coverage
```

每个决策关键变量保留：最新值、具名基线、变化、定义、单位、商业影响、盈利/现金流影响、来源与日期、下一验证。

当财务变化被解释为行业景气或公司竞争力时，附 `行业 Beta / 公司 Alpha / 分部结构 / 并表重述或基数` 的竞争解释。证据只支持公司自身时，不得在 Packet 中升级成行业事实。

## 3. 下游路由

| 证据 | 下游 Skill | 边界 |
|---|---|---|
| 历史财务、分部经济与经营驱动 | `narrative-valuation` | 帮助判断公司能否从行业增长中受益，不直接证明未来市场份额 |
| 可持续利润与可供股东使用的现金及差异 | `narrative-valuation` | 提供 `C0`，不直接形成价值结论 |
| 资本结构、少数股东与稀释 | `narrative-valuation` | 统一股权价值和完全摊薄每股口径 |
| 新财报相对冻结假设的变化 | `narrative-valuation` | 识别可能受影响的 `C0/Cn/n/r/持续性`，不自动改写假设 |

若数据包缺失报告期、来源、口径或关键勾稽关系，下游不得静默升级其置信度。
