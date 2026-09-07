# Data Source Routing and Evidence Contract v2.0

This reference defines how the Investment Agent obtains evidence for the six investment skills. It is a routing and evidence policy, not a database schema and not an automatic trading interface.

## 0. 问题类型 → 数据源匹配（决定性规则）

先判定问题的性质，再选数据源，不要用“事实源”验证“叙事类”问题：

- **事实核查类**（业绩/公告/价格/监管/事件日期）→ 官方公告 + Tushare/结构化 + 权威媒体；
- **叙事 / 产业链关联 / 传闻 / 催化预期类**（“某公司是否进入某产业链”“市场在传什么”“前瞻合作是否成立”）→ **观察者03 星球 + IMA 研报 + 研报CLI/互动易优先**；官方公告与财经媒体只做**最后确认**。这类信息在官方渠道往往缺位或滞后，**不得用“官方查不到”等同于“不存在”**。
- 判定示例：单公司“是否绑定英伟达/某链”→ 先在星球搜该公司词 → 研报 → 再官方验证；同理，“某公司最近有何大动作”应先看星球/研报/互动易，而非只看公告。

## 1. Source roles

### Tushare MCP — structured facts

Use Tushare as the primary source for numeric and tabular facts:

- market and index prices, turnover, breadth proxies and industry performance;
- stock master data and industry membership;
- income statement, balance sheet, cash flow and financial indicators;
- daily valuation and liquidity metrics;
- earnings forecasts, earnings previews and broker forecast records;
- research-report indexes and selected market-flow data.

The runtime should expose the user-configured Tushare MCP server as a read-only tool. Do not hard-code the token in a skill or script. Use the smallest field set and explicit dates needed for the current stage.

Core tool mapping:

| Research need | Tushare tools |
|---|---|
| Market regime | `trade_cal`, `index_daily`, `index_dailybasic`, `daily_info`, `moneyflow_hsgt`, `margin`, `shibor`, `index_global` |
| Industry opportunity | `sw_daily`, `index_classify`, `index_member_all`, `daily`, `daily_basic`, `stock_basic` |
| Industry/company economics | `fina_mainbz`, `income`, `balancesheet`, `cashflow`, `fina_indicator` |
| Company events and execution | `forecast`, `express`, `disclosure_date`, `stk_managers`, `stk_rewards`, `top10_holders` |
| Financial-statement review | `income`, `balancesheet`, `cashflow`, `fina_indicator`, `fina_mainbz`, `express`, `forecast`, `disclosure_date` |
| Earnings and market expectations | `forecast`, `express`, `report_rc`, `research_report`, `income`, `fina_indicator` |
| Valuation and liquidity | `daily`, `daily_basic`, `trade_cal`, `margin_detail`, `moneyflow` |
| Trend and monitoring | `daily`, `daily_basic`, `index_daily`, `sw_daily`, `moneyflow`, `stk_limit`, `suspend_d` |

`report_rc` is a sell-side forecast set, not automatically a consensus. If an aggregate consensus is not explicitly available, label the result as a forecast range or broker-estimate set.

### Knowledge Star — `观察者03`

Use the fixed group `观察者03` for Chinese research notes, institutional views, industry-chain discussion, catalysts and thesis changes.

Read-only route:

1. Resolve the group by name once per runtime or configuration check with `group +list`.
2. Search with `topic +search` using a short query: entity + topic, for example `公司名 业绩`, `行业名 供需`, or `公司名 机器人业务`.
3. Open only selected hits with `topic +detail`.
4. For monitoring, use `group +topics` for recent topics, then search/detail only when a topic is relevant.

For opportunity discovery, do not rely on the latest 30 topics alone. Use a bounded recall strategy:

1. `group +topics --limit 30` for a fast snapshot;
2. paginate with the previous page's `next_end_time` to cover the task's 7—30 day current window or 30—90 day structural window;
3. run several short `topic +search` queries (entity + topic, or related synonyms) because search has no pagination;
4. merge and de-duplicate by `topic_id`;
5. call `topic +detail` only for shortlisted relevant topics;
6. report time window, pages, keywords, unique topics, details retrieved and coverage gaps.

Evidence labels:

- `Radar Only`: list/title/heat signal;
- `Narrative Extracted`: topic body, report summary or analyst view read;
- `Cross-Validated`: corroborated by Tushare, company filing, regulator, government, association or another primary source.

