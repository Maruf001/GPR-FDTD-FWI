#!/usr/bin/env python3
"""Move post-535 admin output folders with compatibility symlinks.

Default mode is a dry run. Use --execute to perform moves.
"""

from __future__ import annotations

import argparse
import csv
import os
import shutil
from pathlib import Path


DEFAULT_CLASSIFICATION = Path(
    "outputs/archive_resolution/post535_735_resolution_audit/"
    "post535_735_output_classification.csv"
)
DEFAULT_DEST = Path("outputs/experiment_admin_archive/535_735")


def relative_symlink_target(link_path: Path, target_path: Path) -> str:
    return os.path.relpath(target_path, start=link_path.parent)


def load_admin_rows(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if row["bucket"] == "relocate_or_consolidate_admin_churn"]


def move_one(row: dict, destination_root: Path, execute: bool) -> str:
    source = Path(row["path"])
    destination = destination_root / source.name
    if source.is_symlink():
        return f"skip symlink already present: {source}"
    if not source.exists():
        return f"skip missing source: {source}"
    if destination.exists():
        return f"skip existing destination: {destination}"
    link_target = relative_symlink_target(source, destination)
    if not execute:
        return f"dry-run move {source} -> {destination}; symlink {source} -> {link_target}"
    destination_root.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    source.symlink_to(link_target)
    return f"moved {source} -> {destination}; symlinked original path"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classification", type=Path, default=DEFAULT_CLASSIFICATION)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--execute", action="store_true", help="actually move directories")
    parser.add_argument("--limit", type=int, default=None, help="only process first N rows")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    rows = load_admin_rows(args.classification)
    if args.limit is not None:
        rows = rows[: args.limit]
    print(f"admin rows: {len(rows)}")
    print(f"destination: {args.destination}")
    print(f"mode: {'execute' if args.execute else 'dry-run'}")
    for row in rows:
        print(move_one(row, args.destination, args.execute))


if __name__ == "__main__":
    main()
