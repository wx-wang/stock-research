# Investment Agent Data Source Connectivity Report v1.1

## 1. 报告目的

本报告只验证当前 Investment Agent 计划使用的三类数据源是否能够在当前环境中完成只读调用，并梳理六个核心 Skill 后续可能需要的接口。

本次不修改任何 Skill，不写入数据源调用逻辑，也不设计数据库、UI 或自动交易流程。

## 2. 结论摘要

| 数据源 | 当前连通性 | 已验证能力 | 主要限制 | 当前建议 |
|---|---|---|---|---|
| Tushare MCP | HTTP MCP 已连通 | 完成协议握手；工具列表返回 248 个工具；股票、行情、财务、行业、估值、卖方预测接口均成功返回 | 当前 Codex 工具列表仍未将该地址注册为原生工具；字段口径和权限需在 Skill 接入时固定 | 可以进入下一步 Skill 接入评审，但先保留只读和最小字段集合 |
| 知识星球 Skill | 已连通 | 已定位“观察者03”；全文搜索、最新主题浏览、主题详情均成功 | 主要是非结构化研究资料；需要控制搜索和分页频率 | 可以作为研究叙事、研报、催化剂和逻辑跟踪的数据源 |
| IMA 知识库 Skill | API 连通 | 知识库名称搜索、知识库详情、知识条目检索均成功 | 当前没有名为“观察者03”的 IMA 知识库；长句查询未稳定命中；某 PDF 原文获取失败 | 可以作为补充研究资料源，但要用短关键词检索，并保留原文不可得的降级路径 |

## 3. 已执行的验证

### 3.1 知识星球：观察者03

已成功完成以下只读链路：

1. `group +list --json`：按名称定位“观察者03”。
2. `topic +search --group-id <group_id> --query <关键词> --json`：关键词“投资”返回主题结果。
3. `topic +detail --topic-id <topic_id> --json`：成功读取主题正文、附件和元信息。
4. `group +topics --group-id <group_id> --limit 5 --json`：成功读取最新主题，并返回分页游标。

因此，知识星球可以支持两种研究入口：

- 主题搜索：围绕行业、公司、产业链、业绩、估值等关键词查找历史资料；
- 最新主题巡查：用于催化剂、市场叙事和已有投资逻辑的变化跟踪。

本报告不保存或向用户展示 group_id、topic_id 等内部标识；后续由 Skill 在运行时自动解析和传递。

### 3.2 IMA 知识库

已确认本机 IMA 凭证存在，并成功调用官方只读接口：

1. `openapi/wiki/v1/search_knowledge_base`
   - 搜索“观察者03”返回空结果，说明 IMA 中没有同名知识库，或名称并非该名称。
   - 空关键词列出当前可见知识库，确认账户具备多个投研相关知识库。
2. `openapi/wiki/v1/get_knowledge_base`
   - 对一个财经资料知识库调用成功，返回名称、描述和推荐问题。
3. `openapi/wiki/v1/search_knowledge`
   - 使用公司名称“三花智控”成功返回多份相关研报条目。
   - 使用“分析商业航天产业趋势、利润池和主要受益公司”“分析一下商业航天板块未来发展前景”等长句未返回条目。
4. `openapi/wiki/v1/get_media_info`
   - 对一份搜索到的 PDF 尝试读取原文，接口返回“文件获取失败，请至 IMA 内查看处理”。

结论：IMA 的检索接口可以接受自然语言字符串，但本次实测更接近基于索引的关键词/实体检索，而不是稳定的自然语言问答。后续 Skill 不应假设一次长句搜索就能得到完整答案，应将研究问题压缩为“公司/行业实体 + 主题关键词”，并由 Agent 自己完成事实到投资结论的推理。

### 3.3 Tushare MCP

使用用户提供的 MCP 地址完成了只读 HTTP MCP 验证：

1. **协议握手成功**：`initialize` 返回 Tushare Server，协议版本为 `2025-06-18`。
2. **工具发现成功**：`tools/list` 返回 248 个可调用工具，覆盖 A 股、港股、指数、行业、财务、估值、资金流向、研报和宏观数据。
3. **股票基础信息成功**：调用 `stock_basic` 查询 `000001.SZ`，返回股票名称、行业、市场和上市日期。
4. **历史行情成功**：调用 `daily` 查询指定交易日，返回收盘价、涨跌幅、成交量和成交额。
5. **财务指标成功**：调用 `fina_indicator` 返回 ROE、净利率、收入增速、净利润增速和资产负债率等字段。
6. **行业分类成功**：调用 `index_classify` 返回申万一级行业列表。
7. **估值和流动性成功**：调用 `daily_basic` 返回换手率、PE、PB、PS、股息率和市值。
8. **卖方盈利预测成功**：调用 `report_rc` 返回券商研报中的预测收入、净利润、EPS、PE、评级和目标价区间等字段。

