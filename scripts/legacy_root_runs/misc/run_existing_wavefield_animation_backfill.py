#!/usr/bin/env python3
"""Inventory and validate already-saved true FDTD wavefield animations.

This script never runs FDTD/FWI. It only uses existing wavefield GIFs and their
metadata summaries, then writes a per-run inventory plus audit reports.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from run_wavefield_animation import validate_animation  # noqa: E402


def _run_number(path):
    match = re.match(r"(\d+)_", Path(path).name)
    if match is None:
        return None
    return int(match.group(1))


def numbered_experiment_dirs(experiments_root):
    """Return numbered experiment directories newest first."""
    root = Path(experiments_root)
    dirs = []
    for candidate in root.iterdir():
        if not candidate.is_dir():
            continue
        number = _run_number(candidate)
        if number is None:
            continue
        dirs.append((number, candidate))
    return [path for _, path in sorted(dirs, key=lambda item: item[0], reverse=True)]


def is_true_wavefield_gif(path):
    """Return whether a GIF is an existing true wavefield animation artifact."""
    name = Path(path).name
    if not name.endswith(".gif"):
        return False
    if "wavefield" not in name:
        return False
    if name == "geometric_wave_propagation.gif":
        return False
    return True


def matching_summary_path(run_dir, gif_path):
    """Return the conventional summary path for an existing wavefield GIF."""
    stem = Path(gif_path).stem
    return Path(run_dir) / "data" / f"{stem}_animation_summary.json"


def _read_json_if_exists(path):
    path = Path(path)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def discover_wavefield_entries(run_dir):
    """Discover and validate existing wavefield GIFs in one run directory."""
    run_dir = Path(run_dir)
    figures_dir = run_dir / "figures"
    if not figures_dir.exists():
        return []
    entries = []
    for gif_path in sorted(figures_dir.glob("*.gif")):
        if not is_true_wavefield_gif(gif_path):
            continue
        validation = validate_animation(gif_path)
        summary_path = matching_summary_path(run_dir, gif_path)
        summary = _read_json_if_exists(summary_path)
        entries.append({
            "animation": str(gif_path),
            "summary": str(summary_path) if summary_path.exists() else "",
            "summary_present": summary_path.exists(),
            "run_summary_metadata": summary,
            "validation": validation,
        })
    return entries


def upsert_figure_notes(figures_dir, inventory_name, entries):
    """Add or replace the existing-wavefield inventory section."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    start = "<!-- existing_true_wavefield_animations:start -->"
    end = "<!-- existing_true_wavefield_animations:end -->"
    lines = [
        start,
        "## Existing true FDTD wavefield animations",
        "",
        "These GIFs are already-saved FDTD wavefield animations from the run.",
        "They were validated and inventoried without launching a new simulation.",
        "",
    ]
    for entry in entries:
        gif_name = Path(entry["animation"]).name
        frame_count = entry["validation"].get("frame_count")
        width = entry["validation"].get("width_px")
        height = entry["validation"].get("height_px")
        lines.append(f"- `{gif_name}`: {frame_count} frames, {width}x{height} px.")
    lines.extend([
        "",
        f"Inventory metadata is saved in `../data/{inventory_name}`.",
        end,
        "",
    ])
    section = "\n".join(lines)
    text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else "# Figure Notes\n"
    pattern = re.compile(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", flags=re.DOTALL)
    text = pattern.sub("\n", text).rstrip() + "\n\n" + section
    notes_path.write_text(text, encoding="utf-8")
    return str(notes_path)


def write_run_inventory(run_dir, entries, update_notes=True, label="existing_true_wavefield_animations"):
    """Write per-run inventory JSON for existing true wavefield animations."""
    run_dir = Path(run_dir)
    data_dir = run_dir / "data"
    figures_dir = run_dir / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    inventory_name = f"{label}_summary.json"
    inventory_path = data_dir / inventory_name
    payload = {
        "source": "existing saved wavefield GIFs",
        "run_dir": str(run_dir),
        "animation_count": len(entries),
        "animations": entries,
        "note": "No FDTD/FWI was run; this inventory validates already-saved true wavefield animations.",
    }
    inventory_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    notes_path = None
    if update_notes:
        notes_path = upsert_figure_notes(figures_dir, inventory_name, entries)
    return {
        "inventory": str(inventory_path),
        "figure_notes": notes_path,
    }


def _audit_row(
        run_dir,
        status,
        reason,
        inventory_path=None,
        figure_notes_path=None,
        entries=None):
    entries = entries or []
    frame_counts = [
        int(entry["validation"]["frame_count"])
        for entry in entries
        if entry.get("validation") and entry["validation"].get("frame_count") is not None
    ]
    return {
        "run_dir": str(run_dir),
        "run_number": _run_number(run_dir),
        "status": status,
        "reason": reason,
        "inventory_path": "" if inventory_path is None else str(inventory_path),
        "figure_notes_path": "" if figure_notes_path is None else str(figure_notes_path),
        "animation_count": len(entries),
        "total_frames": sum(frame_counts),
        "animations": ";".join(Path(entry["animation"]).name for entry in entries),
    }


def audit_counts(rows):
    counts = {}
    for row in rows:
        status = row.get("status", "")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _write_audit_json(rows, audit_json):
    path = Path(audit_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"rows": rows, "counts": audit_counts(rows)}, indent=2),
        encoding="utf-8",
    )
    return str(path)


