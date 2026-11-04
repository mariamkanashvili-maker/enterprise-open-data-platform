"""
lecture 9 lab (დანართი): custom retry.py-ის ეკვივალენტი tenacity ბიბლიოთეკით.
იგივე ქცევა (3 ცდა, exponential backoff 1s → 2s), production-ში ხშირად ამჯობინებენ,
რადგან already-tested, well-maintained library-ია.
"""

import logging
import sys
import time
from pathlib import Path
from unittest import mock

import requests
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging

logger = logging.getLogger("tenacity_demo")
BASE_URL = "https://api.open-meteo.com/v1/forecast"


class TenacityWeatherClient:
    @retry(
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        reraise=True,
    )
    def _get(self, params: dict) -> requests.Response:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        return response


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return {"current": {"temperature_2m": 24.3}}


def main() -> int:
    setup_logging()
    calls = {"n": 0}

    def flaky_get(url, params=None, timeout=None):
        calls["n"] += 1
        if calls["n"] < 3:
            raise requests.exceptions.ConnectionError("simulated glitch")
        return FakeResponse()

    start = time.perf_counter()
    with mock.patch("requests.get", side_effect=flaky_get):
        data = TenacityWeatherClient()._get({}).json()
    print(f"[OK] tenacity: temperature={data['current']['temperature_2m']}°C, "
          f"სულ ცდა: {calls['n']}, სულ დრო: {time.perf_counter() - start:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
