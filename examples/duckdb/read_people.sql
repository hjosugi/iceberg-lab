-- Run `.read .generated/duckdb_attach.sql` first.

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
