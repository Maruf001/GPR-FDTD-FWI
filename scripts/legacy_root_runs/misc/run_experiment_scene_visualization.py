#!/usr/bin/env python3
"""Generate reusable experiment scene/context figures.

This script is intentionally lightweight: it draws the physical scene that an
experiment is testing, without running FDTD. It can read a coordinate optimizer
summary or accept explicit geometry values from the command line.
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
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", os.path.join(PROJECT_ROOT, "outputs", ".matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", os.path.join(PROJECT_ROOT, "outputs", ".cache"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)
os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)

import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.patches as patches  # noqa: E402

import config as cfg  # noqa: E402
from visualization.plot_style import save_validated_figure  # noqa: E402


def parse_vector_mm(text):
    """Parse comma-separated floats or min:max:step ranges in millimetres."""
    values = []
    for item in str(text).split(","):
        item = item.strip()
        if not item:
            continue
        if ":" in item:
            parts = [float(part.strip()) for part in item.split(":") if part.strip()]
            if len(parts) != 3:
                raise argparse.ArgumentTypeError("ranges must use min:max:step")
            start, stop, step = parts
            if step <= 0.0 or start > stop:
                raise argparse.ArgumentTypeError("range requires positive step and start <= stop")
            count = int(np.floor((stop - start) / step + 1e-9)) + 1
            values.extend(round(float(start + step * idx), 10) for idx in range(count))
        else:
            values.append(round(float(item), 10))
    if not values:
        raise argparse.ArgumentTypeError("at least one value is required")
    return values


def parse_indices(text):
    """Parse comma-separated non-negative integer indices."""
    values = [int(part.strip()) for part in str(text).split(",") if part.strip()]
    if any(value < 0 for value in values):
        raise argparse.ArgumentTypeError("target indices must be non-negative")
    return values


def rebar_specs(x_values_mm, z_values_mm, radius_values_mm):
    """Return rebar dictionaries after validating vector lengths."""
    if len(x_values_mm) != len(z_values_mm) or len(x_values_mm) != len(radius_values_mm):
        raise ValueError("x, z, and radius lists must have the same length")
    return [
        {
            "index": int(idx),
            "x_mm": float(x_mm),
            "z_mm": float(z_mm),
            "radius_mm": float(radius_mm),
        }
        for idx, (x_mm, z_mm, radius_mm) in enumerate(
            zip(x_values_mm, z_values_mm, radius_values_mm)
        )
    ]


def _state_specs(summary, state_key):
    state = summary.get(state_key) or {}
    return rebar_specs(
        state.get("x_values_mm", []),
        state.get("z_values_mm", []),
        state.get("radii_mm", []),
    )


def scene_from_summary(summary, summary_path=None):
    """Build a scene dictionary from a coordinate optimizer summary."""
    truth = rebar_specs(
        summary.get("true_x_values_mm", []),
        summary.get("true_z_values_mm", []),
        summary.get("truth_radius_values_mm", []),
    )
    final = _state_specs(summary, "final_state")
    initial = _state_specs(summary, "initial_state")
    return {
        "source": "summary",
        "summary_path": None if summary_path is None else str(summary_path),
        "run_name": summary.get("run_name", ""),
        "truth": truth,
        "initial": initial,
        "final": final,
        "target_indices": [int(value) for value in summary.get("target_indices", [])],
        "scan_x_values_mm": [float(value) for value in summary.get("scan_x_values_mm", [])],
        "tx_rx_offset_mm": float(summary.get("tx_rx_offset_mm", cfg.TX_RX_OFFSET * 1000.0)),
        "source_z_mm": float(cfg.TX_Z * 1000.0),
        "receiver_z_mm": float(cfg.RX_Z * 1000.0),
        "concrete_top_mm": float(cfg.CONCRETE_TOP * 1000.0),
        "domain_x_mm": float(cfg.DOMAIN_X * 1000.0),
        "domain_z_mm": float(cfg.DOMAIN_Z * 1000.0),
        "frequency_ghz": summary.get("frequency_ghz"),
        "sources": summary.get("sources"),
        "receiver_sampling": summary.get("receiver_sampling", ""),
    }


def explicit_scene(args):
    """Build a scene dictionary from CLI geometry vectors."""
    truth = rebar_specs(args.x_values_mm, args.z_values_mm, args.radius_values_mm)
    final = truth
    if args.final_x_values_mm or args.final_z_values_mm or args.final_radius_values_mm:
        if not (args.final_x_values_mm and args.final_z_values_mm and args.final_radius_values_mm):
            raise ValueError("final x, z, and radius lists must be supplied together")
        final = rebar_specs(args.final_x_values_mm, args.final_z_values_mm, args.final_radius_values_mm)
    return {
        "source": "explicit",
        "summary_path": None,
        "run_name": args.run_name or "",
        "truth": truth,
        "initial": [],
        "final": final,
        "target_indices": list(args.target_indices or []),
        "scan_x_values_mm": list(args.scan_x_values_mm or []),
        "tx_rx_offset_mm": float(args.tx_rx_offset_mm),
        "source_z_mm": float(args.source_z_mm),
        "receiver_z_mm": float(args.receiver_z_mm),
        "concrete_top_mm": float(args.concrete_top_mm),
        "domain_x_mm": float(args.domain_x_mm),
        "domain_z_mm": float(args.domain_z_mm),
        "frequency_ghz": args.frequency_ghz,
        "sources": None,
        "receiver_sampling": "",
    }


def specs_are_same(left, right, atol=1e-9):
    """Return whether two rebar spec lists are numerically identical."""
    if len(left) != len(right):
        return False
    for lval, rval in zip(left, right):
        for key in ("x_mm", "z_mm", "radius_mm"):
            if not np.isclose(float(lval[key]), float(rval[key]), atol=atol):
                return False
    return True


def _add_unique_legend(ax):
    handles, labels = ax.get_legend_handles_labels()
    by_label = {}
    for handle, label in zip(handles, labels):
        if label and label not in by_label:
            by_label[label] = handle
    ax.legend(by_label.values(), by_label.keys(), loc="lower right", fontsize=8, frameon=True)


def _format_rebar_label(spec):
    return (
        f"t{int(spec['index'])}: "
        f"x={spec['x_mm']:.0f}, z={spec['z_mm']:.0f}, r={spec['radius_mm']:.2g}"
    )


def _annotate_rebar_specs(ax, specs, concrete_top_mm, domain_x_mm):
    if not specs:
        return
    sorted_specs = sorted(specs, key=lambda spec: (float(spec["x_mm"]), int(spec["index"])))
    n_specs = len(sorted_specs)
    min_bar_top = min(float(spec["z_mm"]) - float(spec["radius_mm"]) for spec in sorted_specs)
    max_bar_bottom = max(float(spec["z_mm"]) + float(spec["radius_mm"]) for spec in sorted_specs)
    if min_bar_top - concrete_top_mm >= 18.0:
        label_y = min_bar_top - 8.0
        va = "bottom"
    else:
        label_y = max_bar_bottom + 12.0
        va = "top"

    min_x = min(float(spec["x_mm"]) for spec in sorted_specs)
    max_x = max(float(spec["x_mm"]) for spec in sorted_specs)
    pad = max(70.0, 35.0 * n_specs)
    left = max(45.0, min_x - pad)
    right = min(domain_x_mm - 45.0, max_x + pad)
    if right - left < 60.0 * max(1, n_specs - 1):
        left = 45.0
        right = domain_x_mm - 45.0
    label_xs = np.linspace(left, right, n_specs) if n_specs > 1 else [float(sorted_specs[0]["x_mm"])]

    for label_x, spec in zip(label_xs, sorted_specs):
        ax.annotate(
            _format_rebar_label(spec),
            xy=(float(spec["x_mm"]), float(spec["z_mm"]) - float(spec["radius_mm"])),
            xytext=(float(label_x), label_y),
            textcoords="data",
            fontsize=8,
            color="#222222",
            ha="center",
            va=va,
            arrowprops={"arrowstyle": "-", "color": "#777777", "lw": 0.7, "shrinkA": 2, "shrinkB": 2},
            bbox={"boxstyle": "round,pad=0.16", "fc": "white", "ec": "none", "alpha": 0.72},
            zorder=8,
        )


def _draw_rebars(ax, specs, style, target_indices, concrete_top_mm=None, domain_x_mm=None):
    for spec in specs:
        idx = int(spec["index"])
        is_target = idx in target_indices
        if is_target:
            ax.add_patch(patches.Circle(
                (spec["x_mm"], spec["z_mm"]),
                spec["radius_mm"] + 3.0,
                linewidth=1.8,
                edgecolor="#f2b447",
                facecolor="none",
                linestyle="-",
                zorder=4,
                label="target rebar",
            ))
        ax.add_patch(patches.Circle(
            (spec["x_mm"], spec["z_mm"]),
            spec["radius_mm"],
            linewidth=style["linewidth"],
            edgecolor=style["edgecolor"],
            facecolor=style["facecolor"],
            alpha=style["alpha"],
            linestyle=style["linestyle"],
            zorder=style["zorder"],
            label=style["label"],
        ))
    if style.get("annotate", False):
        _annotate_rebar_specs(ax, specs, float(concrete_top_mm), float(domain_x_mm))


def _sample_scan_positions(scan_x_values_mm, max_markers):
    if len(scan_x_values_mm) <= max_markers:
        return list(scan_x_values_mm)
    indices = np.linspace(0, len(scan_x_values_mm) - 1, max_markers).round().astype(int)
    return [scan_x_values_mm[int(idx)] for idx in sorted(set(indices))]


def plot_scene(scene, save_path, title=None, max_scan_markers=25):
    """Plot and save one scaled scene/context figure."""
    fig, ax = plt.subplots(figsize=(12.5, 6.5))
    domain_x = float(scene["domain_x_mm"])
    domain_z = float(scene["domain_z_mm"])
    concrete_top = float(scene["concrete_top_mm"])
    source_z = float(scene["source_z_mm"])
    receiver_z = float(scene["receiver_z_mm"])
    target_indices = set(int(value) for value in scene.get("target_indices", []))

    ax.axhspan(0.0, concrete_top, facecolor="#eef3f7", edgecolor="none", zorder=0, label="air")
    ax.axhspan(concrete_top, domain_z, facecolor="#f4f0e8", edgecolor="none", zorder=0, label="concrete")
    ax.axhline(concrete_top, color="#566573", linewidth=1.2, linestyle="-", label="concrete surface")
    ax.axhline(source_z, color="#4c78a8", linewidth=1.0, linestyle="--", label="Tx/Rx path")

    scan_x_values = [float(value) for value in scene.get("scan_x_values_mm", [])]
    tx_rx_offset = float(scene.get("tx_rx_offset_mm", cfg.TX_RX_OFFSET * 1000.0))
    sampled_scan = _sample_scan_positions(scan_x_values, int(max_scan_markers))
    for src_x in sampled_scan:
        rec_x = src_x + tx_rx_offset
        ax.plot([src_x, rec_x], [source_z, receiver_z], color="#9aa6b2", linewidth=0.7, alpha=0.6, zorder=2)
    if sampled_scan:
        src_x = np.asarray(sampled_scan, dtype=np.float64)
        rec_x = src_x + tx_rx_offset
        ax.scatter(src_x, np.full_like(src_x, source_z), marker="^", s=40, color="#1b7837",
                   edgecolor="black", linewidth=0.4, label="Tx", zorder=6)
        ax.scatter(rec_x, np.full_like(rec_x, receiver_z), marker="v", s=40, color="#762a83",
                   edgecolor="black", linewidth=0.4, label="Rx", zorder=6)
        valid_pairs = [
            (float(src), float(rec))
            for src, rec in zip(src_x, rec_x)
            if 0.0 <= float(src) <= domain_x and 0.0 <= float(rec) <= domain_x
        ]
        if valid_pairs:
            src_ann, rec_ann = valid_pairs[len(valid_pairs) // 2]
            offset_y = max(6.0, min(concrete_top - 8.0, source_z - 10.0))
            ax.annotate(
                "",
                xy=(src_ann, offset_y),
                xytext=(rec_ann, offset_y),
                arrowprops={"arrowstyle": "<->", "color": "#3b3b3b", "lw": 1.0},
                zorder=7,
            )
            ax.text(
                0.5 * (src_ann + rec_ann),
                max(4.0, offset_y - 4.0),
                f"Tx-Rx {tx_rx_offset:.1f} mm",
                fontsize=8,
                ha="center",
                va="bottom",
                color="#333333",
                zorder=8,
            )

    truth_style = {
        "label": "true rebar",
        "edgecolor": "#111111",
        "facecolor": "#8a8f93",
        "linewidth": 1.2,
        "linestyle": "-",
        "alpha": 0.28,
        "zorder": 3,
        "annotate": True,
    }
    final_style = {
        "label": "selected/final rebar",
        "edgecolor": "#1b8f3a",
        "facecolor": "none",
        "linewidth": 2.2,
        "linestyle": "-",
        "alpha": 1.0,
        "zorder": 5,
        "annotate": False,
    }
    initial_style = {
        "label": "initial rebar",
        "edgecolor": "#4169e1",
        "facecolor": "none",
        "linewidth": 1.6,
        "linestyle": "--",
        "alpha": 0.9,
        "zorder": 4,
        "annotate": False,
    }
    _draw_rebars(
        ax,
        scene["truth"],
        truth_style,
        target_indices,
        concrete_top_mm=concrete_top,
        domain_x_mm=domain_x,
    )
    if scene.get("initial") and not specs_are_same(scene["initial"], scene["truth"]):
        _draw_rebars(ax, scene["initial"], initial_style, target_indices)
    if scene.get("final"):
        _draw_rebars(ax, scene["final"], final_style, target_indices)

    if scene["truth"]:
        annotated = None
        for spec in scene["truth"]:
            if int(spec["index"]) in target_indices:
                annotated = spec
                break
        if annotated is None:
            annotated = min(
                scene["truth"],
                key=lambda spec: float(spec["z_mm"]) - float(spec["radius_mm"]),
            )
        bar_top_mm = max(concrete_top, float(annotated["z_mm"]) - float(annotated["radius_mm"]))
        cover = max(0.0, bar_top_mm - concrete_top)
        right_x = float(annotated["x_mm"]) + float(annotated["radius_mm"]) + 40.0
        left_x = float(annotated["x_mm"]) - float(annotated["radius_mm"]) - 40.0
        x_ann = right_x if right_x <= domain_x - 55.0 else left_x
        x_ann = min(domain_x - 35.0, max(35.0, x_ann))
        ax.annotate(
            "",
            xy=(x_ann, concrete_top),
            xytext=(x_ann, bar_top_mm),
            arrowprops={"arrowstyle": "<->", "color": "#4d4d4d", "lw": 1.0},
            zorder=7,
        )
        ax.text(x_ann + 5.0, 0.5 * (concrete_top + bar_top_mm), f"{cover:.0f} mm bar-top cover",
                fontsize=8, va="center", color="#333333", zorder=8)

    subtitle = []
    if scene.get("sources") is not None:
        subtitle.append(f"{scene['sources']} sources")
    if scene.get("frequency_ghz") is not None:
        subtitle.append(f"{float(scene['frequency_ghz']):g} GHz")
    subtitle.append(f"Tx/Rx offset {tx_rx_offset:.1f} mm")
    title_text = title or scene.get("run_name") or "Experiment Scene Geometry"
    title_text = textwrap.fill(str(title_text), width=92)
    ax.set_title(f"{title_text}\n" + " | ".join(subtitle), fontsize=13, fontweight="bold")
    ax.set_xlabel("x [mm]")
    ax.set_ylabel("z [mm]")
    ax.set_xlim(0.0, domain_x)
    ax.set_ylim(domain_z, 0.0)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color="#d4d4d4", linewidth=0.6, linestyle="-", alpha=0.8)
    _add_unique_legend(ax)
    save_validated_figure(fig, str(save_path))
    plt.close(fig)
    return str(save_path)


def validate_scene_figure(path):
    """Return nonblank image metrics for a saved scene figure."""
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        arr = np.asarray(rgb)
    unique = len(np.unique(arr.reshape(-1, 3), axis=0))
    nonwhite = float(np.mean(np.any(arr < 250, axis=2)))
    if unique < 32 or nonwhite < 0.01:
        raise ValueError(f"Saved scene figure appears degenerate: {path}")
    return {
        "width_px": int(rgb.size[0]),
        "height_px": int(rgb.size[1]),
        "unique_colors": int(unique),
        "nonwhite_fraction": nonwhite,
    }


def validate_backfill_scene_metadata(scene):
    """Raise if a scene lacks enough machine-readable geometry for backfill."""
    if not scene.get("truth"):
        raise ValueError("missing true rebar geometry")
    if not scene.get("scan_x_values_mm"):
        raise ValueError("missing scan_x_values_mm Tx/Rx acquisition metadata")
    if float(scene.get("domain_x_mm", 0.0)) <= 0.0:
        raise ValueError("domain_x_mm must be positive")
    if float(scene.get("domain_z_mm", 0.0)) <= 0.0:
        raise ValueError("domain_z_mm must be positive")
    target_indices = [int(value) for value in scene.get("target_indices", [])]
    truth_indices = {int(spec["index"]) for spec in scene["truth"]}
    invalid_targets = sorted(set(target_indices) - truth_indices)
    if invalid_targets:
        raise ValueError(f"target indices outside truth geometry: {invalid_targets}")


def upsert_figure_notes(figures_dir, figure_name, summary_name):
    """Add or replace the scene-geometry section in FIGURE_NOTES.md."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    start = "<!-- system_scene_geometry:start -->"
    end = "<!-- system_scene_geometry:end -->"
    section = f"""{start}
## `{figure_name}` - experiment scene geometry

This figure is the system/context view for the experiment. It shows the
scaled x-z cross-section, concrete surface, transmitter/receiver (Tx/Rx)
aperture, true rebar locations, selected/final rebar locations, and target
highlight. Inspect it before the objective-margin plots to confirm which
physical scene the run tested.

Validation metadata for this figure is saved in `../data/{summary_name}`.
{end}
"""
    if notes_path.exists():
        text = notes_path.read_text(encoding="utf-8")
    else:
        text = "# Figure Notes\n"
    pattern = re.compile(
        rf"\n?{re.escape(start)}.*?{re.escape(end)}\n?",
        flags=re.DOTALL,
    )
    text = pattern.sub("\n", text).rstrip() + "\n\n" + section
    notes_path.write_text(text, encoding="utf-8")
    return str(notes_path)


