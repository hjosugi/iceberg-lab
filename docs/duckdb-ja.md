<!-- i18n: language-switcher -->
[English](duckdb-en.md) | [日本語](duckdb-ja.md)

# DuckDB から Cloudflare R2 Data Catalog に接続する

## SQL を生成

```bash
iceberg-r2-lab duckdb-sql > .generated/duckdb_attach.sql
```

生成SQLにはtoken値を埋め込みません。DuckDB 1.3以降の`getenv()`を使い、実行時に`ICEBERG_TOKEN`を読みます。

## DuckDB

`.env`の値をshell環境へexportしてからDuckDBを起動します。

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

token値をcommand lineへ直接書かないため、shell historyにもtoken literalを残しません。

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
    TOKEN getenv('ICEBERG_TOKEN')
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

生成SQLにはtoken値が入りません。`ICEBERG_TOKEN`はDuckDB processの環境だけに渡してください。
DuckDB CLIへtoken literalを含む`CREATE SECRET`を直接入力するとhistoryへ残るため、`getenv()`を使います。

### `getenv('ICEBERG_TOKEN')` が空になる

Python CLIは`.env`を読みますが、別processで起動したDuckDBには自動継承されません。上記のbash / zshまたはPowerShell手順で環境変数を設定してから起動してください。
