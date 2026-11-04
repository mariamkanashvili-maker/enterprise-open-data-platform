"""
lecture 11 lab: synthetic მონაცემების გენერაცია ფორმატების შედარებისთვის.
რეალურ sample-ს (Lab 4-5, ~24 row) მასშტაბი აკლია საინტერესო შედარებისთვის —
ამიტომ ვაგენერირებთ 10,000 მსგავს row-ს.
"""

import random
from datetime import datetime, timedelta, timezone


def generate_weather_records(n: int = 10_000) -> list:
    random.seed(42)  # რეპროდუცირებადობისთვის
    base_time = datetime(2026, 8, 1, tzinfo=timezone.utc)
    records = []
    for i in range(n):
        records.append({
            "city": random.choice(["Tbilisi", "Batumi", "Kutaisi", "Telavi"]),
            "latitude": round(random.uniform(41.0, 43.0), 4),
            "longitude": round(random.uniform(41.0, 46.0), 4),
            "forecast_time": (base_time + timedelta(hours=i)).isoformat(),
            "temperature_c": round(random.uniform(-5, 35), 2),
            "humidity_pct": round(random.uniform(20, 90), 2),
        })
    return records


if __name__ == "__main__":
    first = generate_weather_records()
    second = generate_weather_records()
    print(f"[OK] გენერირებულია {len(first):,} row")
    print(f"[OK] პირველი row: {first[0]}")
    print(f"[OK] seed=42 რეპროდუცირებადია: {'კი' if first == second else 'არა'}")
