#!/usr/bin/env python3
"""Bump the plugin version and build the uploadable skill archive."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
SKILL_DIR = ROOT / "skills" / "prudent-ponytail"
DIST_DIR = ROOT / "dist"
VERSION_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
IGNORED_NAMES = {".DS_Store", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def parse_version(value: str) -> tuple[int, int, int]:
    match = VERSION_RE.fullmatch(value)
    if not match:
        raise ValueError(f"version must be X.Y.Z, got {value!r}")
    return tuple(int(part) for part in match.groups())


def skill_files() -> list[Path]:
    files = [
        path
        for path in SKILL_DIR.rglob("*")
        if path.is_file()
        and not any(part in IGNORED_NAMES for part in path.relative_to(SKILL_DIR).parts)
        and path.suffix not in IGNORED_SUFFIXES
    ]
    if SKILL_DIR / "SKILL.md" not in files:
        raise RuntimeError("skills/prudent-ponytail/SKILL.md is required")
    return sorted(files, key=lambda path: path.relative_to(SKILL_DIR).as_posix())


def build_archive(version: str, files: list[Path]) -> tuple[Path, Path]:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    destination = DIST_DIR / f"prudent-ponytail-skill-{version}.zip"
    fd, temporary_name = tempfile.mkstemp(prefix=".prudent-ponytail-", suffix=".zip", dir=DIST_DIR)
    os.close(fd)
    temporary = Path(temporary_name)

    try:
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for source in files:
                relative = source.relative_to(SKILL_DIR).as_posix()
                info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
                mode = 0o755 if os.access(source, os.X_OK) else 0o644
                info.external_attr = (0o100000 | mode) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, source.read_bytes(), compresslevel=9)

        with zipfile.ZipFile(temporary) as archive:
            if "SKILL.md" not in archive.namelist():
                raise RuntimeError("archive is missing SKILL.md at its root")
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"archive integrity check failed at {bad}")
    except Exception:
        temporary.unlink(missing_ok=True)
        raise

    return temporary, destination


def write_manifest(manifest: dict[str, object]) -> None:
    fd, temporary_name = tempfile.mkstemp(prefix="plugin-", suffix=".json", dir=MANIFEST.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        temporary.replace(MANIFEST)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Optionally bump plugin.json, then build the ChatGPT skill ZIP."
    )
    parser.add_argument("version", nargs="?", help="new release version in X.Y.Z form")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    current = manifest.get("version")
    if not isinstance(current, str):
        raise RuntimeError("plugin.json must contain a string version")
    current_tuple = parse_version(current)

    target = args.version or current
    target_tuple = parse_version(target)
    if args.version and target_tuple < current_tuple:
        raise ValueError(f"version cannot move backwards: {current} -> {target}")

    temporary_archive, destination = build_archive(target, skill_files())
    if target != current:
        manifest["version"] = target
        write_manifest(manifest)
        print(f"Version: {current} -> {target}")
    else:
        print(f"Version: {current}")

    temporary_archive.replace(destination)
    print(f"Archive: {destination.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
