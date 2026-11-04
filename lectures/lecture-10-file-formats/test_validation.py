"""
lecture 10: ვალიდაციის ჩავარდნის ცოცხლად ნახვა — არარსებული სვეტის მოთხოვნა.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.file_import import FileImportError, read_csv

try:
    read_csv(
        "data/sample/currency_rates_2026-08-27.csv",
        required_columns=["currency_code", "nonexistent_column"],
    )
    print("[FAIL] ვალიდაცია უნდა ჩავარდნილიყო")
except FileImportError as exc:
    print(f"[OK] ვალიდაცია სწორად ჩავარდა: {exc}")
