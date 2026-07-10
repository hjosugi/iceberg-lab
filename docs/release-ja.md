# Release guide

## Local package

```bash
make package
```

出力:

```text
dist/iceberg-r2-online-lab-v1.0.0.zip
dist/iceberg-r2-online-lab-v1.0.0.zip.sha256
```

## GitHub release

```bash
git tag v1.0.0
git push origin v1.0.0
```

`.github/workflows/release.yml` が ZIP と SHA256 を GitHub Release に添付します。

## Verify SHA256

```bash
shasum -a 256 dist/iceberg-r2-online-lab-v1.0.0.zip
cat dist/iceberg-r2-online-lab-v1.0.0.zip.sha256
```
