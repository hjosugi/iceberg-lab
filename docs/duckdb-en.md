<!-- i18n: language-switcher -->
[English](duckdb-en.md) | [日本語](duckdb-ja.md)

# Connecting DuckDB to Cloudflare R2 Data Catalog

## Generating SQL

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

The generated SQL does not embed the token value. Starting from DuckDB 1.3, use `getenv()` to read `ICEBERG_TOKEN` at runtime.

## DuckDB

Export the values from `.env` to the shell environment before starting DuckDB.

### bash / zsh

```bash
set -a
source .env
set +a
duckdb
```

### PowerShell

```powershell
$line = Get-Content .env | Where-Object { $_ -match '^ICEBERG_TOKEN=' }
$env:ICEBERG_TOKEN = $line.Split('=', 2)[1]
duckdb
```

By not writing the token value directly to the command line, the token literal will not remain in the shell history.

```sql
.read .generated/duckdb_attach.sql

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
```

## Manual Template

```sql
INSTALL iceberg;
LOAD iceberg;

INSTALL httpfs;
LOAD httpfs;

CREATE SECRET r2_iceberg_secret (
    TYPE iceberg,
    TOKEN getenv('ICEBERG_TOKEN')
);

ATTACH '<ICEBERG_WAREHOUSE>' AS r2_iceberg (
    TYPE iceberg,
    SECRET r2_iceberg_secret,
    ENDPOINT '<ICEBERG_CATALOG_URI>',
    SUPPORT_NESTED_NAMESPACES true
);
```

## Common Issues

### Failing to Attach

Update the Iceberg extension for DuckDB.

```sql
UPDATE EXTENSIONS;
LOAD iceberg;
LOAD httpfs;
```

### Risk of Token Leakage

The generated SQL does not include the token value. Please pass `ICEBERG_TOKEN` only to the DuckDB process environment. If you directly input a `CREATE SECRET` containing the token literal into the DuckDB CLI, it will remain in the history, so use `getenv()`.

### `getenv('ICEBERG_TOKEN')` is Empty

The Python CLI reads `.env`, but it is not automatically inherited by DuckDB started in a separate process. Please set the environment variable using the above bash / zsh or PowerShell steps before starting.