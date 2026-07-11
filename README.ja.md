<!-- i18n: language-switcher -->
[English](README.md) | [日本語](README.ja.md)

# Iceberg R2 オンラインラボ

Cloudflare R2 Data Catalog を使って、ほぼ固定費なしで Apache Iceberg をオンラインで試すための最小プロジェクトです。

```text
クライアントデバイス
  - Mac / Windows / Linux
  - GitHub Codespaces
  - iPadブラウザ + Codespaces
  - DuckDB CLI
  - PyIcebergスクリプト
        |
        | Iceberg REST Catalog API
        v
Cloudflare R2 Data Catalog
        |
        v
Cloudflare R2バケット
  - Icebergメタデータ
  - Parquetデータファイル
```

## 何ができるか

- Cloudflare R2バケット上にIcebergテーブルを作成
- PyIcebergからテーブルの作成・追加・読み取り
- DuckDBから同じIceberg REST Catalogにアタッチして読み取り
- 複数端末から同じ `Catalog URI`、`Warehouse`、`Token` で同じテーブルにアクセス
- GitHub ActionsでリリースZIPを自動生成
- GitHub Codespaces / Docker / ローカル仮想環境のいずれでも動作

## 最安にする考え方

固定のVMを持たない構成にします。

```text
ストレージ + カタログ: Cloudflare R2 + R2 Data Catalog
計算資源: 必要な時だけローカルPC / GitHub Codespaces / DuckDB / Python
```

Cloudflare R2 Data CatalogはR2バケットに組み込まれたマネージドApache Icebergカタログです。標準のIceberg REST Catalogインターフェースを公開しているため、PyIcebergやDuckDBなどから接続可能です。

Data Catalogのカタログ操作、コンパクション、R2ストレージ/操作には無料枠と従量課金があります。料金や無料枠は変更される可能性があるため、実行前に [R2 Data Catalogの料金](https://developers.cloudflare.com/r2/data-catalog/platform/pricing/) と [R2の料金](https://developers.cloudflare.com/r2/pricing/) を確認してください。

## 前提条件

- Cloudflareアカウント
- R2サブスクリプション
- Python 3.10以降
- Node.js / npm
- 任意：Docker
- 任意：GitHub Codespaces

## 1. R2バケットとData Catalogの作成

```bash
npx wrangler@latest login

npx wrangler@latest r2 bucket create iceberg-lab

npx wrangler@latest r2 bucket catalog enable iceberg-lab
```

実行後に表示される値を控えます。

```text
カタログURI
ワークスペース名
```

ダッシュボードから作成する場合は、R2 Data Catalogの画面でカタログを作成し、詳細ページに表示される `Catalog URI` と `Warehouse name` を使用します。

## 2. APIトークンの作成

CloudflareダッシュボードでR2 APIトークンを作成します。

必要な権限:

- R2 Data Catalogの読み書き
- R2ストレージの読み書き

最初のラボでは `Admin Read & Write` 相当の権限で始めるのが簡単です。ただし、共有リポジトリには絶対にトークンをコミットしないでください。

## 3. `.env` ファイルの作成

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

## 4. ローカルで実行

### venv + pip

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### uvを使う場合

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## 5. PyIcebergでテーブルを作成・読み取り

```bash
iceberg-r2-lab doctor

iceberg-r2-lab create
iceberg-r2-lab append --batch 1
iceberg-r2-lab read --limit 20
iceberg-r2-lab list
```

同じ処理はMakefileからも呼び出せます。

```bash
make doctor
make create
make append
make read
make list
```

## 6. DuckDBから読む

DuckDBで使うアタッチSQLを生成します。

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

生成されたSQLにはトークン値は含まれません。.envをシェル環境にエクスポートしてからDuckDBを起動します。

```bash
set -a
source .env
set +a
duckdb
```

DuckDB内で実行します。

```sql
.read .generated/duckdb_attach.sql

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
```

テンプレートSQLはここにもあります。

```text
examples/duckdb/attach_r2_template.sql
```

## 7. Dockerで実行

```bash
docker compose build
docker compose run --rm lab iceberg-r2-lab doctor
docker compose run --rm lab iceberg-r2-lab create
docker compose run --rm lab iceberg-r2-lab append
docker compose run --rm lab iceberg-r2-lab read
```

## 8. GitHub Codespacesで使う

1. このZIPをGitHubリポジトリにアップロード / プッシュ
2. Codespacesを開く
3. Codespacesのシークレットに以下を追加
   - `ICEBERG_CATALOG_URI`
   - `ICEBERG_WAREHOUSE`
   - `ICEBERG_TOKEN`
4. ターミナルで実行

```bash
python -m pip install -e ".[dev]"
iceberg-r2-lab doctor
iceberg-r2-lab read
```

iPadからでもCodespacesのブラウザターミナルで同じテーブルにアクセス可能です。

## 9. リリースZIPの作成

ローカルで作成する場合:

```bash
make package
```

出力:

```text
dist/iceberg-r2-online-lab-v1.0.1.zip
dist/iceberg-r2-online-lab-v1.0.1.zip.sha256
```

GitHub Actionsでリリースする場合:

```bash
VERSION="$(cat VERSION)"
git tag "v${VERSION}"
git push origin "v${VERSION}"
```

`.github/workflows/release.yml`がリリースアセットとしてZIPとSHA256を添付します。

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

## クリーンアップ

検証用テーブルを削除する場合:

```bash
iceberg-r2-lab drop-table --yes
```

カタログ自体を停止する場合:

```bash
npx wrangler@latest r2 bucket catalog disable iceberg-lab
```

バケットを削除する場合は、CloudflareダッシュボードまたはWranglerで中身を確認してから行ってください。

## セキュリティ

`.env`、`.generated/`、トークン、資格情報はコミットしないでください。

```bash
git status
```

で`.env`が表示されないことを確認してください。

## 参考リンク

- Cloudflare R2 Data Catalog: https://developers.cloudflare.com/r2/data-catalog/
- Cloudflare R2 Data Catalog管理: https://developers.cloudflare.com/r2/data-catalog/manage-catalogs/
- PyIceberg: https://py.iceberg.apache.org/
- DuckDB Iceberg RESTカタログ: https://duckdb.org/docs/lts/core_extensions/iceberg/iceberg_rest_catalogs.html
- GitHubリリース: https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases