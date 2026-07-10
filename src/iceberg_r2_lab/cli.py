from __future__ import annotations

import argparse
import sys

from iceberg_r2_lab.catalog import connect_catalog, ensure_namespace, ensure_table, load_table
from iceberg_r2_lab.duckdb_sql import generate_attach_sql
from iceberg_r2_lab.sample_data import people_arrow_table
from iceberg_r2_lab.settings import ConfigurationError, env_report, load_settings


def print_env_report(strict: bool = False) -> int:
    try:
        settings = load_settings(strict=strict)
    except ConfigurationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        settings = load_settings(strict=False)
        code = 2
    else:
        code = 0

    print("Environment")
    print("-----------")
    for name, value, _ in env_report(settings):
        print(f"{name}={value}")

    print()
    print(f"Table: {settings.table_identifier_string}")
    return code


def cmd_doctor(args: argparse.Namespace) -> int:
    code = print_env_report(strict=False)

    settings = load_settings(strict=False)
    missing = not (settings.catalog_uri and settings.warehouse and settings.token)
    if missing:
        print()
        print("Status: missing Cloudflare R2 Data Catalog settings.")
        print("Next: copy .env.example to .env and fill ICEBERG_CATALOG_URI, ICEBERG_WAREHOUSE, ICEBERG_TOKEN.")
        return 2

    if args.connect:
        try:
            catalog = connect_catalog(settings)
            namespaces = catalog.list_namespaces()
        except Exception as exc:  # pragma: no cover - requires remote catalog
            print()
            print(f"Connection test failed: {exc}", file=sys.stderr)
            return 1

        print()
        print("Connection test: ok")
        print("Namespaces:")
        for ns in namespaces:
            print(f"  - {'.'.join(ns)}")

    print()
    print("Status: ready")
    return code


def cmd_create(_: argparse.Namespace) -> int:
    settings = load_settings()
    catalog = connect_catalog(settings)
    ensure_namespace(catalog, settings.namespace)

    sample = people_arrow_table(batch=0)
    table = ensure_table(catalog, settings, sample.schema)

    print(f"Created or loaded table: {settings.table_identifier_string}")
    print(f"Schema: {table.schema()}")
    return 0


def cmd_append(args: argparse.Namespace) -> int:
    settings = load_settings()
    catalog = connect_catalog(settings)
    ensure_namespace(catalog, settings.namespace)

    sample = people_arrow_table(batch=args.batch)
    table = ensure_table(catalog, settings, sample.schema)
    table.append(sample)

    print(f"Appended {sample.num_rows} rows to {settings.table_identifier_string}")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    settings = load_settings()
    catalog = connect_catalog(settings)
    table = load_table(catalog, settings)

    scan = table.scan(limit=args.limit) if args.limit else table.scan()
    arrow_table = scan.to_arrow()

    if args.format == "arrow":
        print(arrow_table)
    else:
        print(arrow_table.to_pandas().to_string(index=False))

    return 0


def cmd_list(_: argparse.Namespace) -> int:
    settings = load_settings()
    catalog = connect_catalog(settings)

    print("Namespaces")
    print("----------")
    namespaces = catalog.list_namespaces()
    for namespace in namespaces:
        print(".".join(namespace))

    print()
    print(f"Tables in {settings.namespace}")
    print("-" * (10 + len(settings.namespace)))
    if catalog.namespace_exists(settings.namespace):
        for table in catalog.list_tables(settings.namespace):
            print(".".join(table))
    else:
        print("<namespace does not exist>")

    return 0


def cmd_metadata(_: argparse.Namespace) -> int:
    settings = load_settings()
    catalog = connect_catalog(settings)
    table = load_table(catalog, settings)

    print(f"Table: {settings.table_identifier_string}")
    print(f"Location: {table.location()}")
    current = table.current_snapshot()
    print(f"Current snapshot: {current.snapshot_id if current else '<none>'}")

    snapshots = table.snapshots()
    print(f"Snapshot count: {len(snapshots)}")
    for snapshot in snapshots[-10:]:
        print(f"  - id={snapshot.snapshot_id} parent={snapshot.parent_snapshot_id}")
    return 0


def cmd_duckdb_sql(_: argparse.Namespace) -> int:
    settings = load_settings()
    print(generate_attach_sql(settings), end="")
    return 0


def cmd_drop_table(args: argparse.Namespace) -> int:
    settings = load_settings()
    if not args.yes:
        print("Refusing to drop table without --yes.", file=sys.stderr)
        return 2

    catalog = connect_catalog(settings)
    if catalog.table_exists(settings.table_identifier):
        catalog.drop_table(settings.table_identifier)
        print(f"Dropped table: {settings.table_identifier_string}")
    else:
        print(f"Table does not exist: {settings.table_identifier_string}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="iceberg-r2-lab",
        description="Low-cost Apache Iceberg lab on Cloudflare R2 Data Catalog.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="Check local environment.")
    doctor.add_argument("--connect", action="store_true", help="Also test remote catalog connection.")
    doctor.set_defaults(func=cmd_doctor)

    create = sub.add_parser("create", help="Create namespace and sample table if needed.")
    create.set_defaults(func=cmd_create)

    append = sub.add_parser("append", help="Append sample rows.")
    append.add_argument("--batch", type=int, default=1, help="Batch id used to generate sample row ids.")
    append.set_defaults(func=cmd_append)

    read = sub.add_parser("read", help="Read sample table.")
    read.add_argument("--limit", type=int, default=20)
    read.add_argument("--format", choices=("pandas", "arrow"), default="pandas")
    read.set_defaults(func=cmd_read)

    list_cmd = sub.add_parser("list", help="List namespaces and tables.")
    list_cmd.set_defaults(func=cmd_list)

    metadata = sub.add_parser("metadata", help="Show table location and recent snapshots.")
    metadata.set_defaults(func=cmd_metadata)

    duckdb_sql = sub.add_parser("duckdb-sql", help="Generate DuckDB attach SQL.")
    duckdb_sql.set_defaults(func=cmd_duckdb_sql)

    drop = sub.add_parser("drop-table", help="Drop the configured sample table.")
    drop.add_argument("--yes", action="store_true", help="Required confirmation.")
    drop.set_defaults(func=cmd_drop_table)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except ConfigurationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
