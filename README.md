# 股票投研工作空间

以行业研究、财报分析和个股估值为核心，支持市场扫描、外部资料研读、行业方法积累，以及有条件的购买判断。项目总规则见 [AGENTS.md](AGENTS.md)。

## 三个核心技能，只维护一份

| 技能 | 唯一源目录 |
|---|---|
| 行业分析 | [Skills/industry-understanding](Skills/industry-understanding/SKILL.md) |
| 财报分析 | [Skills/investment-financial-statement-analysis](Skills/investment-financial-statement-analysis/SKILL.md) |
| 个股分析与估值 | [Skills/narrative-valuation](Skills/narrative-valuation/SKILL.md) |

全局技能目录只放指向上述源目录的链接，不复制内容。项目中修改后，本机其他 Codex 任务也使用同一份。技能中的相对引用应从实际源文件所在目录解析。

## 本机或另一台电脑使用

需要 Python 3 和支持符号链接的文件系统。在项目根目录执行：

```sh
python3 scripts/link_core_skills.py
python3 scripts/link_core_skills.py --check
```

脚本在当前用户的 `~/.agents/skills/` 注册三个链接。遇到已有副本或不同目标时停止，不覆盖；先比较、备份并处理冲突后再运行。移动项目后也需要修正旧链接。若技能列表未刷新，重新打开 Codex。

另一台电脑先克隆本仓库并执行上述命令；后续拉取更新即可。GitHub 不会自动给其他电脑或云端任务安装技能、连接账号或同步凭据。云端任务须取得本仓库，并按该环境支持的方式注册；本机链接不能跨设备使用。

在其他项目调用时，复用这里的研究方法和写作规范；研究输出与原始数据保存到当前任务的工作空间，不把其他项目的数据自动写回本仓库。

## 数据与资料

- 股票基础信息、行情与财务优先使用已配置的 Tushare MCP。
- 消息来源包括 Tushare 长篇新闻、Web 和知识星球观察者03；IMA 按指定知识库使用。
- IBKR 可补充证券检索、行情与公司关系资料。
- 接口覆盖和权限以 [实测记录](研究规则/数据渠道实测记录.md) 为准；其他电脑需自行配置相应连接，不能把本机测试视为所有账号均可用。
- 外部书籍、研报和 agent 成果按 [外部资料规则](研究规则/外部资料接收与研读.md) 处理。

## 版本管理范围

GitHub 保存技能、研究规则、研究输出、说明和可复用代码。`研究输出/` 会随推送上传，并作为 GitHub Pages 研究站的内容源；`research_data/`、下载的第三方资料、凭据、个人持仓和个人配置仍默认只留本地。推送前需确认研究报告不含凭据、未授权的第三方原文或不应公开的个人信息。

## 研究阅读站

本仓库使用 MkDocs Material 和 GitHub Actions 把 `研究输出/` 自动生成 GitHub Pages。首次启用时，在 GitHub 仓库的 **Settings → Pages → Build and deployment** 中将 **Source** 设为 **GitHub Actions**；之后每次向 `main` 推送报告或站点配置都会自动更新。

本地预览：

```sh
python3 -m pip install -r requirements-pages.txt
python3 scripts/prepare_pages.py
mkdocs serve
```

站点构建中间目录 `.site-src/` 和输出目录 `site-output/` 不进入 Git。

旧技能备份也位于本机仓库之外，不重新启用。需要分享某份研究成果时，单独检查并明确选择该文件。

## 开始研究

可以直接提出“扫描最近一周值得研究的变化”“分析某行业”“阅读某公司财报”“判断某公司当前价格是否值得购买”或“拆解这份研报的研究方法”。报告使用正常研报式中文，说明依据、条件、风险与下一验证。
