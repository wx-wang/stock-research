# Data Requirements

## Mandatory Upstream Data

- Market State, Risk Level, and risk-exposure direction;
- Industry Thesis and Profit Pool decisions;
- Company Alpha decision and key drivers;
- earnings scenarios, variant, and validation timeline;
- the dated Expectation Position Record by horizon, including market baseline, Agent variant, descriptive phase, preserved pre-event expectations, revision path, next surprise tests, and falsifiers;
- current valuation, value ranges, upside, downside, risk reward, and liquidity;
- all key assumptions, falsifiers, metrics, catalysts, confidence, and unresolved gaps;
- as-of date.

If these inputs do not support an end-to-end causal chain, return Recheck rather than a buy state.

## Trend and Timing Data

- price and volume history sufficient to assess annual and quarterly structure;
- data sufficient to assess the 60-day trend;
- medium-term highs, lows, and relative strength;
- short-term volume, breakout, and pullback behavior;
- relevant benchmark or peer-relative behavior when used;
- catalyst date and price/volume response;
- actual result versus the preserved pre-event expectation, post-event forecast/narrative revisions, and a defined response window;
- ownership, turnover, supply, or selling evidence when claiming distribution rather than mere attention diffusion;
- current price aligned to valuation as-of date.

## Portfolio Context

For a directional state:

- current recommended or actual state;
- whether the user currently holds the security;
- relevant liquidity constraint.

For a specific position-size recommendation, also require investor-supplied:

- acceptable loss or risk boundary;
- existing position and exposure context;
- any maximum position constraint;
- any other constraint the investor wants applied.

Without these investor constraints, provide only Observe / Trial / Buy / Hold / Add / Reduce / Sell and a qualitative position direction.

## Minimum Pass Data

- valid upstream thesis and odds;
- long-, medium-, and short-term market evidence;
- catalyst and validation context;
- observable action and exit conditions;
- no hidden decisive Recheck or Reject upstream.