def figure_notes_has_scene_section(figures_dir):
    """Return whether FIGURE_NOTES.md already has the scene geometry block."""
    notes_path = Path(figures_dir) / "FIGURE_NOTES.md"
    if not notes_path.exists():
        return False
    text = notes_path.read_text(encoding="utf-8")
    return (
        "<!-- system_scene_geometry:start -->" in text
        and "<!-- system_scene_geometry:end -->" in text
    )


def write_scene_artifacts(
        scene,
        outdir,
        label="system_scene_geometry",
        title=None,
        max_scan_markers=25,
        update_notes=True):
    """Write scene figure, validation summary, and optional figure notes."""
    outdir = Path(outdir)
    figures_dir = outdir / "figures"
    data_dir = outdir / "data"
    figures_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    figure_path = figures_dir / f"{label}.png"
    plot_scene(scene, figure_path, title=title, max_scan_markers=max_scan_markers)
    validation = validate_scene_figure(figure_path)
    summary_name = f"{label}_summary.json"
    summary_path = data_dir / summary_name
    summary_payload = {
        "scene": scene,
        "validation": validation,
        "paths": {
            "figure": str(figure_path),
        },
    }
    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary_payload, handle, indent=2)

    notes_path = None
    if update_notes:
        notes_path = upsert_figure_notes(figures_dir, figure_path.name, summary_name)

    return {
        "figure": str(figure_path),
        "summary": str(summary_path),
        "figure_notes": notes_path,
        "validation": validation,
    }