Do not treat topic count, likes or heat as investment evidence. Use the content as a dated source for a claim, hypothesis or catalyst, and never upgrade `Radar Only` to a verified fact without corroboration.

### IMA — fixed knowledge base `【爱分享】的财经资讯`

Do not search all IMA knowledge bases during normal research. Resolve and verify this knowledge base once, then call it directly.

Configuration/check route:

1. `search_knowledge_base` with the exact name `【爱分享】的财经资讯`.
2. `get_knowledge_base` to verify the returned name and description.

Runtime route:

1. `search_knowledge` with the fixed knowledge-base identifier and a short entity/topic query.
2. Call `get_media_info` only for a selected item whose original content is necessary.

IMA results may be metadata only. If original retrieval fails, preserve the item title, date and available fields but mark the underlying claim as unverified.

### Report CLI Skill — report discovery and PDF evidence

`report-cli` is an HTTP-backed skill, not a local shell binary. Use it when the task needs a report list, rating/page filters, report summaries or PDF retrieval.

Routes:

- Stock reports: `POST https://reportapi.eastmoney.com/report/list2`.
- Industry reports: `GET https://reportapi.eastmoney.com/report/list`.
- Strategy, macro and morning reports: `GET https://reportapi.eastmoney.com/report/jg`.
- Detail and PDF: use the returned `encodeUrl` to open the appropriate report detail page, then extract the summary or PDF link.

Use list-first, detail-second retrieval. Filter by date, entity, rating and page count before opening reports. Respect the skill's rate limits and do not download more than the task needs.

### Web Search — current public evidence

Use Web Search as a targeted supplement, not as the default numeric data source.

Use `search_query` for up to four focused queries per call, then `open` the most relevant primary pages. Prioritize:

1. regulators, governments, exchanges and company announcements/IR;
2. industry associations and original technical or policy documents;
3. reputable financial media and research pages;
4. community or self-media only as hypothesis/market-narrative evidence.

Typical triggers are a new policy, a company announcement, a technology/commercialization event, a customer/qualification claim, a catalyst date, or information not yet present in Tushare/knowledge sources.

## 2. Structured versus unstructured processing

### Structured packet

For each Tushare call, retain:

- tool name and query arguments;
- observation date, report period and announcement date where applicable;
- requested fields and units;
- returned values and missing values;
- source and retrieval timestamp.

The model may calculate changes, ratios and scenario inputs from this packet, but must not silently fill missing fields.

### Unstructured evidence packet

For each selected Knowledge Star, IMA, report-cli or Web Search item, the model should extract:

- title, publisher/author and source;
- publication date and event date if different;
- the exact claim or a faithful short paraphrase;
- entity/industry and causal link affected;
- evidence type: Fact, market narrative, analyst view, management statement or hypothesis;
- supporting and contradicting signals;
- reliability and freshness;
- which verification metric or falsification condition it affects.

The model must not convert a single report, media item or opinion into consensus or fact without corroboration.

## 3. Skill-specific routing

### Market & Opportunity Scanner

1. Tushare market/industry snapshot.
2. Tushare candidate stock and valuation snapshot.
3. `观察者03` and IMA searches for the dated change and catalyst.
4. Report CLI for recent industry/strategy/company report discovery.
5. Web Search for current official confirmation when the change is recent or disputed.

Output a candidate queue and research priority, not a Buy decision.

### Industry Value Chain Analyzer

1. Tushare industry boundary, members, sector performance and peer economics.
2. Knowledge Star/IMA industry-chain searches.
3. Report CLI industry reports and selected summaries.
4. Web Search for government/association demand, capacity, policy and technology evidence.

Output industry thesis, value-chain map, profit-pool location and beneficiary segment.

Six-question routing within this Skill:

| Question | Preferred evidence mix |
|---|---|
| Q1 size/growth/cycles | Tushare/structured series + government/association definitions + company operating data |
| Q2 map/profit distribution | selected industry reports + participant filings/segment economics + primary transaction/dependency evidence |
| Q3 segment economics/moats | peer financials and return metrics + market-share/customer evidence + reports for hypotheses |
| Q4 technology | primary technical/standards papers, company R&D/commercialization disclosures, association data; media only as trigger |
| Q5 regulation/geopolitics/localization | government/regulator/customs/association and company disclosures; reports/narratives for interpretation |
| Q6 valuation/narrative | Tushare valuation/financial series + explicit forecast sets/reports + Knowledge Star/IMA for dated market narrative |

