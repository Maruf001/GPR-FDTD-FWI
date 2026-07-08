"""Helpers for numbered experiment output directories and manifests."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


_RUN_DIR_RE = re.compile(r"^(\d{3,})_(.+)$")


def _slugify(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "run"


def allocate_output_dir(outdir: str | None, run_name: str, root: str = "outputs/experiments") -> str:
    """Return an output directory, allocating the next numbered run if needed.

    If ``outdir`` is provided, it is used exactly. Otherwise, the next
    ``NNN_<run_name>`` directory under ``root`` is created.
    """
    if outdir:
        Path(outdir).mkdir(parents=True, exist_ok=True)
        return outdir

    root_path = Path(root)
    root_path.mkdir(parents=True, exist_ok=True)
    max_index = 0
    for child in root_path.iterdir():
        if not child.is_dir():
            continue
        match = _RUN_DIR_RE.match(child.name)
        if match:
            max_index = max(max_index, int(match.group(1)))

    path = root_path / f"{max_index + 1:03d}_{_slugify(run_name)}"
    path.mkdir(parents=False, exist_ok=False)
    return str(path)


def _git_value(args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def write_run_manifest(outdir: str, run_kind: str, extra: dict | None = None) -> str:
    """Write a compact manifest for a run and return its path."""
    manifest = {
        "run_kind": run_kind,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "cwd": os.getcwd(),
        "command": [sys.executable, *sys.argv],
        "git_commit": _git_value(["rev-parse", "HEAD"]),
        "git_status_short": _git_value(["status", "--short"]),
    }
    if extra:
        manifest.update(extra)

    path = Path(outdir) / "run_manifest.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return str(path)
