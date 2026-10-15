"""Synthetic regression: aggregate daily amounts without losing stores."""

import argparse
from decimal import Decimal
import unittest


def old_daily_total(rows):
    return {row["date"]: row["amount"] for row in rows}


def fixed_daily_total(rows):
    totals = {}
    for row in rows:
        date = row["date"]
        totals[date] = totals.get(date, Decimal("0")) + row["amount"]
    return totals


class DailyAggregationContract(unittest.TestCase):
    implementation = staticmethod(fixed_daily_total)

    def setUp(self):
        self.rows = [
            {"store_id": 101, "date": "2026-01-01", "amount": Decimal("10.25")},
            {"store_id": 202, "date": "2026-01-01", "amount": Decimal("20.50")},
            {"store_id": 101, "date": "2026-01-02", "amount": Decimal("5.00")},
        ]

    def test_same_date_keeps_both_stores(self):
        self.assertEqual(
            self.implementation(self.rows),
            {"2026-01-01": Decimal("30.75"), "2026-01-02": Decimal("5.00")},
        )

    def test_input_order_does_not_change_result(self):
        self.assertEqual(
            self.implementation(self.rows), self.implementation(list(reversed(self.rows)))
        )

    def test_total_is_conserved(self):
        self.assertEqual(
            sum(self.implementation(self.rows).values()),
            sum(row["amount"] for row in self.rows),
        )

    def test_empty_input(self):
        self.assertEqual(self.implementation([]), {})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("before", "after"), default="after")
    args = parser.parse_args()
    DailyAggregationContract.implementation = staticmethod(
        old_daily_total if args.mode == "before" else fixed_daily_total
    )
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DailyAggregationContract)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
