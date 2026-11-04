"""
lecture 10 (დამატება): Excel (.xlsx) წაკითხვა/ჩაწერა — pandas + openpyxl.
დანარჩენ file_import.py-ს (CSV/JSON/XML) ავსებს, არ ანაცვლებს.
"""

from typing import Optional, Union

import pandas as pd


class ExcelImportError(Exception):
    """Excel ფაილის წაკითხვა/ვალიდაციისას წარმოქმნილი შეცდომა."""


def read_excel(path: str, sheet_name: Union[str, int] = 0, required_columns: Optional[set] = None) -> pd.DataFrame:
    """
    კითხულობს .xlsx ფაილს pandas-ით (openpyxl engine).
    ვალიდაცია: required_columns თუ მითითებულია, მოწმდება რომ ყველა საჭირო სვეტი არსებობს.
    """
    try:
        df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    except FileNotFoundError as exc:
        raise ExcelImportError(f"ფაილი ვერ მოიძებნა: {path}") from exc
    except ValueError as exc:
        raise ExcelImportError(f"Excel parsing შეცდომა: {exc}") from exc

    if required_columns:
        missing = required_columns - set(df.columns)
        if missing:
            raise ExcelImportError(f"აკლია სვეტები: {missing}")
    return df


def write_excel(df: pd.DataFrame, path: str, sheet_name: str = "Sheet1") -> None:
    """წერს DataFrame-ს .xlsx-ად — pandas-ის to_excel, openpyxl engine-ით."""
    df.to_excel(path, sheet_name=sheet_name, index=False, engine="openpyxl")
