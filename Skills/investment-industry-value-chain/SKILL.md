---
name: investment-industry-value-chain
description: Test an industry thesis, lifecycle, supply-demand structure, value chain, competitive dynamics, and profit-pool migration under the user's personal Investment Decision Framework. Use for a candidate industry, a named company's industry position, or an industry-opportunity scan that has already produced a concrete change hypothesis. Do not use for company-specific competitive advantage, final valuation, or timing decisions.
---

# Investment Industry Value Chain v2.0

Determine whether an industry creates value and, separately, where that value is captured.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before assigning Granularity, Industry Thesis, or Profit Pool decisions. (INV-08/11/12/13/20)

Read [references/data-requirements.md](references/data-requirements.md). Preserve the distinction between missing data and a negative conclusion.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Industry Value Chain Analyzer row. Retrieve structured peer/industry facts first; treat Knowledge Star, IMA, report-cli, and Web Search as dated evidence to be extracted and evaluated.

Read [the shared six-question industry contract](../investment-agent/references/industry-six-question-framework.md). Use its scope card, six-question coverage record, dynamic deep-dive order, industry-map schema, cross-question constraint loop, and industry/company boundaries.

## Granularity and Profit-Pool Precheck

Use the Scanner's Industry Scope Card, Six-Question Rough Cut, candidate granularity, deep-dive order, and `Investment Opportunity Hypothesis` as starting points, not confirmed conclusions. Rebuild missing or stale scope fields. If the input is a broad or heterogeneous industry, explicitly split it into no more than 3—5 subsegments with distinct demand, technology, supply, economics, or profit pools before making an industry-level decision. A weak aggregate industry index is not sufficient to reject every subsegment.

## Investment Question

> Over the next three to five years, is there a durable industry value change, is prosperity now accelerating versus a named baseline, and which value-chain segment captures the resulting profit?

Keep two sub-decisions visible:

1. Industry Thesis Decision.
2. Profit Pool Decision.

## Required Reasoning

Follow:

> Fact → Change → Industry Commercial Impact → Segment Earnings Impact → Pricing Impact

1. Confirm the Industry Scope Card and the unit, time, geography, and definition of every decision-critical comparison.
2. Scan all six questions, identify the dominant driver, and choose a justified deep-dive order; do not mechanically force Q1→Q6.
3. Complete Q1: size, growth, lifecycle, development phase, and applicable inventory/capacity/price cycle; distinguish structural value creation from temporary disturbance.
4. Identify the decision-critical prosperity indicators, named baselines, current direction, and whether acceleration is broad, narrow, early, mature, or still unverified.
5. Complete Q2: build the Industry Map with main-chain, lateral-support, platform, and critical-technology nodes as material; locate current profit and expected migration.
6. Complete Q3: test segment business models, competitive forces, profit-retention mechanisms, supply response, and fit-for-purpose return evidence; output winner characteristics without pre-judging Company Alpha.
7. Complete Q4: test current and next technology S-curves, commercialization milestones, displacement risk, and impact on the map and moat durability.
8. Complete Q5: test regulation, geopolitics, cross-market differences, and localization by subsegment, including whether substitution remains profitable and durable.
9. Complete Q6: select an industry valuation adapter, identify the market narrative and evidence level, translate the narrative into numeric assumptions, run 3P and scenarios when material, and stop short of company fair value.
10. Run the Cross-Question Constraint Loop and revise any conclusion that conflicts with another material question.
11. Explain why the change is occurring now, its plausible duration, beneficiary/disadvantaged segments, and the observable path to segment earnings.
12. Compare industry reality with current market narrative and identify validation timing.

13. For each candidate subsegment, test the full chain:

> Industry Change → Value Migration → Profit-Pool Location → Pricing Power → Segment Earnings → Market Pricing

14. Do not mark Industry Thesis Pass as a final opportunity conclusion until the relevant profit-pool precheck identifies a plausible value-capture segment, critical six-question coverage is sufficient, and the evidence level is stated.

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return:

- Industry Scope Card;
- Dominant Driver and Deep-Dive Order;
- Six-Question Industry Card;
- Cross-Question Constraint Map;
- Industry Thesis;
- Era / Reality Driver and Observable-Variable Bridge;
- Prosperity Indicators, Named Baselines, and Acceleration Assessment;
- Industry Thesis Decision: Pass / Recheck / Reject;
- Demand Drivers;
- Supply Constraints;
- Nested Cycle Position: Lifecycle / Development Phase / Shorter Cycle;
- Value Creation Mechanism;
- Growth Duration;
- Industry Map with node types, relationships, representative participants, and profit concentration;
- Current Profit Pool;
- Profit Migration Direction;
- Profit Pool Decision: Pass / Recheck / Reject;
- Pricing Power Holder;
- Beneficiary Segments;
- Disadvantaged Segments;
- Winner Characteristics;
- Candidate Companies when the task is industry discovery;
- Profit Migration Timing;
- Technology S-Curve and Disruption Risk;
- Regulation / Geopolitics / Localization;
- Segment Business Models and Return Evidence;
- Industry Valuation Adapter;
- Current Market Narrative and Evidence Level;
- Narrative-to-Numbers Bridge and 3P Test;
- Preliminary Priced-In Industry Assumptions;
- Six-Question Monitoring Baseline;

