#!/usr/bin/env python3
"""Deterministic analytical helper for the narrative-valuation skill.

All operating-base and value inputs must use the same basis: either total
equity amounts or fully diluted per-share amounts. Profit mode converts the
modeled profit path into shareholder-distributable cash before discounting.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Any


def _positive(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite number greater than zero")


def _nonnegative_int(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative")


def _conversion_rate(name: str, value: float) -> None:
    if not math.isfinite(value) or value < 0 or value > 1:
        raise ValueError(f"{name} must satisfy 0 <= value <= 1")


def present_value(
    c0: float,
    terminal_multiple: float,
    years: int,
    discount_rate: float,
    terminal_mode: str = "perpetuity",
    plateau_years: int = 0,
    decay_rate: float = 0.0,
    terminal_growth_rate: float = 0.0,
    basis: str = "cash-flow",
    current_cash_conversion: float = 1.0,
    terminal_cash_conversion: float = 1.0,
) -> dict[str, float | int | str]:
    _positive("c0", c0)
    _positive("terminal_multiple", terminal_multiple)
    _positive("years", float(years))
    _positive("discount_rate", discount_rate)
    _nonnegative_int("plateau_years", plateau_years)
    if decay_rate < 0 or decay_rate >= 1:
        raise ValueError("decay_rate must satisfy 0 <= decay_rate < 1")
    if terminal_growth_rate <= -1 or not math.isfinite(terminal_growth_rate):
        raise ValueError("terminal_growth_rate must be finite and greater than -1")
    if basis not in {"cash-flow", "profit"}:
        raise ValueError("basis must be cash-flow or profit")
    _conversion_rate("current_cash_conversion", current_cash_conversion)
    _conversion_rate("terminal_cash_conversion", terminal_cash_conversion)
    if basis == "profit" and current_cash_conversion == 0 and terminal_cash_conversion == 0:
        raise ValueError("profit basis requires a positive cash-conversion rate somewhere on the path")
    if basis == "cash-flow" and (
        current_cash_conversion != 1.0 or terminal_cash_conversion != 1.0
    ):
        raise ValueError("cash-flow basis requires both cash-conversion rates to equal 1")

    q = terminal_multiple ** (1.0 / years)
    terminal_base_metric = c0 * terminal_multiple

    def conversion_at(t: int) -> float:
        return current_cash_conversion + (
            terminal_cash_conversion - current_cash_conversion
        ) * t / years

    def distributable_cash_at(t: int) -> float:
        return c0 * q**t * conversion_at(t)

    ramp_pv = sum(
        distributable_cash_at(t) / (1.0 + discount_rate) ** t
        for t in range(1, years + 1)
    )
    terminal_distributable_cash = terminal_base_metric * terminal_cash_conversion

    if terminal_mode == "perpetuity":
        if terminal_growth_rate != 0:
            raise ValueError("perpetuity mode requires terminal_growth_rate = 0")
        terminal_pv = (
            terminal_distributable_cash / discount_rate
        ) / (1.0 + discount_rate) ** years
    elif terminal_mode == "growing-perpetuity":
        if terminal_growth_rate >= discount_rate:
            raise ValueError("growing perpetuity requires terminal_growth_rate < discount_rate")
        terminal_value = terminal_distributable_cash * (
            1.0 + terminal_growth_rate
        ) / (discount_rate - terminal_growth_rate)
        terminal_pv = terminal_value / (1.0 + discount_rate) ** years
    elif terminal_mode == "finite":
        if plateau_years == 0:
            raise ValueError("finite mode requires plateau_years > 0")
        terminal_pv = sum(
            terminal_distributable_cash / (1.0 + discount_rate) ** (years + k)
            for k in range(1, plateau_years + 1)
        )
    elif terminal_mode == "decay":
        plateau_pv = sum(
            terminal_distributable_cash / (1.0 + discount_rate) ** (years + k)
            for k in range(1, plateau_years + 1)
        )
        declining_value_at_plateau_end = terminal_distributable_cash * (
            1.0 - decay_rate
        ) / (discount_rate + decay_rate)
        decline_pv = declining_value_at_plateau_end / (1.0 + discount_rate) ** (
            years + plateau_years
        )
        terminal_pv = plateau_pv + decline_pv
    else:
        raise ValueError(f"unsupported terminal_mode: {terminal_mode}")

    value = ramp_pv + terminal_pv
    first_year_base_metric = c0 * q
    first_year_cash_flow = distributable_cash_at(1)
    return {
        "c0": c0,
        "basis": basis,
        "current_cash_conversion": current_cash_conversion,
        "terminal_cash_conversion": terminal_cash_conversion,
        "first_year_base_metric": first_year_base_metric,
        "terminal_base_metric": terminal_base_metric,
        "terminal_cash_flow": terminal_distributable_cash,
        "terminal_multiple": terminal_multiple,
        "years": years,
        "discount_rate": discount_rate,
        "annual_path_factor": q,
        "first_year_cash_flow": first_year_cash_flow,
        "terminal_mode": terminal_mode,
        "terminal_growth_rate": terminal_growth_rate,
        "plateau_years": plateau_years,
        "decay_rate": decay_rate,
        "ramp_present_value": ramp_pv,
        "terminal_present_value": terminal_pv,
        "present_value": value,
        "forward_cash_flow_multiple": value / first_year_cash_flow,
    }


def implied_terminal_multiple(
    market_value: float,
    c0: float,
    years: int,
    discount_rate: float,
    terminal_mode: str,
    plateau_years: int,
    decay_rate: float,
    terminal_growth_rate: float = 0.0,
    basis: str = "cash-flow",
    current_cash_conversion: float = 1.0,
    terminal_cash_conversion: float = 1.0,
) -> dict[str, Any]:
    _positive("market_value", market_value)
    low = 1e-12
    high = 1.0

    while present_value(
        c0, high, years, discount_rate, terminal_mode, plateau_years, decay_rate,
        terminal_growth_rate, basis, current_cash_conversion, terminal_cash_conversion
    )["present_value"] < market_value:
        high *= 2.0
        if high > 1e12:
            raise ValueError("could not bracket an implied terminal multiple below 1e12")

    for _ in range(200):
        mid = (low + high) / 2.0
        value = present_value(
            c0, mid, years, discount_rate, terminal_mode, plateau_years, decay_rate,
            terminal_growth_rate, basis, current_cash_conversion, terminal_cash_conversion
        )["present_value"]
        if value < market_value:
            low = mid
        else:
            high = mid

    result = present_value(
        c0, (low + high) / 2.0, years, discount_rate, terminal_mode, plateau_years, decay_rate,
        terminal_growth_rate, basis, current_cash_conversion, terminal_cash_conversion
    )
    result["market_value"] = market_value
    result["value_error"] = result["present_value"] - market_value
    return result


def _csv_floats(value: str) -> list[float]:
    return [float(item.strip()) for item in value.split(",") if item.strip()]


def _csv_ints(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def add_model_args(parser: argparse.ArgumentParser, include_multiple: bool = True) -> None:
    parser.add_argument(
        "--c0", type=float, required=True,
        help="normalized current base metric: cash flow or attributable profit",
    )
    if include_multiple:
        parser.add_argument("--terminal-multiple", type=float, required=True)
    parser.add_argument("--years", type=int, required=True)
    parser.add_argument("--discount-rate", type=float, required=True, help="decimal, e.g. 0.10")
    parser.add_argument(
        "--terminal-mode",
        choices=("perpetuity", "growing-perpetuity", "finite", "decay"),
        default="perpetuity",
    )
    parser.add_argument("--plateau-years", type=int, default=0)
    parser.add_argument("--decay-rate", type=float, default=0.0, help="decimal annual decline")
    parser.add_argument(
        "--terminal-growth-rate", type=float, default=0.0,
        help="company distributable-cash growth after year n; used by growing-perpetuity",
    )
    parser.add_argument("--basis", choices=("cash-flow", "profit"), default="cash-flow")
    parser.add_argument("--current-cash-conversion", type=float, default=1.0)
    parser.add_argument("--terminal-cash-conversion", type=float, default=1.0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    value_parser = subparsers.add_parser("value", help="calculate present value")
    add_model_args(value_parser)

    reverse_parser = subparsers.add_parser("reverse", help="infer terminal multiple from market value")
    add_model_args(reverse_parser, include_multiple=False)
    reverse_parser.add_argument("--market-value", type=float, required=True)

    grid_parser = subparsers.add_parser("grid", help="calculate discount-rate and duration sensitivity")
    grid_parser.add_argument("--c0", type=float, required=True)
    grid_parser.add_argument("--terminal-multiple", type=float, required=True)
    grid_parser.add_argument("--discount-rates", type=_csv_floats, required=True)
    grid_parser.add_argument("--years-list", type=_csv_ints, required=True)
    grid_parser.add_argument(
        "--terminal-mode",
        choices=("perpetuity", "growing-perpetuity", "finite", "decay"),
        default="perpetuity",
    )
    grid_parser.add_argument("--plateau-years", type=int, default=0)
    grid_parser.add_argument("--decay-rate", type=float, default=0.0)
    grid_parser.add_argument("--terminal-growth-rate", type=float, default=0.0)
    grid_parser.add_argument("--basis", choices=("cash-flow", "profit"), default="cash-flow")
    grid_parser.add_argument("--current-cash-conversion", type=float, default=1.0)
    grid_parser.add_argument("--terminal-cash-conversion", type=float, default=1.0)

    args = parser.parse_args()
    if args.command == "value":
        result: Any = present_value(
            args.c0,
            args.terminal_multiple,
            args.years,
            args.discount_rate,
            args.terminal_mode,
            args.plateau_years,
            args.decay_rate,
            args.terminal_growth_rate,
            args.basis,
            args.current_cash_conversion,
            args.terminal_cash_conversion,
        )
    elif args.command == "reverse":
        result = implied_terminal_multiple(
            args.market_value,
            args.c0,
            args.years,
            args.discount_rate,
            args.terminal_mode,
            args.plateau_years,
            args.decay_rate,
            args.terminal_growth_rate,
            args.basis,
            args.current_cash_conversion,
            args.terminal_cash_conversion,
        )
    else:
        result = []
        for years in args.years_list:
            for rate in args.discount_rates:
                result.append(
                    present_value(
                        args.c0,
                        args.terminal_multiple,
                        years,
                        rate,
                        args.terminal_mode,
                        args.plateau_years,
                        args.decay_rate,
                        args.terminal_growth_rate,
                        args.basis,
                        args.current_cash_conversion,
                        args.terminal_cash_conversion,
                    )
                )

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
