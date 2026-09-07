---
name: investment-earnings-valuation
description: Build an independent earnings view, compare it with market expectations, and assess valuation, implied expectations, liquidity, upside, downside, and risk reward under the user's personal Investment Decision Framework. Use after valid industry, profit-pool, and company-alpha conclusions, or for a focused earnings or valuation question with equivalent upstream context. Do not use for price-only cheapness claims or final timing and position decisions.
---

# Investment Earnings Valuation v2.0

Decide whether a supported earnings variant exists and, separately, whether the current price still offers sufficient odds.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before assigning Earnings/Variant or Valuation/Liquidity decisions. Market recognition and pricing completeness remain separate, and valuation Reject applies to the current price rather than Company Alpha. (INV-01/02/10/18/20)

Read [references/data-requirements.md](references/data-requirements.md). If consensus, price, financial, or upstream causal data needed for the requested conclusion is missing, return Recheck. Do not label one analyst opinion as consensus or infer precise implied expectations from incomplete inputs. Use the upstream Q6 Industry Valuation Adapter, market narrative, narrative-to-numbers bridge, and preliminary priced-in industry assumptions as context, not as a company valuation conclusion.

Use a dated `Financial Statement Evidence Packet` from [Financial Statement Analyzer](../investment-financial-statement-analysis/SKILL.md) when a recent filing is material. If the user provides only a raw quarterly, interim, or annual report and no equivalent normalized packet exists, run that supporting analysis first. Do not silently duplicate it or promote its accounting observations into an earnings-variant decision.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Earnings & Valuation Analyzer row. Build the independent earnings baseline from Tushare, use report_rc/research_report and report-cli for forecast evidence, and use Knowledge Star, IMA, and Web Search to test market narrative and current disclosures.

## Investment Question

> Does the market underestimate future earnings, where is that expectation in its formation and revision path, and does the current price still under-reflect the change with sufficient risk reward and liquidity?

Keep two sub-decisions visible:

1. Earnings & Variant Decision.
2. Valuation & Liquidity Decision.

## Required Reasoning

Follow:

> Operating Facts → Driver Changes → Business Impact → Earnings and Cash-Flow Scenarios → Pricing and Risk-Reward Impact

1. Confirm the Financial Statement Evidence Packet or equivalent normalized history, operating drivers, earnings-quality reconciliation, company guidance, consensus timing, market narrative, current price, valuation, liquidity, and whether the upstream industry valuation adapter remains appropriate for this company's actual business mix.
2. Translate industry and company-alpha changes into demand, volume, price, share, product mix, costs, and margins.
3. Build the bridge: demand → volume → price → revenue → margin → profit → cash flow.
4. Produce Bull, Base, and Bear earnings scenarios with explicit assumptions.
5. Distinguish analyst consensus, market narrative, and price-implied expectations.
6. Establish the dated `Expectation Position Record` for each material horizon: market baseline, Agent variant, descriptive phase, pre-event expectation, revision path, next surprise test, and falsifier. Phase labels are descriptive only and may differ by horizon.
7. Assess expectation-side market recognition: whether forecasts, narrative, coverage, or ownership expectations are changing, with source/date and evidence level. Do not use this as proof of price/volume confirmation.
8. State the exact variant variable, magnitude, timing, why the market may be wrong, and why the independent view may be wrong.
9. For each material catalyst, define before the event what would count as above, in line with, or below expectations. An event occurring or becoming popular is not itself a positive surprise.
10. Map earnings scenarios to Bull, Base, and Bear value ranges without using a high/low multiple as a conclusion by itself.
11. Assess what optimism or pessimism is already priced, upside, downside, risk reward, and liquidity constraints.
12. Identify validation events, the expected revision path, and rerating catalysts.

When the thesis specifically depends on a good business with currently weak reported earnings, run a `Temporarily Depressed Earnings Check`: confirm supported business quality and Alpha, diagnose temporary versus structural causes, test balance-sheet and cash-flow runway, identify improving leading indicators, test whether price still reflects the old earnings path, and set a dated verification window and falsifier. Missing decision-critical evidence makes the conclusion Recheck, not an early-stage opportunity by default.

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return the earnings and variant fields:

- Consensus;
- Financial Statement Evidence Carryover: report period, comparison basis, operating deltas, earnings-quality findings, accounting caveats, and Unknowns;
- Market Narrative;
- Expectation Position Record by horizon and as-of date;
- Pre-Event Expectation and Next Surprise Test;
- Expectation Revision Path: accelerating / stable / peaking / reversing, with evidence;
- Temporarily Depressed Earnings Check when applicable;
- Market Recognition — Expectation/Narrative Evidence;
- Recognition Evidence Level and Missing Behavioral Confirmation;
- Industry Q6 Carryover and Company-Specific Adjustment;
- Priced-In Earnings Expectation;
- Own Earnings View;
- Bull / Base / Bear Earnings Scenarios;
- Earnings and Cash-Flow Bridge;
- Variant Source and Magnitude;
- Why Market May Be Wrong;
- Why Own View May Be Wrong;
- Validation Timeline;
- Earnings & Variant Decision.

Also return the valuation and liquidity fields:

- Current Valuation Status;
- Priced-In Expectations;
- Pricing Completeness: what is reflected, what is not, and confidence;
- Bull / Base / Bear Value Range;
- Upside;
- Downside;
- Risk Reward;
- Liquidity Constraint;
- Re-rating Conditions;
- Valuation & Liquidity Decision;
- Reject Scope: no variant / no current-price odds / insufficient liquidity.

## Gates

### Earnings & Variant

