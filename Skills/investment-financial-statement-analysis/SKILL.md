---
name: investment-financial-statement-analysis
description: Analyze an A-share or Hong Kong listed company's financial statements, earnings quality, working capital, cash flow, reinvestment, dilution, accounting anomalies, and operating changes. Use for a standalone review or to build the Financial Base Packet for narrative valuation. Do not issue valuation, timing, position, or buy/hold/sell conclusions.
---

# Financial Statement Analysis

Produce a dated, traceable financial-statement review and a reliable cash-flow base for narrative valuation without turning accounting results into an investment decision.

## Before Analysis

Read:

- [references/data-and-calculation-contract.md](references/data-and-calculation-contract.md) for period normalization, formulas, accounting definitions, anomaly tests, and industry-specific applicability.
- [references/output-contract.md](references/output-contract.md) for the standalone report and `Financial Statement Evidence Packet` schemas.

For a named company, first confirm the listed entity and ticker with Tushare `stock_basic`. Record the market, as-of date, report type, report period, publication date, investor question, available comparison periods, and known missing inputs. Do not confuse a parent group, subsidiary, brand, or concept with the listed entity.

Use the company's filing and notes when the analysis depends on accounting policy, segment definitions, audit opinion, impairments, related parties, commitments, or management explanations. Use Tushare as the default structured source: `income`, `balancesheet`, `cashflow`, `fina_indicator`, `fina_mainbz`, `forecast`, `express`, and `disclosure_date`; use `daily`, `adj_factor`, and `daily_basic` only when price, shares, or market value are needed for the downstream valuation date. Use `report_rc` for a dated sell-side forecast set and label its broker/sample coverage; it is not automatically complete consensus. Treat broker reports, Knowledge Star, IMA, and media as expectation or narrative evidence, not proof of reported accounting facts.

Classify at the **atomic-claim level**, not the document level: `Source → Claim → Claim Class → Evidence Role → Source Lineage → Confidence → Verification/Falsifier`. A filing may contain a reported fact, a management explanation, and forward guidance; keep them separate. For decision-relevant claims, use `Fact / Inference-Hypothesis / Market Narrative-Expectation / Valuation View-Model Output` alongside the existing Chinese evidence labels. Assign `Evidence Confidence: High / Medium / Low` from directness, proximity to the original event, scope and accounting-definition completeness, timeliness, independent corroboration, and unresolved conflicts. Do not score mechanically; low-confidence evidence may generate an investigation or hypothesis but cannot by itself verify a key accounting fact.

Trace `Original Source → Secondary Source → Repost / Commentary`. Tushare fields reproduced from a company filing and the filing itself are one lineage, not two independent confirmations. Record discrepancies between the structured field and filing instead of choosing silently.

## Operating Modes

### Standalone Financial-Report Review

Use when the user asks to read, review, compare, or diagnose a quarter, interim report, annual report, or five-year financial history. Output a `财报分析报告`, not a complete `Investment Memo`. State the maximum supported conclusion and list the investment stages that remain uncompleted.

### Narrative-Valuation Support

Produce a `Financial Base Packet` for `narrative-valuation`. In addition to normalized history and earnings quality, preserve both normalized attributable profit and shareholder-distributable cash flow or FCFE. Diagnose whether negative cash flow is caused by growth capital expenditure, working-capital timing, one-offs, or a structural inability to monetize accounting profit. State the recommended valuation-basis route (`cash-flow / profit-with-cash-conversion / revenue-or-unit-economics pressure test`), the basis and unit of `C0/E0`, maintenance versus growth capital expenditure, working-capital needs, net debt, minority interests, potential dilution, and fully diluted shares. The downstream skill decides whether the valuation model is applicable.

### Financial-Report Delta

Use after a new filing to compare actual results with the prior filing, management guidance, an identified forecast baseline, and the previously frozen narrative assumptions. Preserve the prior baseline. State which observations could change `C0`, terminal cash flow, development time, discount rate, or terminal durability; do not independently change the valuation conclusion.

## Required Analysis

