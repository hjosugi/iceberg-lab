-- Replace placeholders before running.
-- Do not commit a filled-in version of this file.

INSTALL iceberg;
LOAD iceberg;

CREATE SECRET r2_iceberg_secret (
    TYPE iceberg,
    TOKEN '<ICEBERG_TOKEN>'
);

ATTACH '<ICEBERG_WAREHOUSE>' AS r2_iceberg (
    TYPE iceberg,
    ENDPOINT '<ICEBERG_CATALOG_URI>'
);

CREATE SCHEMA IF NOT EXISTS r2_iceberg.demo;
USE r2_iceberg.demo;

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
