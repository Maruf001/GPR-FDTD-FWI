"""Resolve generated-checkpoint paths moved out of ``outputs/summary_tables``."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from run_project_core_homogeneous_dielectric_bridge_adapter import PROJECT_ROOT

SUMMARY_TABLES_ROOT = PROJECT_ROOT / "outputs" / "summary_tables"
GENERATED_CHECKPOINT_ROOT = PROJECT_ROOT / "outputs" / "_generated_checkpoints"


@lru_cache(maxsize=None)
def _moved_checkpoint_dir(folder_name: str) -> Path | None:
    if not GENERATED_CHECKPOINT_ROOT.exists():
        return None
    matches = [path for path in GENERATED_CHECKPOINT_ROOT.rglob(folder_name) if path.is_dir()]
    if len(matches) == 1:
        return matches[0]
    return None


def resolve_generated_checkpoint_path(path: Path | str) -> Path:
    """Return the moved generated-checkpoint path when an old summary path is missing."""

    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = PROJECT_ROOT / candidate
    if candidate.exists():
        return candidate
    try:
        relative = candidate.relative_to(SUMMARY_TABLES_ROOT)
    except ValueError:
        return candidate
    if not relative.parts:
        return candidate
    moved_dir = _moved_checkpoint_dir(relative.parts[0])
    if moved_dir is None:
        return candidate
    return moved_dir.joinpath(*relative.parts[1:])
