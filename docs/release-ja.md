# Release guide

## Local package

```bash
make package
```

出力:

```text
dist/iceberg-r2-online-lab-v1.0.1.zip
dist/iceberg-r2-online-lab-v1.0.1.zip.sha256
```

## GitHub release

```bash
VERSION="$(cat VERSION)"
git tag "v${VERSION}"
git push origin "v${VERSION}"
```

`.github/workflows/release.yml` が ZIP と SHA256 を GitHub Release に添付します。

## Verify SHA256

```bash
VERSION="$(cat VERSION)"
shasum -a 256 "dist/iceberg-r2-online-lab-v${VERSION}.zip"
cat "dist/iceberg-r2-online-lab-v${VERSION}.zip.sha256"
```
