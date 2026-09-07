---
name: investment-timing-portfolio
description: Assess whether price and volume confirm a completed fundamental thesis, then translate thesis strength, confidence, risk reward, market regime, trend, and liquidity into a research-level investment state. Use for observe, trial, buy, hold, add, reduce, or sell-condition questions after valid upstream analysis exists. Do not use for price-only trading signals, automatic orders, or fund-level portfolio construction.
---

# Investment Timing Portfolio v2.0

Use trend as market validation and position state as the expression of judgment strength, without replacing fundamentals or the investor's final decision.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before assigning timing or portfolio decisions. A timing Reject applies to the current time unless new fundamental evidence requires upstream rerouting. (INV-05/17/24/25)

Read [references/data-requirements.md](references/data-requirements.md). A direct “can I buy?” request cannot Pass without valid upstream industry, company, earnings, variant, valuation, and liquidity conclusions. If investor risk boundaries are absent, give a state and direction only, not a fabricated percentage.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Timing & Portfolio Manager row. Use Tushare for price/volume and relative-strength evidence; use Knowledge Star, IMA, report-cli, or Web Search only to verify catalyst timing or material events.

## Investment Question

> Is the market beginning to confirm the fundamental thesis, and what research-level investment state is justified now?

Keep two sub-decisions visible:

1. Trend & Timing Decision.
2. Portfolio Decision.

## Required Reasoning

Follow:

> Market Facts → Trend Change → Recognition of Business/Earnings Thesis → Pricing Confirmation → Investment State

1. Confirm all upstream conclusions, confidence, gates, valuation, risk reward, catalysts, liquidity, and the dated `Expectation Position Record`, including preserved pre-event baselines and next surprise tests.
2. Describe long-term annual/quarterly structure, medium-term 60-day trend and relative strength, and short-term volume, breakout, and pullback behavior.
3. Judge whether trend is improving, stable, or deteriorating.
4. Compare price and volume behavior with fundamental catalysts and the earnings validation timeline. Test the response against what the market expected before the event, not merely whether the event looked positive or attracted attention.
5. Append actual results, post-event revisions, and behavioral response to the upstream Expectation Position Record without rewriting the original baseline. State whether revisions are accelerating, stable, peaking, or reversing.
6. Combine upstream expectation/narrative recognition with price/volume behavior, but report the two evidence types separately before forming the overall Market Recognition conclusion.
7. Treat trend as behavioral recognition evidence, not proof of business quality, earnings, Alpha, or underpricing.
8. Investigate persistent price/fundamental conflict as a possible unknown; do not reverse-engineer a fundamental story from price.
9. Define objective Observe, Trial, Entry, Add, Reduce, and Exit conditions. Include, when material, leading-indicator deterioration, actual results missing the preserved expectation, revision peak/reversal, valuation exhaustion, positive surprise without expected recognition, trend failure, and thesis falsification.
10. Combine thesis completeness, confidence, variant magnitude, risk reward, Market Regime, trend confirmation, liquidity, and known position context.
11. Recommend an investment state and direction, then identify what only the investor can decide.

A-share market-structure note（v2.1）：A股做空受限使边际价格由最乐观的持有者决定，价格系统性高于平均预期；"天花板算不清"的标的在流动性脉冲中弹性被放大。解读 A 股标的价格/量能认可证据时以此作背景——流动性时段的强势对"平均预期已确认"的证明力要打折扣，叙事打满检查（INV-01）因此更重要而非更不重要。不适用于港股；不得据此把广泛扩散标注为出货（INV-07）。

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return trend and timing fields:

- Long-Term Trend Status;
- Medium-Term Trend Status;
- Short-Term Confirmation;
- Fundamental–Price Alignment;
- Expectation Position Carryover and Behavioral Update;
- Surprise–Response Test: preserved pre-event baseline, actual result, revisions, and price/volume response;
- Revision Peak / Exhaustion Watch;
- Market Recognition — Upstream Expectation/Narrative Evidence;
- Market Recognition — Behavioral Price/Volume Evidence;
- Overall Market Recognition Status and unresolved conflict;
- Observe Condition;
- Trial Position Condition;
- Entry Condition;
- Add Condition;
- Reduce Condition;
- Exit Condition;
- Trend & Timing Decision.

Also return:

- Catalyst Priority;
- Investment Mistake Analysis.

Also return portfolio fields:

- Recommended State: Observe / Trial Position / Buy / Hold / Add / Reduce / Sell;
- Position Direction;
- Position Rationale;
- Supporting Evidence;
- Main Risks;
- Upgrade Conditions;
- Downgrade Conditions;
- Portfolio Exit Conditions;
- Unresolved Conflicts;
- Human Decision Required;
- Portfolio Decision.

`Catalyst Priority` must rank the top decision-relevant catalysts. For each item include: event, affected variable, preserved pre-event expectation, expected window, importance, evidence confidence, upside outcome if confirmed, downside outcome if missed, revision implication, and next verification date. Do not treat every announcement or product launch as a catalyst unless it can change earnings, valuation, or market recognition.

