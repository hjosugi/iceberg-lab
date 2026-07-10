from iceberg_r2_lab.settings import load_settings


def test_load_settings_from_environment(monkeypatch):
    monkeypatch.setenv("ICEBERG_CATALOG_URI", "https://example.com/catalog")
    monkeypatch.setenv("ICEBERG_WAREHOUSE", "warehouse")
    monkeypatch.setenv("ICEBERG_TOKEN", "secret-token")
    monkeypatch.setenv("ICEBERG_NAMESPACE", "demo")
    monkeypatch.setenv("ICEBERG_TABLE", "people")

    settings = load_settings(strict=True)

    assert settings.catalog_uri == "https://example.com/catalog"
    assert settings.warehouse == "warehouse"
    assert settings.token == "secret-token"
    assert settings.table_identifier == ("demo", "people")
    assert settings.table_identifier_string == "demo.people"


def test_load_settings_without_required_env(monkeypatch):
    for key in ("ICEBERG_CATALOG_URI", "ICEBERG_WAREHOUSE", "ICEBERG_TOKEN"):
        monkeypatch.delenv(key, raising=False)

    settings = load_settings(strict=False)

    assert settings.catalog_uri == ""
    assert settings.warehouse == ""
    assert settings.token == ""
