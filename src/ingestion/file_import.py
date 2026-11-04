"""
lecture 10: File Import Engine — CSV/JSON/XML უნიფიცირებული წაკითხვა,
ვალიდაციითა და encoding-ის მართვით.
"""

import csv
import json
import logging
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class FileImportError(Exception):
    """ფაილის წაკითხვის ან ვალიდაციის შეცდომა."""


def read_csv(path: Path, required_columns: Optional[list] = None) -> list:
    path = Path(path)
    try:
        with open(path, encoding="utf-8-sig") as f:  # utf-8-sig BOM-ს თვითონ ამოიცნობს
            rows = list(csv.DictReader(f))
    except UnicodeDecodeError as exc:
        raise FileImportError(f"CSV encoding შეცდომა {path}: {exc}") from exc

    if not rows:
        raise FileImportError(f"CSV ცარიელია: {path}")

    if required_columns:
        missing = set(required_columns) - set(rows[0].keys())
        if missing:
            raise FileImportError(f"CSV-ს აკლია სვეტები {path}: {missing}")

    logger.info("წაკითხულია %d row CSV-დან: %s", len(rows), path.name)
    return rows


def read_json(path: Path) -> Any:
    path = Path(path)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise FileImportError(f"არასწორი JSON {path}: {exc}") from exc
    logger.info("წაკითხულია JSON: %s", path.name)
    return data


def read_xml(path: Path) -> list:
    path = Path(path)
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        raise FileImportError(f"არასწორი XML {path}: {exc}") from exc

    root = tree.getroot()
    records = []
    for record_elem in root:
        record = {child.tag: child.text for child in record_elem}
        records.append(record)
    logger.info("წაკითხულია %d ჩანაწერი XML-დან: %s", len(records), path.name)
    return records
