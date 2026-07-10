from pathlib import Path
import re

from iceberg_r2_lab import __version__


ROOT = Path(__file__).parents[1]


def test_version_declarations_agree():
    release_version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version = "([^"]+)"$', pyproject, flags=re.MULTILINE)

    assert match is not None
    assert match.group(1) == release_version
    assert __version__ == release_version
