"""
lecture 10: seismic_client.py-ის შემოწმება.
1) mock-ტესტი: GeoJSON coordinates=[lon, lat, depth] სწორად იშლება (swap არ ხდება)
2) რეალური გამოძახება: USGS — საქართველოს რეგიონი, ბოლო 30 დღე
"""

import sys
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ingestion.logging_config import setup_logging
from src.ingestion.seismic_client import SeismicAPIError, SeismicClient

FAKE_GEOJSON = {
    "features": [{
        "id": "test001",
        "properties": {"mag": 3.1, "place": "near Tbilisi, Georgia", "time": 1787832000000},
        "geometry": {"coordinates": [44.75, 41.65, 8.2]},  # [lon, lat, depth]
    }]
}


class FakeResponse:
    def raise_for_status(self) -> None:
        pass

    def json(self) -> dict:
        return FAKE_GEOJSON


def test_no_coordinate_swap() -> None:
    with mock.patch("src.ingestion.seismic_client.requests.get", return_value=FakeResponse()):
        events = SeismicClient().get_recent_events("2026-07-28", "2026-08-27")
    e = events[0]
    assert e["latitude"] == 41.65 and e["longitude"] == 44.75, "coordinate swap მოხდა"
    print(f"[OK] mock: latitude={e['latitude']}, longitude={e['longitude']}, depth={e['depth_km']} km, "
          f"time={e['event_time'].isoformat()} — swap არ მომხდარა")


def live_call() -> None:
    end = date.today()
    start = end - timedelta(days=30)
    try:
        events = SeismicClient().get_recent_events(start.isoformat(), end.isoformat(), min_magnitude=1.5)
    except SeismicAPIError as exc:
        print(f"[FAIL] USGS: {exc}")
        return
    print(f"[OK] USGS live: {len(events)} მოვლენა ბოლო 30 დღეში")
    for e in events[:3]:
        print(f"     M{e['magnitude']} | {e['place']} | {e['event_time']:%Y-%m-%d %H:%M} UTC")


if __name__ == "__main__":
    setup_logging()
    test_no_coordinate_swap()
    live_call()
