"""
lecture 9 lab: Weather + Currency API-ების ერთად fetch —
"რამდენიმე API-დან მონაცემების ავტომატური მიღება".
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging
from src.ingestion.weather_client import WeatherAPIError, WeatherClient
from src.ingestion.currency_client import CurrencyAPIError, CurrencyClient


def main() -> int:
    setup_logging()
    exit_code = 0

    weather_client = WeatherClient()
    try:
        weather = weather_client.get_current_weather()
        print(f"[OK] ამინდი: {weather['current']['temperature_2m']}°C")
    except WeatherAPIError as exc:
        print(f"[FAIL] ამინდი ჩავარდა: {exc}")
        exit_code = 1

    currency_client = CurrencyClient()
    try:
        rates = currency_client.get_rates()
        usd = next(c for c in rates["currencies"] if c["code"] == "USD")
        print(f"[OK] USD კურსი: {usd['rate']} GEL")
    except CurrencyAPIError as exc:
        print(f"[FAIL] ვალუტა ჩავარდა: {exc}")
        exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
