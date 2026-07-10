# Architecture

## 構成

```text
Client
  |
  | Iceberg REST Catalog API
  v
Cloudflare R2 Data Catalog
  |
  v
Cloudflare R2 bucket
```

## 役割

| Component | Role |
|---|---|
| Apache Iceberg | Table format |
| R2 bucket | Object storage for Parquet and Iceberg metadata |
| R2 Data Catalog | Current metadata pointer and table namespace management |
| PyIceberg | Python client and writer |
| DuckDB | Lightweight SQL query engine |
| Codespaces | Browser-accessible compute |

## Interview 向け整理

Iceberg は database ではなく table format です。

Object storage には data files と metadata files が置かれます。
Catalog は table name から current metadata file への pointer を管理します。
Query engine は catalog から metadata を取得し、必要な Parquet files を読みます。

## なぜ安いか

compute を常時起動しないためです。
状態は R2 bucket と R2 Data Catalog に置き、compute は必要なときだけ使います。
