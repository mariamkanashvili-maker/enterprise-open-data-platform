"""
lecture 10: xml_validator.py-ის გადამოწმება — სწორი და არასრული XML.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.xml_validator import XMLSchemaValidationError, validate_against_schema

XSD = "data/sample/weather_forecast.xsd"
GOOD_XML = "data/sample/weather_forecast_2026-08-27.xml"
BAD_XML = "/tmp/weather_forecast_incomplete.xml"

# არასრული XML: temperature_c ველი აკლია
Path(BAD_XML).write_text(
    '<?xml version="1.0" encoding="utf-8"?>\n'
    "<forecasts><forecast><city>Tbilisi</city>"
    "<forecast_time>2026-08-27T12:00:00+00</forecast_time></forecast></forecasts>\n",
    encoding="utf-8",
)

if validate_against_schema(GOOD_XML, XSD):
    print("[OK] სწორი XML გავიდა ვალიდაციას")

try:
    validate_against_schema(BAD_XML, XSD)
    print("[FAIL] არასრული XML ვალიდაციას არ უნდა გასულიყო")
except XMLSchemaValidationError as exc:
    print(f"[OK] სწორად დაიჭირა არასრული XML: {exc}")
