<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Iceberg R2 Online Lab

A minimal project for trying Apache Iceberg online with the Cloudflare R2 Data Catalog, at almost no fixed cost.

```text
Client devices
  - Mac / Windows / Linux
  - GitHub Codespaces
  - iPad browser + Codespaces
  - DuckDB CLI
  - PyIceberg script
        |
        | Iceberg REST Catalog API
        v
Cloudflare R2 Data Catalog
        |
        v
Cloudflare R2 bucket
  - Iceberg metadata
  - Parquet data files
```

## What you can do

- Create an Iceberg table on a Cloudflare R2 bucket
- Create, append to, and read the table from PyIceberg
- Attach DuckDB to the same Iceberg REST Catalog and read from it
- Reach the same table from several machines using one `Catalog URI`, `Warehouse`, and `Token`
- Build a release ZIP automatically with GitHub Actions
- Run it under GitHub Codespaces, Docker, or a local venv

## How this stays cheap

The setup keeps no permanently running VM.

```text
Storage + Catalog: Cloudflare R2 + R2 Data Catalog
Compute: local PC / GitHub Codespaces / DuckDB / Python, only when needed
```

The Cloudflare R2 Data Catalog is a managed Apache Iceberg catalog built into an R2 bucket. It exposes the standard Iceberg REST Catalog interface, so clients such as PyIceberg and DuckDB can connect to it.

Data Catalog catalog operations, compaction, and R2 storage and operations each have a free allowance and usage-based pricing beyond it. Prices and free allowances change, so check [R2 Data Catalog pricing](https://developers.cloudflare.com/r2/data-catalog/platform/pricing/) and [R2 pricing](https://developers.cloudflare.com/r2/pricing/) before you run anything.

## Prerequisites

- Cloudflare account
- R2 subscription
- Python 3.10+
- Node.js / npm
- Optional: Docker
- Optional: GitHub Codespaces

## 1. Create the R2 bucket and Data Catalog

```bash
npx wrangler@latest login

npx wrangler@latest r2 bucket create iceberg-lab

npx wrangler@latest r2 bucket catalog enable iceberg-lab
```

Note down the values printed afterwards.

```text
Catalog URI
Warehouse name
```

To do this from the dashboard instead, create a catalog on the R2 Data Catalog screen and use the `Catalog URI` and `Warehouse name` shown on its detail page.

## 2. Create an API token

Create an R2 API token in the Cloudflare dashboard.

What it needs to cover:

- R2 Data Catalog read/write
- R2 storage read/write

For a first lab, starting with the equivalent of `Admin Read & Write` is simplest. Never commit the token to a shared repository.

## 3. Create `.env`

```bash
cp .env.example .env
```

Edit `.env`.

```bash
ICEBERG_CATALOG_URI=https://...
ICEBERG_WAREHOUSE=...
ICEBERG_TOKEN=...
ICEBERG_NAMESPACE=demo
ICEBERG_TABLE=people
ICEBERG_CATALOG_NAME=r2
DUCKDB_CATALOG_ALIAS=r2_iceberg
```

## 4. Run it locally

### venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Using uv

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## 5. Create and read a table with PyIceberg

```bash
iceberg-r2-lab doctor

iceberg-r2-lab create
iceberg-r2-lab append --batch 1
iceberg-r2-lab read --limit 20
iceberg-r2-lab list
```

The same steps are available through the Makefile.

```bash
make doctor
make create
make append
make read
make list
```

## 6. Read from DuckDB

Generate the attach SQL for DuckDB.

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

The generated SQL does not contain the token value. Export `.env` into the shell environment, then start DuckDB.

```bash
set -a
source .env
set +a
duckdb
```

Run this inside DuckDB.

```sql
.read .generated/duckdb_attach.sql

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
```

A template SQL file is also kept here.

```text
examples/duckdb/attach_r2_template.sql
```

## 7. Run it with Docker

```bash
docker compose build
docker compose run --rm lab iceberg-r2-lab doctor
docker compose run --rm lab iceberg-r2-lab create
docker compose run --rm lab iceberg-r2-lab append
docker compose run --rm lab iceberg-r2-lab read
```

## 8. Use it from GitHub Codespaces

1. Upload or push this ZIP to a GitHub repo
2. Open GitHub Codespaces
3. Add the following to the Codespaces secrets
   - `ICEBERG_CATALOG_URI`
   - `ICEBERG_WAREHOUSE`
   - `ICEBERG_TOKEN`
4. Run it in the terminal

```bash
python -m pip install -e ".[dev]"
iceberg-r2-lab doctor
iceberg-r2-lab read
```

The same table is reachable from an iPad too, through the Codespaces browser terminal.

## 9. Build a release ZIP

Building locally:

```bash
make package
```

Output:

```text
dist/iceberg-r2-online-lab-v1.0.1.zip
dist/iceberg-r2-online-lab-v1.0.1.zip.sha256
```

Releasing through GitHub Actions:

```bash
VERSION="$(cat VERSION)"
git tag "v${VERSION}"
git push origin "v${VERSION}"
```

`.github/workflows/release.yml` attaches the ZIP and its SHA256 as release assets.

## Directory layout

```text
.
├── .devcontainer/
├── .github/workflows/
├── docs/
├── examples/
│   ├── duckdb/
│   ├── pandas/
│   └── pyiceberg/
├── scripts/
├── src/iceberg_r2_lab/
├── tests/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
└── VERSION
```

## Commands you will use often

```bash
make install
make doctor
make create
make append
make read
make list
make duckdb-sql
make test
make package
```

## Cleanup

To drop the test table:

```bash
iceberg-r2-lab drop-table --yes
```

To turn the catalog itself off:

```bash
npx wrangler@latest r2 bucket catalog disable iceberg-lab
```

Before deleting the bucket, check its contents from the Cloudflare dashboard or with Wrangler.

## Security

Do not commit `.env`, `.generated/`, tokens, or credentials.

```bash
git status
```

Confirm that `.env` does not appear in the output.

## Reference links

- Cloudflare R2 Data Catalog: https://developers.cloudflare.com/r2/data-catalog/
- Cloudflare R2 Data Catalog management: https://developers.cloudflare.com/r2/data-catalog/manage-catalogs/
- PyIceberg: https://py.iceberg.apache.org/
- DuckDB Iceberg REST Catalogs: https://duckdb.org/docs/lts/core_extensions/iceberg/iceberg_rest_catalogs.html
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
