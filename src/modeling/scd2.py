"""
lecture 6 (დამატება): Slowly Changing Dimension (SCD) Type 2 — testable ლოგიკა.
თუ ატრიბუტი შეიცვალა, ძველი row 'იხურება' (is_current=False),
ახალი row ემატება (is_current=True) — ისტორია არასდროს იშლება.
"""


def scd2_upsert(existing_rows: list, new_version: dict, key_field: str, tracked_fields: list, effective_date: str) -> list:
    """
    SCD Type 2 upsert:
    - თუ key_field-ის მიხედვით row არ არსებობს → პირველი ვერსია ემატება.
    - თუ არსებობს და tracked_fields არ შეცვლილა → არაფერი იცვლება.
    - თუ არსებობს და tracked_fields შეიცვალა → ძველი row იხურება
      (is_current=False, valid_to=effective_date), ახალი ემატება
      (is_current=True, valid_from=effective_date).
    """
    key_value = new_version[key_field]
    current_row = next(
        (r for r in existing_rows if r[key_field] == key_value and r.get("is_current")), None
    )

    if current_row is None:
        new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
        return existing_rows + [new_row]

    changed = any(current_row.get(f) != new_version.get(f) for f in tracked_fields)
    if not changed:
        return existing_rows

    updated_rows = [
        {**r, "valid_to": effective_date, "is_current": False} if r is current_row else r
        for r in existing_rows
    ]
    new_row = {**new_version, "valid_from": effective_date, "valid_to": None, "is_current": True}
    return updated_rows + [new_row]
