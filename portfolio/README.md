# Portfolio 事实记录（当前不属于默认研究链路）

`positions.json` 是持仓与自选股的**唯一事实源**。所有会话读取/更新同一份文件，禁止在对话里口头漂移。

根目录 `AGENTS.md` 已将择时、组合、仓位和自动投资状态移出当前默认研究链路。本目录目前只保留投资者已确认的持仓/自选事实和历史字段，不应被理解为已经存在一套正式的仓位或退出系统。

## 文件字段

### 顶层

| 字段 | 含义 |
|---|---|
| `updated` | 最近更新日期（YYYY-MM-DD） |
| `cash` | 可用现金（元）；`null` = 未录入 |

### `positions[]`（真实持仓）

| 字段 | 含义 |
|---|---|
| `code` | TS 代码（A股 `xxxxxx.SH/SZ`，港股 `xxxxx.HK`） |
| `name` | 股票名称 |
| `shares` | 持股数量 |
| `cost` | 持仓成本（元/股，含费用） |
| `state` | 投资状态：`watch`观察 / `trial`试仓 / `hold`持有 / `add`加仓评估 / `reduce`减仓评估 / `exit`卖出条件触发 |
| `thesisPath` | 对应 memo 路径（研究输出/个股研究/<公司名>） |
| `entry` | 建仓日期（YYYY-MM-DD） |
| `exit` | 清仓日期（YYYY-MM-DD，已清仓时填写） |
| `notes` | 备注 |

### `watchlist[]`（观察/自选，非持仓）

| 字段 | 含义 |
|---|---|
| `code` / `name` | 代码 / 名称 |
| `state` | 同上（通常为 `watch` 或 `trial`） |
| `thesisPath` | memo 路径 |
| `added` | 加入日期 |
| `reason` | 关注原因 |

## 规则

1. **positions 只记录事实**（已成交/已挂单的股数与成本）；研究状态、投资逻辑、预期差在 `thesisPath` 的 memo 里，不写进这里。
2. **state 是历史兼容字段**。在新的执行与风控规则经投资者批准前，不由任何默认 Skill 自动推导或更新；只能记录投资者明确确认的状态。
3. **禁止虚构**：不知道的字段留 `null`/空，不猜测持仓。
4. 新增研究标的 → 先经 Tushare `stock_basic`/`hk_basic` 核验代码，再入 `watchlist`。
5. 每次研究会话结束，若涉及持仓/自选变化，同步更新 `updated`。
