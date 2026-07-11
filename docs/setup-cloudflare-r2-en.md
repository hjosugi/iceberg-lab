<!-- i18n: language-switcher -->
[English](setup-cloudflare-r2-en.md) | [日本語](setup-cloudflare-r2-ja.md)

# Cloudflare R2 Data Catalog setup

## Purpose

Enable the Iceberg catalog on the Cloudflare R2 bucket so that it can be accessed from PyIceberg / DuckDB.

## 1. Wrangler login

```bash
npx wrangler@latest login
```

## 2. Create Bucket

```bash
npx wrangler@latest r2 bucket create iceberg-lab
```

## 3. Enable Data Catalog

```bash
npx wrangler@latest r2 bucket catalog enable iceberg-lab
```

This output will display the `Catalog URI` and `Warehouse name`.

## 4. Create Token

Create an R2 API token in the Cloudflare dashboard.

For lab use, starting with `Admin Read & Write` is the easiest. For long-term operations or shared repos, please create a token limited to the specific bucket / catalog.

## 5. `.env`

```bash
cp .env.example .env
```

```bash
ICEBERG_CATALOG_URI=https://...
ICEBERG_WAREHOUSE=...
ICEBERG_TOKEN=...
```

## 6. Connection Check

```bash
make doctor
make doctor ARGS=--connect
```

Or:

```bash
iceberg-r2-lab doctor --connect
```