`Investment Mistake Analysis` must state the most likely way the current timing or portfolio decision could be wrong, whether the error is thesis failure, valuation exhaustion, delayed monetization, or recognition failure, the leading indicator, the impact, and the response. Do not invent precise probabilities.

## Gates

### Trend & Timing

- **Pass:** long- or medium-term structure aligns with fundamentals, catalyst response supports repricing, and action conditions are observable.
- **Recheck:** fundamentals hold but trend is unconfirmed, timeframes conflict, or catalyst response is unclear. The state is normally Observe or Trial Position.
- **Reject:** current timing is contradicted by material trend deterioration, persistent negative reaction to key positive evidence, or a predefined exit condition.

Trend rejection normally rejects current timing, not the fundamental thesis. Route a suspected unknown fundamental problem upstream.

### Portfolio

- **Pass:** the causal chain is intact, current state matches risk reward, regime, trend, and liquidity, and upgrade/downgrade/exit conditions are explicit.
- **Recheck:** a decision-critical upstream skill is unresolved, cross-skill conflicts remain, or position context is insufficient for the requested recommendation.
- **Reject:** a decisive upstream link fails, risk reward no longer supports exposure, or a core falsification condition is hit. Do not add risk; the recommendation may be Observe, Reduce, or Sell.

A high-confidence negative recommendation may Pass because the stage has produced a reliable decision. Stage Decision is not bullishness.

## Handoff

Send the full stage record, updated Expectation Position Record with its original baselines intact, separated expectation-side and behavioral market-recognition evidence, surprise-response tests, revision peak/exhaustion watch, overall recognition status, recommended state, position rationale, conditions, unresolved conflicts, human-decision items, and monitoring triggers to the workflow for memo assembly and to `investment-thesis-monitor` as the baseline.

## Boundaries

- Do not predict the lowest price.
- Do not use a trend signal to bypass a fundamental Recheck or Reject.
- Price decline alone is not an Add condition.
- Trend strength alone is not Company Alpha, underpricing, or proof that the thesis remains incompletely priced.
- Do not infer the expectation phase from the chart alone or call attention diffusion an “出货阶段” without direct ownership, turnover, supply, or selling evidence.
- A positive event with a weak response is not automatically bearish; first test whether it was already expected, whether revisions changed, and whether liquidity or market regime explains the response.
- Do not issue an order or imply that a recommendation has been executed.
- Do not fabricate exact position size without investor constraints.

## Decision Dashboard, Ranking and Sell Logic

When assembling the dashboard, state conditions, or candidate comparison, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

Output a decision-first dashboard containing: current state, one-line thesis, thesis strength, variant, implied-expectation gap, catalyst status, trend status, key risk, next verification date, and the exact condition for state change.

If a candidate comparison set exists, consume the workflow-level `Candidate Comparison Record` and explain why this candidate ranks higher or lower on thesis strength, profit-pool position, alpha, variant, risk reward, timing, liquidity, portfolio fit, and opportunity cost. If no set exists, write `Comparison: Not Assessed`; do not invent a winner.

Add `Portfolio Context`: current exposure, new exposure, Industry Beta, Macro Risk, Liquidity Risk, Valuation Risk, portfolio impact, and position adjustment. Add `Opportunity Cost` as a required question, but mark it `Not Assessed` when alternatives or portfolio data are unavailable.

Classify any negative action as one of: `Thesis Invalidated`, `Valuation Exhaustion`, or `Trend/Recognition Failure`, and provide Evidence and Required Action. A trend failure with intact fundamentals is not the same as a falsified thesis.

## Conditional Ranking and Chinese Presentation

If a Candidate Comparison Record is present, rank the candidate against the supplied alternatives using the existing investment logic: industry trend, profit-pool position, company alpha and durability, variant, earnings visibility, valuation/risk reward, catalyst, trend, liquidity, portfolio fit, and opportunity cost. If no comparable candidate set or data is available, output `Opportunity Ranking: Not Assessed` and do not imply that the subject is the best available investment.

Before the detailed timing and portfolio output, provide a short Chinese `从基本面到投资状态` chain:

```text
基本面事实 → 盈利变化 → 市场定价变化 → 趋势确认 → 研究级投资状态
```

The final investor-facing memo should use Chinese labels for states and evidence types even though the internal handoff keys remain stable English identifiers.

## Expectation Phase, Revision Peak, and Exit Discipline

Read the `Expectation Position Record` section in [Presentation Contract](../investment-agent/references/presentation-contract.md). Timing & Portfolio does not independently assign a new cycle. It validates or updates the descriptive phase from both the preserved expectation baseline and subsequent behavioral evidence. Different horizons may remain in different phases.

Keep `Market Recognition`, `Pricing Completeness`, and `Revision Momentum` separate. Broad recognition can coexist with remaining underpricing, full pricing, or overpricing. A revision peak is a monitoring signal, not an automatic sell; route it through refreshed earnings, implied expectations, trend, and portfolio context before changing state.
