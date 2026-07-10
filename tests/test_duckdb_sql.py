import pytest

from iceberg_r2_lab.duckdb_sql import generate_attach_sql, sql_identifier
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
    assert "INSTALL httpfs;" in sql
    assert "LOAD httpfs;" in sql
    assert "ATTACH 'warehouse' AS \"r2_iceberg\"" in sql
    assert "SECRET r2_iceberg_secret" in sql


def test_generate_attach_sql_quotes_identifiers():
    settings = Settings(
        catalog_uri="https://example.com/catalog",
        warehouse="warehouse",
        token="token",
        namespace='team.analytics"daily',
        table="people-import",
        duckdb_catalog_alias="r2-catalog",
    )

    sql = generate_attach_sql(settings)

    assert 'CREATE SCHEMA IF NOT EXISTS "r2-catalog"."team.analytics""daily";' in sql
    assert 'USE "r2-catalog"."team.analytics""daily";' in sql
    assert (
        '-- SELECT * FROM "r2-catalog"."team.analytics""daily"."people-import" LIMIT 20;'
        in sql
    )
    assert "SUPPORT_NESTED_NAMESPACES true" in sql


def test_sql_identifier_rejects_an_empty_value():
    with pytest.raises(ValueError, match="must not be empty"):
        sql_identifier("")
