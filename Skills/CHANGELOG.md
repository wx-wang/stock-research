# Investment Skills Changelog

本文件只供人工维护与审计，不是运行时必读参考。

- 2026-09-01：合并投资 Skill v2.0。项目 `Skills/` 成为唯一正本；新增 `evidence-and-gates.md` 与 `presentation-contract.md`；解散旧编排、研究和呈现补丁文件；8个投资 Skill 改为渐进读取共享契约；投资理念、阶段、闸门和字段语义不变。
- 2026-09-01（v2.1）：《穿透叙事》估值方法吸收（投资者批准；决策记录见 `研究输出/方法论/20260901_穿透叙事估值尺子与c修正.md`）。① earnings-valuation 增加隐含天花板标准反算（表 1-3 口径、r∈{8,10,12}% 情景、重资产/持续融资定性护栏、敏感性声明），data-requirements 补动态 PE 口径与股本变动；② presentation-contract 预期位置记录"定价充分度"字段纳入隐含 m；③ timing-portfolio 增加 A 股拍卖机制解读注记（港股不适用）；④ thesis-monitor 预期位置增量并入叙事拐点五问。不含 c 参数化（投资者决策降级为待验证假设）。闸门语义、阶段结构无变化。
- 2026-09-07：Investment OS Handoff 增量审查。修正 `Skills/README.md` 的默认路由漂移；行业研究显式采用“驱动力→领先信号→景气/结构变化→盈利传导”；叙事估值新增龙头/高弹性角色辨析与“滞涨不等于补涨”护栏；Reverse DCF 增加回归测试与零现金转化输入保护；既有共识/断层筛选脚本明确标为 Candidate / Sandbox。仓位、三类退出和行为风控仍为候选执行层，不进入当前默认研究链路。
- 2026-09-07（Handoff 对齐补充）：将上述研究要求提升到根目录 `AGENTS.md` 与两个主 Skill；明确完整个股研究必须回答市场基线、独立判断、差异依据、公司角色、价格隐含状态和下一验证。按投资者指示，仓位、组合、加减仓和价格止损继续留在当前范围外。
- 2026-09-07（关注池）：新增 `研究输出/关注池/Investment_OS_关注池.md`，作为投资者明确指定行业与股票的总索引；采用“总表 + 独立日期版本研究档案”，更新只比较增量事实，不覆盖历史判断，不自动扩充或输出交易动作。
- 2026-09-08（主张级证据体系）：不改变三个核心 Skill 职责，增量加入 `Source → Atomic Claim → Claim Class → Evidence Role`；统一 Fact、Inference/Hypothesis、Market Narrative/Expectation、Valuation View/Model Output；采用主张级高/中/低 Evidence Confidence；记录 Original Source、Immediate Source、Lineage ID、独立原始证据数和同源转载数；明确数据库复刻财报不构成第二证据，并在代表公司外推行业时强制竞争检验行业 Beta、公司 Alpha、细分结构与口径/基数因素。
- 2026-09-08（行业报告可读性修正）：证据分类、置信度和来源血缘继续作为内部研究纪律，但普通 `industry-understanding` 成品不再展示Claim/Lineage账本或逐条置信度表；正文恢复为产业研究叙事，末尾按官方数据、公司披露、券商研报和知识星球/IMA集中列明来源。仅在投资者明确要求证据审计时附完整账本。
- 2026-09-08（三个核心 Skill 输出分层）：将 Fact/Hypothesis/Narrative、Evidence Confidence、Source Lineage、支持/反证与独立性判断统一定义为 Internal Research Layer；行业、财报和叙事估值的默认主报告只展示核心判断、3—5个关键证据或变化、预期差、最大不确定性和下一验证。完整证据账本改存 `research_data/` 或按需生成独立 Research Notes / Evidence Appendix / Audit Log，不再自动进入正文。
- 2026-09-08（Narrative Gap Candidate 接口）：industry-understanding 新增“叙事差异候选（待估值层确认）”，作为 industry-understanding 与 narrative-valuation 的移交接口：当产业事实足以挑战某项现有经营假设、但尚缺明确市场预期基线与价格隐含分析时标记为候选并写明缺失证据。落点四处：`SKILL.md` 流程第 5 条与 Industry Terminal Packet 新增承接字段；`state-change-and-narrative.md` 的 Narrative Change Card 增加候选列并新增候选小节；`output-template.md` 第 6 节表格增加“叙事差异候选”列；`methodology.md` 补一句定义。行业层不得将候选升级为正式预期差，也不得判断股票是否充分定价；股价未涨、关注较少或估值较低不构成候选。（来源：投资者转交 Codex 审查建议；实施：GLM，同步更新项目正本与 `~/.agents` 运行时副本）
