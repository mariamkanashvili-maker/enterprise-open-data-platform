"""
lecture 10: sample CSV/XML/GeoJSON ფაილების გენერაცია (File Naming Conventions-ის დემონსტრაცია).
"""

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path

SAMPLE_DIR = Path("data/sample")

CURRENCY_ROWS = [
    {"currency_code": "USD", "quantity": "1", "rate": "2.6512", "rate_date": "2026-08-27"},
    {"currency_code": "EUR", "quantity": "1", "rate": "2.9284", "rate_date": "2026-08-27"},
]

# მრავალდღიანი ვალუტის მონაცემი pandas_transform-ის ტესტისთვის (Step 6)
CURRENCY_MULTI_DAY_ROWS = [
    {"currency_code": "USD", "rate": "2.6455", "rate_date": "2026-08-25"},
    {"currency_code": "USD", "rate": "2.6480", "rate_date": "2026-08-26"},
    {"currency_code": "USD", "rate": "2.6502", "rate_date": "2026-08-27"},
    {"currency_code": "EUR", "rate": "2.9150", "rate_date": "2026-08-25"},
    {"currency_code": "EUR", "rate": "2.9180", "rate_date": "2026-08-26"},
    {"currency_code": "EUR", "rate": "2.9210", "rate_date": "2026-08-27"},
]

WEATHER_ROWS = [
    {"city": "Tbilisi", "forecast_time": "2026-08-27T12:00:00+00", "temperature_c": "28.3"},
    {"city": "Tbilisi", "forecast_time": "2026-08-27T13:00:00+00", "temperature_c": "29.2"},
]

# USGS-ის ფორმატის GeoJSON (coordinates = [lon, lat, depth], time მილიწამებში)
EARTHQUAKE_FEATURES = [
    {"id": "us7000aaa1", "mag": 3.1, "place": "near Tbilisi, Georgia", "time": 1787832000000, "coords": [44.75, 41.65, 8.2]},
    {"id": "us7000aaa2", "mag": 2.4, "place": "near Gori, Georgia", "time": 1787745600000, "coords": [44.11, 41.98, 10.0]},
    {"id": "us7000aaa3", "mag": 4.0, "place": "near Ambrolauri, Georgia", "time": 1787659200000, "coords": [43.15, 42.52, 12.5]},
]


def write_csv(path: Path, rows: list) -> Path:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return path


def build_weather_xml() -> Path:
    path = SAMPLE_DIR / "weather_forecast_2026-08-27.xml"
    root = ET.Element("forecasts")
    for row in WEATHER_ROWS:
        record = ET.SubElement(root, "forecast")
        for key, value in row.items():
            field = ET.SubElement(record, key)
            field.text = value
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def build_earthquakes_geojson() -> Path:
    path = SAMPLE_DIR / "earthquakes_sample.geojson"
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": e["id"],
                "properties": {"mag": e["mag"], "place": e["place"], "time": e["time"]},
                "geometry": {"type": "Point", "coordinates": e["coords"]},
            }
            for e in EARTHQUAKE_FEATURES
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


if __name__ == "__main__":
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[OK] {write_csv(SAMPLE_DIR / 'currency_rates_2026-08-27.csv', CURRENCY_ROWS)}")
    print(f"[OK] {build_weather_xml()}")
    geo = SAMPLE_DIR / "earthquakes_sample.geojson"
    if geo.exists():
        print(f"[SKIP] {geo} უკვე არსებობს (წინა ლაბიდან)")
    else:
        print(f"[OK] {build_earthquakes_geojson()}")
    print(f"[OK] {write_csv(SAMPLE_DIR / 'currency_rates_2026-08-25_2026-08-27.csv', CURRENCY_MULTI_DAY_ROWS)}")
