param(
  [string]$BucketName = $(if ($env:R2_BUCKET_NAME) { $env:R2_BUCKET_NAME } else { "iceberg-lab" })
)

Write-Host "Bucket: $BucketName"
Write-Host ""

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
  Write-Error "npx is required. Install Node.js first."
  exit 1
}

Write-Host "1) Login to Cloudflare"
npx wrangler@latest login

Write-Host ""
Write-Host "2) Create R2 bucket"
npx wrangler@latest r2 bucket create $BucketName

Write-Host ""
Write-Host "3) Enable R2 Data Catalog"
npx wrangler@latest r2 bucket catalog enable $BucketName

Write-Host ""
Write-Host "Next:"
Write-Host "  Copy Catalog URI and Warehouse name."
Write-Host "  Create R2 API token."
Write-Host "  Copy .env.example to .env."
Write-Host "  Run: make doctor; make create; make append; make read"
