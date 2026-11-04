"""
lecture 11 lab: ფორმატების შედარება — ზომა და წაკითხვის სისწრაფე.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from generate_synthetic_data import generate_weather_records
from src.ingestion.format_writer import (
    read_avro, read_csv, read_json, read_parquet,
    write_avro, write_csv, write_json, write_parquet,
)

OUT_DIR = Path("data/format_comparison")


def human_size(num_bytes: float) -> str:
    for unit in ["B", "KB", "MB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f}GB"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    records = generate_weather_records(10_000)
    print(f"გენერირებულია {len(records)} row synthetic weather მონაცემი\n")

    writers = {
        "json": (write_json, read_json, "weather.json"),
        "csv": (write_csv, read_csv, "weather.csv"),
        "parquet": (write_parquet, read_parquet, "weather.parquet"),
        "avro": (write_avro, read_avro, "weather.avro"),
    }

    print(f"{'ფორმატი':<10} {'ზომა':<10} {'ჩაწერა':<10} {'წაკითხვა':<10}")
    for name, (write_fn, read_fn, filename) in writers.items():
        path = OUT_DIR / filename
        try:
            start = time.perf_counter()
            write_fn(records, path)
            write_time = time.perf_counter() - start

            start = time.perf_counter()
            read_fn(path)
            read_time = time.perf_counter() - start

            size = path.stat().st_size
            print(f"{name:<10} {human_size(size):<10} {write_time:.3f}s{'':<4} {read_time:.3f}s")
        except ImportError as exc:
            print(f"{name:<10} გამოტოვებულია — ბიბლიოთეკა ვერ მოიძებნა ({exc})")


if __name__ == "__main__":
    main()