def _audit_row(
        run_dir,
        status,
        reason,
        summary_path=None,
        figure_path=None,
        scene_summary_path=None,
        figure_notes_path=None,
        validation=None):
    validation = validation or {}
    return {
        "run_dir": str(run_dir),
        "run_number": _run_number(run_dir),
        "summary_path": "" if summary_path is None else str(summary_path),
        "status": status,
        "reason": reason,
        "figure_path": "" if figure_path is None else str(figure_path),
        "scene_summary_path": "" if scene_summary_path is None else str(scene_summary_path),
        "figure_notes_path": "" if figure_notes_path is None else str(figure_notes_path),
        "width_px": validation.get("width_px", ""),
        "height_px": validation.get("height_px", ""),
        "unique_colors": validation.get("unique_colors", ""),
        "nonwhite_fraction": validation.get("nonwhite_fraction", ""),
    }


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


def _write_audit_json(rows, audit_json):
    path = Path(audit_json)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "rows": rows,
        "counts": audit_counts(rows),
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
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
        "figure_path",
        "scene_summary_path",
        "figure_notes_path",
        "width_px",
        "height_px",
        "unique_colors",
        "nonwhite_fraction",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})
    return str(path)


def audit_counts(rows):
    """Return row counts grouped by status."""
    counts = {}
    for row in rows:
        status = row.get("status", "")
        counts[status] = counts.get(status, 0) + 1
    return counts


