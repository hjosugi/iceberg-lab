#!/usr/bin/env bash
set -euo pipefail

BUCKET_NAME="${1:-${R2_BUCKET_NAME:-iceberg-lab}}"

echo "Bucket: ${BUCKET_NAME}"
echo

if ! command -v npx >/dev/null 2>&1; then
  echo "ERROR: npx is required. Install Node.js first." >&2
  exit 1
fi

echo "1) Login to Cloudflare"
npx wrangler@latest login

echo
echo "2) Create R2 bucket"
npx wrangler@latest r2 bucket create "${BUCKET_NAME}" || true

echo
echo "3) Enable R2 Data Catalog"
npx wrangler@latest r2 bucket catalog enable "${BUCKET_NAME}"

cat <<'EOF'

Next:
  1. Copy the Catalog URI and Warehouse name from the output above.
  2. Create an R2 API token in Cloudflare dashboard.
  3. Copy .env.example to .env and fill:
       ICEBERG_CATALOG_URI
       ICEBERG_WAREHOUSE
       ICEBERG_TOKEN
  4. Run:
       make doctor
       make create
       make append
       make read

EOF
