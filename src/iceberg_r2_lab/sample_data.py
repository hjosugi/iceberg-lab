from __future__ import annotations

from datetime import datetime, timezone


def people_rows(batch: int = 1) -> list[dict[str, object]]:
    """Return deterministic sample rows for the lab."""
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    base_id = batch * 1000
    return [
        {
            "id": base_id + 1,
            "name": "Alice",
            "team": "data",
            "score": 80.0 + batch,
            "ingested_at": now,
        },
        {
            "id": base_id + 2,
            "name": "Bob",
            "team": "platform",
            "score": 92.5 + batch,
            "ingested_at": now,
        },
        {
            "id": base_id + 3,
            "name": "Carol",
            "team": "analytics",
            "score": 88.0 + batch,
            "ingested_at": now,
        },
    ]


def people_arrow_table(batch: int = 1):
    import pyarrow as pa

    schema = pa.schema(
        [
            ("id", pa.int64()),
            ("name", pa.string()),
            ("team", pa.string()),
            ("score", pa.float64()),
            ("ingested_at", pa.string()),
        ]
    )
    return pa.Table.from_pylist(people_rows(batch), schema=schema)