def process_summary_for_backfill(
        run_dir,
        summary_path,
        label="system_scene_geometry",
        title=None,
        max_scan_markers=25,
        update_notes=True,
        refresh_existing=False):
    """Generate or skip one summary-backed scene figure with audit metadata."""
    run_dir = Path(run_dir)
    summary_path = Path(summary_path)
    figures_dir = run_dir / "figures"
    data_dir = run_dir / "data"
    figure_path = figures_dir / f"{label}.png"
    scene_summary_path = data_dir / f"{label}_summary.json"
    notes_path = figures_dir / "FIGURE_NOTES.md"

    if figure_path.exists() and not refresh_existing:
        try:
            validation = validate_scene_figure(figure_path)
        except Exception as exc:
            existing_reason = f"existing figure invalid: {exc}"
        else:
            has_summary = scene_summary_path.exists()
            has_notes = (not update_notes) or figure_notes_has_scene_section(figures_dir)
            if has_summary and has_notes:
                return _audit_row(
                    run_dir,
                    "skipped",
                    "existing valid scene artifacts",
                    summary_path=summary_path,
                    figure_path=figure_path,
                    scene_summary_path=scene_summary_path,
                    figure_notes_path=notes_path if notes_path.exists() else None,
                    validation=validation,
                )
            missing = []
            if not has_summary:
                missing.append(scene_summary_path.name)
            if not has_notes:
                missing.append(notes_path.name)
            existing_reason = "existing figure missing companion artifacts: " + ", ".join(missing)
    else:
        existing_reason = "refresh requested" if figure_path.exists() else "missing scene artifacts"

    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        scene = scene_from_summary(summary, summary_path)
        validate_backfill_scene_metadata(scene)
        artifacts = write_scene_artifacts(
            scene,
            run_dir,
            label=label,
            title=title,
            max_scan_markers=max_scan_markers,
            update_notes=update_notes,
        )
    except Exception as exc:
        return _audit_row(
            run_dir,
            "skipped",
            f"incompatible metadata: {exc}",
            summary_path=summary_path,
            figure_path=figure_path if figure_path.exists() else None,
            scene_summary_path=scene_summary_path if scene_summary_path.exists() else None,
            figure_notes_path=notes_path if notes_path.exists() else None,
        )

    status = "refreshed" if figure_path.exists() and existing_reason != "missing scene artifacts" else "generated"
    return _audit_row(
        run_dir,
        status,
        existing_reason,
        summary_path=summary_path,
        figure_path=artifacts["figure"],
        scene_summary_path=artifacts["summary"],
        figure_notes_path=artifacts["figure_notes"],
        validation=artifacts["validation"],
    )


