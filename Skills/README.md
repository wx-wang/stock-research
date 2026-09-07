# Investment Agent Skills

本目录保存 Investment Agent 项目使用的核心研究 Skill 及其配套参考资料。

## 调度入口

- `investment-agent/SKILL.md`：总调度 Skill，负责选择研究入口、安排调用顺序、执行研究闸门和汇总输出。

## 六个核心研究 Skill

1. `investment-market-opportunity-scanner/SKILL.md`：市场环境与机会扫描
2. `investment-industry-value-chain/SKILL.md`：产业趋势、价值链与利润池
3. `investment-company-alpha/SKILL.md`：公司价值获取与竞争优势
4. `investment-earnings-valuation/SKILL.md`：盈利、预期差、估值与流动性
5. `investment-timing-portfolio/SKILL.md`：趋势确认与研究级投资状态
6. `investment-thesis-monitor/SKILL.md`：投资逻辑跟踪与重跑触发

每个 Skill 的 `references/` 目录包含该 Skill 的数据要求；调度 Skill 的 `references/` 目录包含共享数据路由、研究契约、编排规则和决策呈现规范。

核心链路：

```text
Market Regime
→ Industry Thesis
→ Profit Pool
→ Company Alpha
→ Earnings & Variant Perception
→ Valuation & Liquidity
→ Trend & Timing
→ Portfolio Management
```

这些 Skill 只用于研究和决策辅助，不执行自动交易，也不替代投资者的最终判断。
