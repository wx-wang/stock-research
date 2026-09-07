---
name: investment-thesis-monitor
description: Monitor an existing Investment Agent thesis against new facts, original assumptions, falsification conditions, verification metrics, catalysts, earnings expectations, valuation, and trend. Use when the user asks to update a prior memo, review a holding after news or results, or decide whether a thesis is strengthened, unchanged, weakened, or invalidated. Requires a baseline thesis and does not create a new thesis from scratch.
---

# Investment Thesis Monitor v2.0

Compare actual developments with the original path, locate the earliest affected research skill, and trigger focused reanalysis without moving the original goalposts.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before classifying thesis status or rerouting. Preserve every upstream Recheck/Reject/Unknown and never upgrade it without new evidence. (INV-02/24/30)

Read [references/data-requirements.md](references/data-requirements.md). A baseline Investment Memo or equivalent original thesis record is mandatory. Without one, return Recheck and route the request to a new research workflow.

When the update trigger is a quarterly, interim, or annual filing, use [Financial Statement Analyzer](../investment-financial-statement-analysis/SKILL.md) to produce a dated delta packet against the original reporting metrics and identified expectation baseline. The packet supplies new facts; this Skill still owns thesis-status classification and rerun routing.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Investment Thesis Monitor row. Query Tushare only for the baseline's delta window and verification metrics; use Knowledge Star, IMA, report-cli, and Web Search only for targeted changes and catalyst confirmation.

## Investment Question

> How do new facts change the original thesis, which research link is affected first, and does the recommended investment state need to change?

## Required Reasoning

Follow:

> New Fact → Change versus Original Expectation → Business Impact → Earnings Impact → Pricing and State Impact

1. Preserve the original memo, assumptions, falsification conditions, metrics, catalysts, timing, confidence, and state.
2. Preserve the original Core Opportunity Fit fields: era/reality change, prosperity evidence and baseline, profit-pool node, company Alpha, the dated Expectation Position Record and its pre-event baselines, expectation-side recognition, behavioral recognition, pricing completeness, Why Now, opportunity ranking, and first blocked link.
3. Record new facts without first labeling them bullish or bearish. For a new filing, normalize cumulative, derived single-quarter, TTM, restated, currency, unit, and consolidation-scope definitions through the Financial Statement Evidence Packet before comparing with the thesis.
4. Compare what was expected by this date with what actually occurred. Never replace the original expectation baseline with the post-event narrative or revised consensus.
5. Distinguish normal volatility, timing delay, thesis weakening, and thesis invalidation.
6. Identify the first affected link: market/opportunity, industry/profit pool, company alpha, earnings/valuation, or timing/portfolio.
7. When the baseline contains an industry thesis, tag the change to Q1-Q6, update only the affected six-question record, and test its material cross-question constraints before choosing the earliest rerun.
8. Assess business, earnings, expectation revision, valuation, liquidity, catalyst, and trend implications. Update the descriptive expectation phase only when new evidence supports the change, and allow different horizons to remain in different phases.
9. Assign Strengthened, Unchanged, Weakened, or Invalidated.
10. Trigger the earliest affected skill and every affected downstream skill; do not rewrite the whole story inside monitoring.
11. Update the research-level state and Core Opportunity Fit only after required downstream reanalysis.

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return:

- Thesis Status: Strengthened / Unchanged / Weakened / Invalidated;
- Core Opportunity Fit Delta: old field, new evidence, new field status, first changed/blocked link;
- New Facts;
- Expected vs Actual;
- Expectation Position Delta: original phase and baseline, new fact, revision path, behavioral response, new descriptive phase, and next surprise test;
- Revision Peak / Reversal Watch;
- Financial Statement Delta Carryover when applicable: report period, comparison basis, operating deltas, earnings-quality findings, accounting caveats, and Unknowns;
- Changed Assumptions;
- Six-Question Delta: affected Q, old view, new evidence, new view, constraint effects, and next check;
- Triggered Falsification Conditions;
- Earliest Affected Skill;
- Affected Downstream Chain;
- Updated Business Impact;
- Updated Earnings Implication;
- Updated Pricing Implication;
- Provisional State Implication;
- Next Review Trigger;
- Human Decision Required.

## Gates

