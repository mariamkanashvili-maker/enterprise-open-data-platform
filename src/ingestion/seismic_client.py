"""
lecture 10: USGS Earthquake Catalog client — მესამე მონაცემთა წყარო.
"""

import logging
from datetime import datetime, timezone
from typing import Any

import requests

from .retry import retry_with_backoff

logger = logging.getLogger(__name__)

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

GEORGIA_BBOX = {
    "minlatitude": 41.0,
    "maxlatitude": 43.6,
    "minlongitude": 40.0,
    "maxlongitude": 46.7,
}


class SeismicAPIError(Exception):
    """USGS API-სთან დაკავშირებული ნებისმიერი შეცდომა."""


class SeismicClient:
    def __init__(self, timeout_seconds: int = 10) -> None:
        self.timeout_seconds = timeout_seconds

    @retry_with_backoff((requests.exceptions.RequestException,), max_attempts=3)
    def _get(self, params: dict) -> requests.Response:
        response = requests.get(BASE_URL, params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response

    def get_recent_events(self, start_date: str, end_date: str, min_magnitude: float = 1.5) -> list[dict[str, Any]]:
        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": min_magnitude,
            "orderby": "time",
            **GEORGIA_BBOX,
        }
        logger.info("მოთხოვნა USGS API-სთან: %s .. %s, minmagnitude=%s", start_date, end_date, min_magnitude)
        try:
            response = self._get(params)
        except requests.exceptions.RequestException as exc:
            logger.error("USGS API საბოლოოდ ჩავარდა: %s", exc)
            raise SeismicAPIError(f"USGS request ჩავარდა: {exc}") from exc

        data = response.json()
        events = []
        for feature in data["features"]:
            props = feature["properties"]
            # GeoJSON: coordinates = [longitude, latitude, depth] — ჯერ lon, მერე lat
            lon, lat, depth = feature["geometry"]["coordinates"]
            events.append({
                "event_id": feature["id"],
                "magnitude": props["mag"],
                "place": props["place"],
                # USGS time მილიწამებშია → წამებად გადაყვანა
                "event_time": datetime.fromtimestamp(props["time"] / 1000, tz=timezone.utc),
                "latitude": lat,
                "longitude": lon,
                "depth_km": depth,
            })
        logger.info("მიღებულია %d სეისმური მოვლენა", len(events))
        return events
