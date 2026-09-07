# Investment Agent Data Call Plan v1.0

## 1. 目的与边界

本文把现有六个投资 Skill 的数据需求和调用顺序明确下来，供下一步把数据源写入 Skill 前评审。

本文不修改投资理念，不设计数据库、UI、自动交易或新的投资 Skill。Web Search 是每个 Skill 内部可选的数据能力，不是独立 Skill。

## 2. 数据源分工

### Tushare MCP：结构化事实的主来源

适合：行情、指数、行业分类、财务报表、财务指标、估值、成交、资金流、业绩预告、券商盈利预测、研报索引。

已验证的核心工具：

- `stock_basic`
- `daily`
- `daily_basic`
- `fina_indicator`
- `index_classify`
- `report_rc`

后续常用工具：`index_daily`、`index_dailybasic`、`sw_daily`、`index_member_all`、`income`、`balancesheet`、`cashflow`、`forecast`、`express`、`fina_mainbz`、`research_report`、`news`、`major_news`、`moneyflow`、`margin`、`trade_cal`、`hk_daily` 等。

调用原则：先取最小字段和明确日期，再按需要展开；必须保留交易日、报告期、公告日、数据更新时间和字段口径。

### 知识星球：观察者03的研究叙事与事件资料

适合：产业趋势、产业链、研报、机构观点、公司事件、催化剂和投资逻辑变化。

推荐只读调用链：

1. 按名称定位“观察者03”（运行时解析内部 group_id）；
2. `topic +search` 按“公司/行业 + 主题词”搜索；
3. 只对候选主题调用 `topic +detail`；
4. 逻辑跟踪使用 `group +topics` 查看最新主题。

调用原则：不把主题热度当作投资结论；搜索结果用于提出或验证假设，并保留主题发布时间和资料来源。

### IMA 知识库：补充研报和资料检索

固定范围：只使用【爱分享】的财经资讯，不在每次任务中扫描全部 IMA 知识库。

适合：按公司、行业、业务主题检索其中的外媒新闻、股票研报、机构观点和公告资料。

推荐只读调用链：

1. 在一次性配置/验收阶段用 `search_knowledge_base` 定位【爱分享】的财经资讯；
2. 用 `get_knowledge_base` 验证知识库名称和描述；
3. 正式运行时直接使用固定知识库标识调用 `search_knowledge`；
4. 只有需要原文时才调用 `get_media_info`。

调用原则：优先使用“公司/行业 + 业绩/供需/利润/估值”等短查询；一条长自然语言问题可能不命中。原文获取失败时只能使用条目元数据，并标记证据不足。

### Report CLI Skill：研报列表、摘要和 PDF

当前环境有 `report-cli` Skill，但没有同名 shell 可执行文件。它通过 HTTP 调用 Eastmoney 研报接口，已验证个股研报查询可用。

适合：行业研报、个股研报、策略报告、宏观研究、券商晨报的列表筛选、摘要提取和 PDF 下载。

主要接口：

- 个股研报：`POST https://reportapi.eastmoney.com/report/list2`；
- 行业研报：`GET https://reportapi.eastmoney.com/report/list`；
- 策略/宏观/晨报：`GET https://reportapi.eastmoney.com/report/jg`；
- 详情页：根据 `encodeUrl` 获取摘要和 PDF 链接。

主要字段：标题、券商、发布日期、评级、研报页数、股票/行业名称、研报编码、摘要和 PDF 链接。

调用原则：列表先筛选，再读取少量详情；API 查询间隔至少 1 秒，PDF 下载间隔至少 2 秒，单次会话不超过 10 份，避免触发限制。

### Web Search：时效性和公开一手证据

适合：最新政策、监管变化、公司公告、交易所文件、政府/协会统计、公司 IR、技术商业化进展、管理层公开表述、突发事件和催化剂。

不适合替代：长期行情序列、统一口径财务数据、精确估值历史、用户持仓和交易执行。

推荐调用方式：