No single source type is sufficient for all six questions. Preserve definition, date, evidence level, and cross-source conflicts for each material question.

### Company Alpha Analyzer

1. Reuse a dated `Financial Statement Evidence Packet` for segment economics and peer-comparable operating changes when available, then retrieve only missing Tushare company master, segment, statement, or indicator facts.
2. Tushare peer set and comparable operating changes.
3. Knowledge Star/IMA company, product, customer and competitor searches.
4. Report CLI stock reports filtered by date, rating and page count.
5. Web Search for filings, IR, customer qualification, technology and execution evidence.

Output company alpha and growth/cash-flow drivers, not valuation or timing.

### Earnings & Valuation Analyzer

1. Reuse a dated `Financial Statement Evidence Packet` when available; otherwise obtain the minimum historical financials and operating drivers needed for the decision.
2. Tushare guidance, previews, `report_rc` forecast set and `research_report` index.
3. Tushare price, valuation and liquidity snapshot.
4. Knowledge Star/IMA and report-cli for market narrative, forecasts and disagreement.
5. Web Search for the newest filing, guidance or public report.

Output independent earnings scenarios, variant perception, implied expectations, valuation and risk/reward.

### Financial Statement Analyzer

1. Confirm the listed entity with Tushare `stock_basic` and retrieve the minimum required `income`, `balancesheet`, `cashflow`, `fina_indicator`, `fina_mainbz`, `express`, `forecast`, and `disclosure_date` fields for explicit report periods.
2. Use the original company filing and notes for audit opinion, accounting policy or estimate changes, restatements, segment definitions, impairments, related parties, guarantees, commitments, contingencies, and management explanations.
3. Use Knowledge Star, IMA, report-cli, and media only for identifiable guidance, forecast, or narrative baselines; they cannot replace reported accounting facts.
4. Preserve annual, year-to-date, derived single-quarter, TTM, restated, currency, unit, consolidation-scope, and continuing-operation definitions.

Output a standalone financial-report review or `Financial Statement Evidence Packet`, never an investment stage gate, valuation, timing, or position conclusion.

### Timing & Portfolio Manager

1. Validate all upstream outputs and user-provided position/risk context.
2. Tushare multi-window price, volume, relative-strength and liquidity data.
3. Knowledge Star/IMA or report-cli only for catalyst and narrative timing.
4. Web Search only to verify an event date or material announcement.

Output research-level state and conditions; never submit or imply an order.

### Investment Thesis Monitor

1. Read the baseline memo and its original metrics first.
2. For a new filing, reuse the Financial Statement Analyzer delta packet; query Tushare only for uncovered fields in the delta window and original verification metrics.
3. Check recent `观察者03` topics and targeted IMA items.
4. Search new reports and public events only when a metric, assumption or catalyst may have changed.
5. Rerun the earliest affected skill and all required downstream skills.

Output Strengthened, Unchanged, Weakened or Invalidated with the affected link.

## 4. Evidence and gating rules

- Source retrieval is not an investment conclusion.
- Every material conclusion must separate Fact, Change, Inference, Assumption and Unknown.
- Structured and unstructured sources must preserve their own dates and definitions.
- Conflicting sources remain visible; do not silently select the bullish interpretation.
- If a required structured field or corroborating evidence is missing, return Recheck with the exact missing input.
- A web result, report or knowledge-base item may support a hypothesis but cannot by itself pass an earnings, valuation or portfolio gate.
- The common reasoning chain remains: Fact → Change → Business Impact → Earnings Impact → Market Pricing Impact.
- A broad or heterogeneous industry must be decomposed before a sector-wide Reject; preserve `Recheck—Subsegment` when the scan has not tested its major profit pools.

## 5. Call-budget defaults

- Tushare: batch compatible fields and dates; avoid retrieving the same series again downstream.
- Knowledge Star: use snapshot + bounded pagination for opportunity discovery, then multiple short keyword searches and detail only for selected hits; de-duplicate in the current task and record coverage rather than scanning the entire historical archive.
- IMA: one targeted `search_knowledge` call per stage by default; do not repeat broad natural-language queries.
- Report CLI: list first, open only shortlisted reports; download only when full text is required.
- Web Search: one focused query bundle per unresolved question, then open primary sources.
