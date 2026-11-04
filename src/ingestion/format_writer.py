"""
lecture 11: მონაცემების შენახვა სხვადასხვა ფორმატში — JSON, CSV, Parquet, Avro.
"""

import csv
import json
from pathlib import Path

WEATHER_AVRO_SCHEMA = {
    "type": "record",
    "name": "WeatherForecast",
    "fields": [
        {"name": "city", "type": "string"},
        {"name": "latitude", "type": "double"},
        {"name": "longitude", "type": "double"},
        {"name": "forecast_time", "type": "string"},
        {"name": "temperature_c", "type": "double"},
        {"name": "humidity_pct", "type": "double"},
    ],
}


def write_json(records: list, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(records, f, default=str)


def read_json(path: Path) -> list:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_csv(records: list, path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def read_csv(path: Path) -> list:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_parquet(records: list, path: Path) -> None:
    import pyarrow as pa
    import pyarrow.parquet as pq

    table = pa.Table.from_pylist(records)
    pq.write_table(table, path, compression="snappy")


def read_parquet(path: Path) -> list:
    import pyarrow.parquet as pq

    return pq.read_table(path).to_pylist()


def write_avro(records: list, path: Path, schema: dict = WEATHER_AVRO_SCHEMA) -> None:
    import fastavro

    with open(path, "wb") as f:
        fastavro.writer(f, schema, records)


def read_avro(path: Path) -> list:
    import fastavro

    with open(path, "rb") as f:
        return list(fastavro.reader(f))
