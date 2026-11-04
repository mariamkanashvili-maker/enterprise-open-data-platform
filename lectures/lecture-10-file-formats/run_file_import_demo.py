"""
lecture 10 lab: File Import Engine-ის დემონსტრაცია — CSV/XML/JSON წაკითხვა და ვალიდაცია.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.file_import import FileImportError, read_csv, read_json, read_xml
from src.ingestion.logging_config import setup_logging

SAMPLE_DIR = Path("data/sample")


def main() -> int:
    setup_logging()
    try:
        csv_rows = read_csv(
            SAMPLE_DIR / "currency_rates_2026-08-27.csv",
            required_columns=["currency_code", "rate", "rate_date"],
        )
        print(f"[OK] CSV: {len(csv_rows)} row, პირველი: {csv_rows[0]}")

        xml_rows = read_xml(SAMPLE_DIR / "weather_forecast_2026-08-27.xml")
        print(f"[OK] XML: {len(xml_rows)} ჩანაწერი, პირველი: {xml_rows[0]}")

        geo_data = read_json(SAMPLE_DIR / "earthquakes_sample.geojson")
        print(f"[OK] GeoJSON: {len(geo_data['features'])} feature")
    except FileImportError as exc:
        print(f"[FAIL] {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
