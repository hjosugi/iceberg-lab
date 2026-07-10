# Troubleshooting

## `Missing required environment variables`

`.env` がないか、値が空です。

```bash
cp .env.example .env
```

以下を埋めます。

```bash
ICEBERG_CATALOG_URI=
ICEBERG_WAREHOUSE=
ICEBERG_TOKEN=
```

## `ModuleNotFoundError`

package が install されていません。

```bash
python -m pip install -e ".[dev]"
```

## Cloudflare 403

よくある原因:

- token が間違っている
- token scope に R2 Data Catalog permission がない
- token scope に R2 storage permission がない
- warehouse / catalog URI が違う

## DuckDB attach error

DuckDB の extension を更新します。

```sql
UPDATE EXTENSIONS;
LOAD iceberg;
```

## Table already exists

この lab の `create` は既存 table を再利用します。
完全に作り直したい場合だけ drop します。

```bash
iceberg-r2-lab drop-table --yes
iceberg-r2-lab create
```

## Cost が心配

- [R2 Data Catalog pricing](https://developers.cloudflare.com/r2/data-catalog/platform/pricing/) と [R2 pricing](https://developers.cloudflare.com/r2/pricing/) で最新の無料枠と従量課金を確認する
- 大量 append しない
- sample data は数行にする
- 不要なら automatic compaction / snapshot expiration を有効にしない
- 検証後は table / catalog / bucket を cleanup する
- Codespaces は使い終わったら stop する
