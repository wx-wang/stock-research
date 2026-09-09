import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).parents[1] / "scripts" / "narrative_dcf.py"
SPEC = importlib.util.spec_from_file_location("narrative_dcf", MODULE_PATH)
assert SPEC and SPEC.loader
narrative_dcf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(narrative_dcf)


class NarrativeDcfTests(unittest.TestCase):
    def test_reverse_round_trip_cash_flow(self):
        expected_multiple = 3.4
        value = narrative_dcf.present_value(100, expected_multiple, 5, 0.10)
        implied = narrative_dcf.implied_terminal_multiple(
            value["present_value"], 100, 5, 0.10, "perpetuity", 0, 0.0
        )
        self.assertAlmostEqual(implied["terminal_multiple"], expected_multiple, places=9)
        self.assertAlmostEqual(implied["value_error"], 0.0, places=8)

    def test_reverse_round_trip_profit_with_conversion(self):
        expected_multiple = 2.6
        value = narrative_dcf.present_value(
            120, expected_multiple, 6, 0.11, basis="profit",
            current_cash_conversion=0.45, terminal_cash_conversion=0.85,
        )
        implied = narrative_dcf.implied_terminal_multiple(
            value["present_value"], 120, 6, 0.11, "perpetuity", 0, 0.0,
            basis="profit", current_cash_conversion=0.45,
            terminal_cash_conversion=0.85,
        )
        self.assertAlmostEqual(implied["terminal_multiple"], expected_multiple, places=9)

    def test_zero_profit_conversion_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "positive cash-conversion"):
            narrative_dcf.present_value(
                100, 2, 5, 0.10, basis="profit",
                current_cash_conversion=0.0, terminal_cash_conversion=0.0,
            )

    def test_growing_perpetuity_requires_growth_below_discount_rate(self):
        with self.assertRaisesRegex(ValueError, "growth_rate < discount_rate"):
            narrative_dcf.present_value(
                100, 2, 5, 0.10, terminal_mode="growing-perpetuity",
                terminal_growth_rate=0.10,
            )


if __name__ == "__main__":
    unittest.main()
