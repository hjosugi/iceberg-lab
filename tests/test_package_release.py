from pathlib import Path
import runpy
import zipfile

import pytest


SCRIPT = Path(__file__).parents[1] / "scripts" / "package_release.py"
build_zip = runpy.run_path(str(SCRIPT), run_name="package_release")["build_zip"]


def archived_paths(zip_path: Path) -> set[str]:
    with zipfile.ZipFile(zip_path) as archive:
        return set(archive.namelist())


def test_build_zip_excludes_local_secrets_and_symlinks(tmp_path):
    (tmp_path / "README.md").write_text("lab", encoding="utf-8")
    (tmp_path / ".env.example").write_text("TOKEN=", encoding="utf-8")
    (tmp_path / ".env").write_text("TOKEN=secret", encoding="utf-8")
    (tmp_path / ".env.local").write_text("TOKEN=local-secret", encoding="utf-8")

    try:
        (tmp_path / "linked-secret").symlink_to(tmp_path / ".env.local")
    except OSError as error:
        pytest.skip(f"Symlink creation is not available: {error}")

    zip_path = build_zip(tmp_path, "1.2.3")
    paths = archived_paths(zip_path)
    prefix = "iceberg-r2-online-lab-v1.2.3"

    assert f"{prefix}/README.md" in paths
    assert f"{prefix}/.env.example" in paths
    assert f"{prefix}/.env" not in paths
    assert f"{prefix}/.env.local" not in paths
    assert f"{prefix}/linked-secret" not in paths
    assert zip_path.with_suffix(".zip.sha256").is_file()
