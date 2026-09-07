---
name: investment-company-alpha
description: Determine whether a specific A-share or Hong Kong company can capture a validated industry profit pool through its business model, competitive advantage, and growth engine. Use after an industry thesis and profit-pool position exist, or for a focused company-alpha question with equivalent upstream context. Do not use to infer industry attractiveness, forecast final earnings, or recommend a trade.
---

# Investment Company Alpha v2.0

Test why value flows to this company rather than merely to its industry or competitors.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before assigning the Company Alpha decision. Industry Beta and company-attributable Alpha remain separate. (INV-04/11/16/20)

Read [references/data-requirements.md](references/data-requirements.md). If the industry thesis or profit-pool position is absent or stale, return Recheck instead of reconstructing them silently. Consume the exact Industry Map node, profit-pool mechanism, segment-level Q3 advantage hypothesis, Winner Characteristics, and relevant six-question Unknowns from upstream when available.

Reuse a dated `Financial Statement Evidence Packet` from [Financial Statement Analyzer](../investment-financial-statement-analysis/SKILL.md) when it contains segment economics or peer-comparable operating evidence. Treat it as evidence input only; do not inherit a financial-health conclusion as Company Alpha.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Company Alpha Analyzer row. Retrieve Tushare company and peer facts first; use Knowledge Star, IMA, report-cli, and Web Search to verify qualitative competitive claims.

## Investment Question

> Why will the validated industry profit flow to this company rather than to competitors?

## Required Reasoning

Follow:

> Company Facts → Competitive Change → Business Value Capture → Earnings and Cash-Flow Impact → Downstream Expectation Questions

1. Confirm the company's products, customers, revenue sources, business model, value-chain position, and any relevant Financial Statement Evidence Packet definitions.
2. Confirm that the company occupies a beneficiary profit-pool segment.
3. Treat upstream Q3 as a segment-level hypothesis only; test whether this company actually possesses the required technology, cost, customer, scale, brand, data, regulatory, or ecosystem mechanism with comparative operating evidence.
4. Compare the company with relevant competitors; separate company alpha from industry beta.
5. Determine whether advantages are durable or merely cyclical and temporary.
6. Decompose revenue growth into market expansion, share, volume, price, and product mix.
7. Decompose profit growth into revenue and margin effects and check cash-flow direction.
8. When the proposed thesis is “good business, currently weak earnings,” separate supported business quality from the current earnings weakness: identify whether the cause is cyclical, execution-related, accounting-timing-related, or structural; test whether the Alpha mechanism remains intact; and pass the required runway and leading-indicator questions downstream. Do not decide underpricing here.
9. Identify company-specific catalysts, verification metrics, and falsification conditions.
10. Form the exact downstream question about whether the market underestimates value capture or overestimates durability, but do not conclude market recognition, underpricing, valuation, or timing inside this Skill.

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return:

- Company Positioning;
- Core Beneficiary Test: exact profit-pool node, value-capture mechanism, and evidence that the company actually occupies it;
- Industry-to-Company Boundary Check;
- Business Model;
- Company Alpha;
- Competitive Advantage by source;
- Advantage Durability;
- Alpha Durability;
- Growth Engine;
- Revenue Growth Bridge;
- Profit Growth Bridge;
- Cash-Flow Direction;
- Relative Competitive Position;
- Named-Peer Alpha Evidence and unresolved comparison gaps;
- Company-Specific Risks;
- Earnings Drivers for the next skill;
- Temporarily Depressed Earnings — Business Quality Carryover when applicable: supported quality evidence, cause of weakness, Alpha intact/broken/Unknown, leading indicators, runway questions, and structural-risk falsifier;
- Downstream Recognition and Pricing Questions that remain untested.

`Alpha Durability` must answer:

- what creates the advantage;
- how long the mechanism may persist under the current industry cycle;
- why competitors cannot easily replicate it;
- how a competitor could erode it;
- which operating metrics verify persistence or erosion;
- whether the advantage is structural, cyclical, temporary, or still Unknown.

Do not convert this field into a numerical moat score. Use comparative evidence and qualitative durability judgment. A current advantage is not automatically a durable advantage.

## Gates

- **Pass:** the company is in a beneficiary profit pool, at least one advantage is supported by operating evidence, and value capture has a plausible revenue, profit, and cash-flow path.
- **Recheck:** the company may benefit, but alpha cannot be separated from industry beta, durability is unverified, or decision-critical customer, product, share, or cost data is missing.
- **Reject:** the company cannot capture the profit pool, claimed advantages lack evidence, improvement comes mainly from unsustainable factors, or competitive position is deteriorating through a falsification threshold.

A Reject applies to the company. Preserve the validated industry thesis and return to the beneficiary-segment candidate set when appropriate.

## Handoff

Send the exact profit-pool node, business model, alpha mechanism, named-peer competitive evidence, durability assumptions, volume/price/share/mix/margin drivers, cash-flow implications, the conditional temporarily-depressed-earnings carryover, company catalysts, risks, falsifiers, metrics, downstream recognition/pricing questions, and missing inputs to `investment-earnings-valuation`.

## Boundaries

- Do not list generic company strengths without comparing them with competitors.
- Do not call industry beta a company moat.
- Do not inherit a segment-level Q3 moat mechanism as Company Alpha without company-versus-competitor evidence.
- Do not treat revenue growth as value creation without checking margins and cash flow.
- Do not treat a standalone financial-report conclusion or superior ratio as Alpha without the named-peer causal comparison required by this Skill.
- Do not infer “market recognized”, “not priced”, “undervalued”, or a final investment state from drawdown, valuation multiples, broker targets, attention, or Company Alpha evidence. Those conclusions belong downstream.
- Do not make a valuation or portfolio recommendation.

## Competitive Map and Attributable Alpha

When assembling a stage memo or competitive map, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

Add a `Competitive Map` containing: target company, key competitors, profit-pool segment, advantage source, dated evidence, likely competitor response, structural versus temporary advantage, why the advantage is difficult to replicate, and a qualitative profit-capture assessment with unresolved evidence. State explicitly which benefits are industry Beta and which are attributable Company Alpha. Do not assign a numerical probability or moat score.

The reasoning must show: company fact → competitive change → business value capture → earnings/FCF impact → downstream expectation question. Include a driver tree for volume, price, share, mix, cost, margin, reinvestment and cash conversion. “Full-stack”, “ecosystem”, or “leading position” is not an alpha conclusion without comparative evidence.

Use the shared evidence taxonomy and label unverified competitor claims `Unknown` or `Recheck`. The handoff must preserve the comparison set and the exact evidence still needed to prove “why this company rather than its alternatives.”

## Alpha Durability and Investor-Facing Narrative

Add a short Chinese `公司价值获取叙事` to the output:

```text
产业利润池变化 → 公司占据的环节 → 竞争优势机制 → 优势持续性 → 收入/利润/现金流影响 → 下游需验证的市场预期与定价问题
```

Label each link as Fact, Change, Inference, Assumption, Hypothesis, or Unknown in the internal record; render the final memo in Chinese. Include the most likely failure path for the alpha: the first stage that could fail, leading indicator, impact, and required response. This is `Investment Mistake Analysis`, not a new Skill.