- 用 `search_query` 搜索“实体 + 事件/指标 + 时间”；一次最多 4 个查询；
- 用 `open` 打开最相关的官方或一手页面；
- 记录页面标题、发布日期、事件发生日期、来源类型和链接；
- 重大结论优先用官方来源交叉验证，无法访问全文则标记 Unknown。

来源优先级：监管/政府/交易所/公司公告与 IR > 行业协会和原始研究 > 主流财经媒体 > 社区和自媒体。后两类只能作为线索或市场叙事证据。

## 3. 六个 Skill 的数据需求与调用顺序

## Skill 1：Market & Opportunity Scanner

### 需要的数据

- 市场状态：指数价格、成交额、成交量、市场宽度、风格和风险偏好；
- 流动性与宏观：利率、汇率、信用、融资融券、北向/南向或其他资金流；
- 行业变化：行业涨跌、相对强弱、成交和估值变化；
- 机会信号：技术、成本、政策、需求、供给、库存、渗透率、业绩或订单变化；
- 至少一个带日期的事实、对比基准、商业传导假设和验证事件。

### 推荐调用链

1. Tushare：`trade_cal` → `index_daily`/`index_dailybasic`/`daily_info` → `sw_daily` → `index_classify`/`index_member_all`；
2. Tushare：对初筛公司调用 `stock_basic`、`daily`、`daily_basic`；
3. 知识星球：搜索行业/主题和最新资料；
4. IMA：用短关键词补充行业或公司研究资料；
5. Report CLI：按行业、主题和日期筛选近期研报，必要时读取摘要；
6. Web Search：验证最新政策、公告、技术或需求变化；
7. 输出候选行业/公司队列和研究优先级，不直接给出 Buy。

### Web Search 触发条件

结构化数据发现异常变化，但缺少“为什么现在”的公开证据；或出现新政策、监管、技术、产品、订单等可能改变价值的事件。

## Skill 2：Industry Value Chain Analyzer

### 需要的数据

- 需求规模、增长、用户、应用和渗透率；
- 供给、产能、库存、成本曲线、进入/退出和替代；
- 上游—中游—下游关系、价格、成本、毛利和市场份额；
- 产业生命周期、变化持续时间和当前催化剂；
- 利润池当前位置、迁移方向、定价权和竞争反应。

### 推荐调用链

1. 接收 Scanner 的候选行业和变化假设；
2. Tushare：`index_classify`/`index_member_all`/`sw_daily` 确认行业边界和市场表现；
3. Tushare：对代表公司调用 `fina_mainbz`、`fina_indicator`、`income`，比较收入、利润和利润率；
4. 知识星球和 IMA：搜索“行业 + 供需/产能/价格/利润/竞争/技术”等短关键词；
5. Report CLI：获取行业研报和产业链研究，提取观点、日期和页数；
6. Web Search：查找政府/协会统计、监管政策、公司扩产和原始技术资料；
7. 输出产业趋势、价值链、利润池和受益环节，决定是否进入 Company Alpha。

### Web Search 触发条件

产业数据、政策、产能和技术演化不在 Tushare 中；或知识库观点无法确认事实来源时。

## Skill 3：Company Alpha Analyzer

### 需要的数据

- 产品、客户、应用、收入和利润来源；
- 公司在价值链中的位置；
- 市占率、客户留存/集中度、认证、切换成本、规模、成本、品牌或技术证据；
- 量、价、份额、产品结构、成本、毛利和现金流变化；
- 竞争对手的可比经营数据和相对变化；
- 订单、产品、客户、扩产和执行催化剂。

### 推荐调用链

1. 接收行业利润池和赢家特征；
2. Tushare：`stock_basic`/`stock_company`、`fina_mainbz`、`income`、`balancesheet`、`cashflow`、`fina_indicator`；
3. Tushare：`forecast`、`express`、`stk_managers`、`stk_rewards`、`top10_holders` 等补充经营和治理信息；
4. 对公司及主要竞争对手分别调用 Tushare 财务和行情接口；
5. 知识星球和 IMA：搜索公司、产品、客户、竞争和研报资料；
6. Report CLI：查询个股研报，筛选日期、评级和页数，必要时读取摘要或 PDF；
7. Web Search：优先验证公司公告、年报/中报、IR、客户认证、监管文件和技术商业化证据；
8. 输出 Company Alpha 和盈利驱动，不做最终估值或交易建议。