这证明 Tushare MCP 服务本身可用。需要区分的是：它目前是通过用户提供的 HTTP MCP 地址直接验证成功，尚未自动出现在当前 Codex 的原生工具清单中。后续把它写入 Skill 时，需要确定 Agent 运行时采用何种 MCP 注册方式，并固定字段、日期和权限口径。

本次已验证的核心工具名：

- `stock_basic`
- `daily`
- `daily_basic`
- `fina_indicator`
- `index_classify`
- `report_rc`

工具列表中还发现与六个 Skill 高度相关的接口，包括 `index_daily`、`sw_daily`、`index_member_all`、`income`、`balancesheet`、`cashflow`、`forecast`、`express`、`fina_mainbz`、`research_report`、`news`、`major_news`、`moneyflow`、`hk_daily` 等。

## 4. 六个核心 Skill 的数据源映射（候选，不代表已经写入）

### Skill 1：Market & Opportunity Scanner

**主要数据需求**

- 市场指数、成交量、波动、行业涨跌和相对强弱；
- 行业/主题近期变化、政策或产业催化剂；
- 候选公司清单及异常价格/成交变化。

**候选接口**

- Tushare：`index_daily`、`sw_daily`、`index_classify`、`index_member_all`、`daily`、`daily_basic`、`stock_basic`、`trade_cal`；
- 知识星球：`group +topics` 获取最新叙事，`topic +search` 搜索行业/主题资料，必要时 `topic +detail` 读取证据；
- IMA：`search_knowledge` 检索行业/主题关键词，必要时 `get_knowledge_base` 确认目标知识库。

**建议调用方式**

先用结构化行情筛选“发生变化的行业/公司”，再用知识星球和 IMA 验证变化是否具有产业和盈利含义。不要直接把知识库热度当成投资机会。

### Skill 2：Industry Value Chain Analyzer

**主要数据需求**

- 需求驱动、供需格局、产业生命周期；
- 产业链环节、议价权、利润池迁移和竞争动态；
- 产业趋势的验证指标和证伪信息。

**候选接口**

- 知识星球：`topic +search` → `topic +detail`，围绕行业、供需、技术、政策、利润率和竞争关键词检索；
- IMA：`search_knowledge`，使用“行业/产业链 + 供需/利润/竞争/景气”等短关键词组合；
- Tushare：`sw_daily`、`index_member_all`、`index_classify`、`fina_mainbz`、`fina_indicator`，并用 `daily`/`daily_basic` 做行业公司横向验证。

### Skill 3：Company Alpha Analyzer

**主要数据需求**

- 公司主营、收入和利润结构；
- 商业模式、竞争优势、客户/产品结构、资本开支和成长来源；
- 管理层执行、行业位置及利润池承接能力。

**候选接口**

- Tushare：`stock_basic`、`income`、`balancesheet`、`cashflow`、`fina_indicator`、`fina_mainbz`、`stk_managers`、`stk_rewards`、`forecast`、`express`、`disclosure_date`；
- 知识星球：公司名称搜索，命中后用 `topic +detail` 获取研报/纪要内容；
- IMA：`search_knowledge` 以公司名称为主词检索研报条目；如需原文，再尝试 `get_media_info`，失败时保留“仅有条目元数据”的降级结果。

### Skill 4：Earnings & Valuation Analyzer

**主要数据需求**

- 历史及前瞻收入、利润、现金流和关键经营指标；
- 市场一致预期或可替代的市场基准；
- 当前价格、估值倍数、隐含增长和流动性；
- 研究资料中的主流预期与可能的 Variant Perception。

**候选接口**

- Tushare：`income`、`forecast`、`express`、`fina_indicator`、`daily_basic`、`daily`、`report_rc`、`research_report`、`disclosure_date`；
- 知识星球：公司/行业业绩、预期、目标价、估值关键词搜索与主题详情；
- IMA：公司名称 + 业绩/盈利/估值/目标价等短关键词检索。

**关键限制**

