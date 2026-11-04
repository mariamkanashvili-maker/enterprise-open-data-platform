"""
lecture 10: excel_handler.py-ის გადამოწმება — round-trip და 2 ჩავარდნის სცენარი.
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.excel_handler import ExcelImportError, read_excel, write_excel


def test_round_trip(tmp_path: str = "/tmp/test_round_trip.xlsx") -> None:
    original = pd.DataFrame({"currency_code": ["USD", "EUR"], "rate": [2.6479, 2.9180]})
    write_excel(original, tmp_path)
    read_back = read_excel(tmp_path)
    assert read_back.equals(original)
    print("[OK] round-trip სწორია — ჩაწერილი და წაკითხული მონაცემი იდენტურია")


def test_missing_required_column() -> None:
    df = pd.DataFrame({"currency_code": ["USD"], "rate": [2.6479]})
    write_excel(df, "/tmp/test_missing_col.xlsx")
    try:
        read_excel("/tmp/test_missing_col.xlsx", required_columns={"nonexistent_column"})
        raise AssertionError("უნდა ატყორცნოს ExcelImportError")
    except ExcelImportError as exc:
        print(f"[OK] სწორად დაიჭირა: {exc}")


def test_file_not_found() -> None:
    try:
        read_excel("/tmp/does_not_exist.xlsx")
        raise AssertionError("უნდა ატყორცნოს ExcelImportError")
    except ExcelImportError as exc:
        print(f"[OK] სწორად დაიჭირა: {exc}")


if __name__ == "__main__":
    test_round_trip()
    test_missing_required_column()
    test_file_not_found()
