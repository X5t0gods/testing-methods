"""Synthetic regression: demonstrate decimal half-up rounding at boundaries."""

import argparse
from decimal import Decimal, ROUND_HALF_UP
import unittest


def old_amount(value: str) -> Decimal:
    return Decimal(str(round(float(value), 2)))


def fixed_amount(value: str) -> Decimal:
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class MoneyContract(unittest.TestCase):
    implementation = staticmethod(fixed_amount)

    def test_half_cent_and_neighboring_boundaries(self):
        cases = [
            ("0", "0.00"),
            ("0.124", "0.12"),
            ("0.125", "0.13"),
            ("0.126", "0.13"),
            ("2.345", "2.35"),
            ("9.995", "10.00"),
            ("-0.125", "-0.13"),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(self.implementation(value), Decimal(expected))

    def test_exact_cent_is_preserved(self):
        self.assertEqual(self.implementation("12.34"), Decimal("12.34"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("before", "after"), default="after")
    args = parser.parse_args()
    MoneyContract.implementation = staticmethod(
        old_amount if args.mode == "before" else fixed_amount
    )
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(MoneyContract)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