1. Normalize periods and definitions before calculating anything: annual, year-to-date, derived single quarter, trailing twelve months, restated history, currency, units, consolidation scope, and continuing operations.
2. Identify the material changes in revenue, gross profit, operating profit, attributable profit, adjusted attributable profit, margins, expenses, assets, liabilities, working capital, operating cash flow, capital expenditure, and free cash flow.
3. Decompose material operating changes where data permit: segment, product, geography, volume, price, market share, mix, unit cost, utilization, customer concentration, and seasonality.
4. Test earnings quality by reconciling profit with cash flow and balance-sheet movements. Inspect receivables, notes, contract assets/liabilities, inventory, prepayments, payables, tax, minority interests, non-recurring items, grants, fair-value changes, impairments, capitalized development, goodwill, restricted cash, debt maturity, guarantees, related parties, and contingent liabilities when material.
5. Review audit opinion, internal-control opinion, accounting-policy or estimate changes, restatements, consolidation-scope changes, and management explanations for annual reports or whenever relevant.
6. Compare actual results with a clearly identified baseline. Keep company guidance, explicit consensus, broker forecast range, historical trend, peer benchmark, and price-implied expectations distinct.
7. Flag anomalies using both materiality and context. A percentage threshold alone is not evidence of risk; test absolute amount, base effect, seasonality, accounting definition, company history, and named peers.
8. Internally classify decision-relevant observations as `事实 / 变化 / 推断 / 关键假设 / 待验证假设 / 未知或数据缺口`, with source, period, publication date, units, baseline, and next verification. Do not expose these fields mechanically in the user-facing report.
9. For each conclusion that compares the company with its industry, test competing explanations: industry Beta, company Alpha, segment mix, consolidation/restatement, and base effects. A company's reported change directly proves only that company's result; do not generalize it into an industry fact without independent industry, peer, customer, or supplier evidence.

## Required Outputs

Return:

- Report identity and comparison basis;
- Executive financial changes;
- Income-statement and operating-driver analysis;
- Balance-sheet and working-capital quality;
- Cash-flow, capital-expenditure, and free-cash-flow analysis;
- Earnings-quality reconciliation;
- Segment and geographic analysis;
- Expense and R&D analysis;
- Accounting, audit, and governance observations;
- Material anomalies and plausible explanations;
- Actual results versus identified guidance or expectation baseline;
- Verification metrics, next reporting window, missing inputs, and human judgment items;
- `Financial Base Packet` for downstream use, including the normalized `C0` bridge and fully diluted basis;
- an internal claim-level evidence register for decisive facts and inferences, including claim class, evidence role, confidence, root source/lineage, independent-chain count, conflicts, and next verification; store it in the `Financial Base Packet`, `research_data/`, or an optional audit appendix rather than the default report;
- a valuation-basis diagnosis that preserves normalized profit even when current shareholder cash flow is negative, plus the dated profit-to-cash conversion path and failure conditions;
- explicit conclusion boundary and uncompleted investment stages.

The default user-facing report is a decision-oriented summary, not an audit export. It should lead with the current financial judgment, then show only the 3–5 most important figures or changes, their operating/cash-flow meaning, the largest uncertainty, and the next verification metrics. Do not print `Claim ID`, `Evidence Type/Tier`, `Confidence`, `Lineage ID`, independent-chain counts, or a full evidence register unless the user explicitly requests an audit. If evidence quality materially limits a conclusion, translate the limitation into plain language, for example: “回款改善目前只见于单季，尚缺后续报告确认。”

When data are absent, write `未知或数据缺口`; do not manufacture values, silently use an industry average, or infer a note disclosure from a summarized database field.

## Handoff Boundary

Send normalized history, segment economics, operating drivers, earnings quality, shareholder-cash-flow bridge, capital structure, dilution, risks and Unknowns to `narrative-valuation`. These are inputs, not proof that the company can capture the industry's terminal value. Preserve dated deltas so the downstream analysis can identify which frozen narrative assumption may need revision.

## Prohibited Conclusions

Do not:

- output Buy, Hold, Add, Reduce, Sell, target price, position size, or timing state;
- call low PE/PB, a drawdown, strong reported growth, or positive free cash flow proof of undervaluation;
- call industry growth or a good financial ratio Company Alpha without named-peer and causal evidence;
- call an earnings beat a durable variant without a market-expectation baseline and downstream analysis;
- create a numerical scorecard, assign narrative probabilities, or convert accounting observations directly into an investment action.
- count a database copy, media quotation, or repeated broker citation of the same filing as independent corroboration.

Archive a standalone written result under `研究输出/个股研究/<公司名>/<YYYYMMDD>_<公司>_财报分析_<报告期>.md`. Never use the complete `Investment Memo` filename for this output.
