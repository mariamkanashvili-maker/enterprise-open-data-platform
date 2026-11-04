"""
lecture 7 lab: REST client + logging + config — გაშვება.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging
from src.ingestion.weather_client import WeatherAPIError, WeatherClient


def main() -> int:
    setup_logging()
    client = WeatherClient()
    try:
        client.get_current_weather()
    except WeatherAPIError as exc:
        print(f"[FAIL] {exc}")
        return 1
    print("[OK] წარმატებით დასრულდა")
    return 0


if __name__ == "__main__":
    sys.exit(main())
