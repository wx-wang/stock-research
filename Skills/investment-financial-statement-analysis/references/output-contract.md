# 财报分析输出契约

## 1. 独立《财报分析报告》

按决策相关性组织，不必机械填满无关指标：

1. **报告边界**：对象、代码、市场、报告期、公告日、截止日、数据源、比较口径和最大可支持结论；
2. **本期最重要的财务变化**：3—5项能够改变经营或盈利判断的变化；
3. **关键数据证据表**：最新值、基线、变化、商业影响、盈利/现金流影响、来源日期、下一验证；
4. **收入与经营驱动**：分部、产品、地区、量价、份额、产品结构、季节性；
5. **利润与盈利能力**：毛利、经营利润、归母、扣非、利润率和驱动；
6. **资产负债表与营运资本**：应收、合同资产/负债、存货、预付、应付、资产质量；
7. **现金流、资本开支与自由现金流**：利润现金含量、资本开支性质、融资和分红影响；
8. **费用、研发与投入产出线索**：销售、管理、研发、财务费用以及费用资本化；
9. **会计、审计与治理观察**：审计意见、政策/估计变化、减值、关联交易、担保和或有事项；
10. **异常项目与解释竞争**：支持解释、反证、持续性、下一验证；
11. **实际结果与基线比较**：公司指引、明确共识、预测区间和历史基线分别列示；
12. **Bull/Bear财务含义**：仅描述后续经营和财务方向，不给估值或投资状态；
13. **验证指标、数据缺口与人工判断事项**。

重要结论使用：`事实 / 变化 / 推断 / 关键假设 / 待验证假设 / 未知或数据缺口`。不设置财务健康度评分，也不把“优秀/良好/一般/较差”作为自动决策。

独立报告结尾固定说明：

```text
输出类型：财报分析报告（辅助证据输出）
最大可支持结论：仅限已披露财务表现、经营变化与盈利质量
尚未完成：产业终局、公司价值捕获、独立终局情景、价格隐含终局与 Narrative Gap
禁止外推：本报告不构成买入、持有、卖出、目标价或仓位结论
```

## 2. Financial Base Packet

供 `narrative-valuation` 复用，至少包含：

```text
Subject / Ticker / Market
As-of Date / Report Period / Publication Date / Report Type
Currency / Units / Consolidation Scope / Restatement Status
Comparison Basis
Source Coverage
Tushare Endpoint / Parameters / Retrieval Date / Raw Data Path

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

## 3. 下游路由

| 证据 | 下游 Skill | 边界 |
|---|---|---|
| 历史财务、分部经济与经营驱动 | `narrative-valuation` | 只约束公司价值捕获桥，不直接证明终局份额 |
| 正常化利润与股东现金流桥 | `narrative-valuation` | 提供 `C0`，不直接形成价值结论 |
| 资本结构、少数股东与稀释 | `narrative-valuation` | 统一股权价值和完全摊薄每股口径 |
| 新财报相对冻结假设的变化 | `narrative-valuation` | 识别可能受影响的 `C0/Cn/n/r/持续性`，不自动改写假设 |

若数据包缺失报告期、来源、口径或关键勾稽关系，下游不得静默升级其置信度。
