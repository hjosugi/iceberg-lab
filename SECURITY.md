# Security Policy

## Secrets

Never commit:

- `.env`
- Cloudflare API token
- R2 access keys
- DuckDB generated SQL containing tokens
- Any file under `.generated/`

## Token scope

For a quick lab, an R2 API token with read/write access is easy.
For shared or long-running use, create a narrower token for the specific bucket and catalog.

## Reporting

Open a private security advisory or contact the repository owner.
