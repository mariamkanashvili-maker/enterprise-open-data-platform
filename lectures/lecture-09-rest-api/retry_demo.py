"""
lecture 9 lab: Retry მექანიზმის შემოწმება — API-ის დროებითი და მუდმივი შეცდომის სიმულაცია.
requests.get-ს unittest.mock-ით დროებით ვცვლით, რეალური API-ს გამოძახების გარეშე.
"""

import sys
import time
from pathlib import Path
from unittest import mock

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging
from src.ingestion.weather_client import WeatherAPIError, WeatherClient


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"current": {"temperature_2m": 24.3, "wind_speed_10m": 8.1}}


def scenario_flaky() -> None:
    """პირველი 2 ცდა ჩავარდება, მე-3 წარმატებულია."""
    calls = {"n": 0}

    def flaky_get(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise requests.exceptions.ConnectionError("simulated glitch")
        return FakeResponse()

    start = time.perf_counter()
    with mock.patch("src.ingestion.weather_client.requests.get", side_effect=flaky_get):
        WeatherClient().get_current_weather()
    print(f"# სულ დრო: {time.perf_counter() - start:.1f}s, სულ ცდა: {calls['n']}")


def scenario_permanent() -> None:
    """ყველა ცდა ჩავარდება — retry ამოიწურება და WeatherAPIError უნდა დავიჭიროთ."""

    def broken_get(url, params=None, timeout=None):
        raise requests.exceptions.ConnectionError("permanent glitch")

    with mock.patch("src.ingestion.weather_client.requests.get", side_effect=broken_get):
        try:
            WeatherClient().get_current_weather()
        except WeatherAPIError as exc:
            print(f"[OK] WeatherAPIError სწორად დაიჭირა: {exc}")


def main() -> int:
    setup_logging()
    print("=== სცენარი 1: დროებითი შეცდომა (2 ჩავარდნა → წარმატება) ===")
    scenario_flaky()
    print("\n=== სცენარი 2: მუდმივი შეცდომა (ყველა ცდა ჩავარდა) ===")
    scenario_permanent()
    return 0


if __name__ == "__main__":
    sys.exit(main())
