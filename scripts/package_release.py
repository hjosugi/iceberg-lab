from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import zipfile


EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "build",
    "dist",
    ".generated",
}

EXCLUDE_FILES = {
    ".env",
}


def should_include(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return False
    if path.name in EXCLUDE_FILES:
        return False
    if path.name.startswith(".env.") and path.name != ".env.example":
        return False
    if path.suffix in {".pyc", ".pyo"}:
        return False
    return True


def build_zip(root: Path, version: str) -> Path:
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    zip_path = dist / f"iceberg-r2-online-lab-v{version}.zip"
    prefix = f"iceberg-r2-online-lab-v{version}"

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_symlink() or not path.is_file():
                continue
            rel = path.relative_to(root)
            if not should_include(rel):
                continue
            archive.write(path, Path(prefix) / rel)

    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sha_path = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sha_path.write_text(f"{digest}  {zip_path.name}\n", encoding="utf-8")

    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=(Path("VERSION").read_text(encoding="utf-8").strip()))
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    zip_path = build_zip(root, args.version)
    print(zip_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
