#!/usr/bin/env python3
"""Generate a lightweight geometric wave-propagation animation for a run.

The GIF is a travel-time schematic, not an FDTD field snapshot. It uses the
machine-readable scene geometry to show outgoing wavefronts, rebar reflections,
and approximate echo arrivals without launching any simulation.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import textwrap
from pathlib import Path

import numpy as np
from PIL import Image, ImageSequence

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.animation as animation  # noqa: E402
import matplotlib.patches as patches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

import config as cfg  # noqa: E402
from run_experiment_scene_visualization import (  # noqa: E402
    scene_from_summary,
    validate_backfill_scene_metadata,
)


def concrete_velocity_mm_per_ns(epsr=cfg.CONCRETE_EPSR):
    """Return approximate EM velocity in concrete in mm/ns."""
    return cfg.C0 / np.sqrt(float(epsr)) * 1.0e-6


def choose_representative_pair(scene):
    """Choose the scan pair whose Tx/Rx midpoint is closest to the target."""
    scan_x = [float(value) for value in scene.get("scan_x_values_mm", [])]
    if not scan_x:
        raise ValueError("missing scan_x_values_mm")
    tx_rx_offset = float(scene["tx_rx_offset_mm"])
    target_indices = set(int(value) for value in scene.get("target_indices", []))
    target = None
    for spec in scene["truth"]:
        if int(spec["index"]) in target_indices:
            target = spec
            break
    if target is None:
        target = scene["truth"][len(scene["truth"]) // 2]
    target_x = float(target["x_mm"])
    best_tx = min(scan_x, key=lambda src_x: abs((float(src_x) + 0.5 * tx_rx_offset) - target_x))
    return {
        "tx_x_mm": float(best_tx),
        "rx_x_mm": float(best_tx) + tx_rx_offset,
        "tx_z_mm": float(scene["source_z_mm"]),
        "rx_z_mm": float(scene["receiver_z_mm"]),
        "target_rebar_index": int(target["index"]),
    }


def _distance_mm(x0, z0, x1, z1):
    return float(np.hypot(float(x1) - float(x0), float(z1) - float(z0)))


def travel_time_metadata(scene, pair):
    """Compute approximate geometric travel times for each rebar."""
    velocity = concrete_velocity_mm_per_ns()
    rows = []
    for spec in scene["truth"]:
        tx_to_bar = _distance_mm(pair["tx_x_mm"], pair["tx_z_mm"], spec["x_mm"], spec["z_mm"])
        bar_to_rx = _distance_mm(spec["x_mm"], spec["z_mm"], pair["rx_x_mm"], pair["rx_z_mm"])
        rows.append({
            "rebar_index": int(spec["index"]),
            "x_mm": float(spec["x_mm"]),
            "z_mm": float(spec["z_mm"]),
            "radius_mm": float(spec["radius_mm"]),
            "tx_to_rebar_time_ns": tx_to_bar / velocity,
            "rebar_to_rx_time_ns": bar_to_rx / velocity,
            "two_way_time_ns": (tx_to_bar + bar_to_rx) / velocity,
            "is_target": int(spec["index"]) == int(pair["target_rebar_index"]),
        })
    direct_distance = _distance_mm(pair["tx_x_mm"], pair["tx_z_mm"], pair["rx_x_mm"], pair["rx_z_mm"])
    return {
        "velocity_model": "straight-ray concrete velocity schematic",
        "concrete_epsr": float(cfg.CONCRETE_EPSR),
        "concrete_velocity_mm_per_ns": velocity,
        "direct_tx_rx_time_ns_air": direct_distance / (cfg.C0 * 1.0e-6),
        "rebar_echoes": rows,
    }


def _draw_static_scene(ax, scene, pair):
    domain_x = float(scene["domain_x_mm"])
    domain_z = float(scene["domain_z_mm"])
    concrete_top = float(scene["concrete_top_mm"])
    ax.axhspan(0.0, concrete_top, facecolor="#eef3f7", edgecolor="none", zorder=0)
    ax.axhspan(concrete_top, domain_z, facecolor="#f4f0e8", edgecolor="none", zorder=0)
    ax.axhline(concrete_top, color="#566573", linewidth=1.2, zorder=1)
    ax.axhline(pair["tx_z_mm"], color="#4c78a8", linewidth=1.0, linestyle="--", zorder=1)
    ax.plot(
        [pair["tx_x_mm"], pair["rx_x_mm"]],
        [pair["tx_z_mm"], pair["rx_z_mm"]],
        color="#6e6e6e",
        linewidth=1.0,
        alpha=0.8,
        zorder=2,
    )
    ax.scatter(
        [pair["tx_x_mm"]],
        [pair["tx_z_mm"]],
        marker="^",
        s=55,
        color="#1b7837",
        edgecolor="black",
        linewidth=0.5,
        label="Tx",
        zorder=6,
    )
    ax.scatter(
        [pair["rx_x_mm"]],
        [pair["rx_z_mm"]],
        marker="v",
        s=55,
        color="#762a83",
        edgecolor="black",
        linewidth=0.5,
        label="Rx",
        zorder=6,
    )
    for spec in scene["truth"]:
        is_target = int(spec["index"]) == int(pair["target_rebar_index"])
        if is_target:
            ax.add_patch(patches.Circle(
                (spec["x_mm"], spec["z_mm"]),
                spec["radius_mm"] + 3.0,
                linewidth=2.0,
                edgecolor="#f2b447",
                facecolor="none",
                zorder=5,
                label="target rebar",
            ))
        ax.add_patch(patches.Circle(
            (spec["x_mm"], spec["z_mm"]),
            spec["radius_mm"],
            linewidth=1.8 if is_target else 1.2,
            edgecolor="#111111",
            facecolor="#8a8f93",
            alpha=0.35,
            zorder=4,
            label="true rebar" if not is_target else None,
        ))
        ax.text(
            spec["x_mm"] + spec["radius_mm"] + 4.0,
            spec["z_mm"] + spec["radius_mm"] + 8.0,
            f"t{int(spec['index'])}",
            fontsize=8,
            color="#222222",
            zorder=7,
        )
    ax.set_xlim(0.0, domain_x)
    ax.set_ylim(domain_z, 0.0)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("z [mm]")
    ax.grid(color="#d4d4d4", linewidth=0.6, alpha=0.75)


def _add_unique_legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    by_label = {}
    for handle, label in zip(handles, labels):
        if label and label not in by_label:
            by_label[label] = handle
    ax.legend(by_label.values(), by_label.keys(), loc="lower right", fontsize=8, frameon=True)


def write_wave_animation(
        scene,
        save_path,
        title=None,
        frames=36,
        fps=8):
    """Write one geometric wave propagation GIF and return metadata."""
    validate_backfill_scene_metadata(scene)
    pair = choose_representative_pair(scene)
    travel = travel_time_metadata(scene, pair)
    velocity = travel["concrete_velocity_mm_per_ns"]
    max_echo = max(row["two_way_time_ns"] for row in travel["rebar_echoes"])
    max_time_ns = max(2.0, 1.15 * max_echo)
    times = np.linspace(0.0, max_time_ns, int(frames))

    fig, ax = plt.subplots(figsize=(8.5, 5.4), constrained_layout=True)

    def draw_frame(frame_index):
        time_ns = float(times[int(frame_index)])
        ax.clear()
        _draw_static_scene(ax, scene, pair)
        outgoing_radius = velocity * time_ns
        ax.add_patch(patches.Circle(
            (pair["tx_x_mm"], pair["tx_z_mm"]),
            outgoing_radius,
            linewidth=2.2,
            edgecolor="#2b6cb0",
            facecolor="none",
            alpha=0.72,
            zorder=3,
            label="forward wavefront",
        ))
        for row in travel["rebar_echoes"]:
            delay = float(row["tx_to_rebar_time_ns"])
            if time_ns >= delay:
                reflection_radius = velocity * (time_ns - delay)
                color = "#d95f02" if row["is_target"] else "#f2a541"
                ax.add_patch(patches.Circle(
                    (row["x_mm"], row["z_mm"]),
                    reflection_radius,
                    linewidth=2.2 if row["is_target"] else 1.4,
                    edgecolor=color,
                    facecolor="none",
                    alpha=0.75 if row["is_target"] else 0.42,
                    zorder=3,
                    label="rebar reflection" if row["is_target"] else None,
                ))
                ax.plot(
                    [pair["tx_x_mm"], row["x_mm"], pair["rx_x_mm"]],
                    [pair["tx_z_mm"], row["z_mm"], pair["rx_z_mm"]],
                    color=color,
                    linewidth=1.2 if row["is_target"] else 0.7,
                    alpha=0.45 if row["is_target"] else 0.22,
                    zorder=2,
                )
            if abs(time_ns - float(row["two_way_time_ns"])) <= max_time_ns / max(int(frames) - 1, 1):
                ax.scatter(
                    [pair["rx_x_mm"]],
                    [pair["rx_z_mm"]],
                    marker="o",
                    s=180,
                    facecolor="none",
                    edgecolor="#d95f02",
                    linewidth=2.2,
                    zorder=8,
                )
        run_name = title or scene.get("run_name") or "Geometric Wave Propagation"
        ax.set_title(
            f"{textwrap.fill(str(run_name), width=72)}\n"
            f"schematic time {time_ns:.2f} ns | blue=forward, orange=reflection",
            fontsize=11,
            fontweight="bold",
        )
        _add_unique_legend(ax)
        ax.text(
            0.02,
            0.03,
            "Travel-time schematic; not an FDTD wavefield amplitude animation.",
            transform=ax.transAxes,
            fontsize=8,
            color="#333333",
            bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "#dddddd", "alpha": 0.88},
        )

    anim = animation.FuncAnimation(fig, draw_frame, frames=len(times), interval=1000.0 / fps)
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    writer = animation.PillowWriter(fps=int(fps))
    anim.save(str(save_path), writer=writer, dpi=115)
    plt.close(fig)
    return {
        "pair": pair,
        "travel_time": travel,
        "frames": int(frames),
        "fps": int(fps),
        "max_time_ns": float(max_time_ns),
    }


def validate_gif(path, min_frames=4):
    """Return basic nonblank metrics for a saved GIF."""
    with Image.open(path) as image:
        frames = [frame.convert("RGB") for frame in ImageSequence.Iterator(image)]
    if len(frames) < int(min_frames):
        raise ValueError(f"GIF has too few frames: {path}")
    arr = np.asarray(frames[min(len(frames) - 1, len(frames) // 2)])
    unique = len(np.unique(arr.reshape(-1, 3), axis=0))
    nonwhite = float(np.mean(np.any(arr < 250, axis=2)))
    if unique < 32 or nonwhite < 0.01:
        raise ValueError(f"Saved wave animation appears degenerate: {path}")
    return {
        "width_px": int(frames[0].size[0]),
        "height_px": int(frames[0].size[1]),
        "frame_count": int(len(frames)),
        "unique_colors_midframe": int(unique),
        "nonwhite_fraction_midframe": nonwhite,
    }


def figure_notes_has_wave_section(figures_dir):
    """Return whether FIGURE_NOTES.md already has the wave animation block."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    if not notes_path.exists():
        return False
    text = notes_path.read_text(encoding="utf-8")
    return (
        "<!-- geometric_wave_propagation:start -->" in text
        and "<!-- geometric_wave_propagation:end -->" in text
    )


