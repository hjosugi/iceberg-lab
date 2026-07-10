# DuckDB から Cloudflare R2 Data Catalog に接続する

## SQL を生成

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

`.generated/duckdb_attach.sql` には token が入るため、commit しないでください。

## DuckDB

```bash
duckdb
```

```sql
.read .generated/duckdb_attach.sql

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
```

## 手動 template

```sql
INSTALL iceberg;
LOAD iceberg;

INSTALL httpfs;
LOAD httpfs;

CREATE SECRET r2_iceberg_secret (
    TYPE iceberg,
    TOKEN '<ICEBERG_TOKEN>'
);

ATTACH '<ICEBERG_WAREHOUSE>' AS r2_iceberg (
    TYPE iceberg,
    SECRET r2_iceberg_secret,
    ENDPOINT '<ICEBERG_CATALOG_URI>',
    SUPPORT_NESTED_NAMESPACES true
);
```

## よくある問題

### attach に失敗する

DuckDB の Iceberg extension を更新します。

```sql
UPDATE EXTENSIONS;
LOAD iceberg;
LOAD httpfs;
```

### token が漏れそう

生成済み SQL は `.generated/` に置きます。
`.generated/` は `.gitignore` に含まれています。
