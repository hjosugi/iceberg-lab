from __future__ import annotations

from typing import Any

from iceberg_r2_lab.settings import Settings


def connect_catalog(settings: Settings) -> Any:
    """Create a PyIceberg REST catalog client.

    Import is intentionally inside the function so `doctor` can run even if
    dependencies are not installed yet.
    """
    from pyiceberg.catalog.rest import RestCatalog

    return RestCatalog(
        name=settings.catalog_name,
        uri=settings.catalog_uri,
        warehouse=settings.warehouse,
        token=settings.token,
    )


def ensure_namespace(catalog: Any, namespace: str) -> None:
    catalog.create_namespace_if_not_exists(namespace)


def ensure_table(catalog: Any, settings: Settings, schema: Any) -> Any:
    identifier = settings.table_identifier
    if catalog.table_exists(identifier):
        return catalog.load_table(identifier)

    return catalog.create_table(
        identifier=identifier,
        schema=schema,
        properties={
            "format-version": "2",
            "write.format.default": "parquet",
        },
    )


def load_table(catalog: Any, settings: Settings) -> Any:
    return catalog.load_table(settings.table_identifier)
