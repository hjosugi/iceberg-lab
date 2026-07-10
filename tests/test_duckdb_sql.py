from iceberg_r2_lab.duckdb_sql import generate_attach_sql
from iceberg_r2_lab.settings import Settings


def test_generate_attach_sql_escapes_token():
    settings = Settings(
        catalog_uri="https://example.com/catalog",
        warehouse="warehouse",
        token="abc'def",
    )

    sql = generate_attach_sql(settings)

    assert "CREATE SECRET" in sql
    assert "abc''def" in sql
    assert "ATTACH 'warehouse' AS r2_iceberg" in sql
