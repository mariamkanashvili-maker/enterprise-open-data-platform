"""
lecture 11 lab: Schema Evolution — ძველი სქემით (V1) ჩაწერილი Avro ფაილის
წაკითხვა ახალი სქემით (V2), რომელსაც დაემატა wind_speed_kmh ველი default-ით.
წინაპირობა: ჯერ compare_formats.py უნდა იყოს გაშვებული (ქმნის weather.avro-ს).
"""

import sys
from pathlib import Path

import fastavro

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.format_writer import WEATHER_AVRO_SCHEMA

OUT_DIR = Path("data/format_comparison")

# V2 = V1-ის ყველა ველი + ახალი ველი default მნიშვნელობით
WEATHER_AVRO_SCHEMA_V2 = {
    "type": "record",
    "name": "WeatherForecast",
    "fields": WEATHER_AVRO_SCHEMA["fields"] + [
        {"name": "wind_speed_kmh", "type": "double", "default": 0.0},
    ],
}


def main() -> None:
    avro_path = OUT_DIR / "weather.avro"

    # 1) reader_schema-ს გარეშე: გამოიყენება ფაილში ჩაშენებული (V1) სქემა
    with open(avro_path, "rb") as f:
        v1_records = list(fastavro.reader(f))
    print(f"[V1] reader_schema-ს გარეშე — ველები: {list(v1_records[0].keys())}")
    print(f"[V1] wind_speed_kmh არსებობს? {'wind_speed_kmh' in v1_records[0]}")

    # 2) reader_schema=V2: Avro schema resolution ახალ ველს default-ით ავსებს
    with open(avro_path, "rb") as f:
        v2_records = list(fastavro.reader(f, reader_schema=WEATHER_AVRO_SCHEMA_V2))
    print(f"\n[V2] reader_schema=V2 — ველები: {list(v2_records[0].keys())}")
    print(f"[V2] wind_speed_kmh = {v2_records[0]['wind_speed_kmh']}")

    filled = all(r["wind_speed_kmh"] == 0.0 for r in v2_records)
    print(f"\n[OK] {len(v2_records):,} ძველი ჩანაწერი წაიკითხა ახალი სქემით; "
          f"wind_speed_kmh ყველგან default-ით შეივსო: {'კი' if filled else 'არა'}")


if __name__ == "__main__":
    main()
