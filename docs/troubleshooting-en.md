<!-- i18n: language-switcher -->
[English](troubleshooting-en.md) | [日本語](troubleshooting-ja.md)

# Troubleshooting

## `Missing required environment variables`

The `.env` file is missing or the values are empty.

```bash
cp .env.example .env
```

Fill in the following.

```bash
ICEBERG_CATALOG_URI=
ICEBERG_WAREHOUSE=
ICEBERG_TOKEN=
```

## `ModuleNotFoundError`

The package is not installed.

```bash
python -m pip install -e ".[dev]"
```

## Cloudflare 403

Common causes:

- The token is incorrect
- The token scope does not have R2 Data Catalog permission
- The token scope does not have R2 storage permission
- The warehouse/catalog URI is incorrect

## DuckDB attach error

Update the DuckDB extension.

```sql
UPDATE EXTENSIONS;
LOAD iceberg;
```

## Table already exists

The `create` in this lab reuses existing tables. Only drop if you want to completely recreate it.

```bash
iceberg-r2-lab drop-table --yes
iceberg-r2-lab create
```

## Concerned about costs

- Check the latest free tier and pay-as-you-go pricing at [R2 Data Catalog pricing](https://developers.cloudflare.com/r2/data-catalog/platform/pricing/) and [R2 pricing](https://developers.cloudflare.com/r2/pricing/)
- Avoid large appends
- Keep sample data to a few rows
- Do not enable automatic compaction/snapshot expiration if not needed
- Clean up tables/catalogs/buckets after validation
- Stop Codespaces when done