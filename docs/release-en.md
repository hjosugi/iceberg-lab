<!-- i18n: language-switcher -->
[English](release-en.md) | [日本語](release-ja.md)

# Release guide

## Local package

```bash
make package
```

Output:

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

`.github/workflows/release.yml` will attach the ZIP and SHA256 to the GitHub Release.

## Verify SHA256

```bash
VERSION="$(cat VERSION)"
shasum -a 256 "dist/iceberg-r2-online-lab-v${VERSION}.zip"
cat "dist/iceberg-r2-online-lab-v${VERSION}.zip.sha256"
```