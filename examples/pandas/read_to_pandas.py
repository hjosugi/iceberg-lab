from iceberg_r2_lab.catalog import connect_catalog, load_table
from iceberg_r2_lab.settings import load_settings


def main() -> None:
    settings = load_settings()
    catalog = connect_catalog(settings)
    table = load_table(catalog, settings)

    df = table.scan(limit=100).to_pandas()
    print(df)


if __name__ == "__main__":
    main()
