import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.modeling.scd2 import scd2_upsert

KEY, TRACKED = "city", ["population_category"]

# Test 1: პირველი ვერსია
v1 = {"city": "Tbilisi", "population_category": "large"}
t1 = scd2_upsert([], v1, KEY, TRACKED, "2026-01-01")
assert len(t1) == 1 and t1[0]["is_current"] is True and t1[0]["valid_to"] is None
print("Test 1:", t1[0])

# Test 2: ცვლილების გარეშე
t2 = scd2_upsert(t1, v1, KEY, TRACKED, "2026-06-01")
assert len(t2) == 1
print("Test 2: row-ების რაოდენობა უცვლელია:", len(t2))

# Test 3: რეალური ცვლილება
v2 = {"city": "Tbilisi", "population_category": "mega"}
t3 = scd2_upsert(t1, v2, KEY, TRACKED, "2026-09-01")
assert len(t3) == 2
assert t3[0]["is_current"] is False and t3[0]["valid_to"] == "2026-09-01"
assert t3[1]["is_current"] is True and t3[1]["valid_from"] == "2026-09-01"
print("Test 3:")
for r in t3:
    print("  ", r)

print("[OK] ყველა 3 სცენარი (პირველი ჩანაწერი, ცვლილების გარეშე, რეალური ცვლილება) სწორად მუშაობს")