For broad or opportunity-discovery inputs, also return:

- Candidate Granularity;
- Subsegments Considered and Rejected/Deferred;
- Segment-Level Industry Thesis;
- Segment-Level Profit-Pool Hypothesis;
- Profit-Pool Evidence Table;
- Market View vs Agent View for the selected segment;
- Evidence Level and Coverage Unknowns;
- Six-Question Status, Critical Unknowns, and Next Checks;
- Recheck Reason when the sector is not yet sufficiently decomposed.

## Gates

### Industry Thesis

- **Pass:** a verifiable demand, supply, or structural change creates commercial value with a plausible duration and current catalyst.
- **Recheck:** direction may be valid, but demand authenticity, supply elasticity, lifecycle, or duration is unresolved.
- **Reject:** no material industry change exists, no commercial value is created, or a core industry assumption is falsified.

### Profit Pool

- **Pass:** value capture, pricing power, and earnings impact can be located in a specific segment and are not immediately competed away.
- **Recheck:** industry growth is valid but profit ownership or competitive response is unclear.
- **Reject:** value does not reach the target segment, pricing power is absent, or the apparent profit improvement is not sustainable.

### Granularity

- **Pass:** the research object is a coherent segment, or a specific subsegment has an independent value and profit-pool path;
- **Recheck—Subsegment:** the input is too broad or multiple profit pools remain mixed;
- **Reject—Current Scope:** after reasonable decomposition, no subsegment has a verifiable value-creation or profit-capture path.

The overall decision Passes only when the relevant Granularity, Industry Thesis, and Profit Pool sub-decisions Pass. An industry-thesis Reject ends the original industry logic. An industry Pass with a profit-pool Reject rejects the segment or named-company position and may be rerouted to another segment. A `Reject—Current Scope` does not imply that every subsegment or future catalyst is invalid.

A critical Q1-Q5 `Recheck` that could reverse value creation, profit-pool location, or durability prevents an overall Pass. A Q6 `Recheck` prevents a strong variant/pricing conclusion when market expectations are unidentified, but does not automatically falsify a supported long-term industry thesis. `Not Material` requires a scope-specific reason. The six-question statuses do not create new gates.

## Handoff

Send the validated industry thesis, era/reality driver, prosperity indicators and named baselines, exact Industry Map node, profit-pool location and mechanism, beneficiary segment, segment-level Q3 advantage hypothesis, winner characteristics, expected competitive response, candidate companies, earnings drivers, relevant Q4/Q5 risks, industry valuation adapter, market narrative, catalysts, falsifiers, metrics, Six-Question Monitoring Baseline, and unresolved questions to `investment-company-alpha`.

## Boundaries

- Do not equate industry growth with company profit.
- Do not equate theme heat or recent outperformance with industry prosperity; prosperity must be tied to dated operating or supply-demand evidence versus a named baseline.
- Do not select a company before locating the profit pool.
- Do not use a large total addressable market as proof of value capture.
- Do not hide a failed profit-pool judgment inside a positive industry conclusion.
- Do not treat a broad sector label, recent price movement, or report-count concentration as a completed Industry Thesis or Profit Pool judgment.
- Do not treat Q3 winner characteristics as proof that a named company has Alpha.
- Do not turn Q6 into a named-company fair value, upside/downside, or portfolio state.
- Do not hard-code illustrative penetration, ROIC, valuation, or timing thresholds as universal rules.

## Cycle, Narrative and Beneficiary Set

When assembling an industry report or handoff, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

Required additions:

- `Industry Cycle Position`: Technology Breakthrough, Capital Investment, Commercial Validation, Profit Release, or Mature Competition; include distance to profit release and the facts that could falsify the phase.
- Demand growth versus effective supply, bottleneck, pricing power, profit elasticity, and the mechanism by which the profit pool migrates.
- `Current Market Narrative`, `Potential Narrative Shift`, `Narrative Gap`, `Required Evidence`, and the risk that the redefinition will not occur.
- A beneficiary set with comparable fields so downstream candidates can be compared on one industry thesis and profit-pool definition.

Keep each conclusion traceable as Fact/Change/Inference/Assumption/Hypothesis/Decision/Unknown. Do not use an industry-level narrative as proof that any one company captures the pool.

## Segment Economics and Opportunity Handoff

Before selecting companies, the skill must show where the opportunity sits in the value chain and whether that location is structural, temporary, or still Unknown. The handoff to Company Alpha must identify the exact segment, profit-pool mechanism, winner characteristics, competitive response, evidence level, and the first verification event. A broad “industry is attractive” statement is not a valid handoff.

## Six-Question Deep Read

The full industry read must use the shared six-question contract. Keep the investor-mandated 12-step workflow and existing Granularity / Industry Thesis / Profit Pool gates. The Six-Question Industry Card is a coverage and uncertainty record, not a scoring system. The final conclusion must show how Q1-Q6 constrain one another rather than presenting six independent summaries.