### Web Search 触发条件

竞争优势是非结构化事实，例如客户认证、产品落地、管理层执行、技术路线或监管限制，结构化数据无法证明时。

## Skill 4：Earnings & Valuation Analyzer

### 需要的数据

- 历史收入、利润、利润率、现金流和分部经营数据；
- 量、价、份额、产品组合、成本和费用驱动；
- 公司指引、业绩预告、业绩快报及公告日期；
- 券商盈利预测、预测区间、评级、目标价和市场叙事；
- 当前价格、股本、市值、PE/PB/PS、历史估值和可比公司；
- 成交量、换手率、流动性和风险收益；
- Bull/Base/Bear 的收入、利润、现金流、时间和估值假设。

### 推荐调用链

1. Tushare：`income`/`balancesheet`/`cashflow`/`fina_indicator` 建立自主历史基线；
2. Tushare：`forecast`/`express`/`report_rc`/`research_report` 获取指引、卖方预测和研报索引；
3. Tushare：`daily`/`daily_basic` 获取价格、估值和流动性；
4. 知识星球和 IMA：检索市场预期、机构观点、争议和预期差线索；
5. Report CLI：获取近期个股研报、评级、预测和目标价，并读取重点研报摘要；
6. Web Search：核实最新财报、公告、公司指引和公开研报；
7. 区分“卖方预测集合”“市场叙事”和真正的 Consensus，不把单一分析师观点当作一致预期；
8. 输出盈利变体、隐含预期、估值和风险收益。

### Web Search 触发条件

最新公告或财报尚未进入结构化数据；需要确认市场是否已经知道某个变化；或需要访问公开研报原文以识别主流预期。

## Skill 5：Timing & Portfolio Manager

### 需要的数据

- 长期、季度、60 日和短期价格/成交量结构；
- 基准和行业相对强弱；
- 突破、回撤、放量、缩量和趋势恶化；
- 催化剂日期及价格/成交反应；
- 上游 thesis、估值、风险收益、流动性和市场状态；
- 用户是否持有、当前状态和风险边界。

### 推荐调用链

1. 接收前四个 Skill 的完整结论；
2. Tushare：`daily`、`daily_basic`、`index_daily`、`sw_daily`、`moneyflow`、`stk_limit`、`trade_cal`；
3. 知识星球/IMA：只用于确认催化剂和市场叙事变化；
4. Report CLI：只在需要确认近期研报观点或评级变化时调用；
5. Web Search：只在催化剂日期、公告或事件状态需要确认时调用；
6. 结合用户持仓和风险边界，输出 Observe/Trial/Buy/Hold/Add/Reduce/Sell 条件，不执行交易。

### Web Search 触发条件

价格异常与基本面事件时间不一致，需要确认是否存在公告、监管、产品、诉讼、停产或其他事件。

## Skill 6：Investment Thesis Monitor

### 需要的数据

- 原始 Memo、假设、证伪条件、验证指标、催化剂和状态；
- 自原始 as-of date 以来的新行业、公司、财务、估值、趋势和事件事实；
- 原始预期与实际结果的对比；
- 最早受影响的研究环节和下游影响。

### 推荐调用链

1. 先读取原始 Memo，不先调用外部数据；
2. Tushare：按原始验证指标和时间窗口做增量查询：`daily`、`daily_basic`、`income`、`fina_indicator`、`forecast`、`express`、`report_rc`；
3. 知识星球：`group +topics` 查看最新资料，`topic +search` 定向查公司/行业，命中后再 `topic +detail`；
4. IMA：只对变化假设做定向搜索；
5. Report CLI：增量检索新研报、评级或预测变化；
6. Web Search：核实最新公告、政策、结果和催化剂兑现情况；
7. 定位最早受影响的 Skill，触发该 Skill 及所有下游 Skill 重跑。

