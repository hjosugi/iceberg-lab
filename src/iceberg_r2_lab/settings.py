from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


class ConfigurationError(RuntimeError):
    """Raised when required environment variables are missing."""


@dataclass(frozen=True)
class Settings:
    catalog_uri: str
    warehouse: str
    token: str
    catalog_name: str = "r2"
    namespace: str = "demo"
    table: str = "people"
    duckdb_catalog_alias: str = "r2_iceberg"

    @property
    def table_identifier(self) -> tuple[str, ...]:
        return tuple(self.namespace.split(".")) + (self.table,)

    @property
    def table_identifier_string(self) -> str:
        return ".".join(self.table_identifier)


REQUIRED_ENV = ("ICEBERG_CATALOG_URI", "ICEBERG_WAREHOUSE", "ICEBERG_TOKEN")


def _load_dotenv(env_file: str | os.PathLike[str] = ".env") -> None:
    """Load .env if python-dotenv is installed."""
    path = Path(env_file)
    if not path.exists():
        return

    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv(path)


def load_settings(*, env_file: str | os.PathLike[str] = ".env", strict: bool = True) -> Settings:
    _load_dotenv(env_file)

    missing = [name for name in REQUIRED_ENV if not os.getenv(name)]
    if missing and strict:
        missing_list = ", ".join(missing)
        raise ConfigurationError(
            f"Missing required environment variables: {missing_list}. "
            "Copy .env.example to .env and fill in the values from Cloudflare R2 Data Catalog."
        )

    return Settings(
        catalog_uri=os.getenv("ICEBERG_CATALOG_URI", ""),
        warehouse=os.getenv("ICEBERG_WAREHOUSE", ""),
        token=os.getenv("ICEBERG_TOKEN", ""),
        catalog_name=os.getenv("ICEBERG_CATALOG_NAME", "r2"),
        namespace=os.getenv("ICEBERG_NAMESPACE", "demo"),
        table=os.getenv("ICEBERG_TABLE", "people"),
        duckdb_catalog_alias=os.getenv("DUCKDB_CATALOG_ALIAS", "r2_iceberg"),
    )


def env_report(settings: Settings) -> list[tuple[str, str, bool]]:
    """Return env var report as (name, display_value, is_secret)."""
    return [
        ("ICEBERG_CATALOG_URI", settings.catalog_uri or "<missing>", False),
        ("ICEBERG_WAREHOUSE", settings.warehouse or "<missing>", False),
        ("ICEBERG_TOKEN", _redact(settings.token), True),
        ("ICEBERG_CATALOG_NAME", settings.catalog_name, False),
        ("ICEBERG_NAMESPACE", settings.namespace, False),
        ("ICEBERG_TABLE", settings.table, False),
        ("DUCKDB_CATALOG_ALIAS", settings.duckdb_catalog_alias, False),
    ]


def _redact(value: str) -> str:
    if not value:
        return "<missing>"
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"
