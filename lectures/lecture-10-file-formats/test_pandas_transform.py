"""
lecture 10: pandas_transform.py-ის გადამოწმება — pandas-ის შედეგს ვადარებთ
stdlib csv-ით ხელით გამოთვლილ შედეგს.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.pandas_transform import compute_daily_currency_stats

CSV_PATH = str(Path(__file__).resolve().parents[2] / "data/sample/currency_rates_2026-08-25_2026-08-27.csv")


def stdlib_stats(path: str) -> dict:
    rates = defaultdict(list)
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rates[row["currency_code"]].append(float(row["rate"]))
    return {code: (round(sum(v) / len(v), 4), min(v), max(v)) for code, v in rates.items()}


def test_compute_daily_currency_stats() -> None:
    stats = compute_daily_currency_stats(CSV_PATH)
    assert set(stats.columns) == {"currency_code", "avg_rate", "min_rate", "max_rate"}
    assert len(stats) == 2

    usd = stats[stats["currency_code"] == "USD"].iloc[0]
    assert usd["avg_rate"] == 2.6479

    manual = stdlib_stats(CSV_PATH)
    for _, row in stats.iterrows():
        assert (row["avg_rate"], row["min_rate"], row["max_rate"]) == manual[row["currency_code"]]

    print(stats.to_string())
    print("[OK] pandas groupby().agg() ზუსტად იგივე შედეგს იძლევა, რაც stdlib csv-ით ხელნაწერი გამოთვლა")


if __name__ == "__main__":
    test_compute_daily_currency_stats()