- **Pass:** a material variant is supported by industry, company, and operating evidence, with identifiable variables and validation timing.
- **Recheck:** direction may be right but consensus, magnitude, evidence, or timing is unclear.
- **Reject:** no material variant exists, the independent view is unsupported, the earnings bridge conflicts with operating facts or cash flow, or the variant is falsified.

### Valuation & Liquidity

- **Pass:** current price does not fully reflect the supported earnings view, scenarios have clear conditions, risk reward is sufficient, and liquidity supports reasonable entry and exit.
- **Recheck:** price is near a reasonable range, valuation is excessively sensitive, upside and downside are balanced, or liquidity is uncertain.
- **Reject:** price reflects or exceeds the Bull Case, upside does not compensate downside, liquidity is inadequate, or a core valuation assumption is falsified.

The overall decision Passes only when both sub-decisions Pass. A variant Reject means no current active edge. A variant Pass with a valuation Reject means the company thesis may remain valid but the current price is not attractive.

## Handoff

Send the earnings scenarios, variant, complete dated Expectation Position Record, preserved pre-event baselines, next surprise tests, revision path, expectation-side market-recognition evidence, validation timeline, priced-in expectations, pricing-completeness conclusion, value ranges, upside, downside, risk reward, liquidity constraints, catalysts, falsifiers, and confidence to `investment-timing-portfolio`.

## Boundaries

- Do not equate a low multiple with undervaluation.
- Do not use drawdown, low PE/PB, PEG, broker targets, attention, or a single forecast source as proof that the market has not priced the thesis.
- Do not call expectation-side recognition “market confirmation” without downstream price/volume evidence.
- Do not infer the expectation phase from price alone, treat a publicized event as above expectations without a pre-event baseline, or treat broad diffusion as proof of underpricing.
- Do not label broad diffusion an “出货阶段” without direct ownership, turnover, supply, or selling evidence.
- Do not inherit an industry-level Q6 narrative, multiple, or scenario as the company's fair value or risk/reward conclusion.
- Do not claim variant perception merely because the view differs from consensus.
- Do not ignore cash flow when profits improve.
- Do not recompute a valid dated Financial Statement Evidence Packet without a changed report period, definition, source conflict, or decision need.
- Do not let a standalone financial-report conclusion substitute for Company Alpha, earnings variant, valuation, timing, or portfolio gates.
- Do not recommend Buy, Add, Reduce, or Sell; timing and state belong downstream.

## Expectation Decomposition and Implied Expectations

When assembling a stage memo, implied-expectation analysis, or expectation record, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

Decompose `Market Expectation` and `Agent View` into three horizons: short term (1–2 quarters), medium term (1–2 years), and long term (3–5 years). For each horizon record Variant Source, supporting Evidence, and Invalidation. State whether the reference is consensus, a forecast range, or an implied expectation; never call one broker report “the market view.”

Perform `Implied Expectation Analysis`: reverse the current price or market value into the required revenue, growth duration, margin, cash-flow and/or multiple assumptions, then compare those assumptions with the Agent Base Case. Explain exactly which variable is under- or over-priced and how the difference changes Bull/Base/Bear risk reward.

### Terminal-Ceiling Reverse Calculation（隐含天花板反算）

When a dynamic PE is meaningful for the business model, use this standard tool for `Implied Expectation Analysis`:

1. Reverse the current dynamic PE (state the earnings basis: next-year or current-year) into the implied terminal-profit multiple `m`（隐含天花板：终局利润相对当前利润的倍数，利润增长至 m 后永续平稳）. Compute under r = 8% / 10% / 12% scenarios with r = 10% as the A-share long-run anchor, and report the scenario range — never a single number. r=10% anchors: m 0.3→PE 5.4, 0.5→6.9, 1→10, 2→15.3, 3→20.1, 5→28.8, 10→48.6.
2. Compare the implied m with the terminal-profit multiples implied by the Agent's Bull / Base / Bear earnings scenarios, and state the variant as a multiple gap (e.g., "price implies m≈3; Base Case supports m≈5"). A variant claim that survives a growth-rate comparison but not this ceiling comparison is not a supported variant.
3. Capital-heavy or chronically financing names (steady-state cash flow materially below accounting profit, or share growth eating profit growth): the accounting-basis implied m is a lower bound on market optimism — trigger the 叙事打满（narrative saturation）check earlier, not later; recompute on a per-share basis when dilution is structural. Do not apply any numeric cash-conversion coefficient; the earnings-quality packet and upstream Q3 return evidence carry that judgment.
4. State the sensitivity: whether r±2% or one m tier flips the Bull/Bear conclusion. If the sensitivity statement cannot be made, return Recheck with the missing variable.

This ruler constrains what must be believed to hold the current price; it is not a fair-value calculator, and a low multiple alone still cannot prove underpricing.

Keep facts, changes, inferences and assumptions separate in the evidence table. If the reverse valuation is too sensitive or inputs are incomplete, return Recheck with the missing variable rather than false precision. Preserve liquidity constraints and the evidence needed for the next earnings validation.

## Expectation Position and Surprise Discipline

Read the `Expectation Position Record` section in [Presentation Contract](../investment-agent/references/presentation-contract.md). Preserve the expectation baseline as it existed before each event, then append the actual result and revision response; never rewrite the baseline after seeing the outcome. A positive business result can be below expectations, and a weak reported result can be above expectations, so the decision variable is the variance versus the dated baseline and the resulting earnings/cash-flow revision.

The descriptive phases are `旧预期消化 / 新预期形成 / 事件或业绩验证与预期修正 / 广泛扩散与充分定价检查`. They are non-exclusive across horizons and do not change the existing Earnings & Variant or Valuation & Liquidity gates.
