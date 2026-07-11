<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Iceberg R2 Online Lab

Cloudflare R2 Data Catalog を使って、ほぼ固定費なしで Apache Iceberg を online に試すための最小プロジェクトです。

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

## 何ができるか

- Cloudflare R2 bucket 上に Iceberg table を作る
- PyIceberg から table 作成・append・read する
- DuckDB から同じ Iceberg REST Catalog に attach して読む
- 複数端末から同じ `Catalog URI`, `Warehouse`, `Token` で同じ table にアクセスする
- GitHub Actions で release ZIP を自動生成する
- GitHub Codespaces / Docker / local venv のどれでも動かす

## 最安にする考え方

固定の VM を持たない構成にします。

```text
Storage + Catalog: Cloudflare R2 + R2 Data Catalog
Compute: 必要な時だけ local PC / GitHub Codespaces / DuckDB / Python
```

Cloudflare R2 Data Catalog は R2 bucket に組み込まれた managed Apache Iceberg catalog です。標準 Iceberg REST Catalog interface を公開するため、PyIceberg や DuckDB などから接続できます。

Data Catalog の catalog operation、compaction、R2 storage / operation には無料枠と従量課金があります。金額や無料枠は変更されるため、実行前に [R2 Data Catalog pricing](https://developers.cloudflare.com/r2/data-catalog/platform/pricing/) と [R2 pricing](https://developers.cloudflare.com/r2/pricing/) を確認してください。

## 前提

- Cloudflare account
- R2 subscription
- Python 3.10+
- Node.js / npm
- 任意: Docker
- 任意: GitHub Codespaces

## 1. R2 bucket と Data Catalog を作る

```bash
npx wrangler@latest login

npx wrangler@latest r2 bucket create iceberg-lab

npx wrangler@latest r2 bucket catalog enable iceberg-lab
```

実行後に表示される値を控えます。

```text
Catalog URI
Warehouse name
```

Dashboard から作る場合は、R2 Data Catalog の画面で catalog を作成し、detail page に表示される `Catalog URI` と `Warehouse name` を使います。

## 2. API token を作る

Cloudflare dashboard で R2 API token を作ります。

必要な考え方:

- R2 Data Catalog read/write
- R2 storage read/write

最初の lab では `Admin Read & Write` 相当で始めるのが簡単です。ただし、共有リポジトリには絶対に token を commit しないでください。

## 3. `.env` を作る

```bash
cp .env.example .env
```

`.env` を編集します。

```bash
ICEBERG_CATALOG_URI=https://...
ICEBERG_WAREHOUSE=...
ICEBERG_TOKEN=...
ICEBERG_NAMESPACE=demo
ICEBERG_TABLE=people
ICEBERG_CATALOG_NAME=r2
DUCKDB_CATALOG_ALIAS=r2_iceberg
```

## 4. local で実行する

### venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### uv を使う場合

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## 5. PyIceberg で table を作って読む

```bash
iceberg-r2-lab doctor

iceberg-r2-lab create
iceberg-r2-lab append --batch 1
iceberg-r2-lab read --limit 20
iceberg-r2-lab list
```

同じ処理は Makefile からも呼べます。

```bash
make doctor
make create
make append
make read
make list
```

## 6. DuckDB から読む

DuckDB で使う attach SQL を生成します。

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

生成SQLにtoken値は含まれません。`.env`をshell環境へexportしてからDuckDBを起動します。

```bash
set -a
source .env
set +a
duckdb
```

DuckDB 内で実行します。

```sql
.read .generated/duckdb_attach.sql

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
```

template SQL はここにもあります。

```text
examples/duckdb/attach_r2_template.sql
```

## 7. Docker で実行する

```bash
docker compose build
docker compose run --rm lab iceberg-r2-lab doctor
docker compose run --rm lab iceberg-r2-lab create
docker compose run --rm lab iceberg-r2-lab append
docker compose run --rm lab iceberg-r2-lab read
```

## 8. GitHub Codespaces で使う

1. この ZIP を GitHub repo に upload / push
2. GitHub Codespaces を開く
3. Codespaces secrets に以下を追加
   - `ICEBERG_CATALOG_URI`
   - `ICEBERG_WAREHOUSE`
   - `ICEBERG_TOKEN`
4. Terminal で実行

```bash
python -m pip install -e ".[dev]"
iceberg-r2-lab doctor
iceberg-r2-lab read
```

iPad からでも Codespaces のブラウザ terminal で同じ table にアクセスできます。

## 9. release ZIP を作る

local で作る場合:

```bash
make package
```

出力:

```text
dist/iceberg-r2-online-lab-v1.0.1.zip
dist/iceberg-r2-online-lab-v1.0.1.zip.sha256
```

GitHub Actions で release する場合:

```bash
VERSION="$(cat VERSION)"
git tag "v${VERSION}"
git push origin "v${VERSION}"
```

`.github/workflows/release.yml` が release asset として ZIP と SHA256 を添付します。

## ディレクトリ構成

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

## よく使うコマンド

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

## cleanup

検証 table を消す場合:

```bash
iceberg-r2-lab drop-table --yes
```

catalog 自体を止める場合:

```bash
npx wrangler@latest r2 bucket catalog disable iceberg-lab
```

bucket を削除する場合は、Cloudflare dashboard または Wrangler で中身を確認してから行ってください。

## Security

`.env`, `.generated/`, token, credential は commit しないでください。

```bash
git status
```

で `.env` が表示されないことを確認してください。

## 参考リンク

- Cloudflare R2 Data Catalog: https://developers.cloudflare.com/r2/data-catalog/
- Cloudflare R2 Data Catalog management: https://developers.cloudflare.com/r2/data-catalog/manage-catalogs/
- PyIceberg: https://py.iceberg.apache.org/
- DuckDB Iceberg REST Catalogs: https://duckdb.org/docs/lts/core_extensions/iceberg/iceberg_rest_catalogs.html
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