### Web Search 触发条件

验证指标或催化剂可能已经发生，但 Tushare/知识库尚未更新，或者需要核对官方公告和事件日期。

## 4. 调度层的统一调用规则

1. 每次任务先确定市场、标的/行业、as-of date、投资问题和比较基准。
2. 结构化事实先取，非结构化资料后取，Web Search 最后用于时效验证或补缺。
3. 每个事实保留来源、观察期、发布日期、事件日期、字段口径和可靠性说明。
4. Web Search 一次最多发起 4 个相关查询；先搜后开源，重大事实优先打开官方页面。
5. 知识星球和 IMA 默认每个阶段一次定向搜索；机会发现任务例外，按滚动窗口和有限关键词集合扩大召回；没有命中时标记 Unknown，不用无边界同义词轰炸。
6. 同一研究任务内传递已取得的数据，不让下游 Skill 重复调用相同接口。
7. 数据源只提供 Fact；Skill 负责完成 Fact → Change → Business Impact → Earnings Impact → Market Pricing Impact。
8. 来源冲突时保留冲突，不用 Web Search 或知识库观点静默覆盖 Tushare 结构化数据。
9. Tushare 的卖方预测可以形成预测集合，但除非有明确聚合口径，不称为 Consensus。
10. Web Search 不能把缺失的财务、估值或持仓数据“搜索出来后直接当成确定事实”；无法确认就返回 Recheck。

## 5. 当前建议

下一步写入 Skill 时，建议按以下顺序：

1. 先写 Tushare 的最小结构化接口集合；
2. 再写观察者03知识星球的只读搜索和详情调用；
3. 再写固定【爱分享】财经资讯知识库的 IMA 短关键词检索和失败降级；
4. 接入 Report CLI 的研报列表、摘要和下载能力；
5. 最后把 Web Search 作为时效验证和一手证据补充；
6. 先做一轮完整研究任务验收，再决定是否增加更多 Tushare 工具。

## 6. v1.1 Opportunity Discovery Recall Plan

### 6.1 默认搜索模式

机会发现任务不再把观察者03最近30条主题作为唯一输入，而采用：

```text
Snapshot
→ Rolling Window Pagination
→ Keyword Recall
→ Selected Topic Detail
→ Tushare / Primary-Source Cross-Validation
```

### 6.2 观察者03调用策略

- `group +topics --limit 30`：快速捕捉当日或最近主题；
- 使用上一页的 `next_end_time` 翻页，覆盖最近7—30天；
- 对结构性产业主题延伸到30—90天；
- `topic +search` 使用多个短关键词召回，因接口无翻页，结果按 `topic_id` 合并去重；
- 对筛选后的高相关主题调用 `topic +detail`；
- 每次报告记录时间窗口、页数、关键词、去重主题数、详情数和未覆盖范围。

### 6.3 证据等级

| 等级 | 数据形态 | 可支持的判断 |
|---|---|---|
| Radar Only | 主题标题、列表、热度 | 市场关注方向 |
| Narrative Extracted | 主题正文、研报摘要、机构观点 | 市场叙事或投资假设 |
| Cross-Validated | 与Tushare、公告、政府/协会或其他一手来源核验 | 事实判断和阶段闸门 |

`Radar Only` 不得单独支撑 Industry Thesis、Profit Pool、Earnings、Valuation 或 Portfolio 的 Pass。

### 6.4 机会发现交接包

传给 Industry Value Chain Analyzer 的数据包必须包含：

- 候选粒度和已考虑的细分方向；
- 触发事实、对比基线和变化；
- 核心观点和市场当前认知；
- 价值迁移与利润池预检；
- 证据等级和来源日期；
- 验证指标、催化剂和数据缺口；
- `Pass`、`Recheck—Subsegment`、`Recheck—Data` 或 `Reject—Current Scope`。