- **Pass:** thesis status is Strengthened or Unchanged, new facts fit the causal chain, and no key falsifier is hit.
- **Recheck:** thesis status is Weakened or unresolved, new facts conflict with prior assumptions, a catalyst is delayed, or affected skills must be rerun before a state conclusion.
- **Reject:** thesis status is Invalidated because a core assumption or causal link is falsified. Trigger timing/portfolio reanalysis for a Reduce or Sell recommendation; do not execute it.

## Handoff and Rerun Map

- Market liquidity, risk preference, or opportunity signal change → `investment-market-opportunity-scanner` and downstream as material.
- Demand, supply, lifecycle, policy, value-chain, profit-pool, or competitive-structure change → `investment-industry-value-chain` and all downstream skills.
- Q1-Q5 change that can affect industry value, profit-pool location, or durability → `investment-industry-value-chain` and downstream as material.
- Pure Q6 market-narrative, valuation-regime, or priced-in-expectation change with Q1-Q5 intact → `investment-earnings-valuation`, then `investment-timing-portfolio`; rerun Industry Value Chain first if the narrative change reflects new industry facts.
- Product, customer, share, cost, advantage, or execution change → `investment-company-alpha` and all downstream skills.
- Financial results, guidance, consensus, price, valuation, or liquidity change → `investment-earnings-valuation`, then `investment-timing-portfolio`.
- A new financial filing → Financial Statement Analyzer supplies the delta packet; then route the earliest affected decision link, normally Company Alpha or Earnings & Valuation, and all affected downstream skills.
- Price/volume confirmation or action-condition change with fundamentals intact → `investment-timing-portfolio` only.

After reruns, the workflow assembles an Updated Investment Memo. The updated memo becomes the next baseline without deleting the original comparison point.

The update must keep expectation position, market recognition, revision momentum, and pricing completeness separate. A stronger chart does not prove improved earnings or underpricing; a cheaper multiple after a decline does not prove better risk reward without updated implied expectations. Broad diffusion does not prove distribution or informed selling.

## Boundaries

- Do not move original assumptions or validation dates to preserve a thesis.
- Do not rewrite a pre-event expectation after seeing the result or label an event above expectations without the preserved baseline.
- Do not treat price decline alone as evidence that value improved.
- Do not record only supporting developments.
- Do not output Strengthened without identifying the strengthened assumption and new evidence.
- Do not execute Reduce or Sell.

## Thesis Evolution Log

When assembling the updated memo or evolution log, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

Every update must append a `Thesis Evolution Log` row with: date, original thesis/assumption, expected metric, actual result, interpretation, state change (Strengthened/Unchanged/Weakened/Invalidated), and rerun trigger. Preserve the original baseline and definitions; never move a target date or assumption merely to preserve the thesis.

Use the evidence taxonomy to distinguish new Fact, Change versus baseline, Inference, Assumption, Hypothesis, Decision, and Unknown. Attribute the error to the earliest affected link (market regime, industry/profit pool, company alpha, earnings/variant, valuation, trend, or portfolio context), then trigger only the necessary Skill chain. The updated memo must show the old view, new view, evidence delta, and next verification rather than rewriting history.

## Six-Question Industry Delta

When the baseline includes an industry Six-Question Monitoring Baseline, preserve the original Q1-Q6 definitions and update only material deltas. A change in one question must be propagated through the recorded Cross-Question Constraint Map before assigning thesis status. Do not redraw the entire industry narrative when only one monitored variable changed.

## Expectation Position Delta

Read the `Expectation Position Record` section in [Presentation Contract](../investment-agent/references/presentation-contract.md). Append changes chronologically: pre-event expectation → actual result → estimate/narrative revision → price/volume response → pricing-completeness update → next surprise test. The phase labels remain descriptive and do not change the existing monitoring gate or thesis-status definitions.

When the new fact is a narrative-change event (policy shift, technology-route change, competitive-lead change, or macro-narrative turn), answer the narrative-inflection five questions before assigning the new descriptive phase: ① what was the old narrative and its implied ceiling; ② why it is wrong or weakening; ③ what the new narrative is; ④ what triggered the change; ⑤ what would mark the new narrative as fully formed (typically the end of relative excess return versus the broad index). The answers feed the delta record and do not change the thesis-status definitions.