def upsert_figure_notes(figures_dir, figure_name, summary_name):
    """Add or replace the geometric wave animation section."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    start = "<!-- geometric_wave_propagation:start -->"
    end = "<!-- geometric_wave_propagation:end -->"
    section = f"""{start}
## `{figure_name}` - geometric wave propagation animation

This GIF is a lightweight travel-time schematic. It shows the selected
transmitter/receiver (Tx/Rx) pair, an outgoing forward wavefront, approximate
rebar reflection fronts, target highlight, and echo arrival timing. It is meant
to explain propagation paths and reflections without running a new FDTD/FWI
simulation.

Validation and travel-time metadata are saved in `../data/{summary_name}`.
{end}
"""
    text = notes_path.read_text(encoding="utf-8") if notes_path.exists() else "# Figure Notes\n"
    pattern = re.compile(rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?", flags=re.DOTALL)
    text = pattern.sub("\n", text).rstrip() + "\n\n" + section
    notes_path.write_text(text, encoding="utf-8")
    return str(notes_path)


def infer_outdir(summary_path, outdir):
    if outdir:
        return Path(outdir)
    path = Path(summary_path)
    if path.parent.name == "data":
        return path.parent.parent
    return path.parent


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


def audit_counts(rows):
    counts = {}
    for row in rows:
        status = row.get("status", "")
        counts[status] = counts.get(status, 0) + 1
    return counts


def _audit_row(
        run_dir,
        status,
        reason,
        summary_path=None,
        animation_path=None,
        context_summary_path=None,
        figure_notes_path=None,
        validation=None):
    validation = validation or {}
    return {
        "run_dir": str(run_dir),
        "run_number": _run_number(run_dir),
        "summary_path": "" if summary_path is None else str(summary_path),
        "status": status,
        "reason": reason,
        "animation_path": "" if animation_path is None else str(animation_path),
        "context_summary_path": "" if context_summary_path is None else str(context_summary_path),
        "figure_notes_path": "" if figure_notes_path is None else str(figure_notes_path),
        "width_px": validation.get("width_px", ""),
        "height_px": validation.get("height_px", ""),
        "frame_count": validation.get("frame_count", ""),
        "unique_colors_midframe": validation.get("unique_colors_midframe", ""),
        "nonwhite_fraction_midframe": validation.get("nonwhite_fraction_midframe", ""),
    }


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
        "summary_path",
        "status",
        "reason",
        "animation_path",
        "context_summary_path",
        "figure_notes_path",
        "width_px",
        "height_px",
        "frame_count",
        "unique_colors_midframe",
        "nonwhite_fraction_midframe",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return str(path)


def process_summary_for_backfill(
        run_dir,
        summary_path,
        label="geometric_wave_propagation",
        frames=36,
        fps=8,
        update_notes=True,
        refresh_existing=False):
    """Generate or skip one geometric wave GIF with audit metadata."""
    run_dir = Path(run_dir)
    summary_path = Path(summary_path)
    figures_dir = run_dir / "figures"
    data_dir = run_dir / "data"
    gif_path = figures_dir / f"{label}.gif"
    context_summary_path = data_dir / f"{label}_summary.json"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    if gif_path.exists() and not refresh_existing:
        try:
            validation = validate_gif(gif_path)
        except Exception as exc:
            existing_reason = f"existing animation invalid: {exc}"
        else:
            has_summary = context_summary_path.exists()
            has_notes = (not update_notes) or figure_notes_has_wave_section(figures_dir)
            if has_summary and has_notes:
                return _audit_row(
                    run_dir,
                    "skipped",
                    "existing valid wave animation artifacts",
                    summary_path=summary_path,
                    animation_path=gif_path,
                    context_summary_path=context_summary_path,
                    figure_notes_path=notes_path if notes_path.exists() else None,
                    validation=validation,
                )
            missing = []
            if not has_summary:
                missing.append(context_summary_path.name)
            if not has_notes:
                missing.append(notes_path.name)
            existing_reason = "existing animation missing companion artifacts: " + ", ".join(missing)
    else:
        existing_reason = "refresh requested" if gif_path.exists() else "missing wave animation artifacts"

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        artifacts = write_animation_artifacts(
            summary,
            run_dir,
            summary_path=summary_path,
            label=label,
            frames=frames,
            fps=fps,
            update_notes=update_notes,
        )
    except Exception as exc:
        return _audit_row(
            run_dir,
            "skipped",
            f"incompatible metadata: {exc}",
            summary_path=summary_path,
            animation_path=gif_path if gif_path.exists() else None,
            context_summary_path=context_summary_path if context_summary_path.exists() else None,
            figure_notes_path=notes_path if notes_path.exists() else None,
        )

    status = "refreshed" if existing_reason != "missing wave animation artifacts" else "generated"
    return _audit_row(
        run_dir,
        status,
        existing_reason,
        summary_path=summary_path,
        animation_path=artifacts["animation"],
        context_summary_path=artifacts["summary"],
        figure_notes_path=artifacts["figure_notes"],
        validation=artifacts["validation"],
    )


def backfill_wave_animation_artifacts(
        experiments_root,
        label="geometric_wave_propagation",
        frames=36,
        fps=8,
        update_notes=True,
        refresh_existing=False,
        min_run_number=None,
        max_run_number=None,
        limit=None,
        audit_json=None,
        audit_csv=None):
    """Backfill geometric wave GIFs newest first."""
    rows = []
    for run_dir in numbered_experiment_dirs(experiments_root):
        run_number = _run_number(run_dir)
        if min_run_number is not None and run_number < int(min_run_number):
            continue
        if max_run_number is not None and run_number > int(max_run_number):
            continue
        if limit is not None and len(rows) >= int(limit):
            break
        summary_path = run_dir / "data" / "multi_rebar_coordinate_optimizer_summary.json"
        if not summary_path.exists():
            rows.append(_audit_row(
                run_dir,
                "skipped",
                "no compatible coordinate optimizer summary",
            ))
            continue
        rows.append(process_summary_for_backfill(
            run_dir,
            summary_path,
            label=label,
            frames=frames,
            fps=fps,
            update_notes=update_notes,
            refresh_existing=refresh_existing,
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


def write_animation_artifacts(
        summary,
        outdir,
        summary_path=None,
        label="geometric_wave_propagation",
        frames=36,
        fps=8,
        update_notes=True):
    """Write animation GIF, metadata summary, and optional notes."""
    outdir = Path(outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    scene = scene_from_summary(summary, summary_path)
    gif_path = figures_dir / f"{label}.gif"
    metadata = write_wave_animation(scene, gif_path, frames=frames, fps=fps)
    validation = validate_gif(gif_path)
    summary_name = f"{label}_summary.json"
    payload = {
        "source": "summary",
        "summary_path": None if summary_path is None else str(summary_path),
        "run_name": summary.get("run_name", ""),
        "scene_basis": "coordinate optimizer summary geometry",
        "animation_type": "geometric travel-time schematic",
        "metadata": metadata,
        "validation": validation,
        "paths": {
            "animation": str(gif_path),
        },
    }
    summary_path_out = data_dir / summary_name
    summary_path_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    notes_path = None
    if update_notes:
        notes_path = upsert_figure_notes(figures_dir, gif_path.name, summary_name)
    return {
        "animation": str(gif_path),
        "summary": str(summary_path_out),
        "figure_notes": notes_path,
        "validation": validation,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=None,
                        help="Path to multi_rebar_coordinate_optimizer_summary.json.")
    parser.add_argument("--outdir", default=None)
    parser.add_argument("--label", default="geometric_wave_propagation")
    parser.add_argument("--frames", type=int, default=36)
    parser.add_argument("--fps", type=int, default=8)
    parser.add_argument("--skip-figure-notes", action="store_true")
    parser.add_argument("--backfill-root", type=Path, default=None,
                        help="Backfill numbered experiment directories under this root.")
    parser.add_argument("--refresh-existing", action="store_true")
    parser.add_argument("--min-run-number", type=int, default=None)
    parser.add_argument("--max-run-number", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum numbered experiment directories to audit in backfill mode.")
    parser.add_argument("--audit-json", type=Path, default=None)
    parser.add_argument("--audit-csv", type=Path, default=None)
    args = parser.parse_args()

    if args.backfill_root is not None:
        result = backfill_wave_animation_artifacts(
            args.backfill_root,
            label=args.label,
            frames=args.frames,
            fps=args.fps,
            update_notes=not args.skip_figure_notes,
            refresh_existing=args.refresh_existing,
            min_run_number=args.min_run_number,
            max_run_number=args.max_run_number,
            limit=args.limit,
            audit_json=args.audit_json,
            audit_csv=args.audit_csv,
        )
        print("Backfill wave animation audit complete.")
        print(json.dumps({
            "counts": result["counts"],
            "audit_paths": result["audit_paths"],
        }, indent=2))
        return

    if args.summary is None:
        raise ValueError("--summary is required unless --backfill-root is supplied")
    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    artifacts = write_animation_artifacts(
        summary,
        infer_outdir(args.summary, args.outdir),
        summary_path=args.summary,
        label=args.label,
        frames=args.frames,
        fps=args.fps,
        update_notes=not args.skip_figure_notes,
    )
    print(f"Wrote wave animation: {artifacts['animation']}")
    print(f"Wrote wave animation summary: {artifacts['summary']}")
    if artifacts["figure_notes"]:
        print(f"Updated figure notes: {artifacts['figure_notes']}")
    print(json.dumps(artifacts["validation"], indent=2))


if __name__ == "__main__":
    main()