IMA 和知识星球不能替代统一口径的结构化财务与行情数据；Tushare 已具备这类数据能力，但仍需在 Skill 中固定复权、报告期、公告日、估值日期和缺失值处理口径。

### Skill 5：Timing & Portfolio Manager

**主要数据需求**

- 价格趋势、成交量、波动和相对强弱；
- 市场环境、流动性和已有仓位；
- 催化剂兑现情况、买入/观察/加仓/减仓条件。

**候选接口**

- Tushare：`daily`、`daily_basic`、`index_daily`、`sw_daily`、`moneyflow`、`trade_cal`；
- 知识星球：`group +topics` 和 `topic +search` 追踪新催化剂、业绩和叙事变化；
- IMA：只作为补充研究资料，不作为实时趋势和持仓数据的主来源。

**关键限制**

数据源只能提供事实和信号，不能替代投资者对仓位、最大可承受损失和最终执行的人工判断。

### Skill 6：Investment Thesis Monitor

**主要数据需求**

- 原始投资逻辑、关键假设、证伪条件和验证指标；
- 新业绩、新公告、新产业资料、价格趋势和估值变化；
- 与原始基准的差异及触发的重新研究阶段。

**候选接口**

- 知识星球：`group +topics` 做最新资料巡查，`topic +search` 查公司/行业变化，`topic +detail` 读取证据；
- IMA：`search_knowledge` 做定向增量检索；
- Tushare：`daily`、`daily_basic`、`income`、`fina_indicator`、`forecast`、`express`、`research_report`、`news`/`major_news`。

## 5. 调用原则（建议先写入规范，再写入 Skill）

1. **先确定目标范围**：知识星球固定为“观察者03”；IMA 必须由用户确认具体知识库名称，不能默认把“观察者03”映射到 IMA。
2. **先结构化、后非结构化**：市场状态、价格、财务和估值优先使用结构化数据；知识库用于解释变化、寻找产业证据和识别市场预期。
3. **查询词短而具体**：IMA 优先使用“公司/行业 + 主题词”，例如“公司名 业绩”“行业名 利润池”“公司名 机器人业务”，避免一条长问题包含多个推理任务。
4. **控制调用次数**：一次研究阶段默认每个知识源一次定向搜索；只有命中结果需要展开时才调用详情，不做无目的全库扫描。
5. **证据与推理分离**：数据源只返回事实、条目、原文或元信息；Skill 负责完成“事实 → 变化 → 商业影响 → 盈利影响 → 市场定价影响”。
6. **保留降级状态**：原文获取失败、数据字段缺失、搜索为空或来源过时，都必须在 Skill 输出中标记，不得静默补全。
7. **只读优先**：第一阶段只接入搜索、浏览、详情和数据读取接口，不接入发布、编辑、删除、自动交易等写操作。

## 6. 是否现在写入 Skill

### 可以在下一步写入的部分

- 知识星球“观察者03”的只读调用约定：按名称定位、主题搜索、最新主题浏览、主题详情读取；
- IMA 的只读调用约定：知识库名称搜索、知识库详情、知识条目搜索，以及原文获取失败时的降级处理；
- 六个 Skill 对上述两类非结构化资料的输入用途、查询词规范和调用次数限制。
- Tushare 的只读调用约定：先接入已验证的 `stock_basic`、`daily`、`daily_basic`、`fina_indicator`、`index_classify`、`report_rc`，再按 Skill 需要增加其他接口。

### 暂不应写入的部分

- Tushare 的全量 248 个工具：不应一次性全部暴露给 Agent，应按六个 Skill 的最小数据需求逐步接入；
- 尚未完成字段口径确认的高级接口，尤其是复权、报告期、公告日、港股和卖方预测数据；
- 把 IMA 长句搜索当作稳定的自然语言问答接口；
- 把知识星球或 IMA 的资料热度直接转成买入结论；
- 任何自动交易或自动调仓动作。

## 7. 需要投资者确认的事项

在正式把数据调用写入六个 Skill 之前，只需要确认两点：

1. IMA 要固定使用哪个知识库。当前测试的是一个财经资料知识库，仅用于验证链路，不应自动成为最终默认库。
2. Tushare MCP 在 Agent 运行时的注册方式。HTTP 端点已经验证可用，下一步需要决定是以原生 MCP Server 注册，还是由一个受控的只读适配层转发。

**当前建议：可以批准知识星球、IMA 和 Tushare 的只读接入方向；Tushare 先只写入已验证的最小接口集合，不要一次性接入全部工具。**
