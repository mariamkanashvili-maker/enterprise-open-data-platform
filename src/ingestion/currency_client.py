"""
lecture 9: NBG (ეროვნული ბანკი) API client — production-grade retry/timeout/error handling.
"""

import logging
from datetime import date as date_type
from typing import Any, Optional

import requests

from .retry import retry_with_backoff

logger = logging.getLogger(__name__)

BASE_URL = "https://nbg.gov.ge/gw/api/ct/monetarypolicy/currencies/en/json/"


class CurrencyAPIError(Exception):
    """NBG API-სთან დაკავშირებული ნებისმიერი შეცდომა."""


class CurrencyClient:
    def __init__(self, timeout_seconds: int = 10) -> None:
        self.timeout_seconds = timeout_seconds

    @retry_with_backoff((requests.exceptions.RequestException,), max_attempts=3)
    def _get(self, params: dict) -> requests.Response:
        response = requests.get(BASE_URL, params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response

    def get_rates(self, on_date: Optional[date_type] = None) -> dict[str, Any]:
        params = {"date": on_date.isoformat()} if on_date else {}
        logger.info("მოთხოვნა NBG API-სთან (date=%s)", on_date or "today")
        try:
            response = self._get(params)
        except requests.exceptions.RequestException as exc:
            logger.error("NBG API საბოლოოდ ჩავარდა: %s", exc)
            raise CurrencyAPIError(f"NBG request ჩავარდა: {exc}") from exc

        data = response.json()
        entry = data[0]
        logger.info("მიღებულია %d ვალუტის კურსი, თარიღი: %s", len(entry["currencies"]), entry["date"])
        return entry
