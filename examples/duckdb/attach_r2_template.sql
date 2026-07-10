-- Replace placeholders before running.
-- Do not commit a filled-in version of this file.

INSTALL iceberg;
LOAD iceberg;

INSTALL httpfs;
LOAD httpfs;

CREATE SECRET r2_iceberg_secret (
    TYPE iceberg,
    TOKEN '<ICEBERG_TOKEN>'
);

ATTACH '<ICEBERG_WAREHOUSE>' AS r2_iceberg (
    TYPE iceberg,
    SECRET r2_iceberg_secret,
    ENDPOINT '<ICEBERG_CATALOG_URI>',
    SUPPORT_NESTED_NAMESPACES true
);

CREATE SCHEMA IF NOT EXISTS r2_iceberg.demo;
USE r2_iceberg.demo;

SHOW ALL TABLES;

SELECT *
FROM r2_iceberg.demo.people
LIMIT 20;
