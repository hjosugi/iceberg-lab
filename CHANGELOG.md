# Changelog

## 1.0.1 - 2026-07-10

- Stop embedding R2 API tokens in generated DuckDB SQL
- Read `ICEBERG_TOKEN` from the DuckDB process environment
- Verify source version declarations and release tags agree

## 1.0.0

Initial release.

- Cloudflare R2 Data Catalog setup guide
- PyIceberg CLI
- DuckDB attach SQL generator
- Explicit DuckDB `httpfs`, named secret, and nested namespace support
- Docker and Codespaces support
- GitHub Actions CI
- GitHub Actions release ZIP workflow
- Release packaging that excludes local secrets and symlinks
- Unit tests for settings, sample data, DuckDB SQL, and release packaging
