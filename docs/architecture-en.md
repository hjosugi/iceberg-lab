<!-- i18n: language-switcher -->
[English](architecture-en.md) | [日本語](architecture-ja.md)

# Architecture

## Configuration

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

## Roles

| Component | Role |
|---|---|
| Apache Iceberg | Table format |
| R2 bucket | Object storage for Parquet and Iceberg metadata |
| R2 Data Catalog | Current metadata pointer and table namespace management |
| PyIceberg | Python client and writer |
| DuckDB | Lightweight SQL query engine |
| Codespaces | Browser-accessible compute |

## Organization for Interviews

Iceberg is not a database but a table format.

Object storage contains data files and metadata files.
The catalog manages the pointer from the table name to the current metadata file.
The query engine retrieves metadata from the catalog and reads the necessary Parquet files.

## Why It Is Cheap

It is because compute is not always running.
State is stored in the R2 bucket and R2 Data Catalog, and compute is used only when necessary.