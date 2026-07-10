# Cloudflare R2 Data Catalog setup

## 目的

Cloudflare R2 bucket に Iceberg catalog を有効化し、PyIceberg / DuckDB から接続できるようにします。

## 1. Wrangler login

```bash
npx wrangler@latest login
```

## 2. Bucket 作成

```bash
npx wrangler@latest r2 bucket create iceberg-lab
```

## 3. Data Catalog 有効化

```bash
npx wrangler@latest r2 bucket catalog enable iceberg-lab
```

この出力に `Catalog URI` と `Warehouse name` が表示されます。

## 4. Token 作成

Cloudflare dashboard で R2 API token を作ります。

lab 用なら最初は `Admin Read & Write` が一番簡単です。
長期運用や共有 repo では、対象 bucket / catalog に絞った token にしてください。

## 5. `.env`

```bash
cp .env.example .env
```

```bash
ICEBERG_CATALOG_URI=https://...
ICEBERG_WAREHOUSE=...
ICEBERG_TOKEN=...
```

## 6. 接続確認

```bash
make doctor
make doctor ARGS=--connect
```

または:

```bash
iceberg-r2-lab doctor --connect
```