def backfill_scene_artifacts(
        experiments_root,
        label="system_scene_geometry",
        title=None,
        max_scan_markers=25,
        update_notes=True,
        refresh_existing=False,
        min_run_number=None,
        max_run_number=None,
        limit=None,
        audit_json=None,
        audit_csv=None):
    """Backfill summary-backed scene figures newest first and write audits."""
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
            title=title,
            max_scan_markers=max_scan_markers,
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


def infer_outdir(summary_path, outdir):
    """Infer experiment output directory from a summary path when possible."""
    if outdir:
        return Path(outdir)
    if summary_path is None:
        raise ValueError("--outdir is required when --summary is not supplied")
    path = Path(summary_path)
    if path.parent.name == "data":
        return path.parent.parent
    return path.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, default=None,
                        help="Path to multi_rebar_coordinate_optimizer_summary.json.")
    parser.add_argument("--outdir", default=None,
                        help="Experiment output directory. Defaults to summary parent.")
    parser.add_argument("--label", default="system_scene_geometry")
    parser.add_argument("--title", default=None)
    parser.add_argument("--max-scan-markers", type=int, default=25)
    parser.add_argument("--skip-figure-notes", action="store_true")
    parser.add_argument("--backfill-root", type=Path, default=None,
                        help="Backfill numbered experiment directories under this root.")
    parser.add_argument("--refresh-existing", action="store_true",
                        help="Regenerate existing scene artifacts during --backfill-root.")
    parser.add_argument("--min-run-number", type=int, default=None)
    parser.add_argument("--max-run-number", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None,
                        help="Maximum numbered experiment directories to audit in backfill mode.")
    parser.add_argument("--audit-json", type=Path, default=None)
    parser.add_argument("--audit-csv", type=Path, default=None)

    parser.add_argument("--run-name", default="")
    parser.add_argument("--x-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--z-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--radius-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--final-x-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--final-z-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--final-radius-values-mm", type=parse_vector_mm, default=None)
    parser.add_argument("--target-indices", type=parse_indices, default=[])
    parser.add_argument("--scan-x-values-mm", type=parse_vector_mm, default=[])
    parser.add_argument("--tx-rx-offset-mm", type=float, default=cfg.TX_RX_OFFSET * 1000.0)
    parser.add_argument("--source-z-mm", type=float, default=cfg.TX_Z * 1000.0)
    parser.add_argument("--receiver-z-mm", type=float, default=cfg.RX_Z * 1000.0)
    parser.add_argument("--concrete-top-mm", type=float, default=cfg.CONCRETE_TOP * 1000.0)
    parser.add_argument("--domain-x-mm", type=float, default=cfg.DOMAIN_X * 1000.0)
    parser.add_argument("--domain-z-mm", type=float, default=cfg.DOMAIN_Z * 1000.0)
    parser.add_argument("--frequency-ghz", type=float, default=None)
    args = parser.parse_args()

    if args.backfill_root is not None:
        result = backfill_scene_artifacts(
            args.backfill_root,
            label=args.label,
            title=args.title,
            max_scan_markers=args.max_scan_markers,
            update_notes=not args.skip_figure_notes,
            refresh_existing=args.refresh_existing,
            min_run_number=args.min_run_number,
            max_run_number=args.max_run_number,
            limit=args.limit,
            audit_json=args.audit_json,
            audit_csv=args.audit_csv,
        )
        print("Backfill scene visualization audit complete.")
        print(json.dumps({
            "counts": result["counts"],
            "audit_paths": result["audit_paths"],
        }, indent=2))
        return

    if args.summary is not None:
        summary = json.loads(args.summary.read_text(encoding="utf-8"))
        scene = scene_from_summary(summary, args.summary)
    else:
        if args.x_values_mm is None or args.z_values_mm is None or args.radius_values_mm is None:
            raise ValueError("--x-values-mm, --z-values-mm, and --radius-values-mm are required")
        scene = explicit_scene(args)

    artifacts = write_scene_artifacts(
        scene,
        infer_outdir(args.summary, args.outdir),
        label=args.label,
        title=args.title,
        max_scan_markers=args.max_scan_markers,
        update_notes=not args.skip_figure_notes,
    )

    print(f"Wrote scene figure: {artifacts['figure']}")
    print(f"Wrote scene summary: {artifacts['summary']}")
    if artifacts["figure_notes"]:
        print(f"Updated figure notes: {artifacts['figure_notes']}")
    print(json.dumps(artifacts["validation"], indent=2))


if __name__ == "__main__":
    main()
