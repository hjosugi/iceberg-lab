from iceberg_r2_lab.sample_data import people_rows


def test_people_rows_are_deterministic_ids():
    rows = people_rows(batch=7)

    assert [row["id"] for row in rows] == [7001, 7002, 7003]
    assert rows[0]["name"] == "Alice"