def _write_audit_csv(rows, audit_csv):
    path = Path(audit_csv)
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "run_number",
        "run_dir",
        "status",
        "reason",
        "inventory_path",
        "figure_notes_path",
        "animation_count",
        "total_frames",
        "animations",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return str(path)


def process_run(
        run_dir,
        update_notes=True,
        refresh_existing=False,
        label="existing_true_wavefield_animations"):
    """Process one run directory for existing true wavefield animations."""
    run_dir = Path(run_dir)
    inventory_path = run_dir / "data" / f"{label}_summary.json"
    notes_path = run_dir / "figures" / "FIGURE_NOTES.md"
    if inventory_path.exists() and not refresh_existing:
        try:
            entries = discover_wavefield_entries(run_dir)
        except Exception as exc:
            return _audit_row(run_dir, "skipped", f"existing inventory invalid source: {exc}")
        if entries:
            return _audit_row(
                run_dir,
                "skipped",
                "existing true wavefield inventory",
                inventory_path=inventory_path,
                figure_notes_path=notes_path if notes_path.exists() else None,
                entries=entries,
            )

    try:
        entries = discover_wavefield_entries(run_dir)
    except Exception as exc:
        return _audit_row(run_dir, "skipped", f"invalid existing wavefield animation: {exc}")
    if not entries:
        return _audit_row(run_dir, "skipped", "no existing true wavefield GIF")
    artifacts = write_run_inventory(
        run_dir,
        entries,
        update_notes=update_notes,
        label=label,
    )
    status = "refreshed" if inventory_path.exists() and refresh_existing else "generated"
    return _audit_row(
        run_dir,
        status,
        "existing true wavefield GIFs validated",
        inventory_path=artifacts["inventory"],
        figure_notes_path=artifacts["figure_notes"],
        entries=entries,
    )


def backfill_existing_wavefield_inventories(
        experiments_root,
        update_notes=True,
        refresh_existing=False,
        min_run_number=None,
        max_run_number=None,
        limit=None,
        audit_json=None,
        audit_csv=None,
        label="existing_true_wavefield_animations"):
    """Backfill inventories for existing true FDTD wavefield GIFs."""
    rows = []
    for run_dir in numbered_experiment_dirs(experiments_root):
        run_number = _run_number(run_dir)
        if min_run_number is not None and run_number < int(min_run_number):
            continue
        if max_run_number is not None and run_number > int(max_run_number):
            continue
        if limit is not None and len(rows) >= int(limit):
            break
        rows.append(process_run(
            run_dir,
            update_notes=update_notes,
            refresh_existing=refresh_existing,
            label=label,
        ))

    audit_paths = {}
    if audit_json is not None:
        audit_paths["json"] = _write_audit_json(rows, audit_json)
    if audit_csv is not None:
        audit_paths["csv"] = _write_audit_csv(rows, audit_csv)
    return {
        "rows": rows,
        "counts": audit_counts(rows),
        "audit_paths": audit_paths,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backfill-root", type=Path, default=Path("outputs/experiments"))
    parser.add_argument("--refresh-existing", action="store_true")
    parser.add_argument("--min-run-number", type=int, default=None)
    parser.add_argument("--max-run-number", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--label", default="existing_true_wavefield_animations")
    parser.add_argument("--skip-figure-notes", action="store_true")
    parser.add_argument("--audit-json", type=Path, default=None)
    parser.add_argument("--audit-csv", type=Path, default=None)
    args = parser.parse_args()

    result = backfill_existing_wavefield_inventories(
        args.backfill_root,
        update_notes=not args.skip_figure_notes,
        refresh_existing=args.refresh_existing,
        min_run_number=args.min_run_number,
        max_run_number=args.max_run_number,
        limit=args.limit,
        audit_json=args.audit_json,
        audit_csv=args.audit_csv,
        label=args.label,
    )
    print("Existing true wavefield inventory audit complete.")
    print(json.dumps({
        "counts": result["counts"],
        "audit_paths": result["audit_paths"],
    }, indent=2))


if __name__ == "__main__":
    main()
