from iceberg_r2_lab.catalog import connect_catalog, ensure_namespace, ensure_table
from iceberg_r2_lab.sample_data import people_arrow_table
from iceberg_r2_lab.settings import load_settings


def main() -> None:
    settings = load_settings()
    catalog = connect_catalog(settings)

    ensure_namespace(catalog, settings.namespace)

    data = people_arrow_table(batch=10)
    table = ensure_table(catalog, settings, data.schema)
    table.append(data)

    print(table.scan(limit=20).to_arrow().to_pandas())


if __name__ == "__main__":
    main()
