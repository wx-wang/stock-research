---
name: investment-market-opportunity-scanner
description: Assess the A-share or Hong Kong market regime and screen industries or companies for fact-based changes worth deeper research under the user's personal Investment Decision Framework. Use when asked which industries are currently worth researching, where opportunities may be emerging, whether a named candidate deserves deep research, or how the market environment should constrain risk. Do not use to issue a final stock recommendation or for price-only momentum screening.
---

# Investment Market Opportunity Scanner v2.0

Identify research-worthy change while keeping market risk context separate from investment thesis quality.

## Before Analysis

Read [the shared evidence and gate contract](../investment-agent/references/evidence-and-gates.md) before assigning a stage decision. It defines the causal chain, evidence labels, gate meanings, and `Recheck—Subsegment` scope. (INV-11/13/20/21)

Read [references/data-requirements.md](references/data-requirements.md). If decision-critical inputs are unavailable, return Recheck and a concrete Missing Inputs list. Do not assume a provider or invent unavailable values.

Read [the shared data-source routing](../investment-agent/references/data-source-routing.md) and use the Market & Opportunity Scanner row. Retrieve structured Tushare facts first; use 观察者03, the fixed IMA knowledge base, report-cli, and Web Search only for targeted evidence and current-event verification.

For sector discovery or a named-industry scan, read [the shared six-question industry contract](../investment-agent/references/industry-six-question-framework.md). This Skill performs only the scope check, six-question rough cut, and deep-dive routing; it does not complete the full industry read.

## Opportunity Discovery Search Contract

For an industry/opportunity-discovery request, do not use the latest 30 Knowledge Star topics as the only recall source. Use a bounded multi-source search:

1. **Snapshot:** recent `group +topics` topics for immediate attention and catalysts;
2. **Rolling Window:** paginate with `next_end_time` to cover the relevant 7—30 day window for current opportunities, or 30—90 days for structural themes; de-duplicate by `topic_id`;
3. **Keyword Recall:** use `topic +search` with several short entity/topic queries because the endpoint has no pagination; merge and de-duplicate results;
4. **Detail Extraction:** call `topic +detail` only for shortlisted high-relevance topics;
5. **Cross-Validation:** use Tushare and official/company/association sources to validate decision-critical claims.

Report the actual coverage: time window, pages, keywords, unique topics, details retrieved, sources not covered, and unresolved gaps. Treat list/title-only results as `Radar Only`, body/summary evidence as `Narrative Extracted`, and cross-validated claims as `Cross-Validated`.

## Investment Questions

Answer both questions separately:

1. What is the current Market Regime and how should it constrain risk exposure?
2. Which industries or companies show a verifiable era/reality change and accelerating prosperity, with a plausible path to business value, earnings, and under-recognized pricing?

This skill determines what deserves deeper research, not what to buy.

## Required Reasoning

Follow:

> Fact → Change → Business Impact → Possible Earnings Impact → Preliminary Pricing Impact

1. Confirm the as-of date, scan scope, market, and comparison baselines.
2. Separate confirmed changes from rumors, repeated news, theme labels, and price-only signals.
3. Assess liquidity, interest-rate, currency, credit, flow, breadth, volume, and risk-appetite direction.
4. Identify industry changes in technology, cost, policy, demand, consumption, supply, or penetration.
5. Translate any “era” narrative into observable variables and compare prosperity evidence with a named historical, cross-industry, or expectation baseline.
6. Identify company signals in revenue, profit, orders, share, pricing, or operating metrics.
7. Form a preliminary commercial and earnings transmission hypothesis without pretending to complete deep industry or earnings work.
8. Assess whether the market may not yet understand the change and identify the next verification event.
9. For industry candidates, define the preliminary Industry Scope Card, scan all six questions, identify the dominant driver, and recommend the deep-dive order without upgrading rough evidence to an Industry Thesis.

### Opportunity Granularity and Hypothesis Formation

For a broad industry, theme, or concept:

1. Build a preliminary `Industry Scope Card`: final product/service and substitute boundary, technology path, geography/market, value-chain position, lifecycle/competition context, as-of date, units, and definitions;
2. Identify whether the object contains multiple distinct demand structures, technology paths, value chains, or profit pools;
3. If it is heterogeneous, split it into no more than 3—5 researchable subsegments before a final Reject;
4. For each surviving subsegment, make a `Six-Question Rough Cut` covering Q1 size/growth/cycle, Q2 map/profit distribution, Q3 segment economics, Q4 technology, Q5 regulation/geopolitics/localization, and Q6 industry valuation/narrative. Record evidence level and critical Unknowns rather than pretending to finish the deep read;
5. Identify `Dominant Driver` and `Recommended Deep-Dive Order` with rationale;
6. Form an `Investment Opportunity Hypothesis`:

> Industry Change → Value Migration → Beneficiary Segment → Profit-Pool Hypothesis → Possible Earnings/FCF Impact → Market View → Agent View → Variant Hypothesis → Verification Metrics

This is a preliminary handoff hypothesis, not an Industry Thesis Pass, Company Alpha conclusion, or Buy signal.

## Required Output

Return the common stage record defined in [Evidence, Gates and Handoff Contract](../investment-agent/references/evidence-and-gates.md), then add the fields below.

Also return:

- Market State;
- Liquidity Direction;
- Risk Appetite Direction;
- Risk Level;
- Recommended Risk Exposure;
- Regime Change Triggers;
- Opportunity Candidates;
- Era / Reality Driver for each candidate;
- Prosperity Evidence and Named Baseline;
- Prosperity Acceleration or Deceleration;
- Trigger Signal for each candidate;
- Value Change Hypothesis;
- Possible Earnings Impact;
- Preliminary Pricing Status;
- Research Priority: High / Medium / Low;
- Relative Research Priority and decisive evidence when comparable candidates exist;
- Research Question;
- Recommended Next Route.

For every candidate also return:

- Industry Scope Card;
- Candidate Granularity and Subsegments Considered;
- Six-Question Rough Cut;
- Dominant Driver and Recommended Deep-Dive Order;
- Six-Question Critical Unknowns;
- Opportunity Radar Coverage;
- Core View (Agent's explicit viewpoint);
- Era-to-Observable-Variable Bridge;
- Prosperity Evidence versus baseline;
- Supporting Evidence Table with Fact, Change, source/date, baseline and definition;
- Market View vs Agent View;
- Variant Hypothesis;
- Profit Pool Pre-check;
- Evidence Level: Radar Only / Narrative Extracted / Cross-Validated;
- Granularity Decision;
- Missing Inputs and Recheck Reason;
- Reopen Conditions.

## Gates

### Market Regime Sub-Decision

- **Pass:** the regime can be described reliably, even if it is adverse.
- **Recheck:** important market signals conflict or are transitioning too quickly for a stable conclusion.
- **Reject:** essential market information is unusable; reject only the risk-exposure conclusion, not the industry thesis.

### Opportunity Screening Sub-Decision

- **Pass:** at least one material, verifiable change has a plausible path to business and earnings impact and may be under-recognized. An industry-candidate Pass also requires a coherent scope or explicit subsegment, a rough six-question coverage record sufficient to route the deep read, and no hidden boundary conflict that could reverse the preliminary hypothesis.
- **Recheck:** a signal exists but persistence, transmission, pricing status, granularity, or evidence coverage is unclear. Label the reason as `Recheck—Subsegment`, `Recheck—Data`, or `Recheck—Variant`.
- **Reject:** after reasonable subsegment decomposition, no candidate has a material change, plausible commercial/earnings path, or research value. Label the scope; do not reject an entire heterogeneous industry solely from an aggregate index move.

## Handoff

Send only candidates that have passed the granularity check or explicitly carry a `Recheck—Subsegment` handoff to `investment-industry-value-chain`. Include the Industry Scope Card, Six-Question Rough Cut, dominant driver, era/reality driver, observable-variable bridge, prosperity evidence and baseline, recommended deep-dive order, trigger facts, coverage record, preliminary opportunity hypothesis, profit-pool pre-check, research priority, validation needs, market state, evidence level, and all unresolved gaps.

Also preserve Market State and Risk Level for `investment-earnings-valuation` and `investment-timing-portfolio`.

## Boundaries

- Do not select industries merely because they recently outperformed.
- Do not call an industry “most prosperous” from attention, price performance, or one favorable datapoint. Relative claims require comparable candidates, a named baseline, and decisive evidence; otherwise mark ranking not assessed.
- Do not call an industry investable before its industry thesis and profit pool are validated.
- Do not convert High Research Priority into Buy.
- Market weakness limits exposure but does not by itself invalidate a structural industry opportunity.
- A broad industry's weak performance does not justify rejecting every subsegment; distinguish `Reject—Current Scope` from a sector-wide thesis failure.
- A Knowledge Star/IMA title or report count is market-attention evidence, not proof of demand, profit, or consensus.
- Do not turn the six-question rough cut into a completed Industry Thesis, Company Alpha judgment, company valuation, or six new gates.

## Trigger, Candidate Queue and Evidence

When assembling a report or candidate comparison, read [Presentation Contract](../investment-agent/references/presentation-contract.md).

For every task, record an `Investment Trigger`: Trigger Event, Why Now, Affected Variables, Potential Beneficiaries, Initial Research Hypothesis, and Market Awareness. A stock name alone is not a trigger.

For an “which industries are worth researching now?” request, produce a candidate industry/company queue with the evidence for each change, causal hypothesis, research priority, unknowns, and next validation. For a single-stock request, preserve the trigger but mark `Candidate Comparison: Not Assessed` unless comparable candidates were supplied or discovered with evidence.

When two or more candidates arise, emit a workflow-level `Candidate Comparison Record` seed using the shared dimensions (industry thesis, profit-pool position, company alpha hypothesis, variant, earnings visibility, valuation/risk reward, catalyst, trend, liquidity, portfolio fit, opportunity cost, unknowns). This is not a new Skill, a score, or a Buy signal.

Use the evidence labels `Fact`, `Change`, `Inference`, `Assumption`, `Hypothesis`, `Decision`, and `Unknown`. A Pass requires a verifiable change and a plausible path from fact to business value, earnings, and pricing; an attractive chart or theme without that chain is Reject.

## Recall, Granularity and Viewpoint Contract

The default opportunity-discovery route is `Rolling Window + Keyword Recall + Selected Detail`, not a single latest-30 snapshot. The skill must make the following visible in the output:

```text
Core View
→ Supporting Facts
→ Change versus baseline
→ Business and earnings transmission
→ Market View
→ Agent View / Variant
→ Profit-Pool Pre-check
→ Falsification and Verification
→ Stage Decision
```

`Opportunity Radar`, `Granularity Gate`, and `Investment Opportunity Hypothesis` are internal workflow abilities. Do not create or invoke a separate Opportunity Classification or Opportunity Hypothesis Skill.
