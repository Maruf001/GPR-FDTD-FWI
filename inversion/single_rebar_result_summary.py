"""Utilities for summarizing saved single-rebar experiment results."""
import csv
import json
from pathlib import Path


def _safe_get(mapping, *keys, default=None):
    current = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def _primary_value(mapping):
    if not isinstance(mapping, dict) or not mapping:
        return None
    first_key = sorted(mapping.keys())[0]
    return mapping[first_key]


def experiment_label(summary_path):
    """Return the numbered experiment directory name for a summary path."""
    path = Path(summary_path)
    for parent in path.parents:
        if parent.name and parent.name[0:3].isdigit():
            return parent.name
    return path.parent.name


def distinct_radius_margin(top_candidates):
    """
    Compute the margin between the best candidate and next distinct radius.

    Duplicate z/x candidates at the same radius are skipped because they do not
    quantify radius ambiguity.
    """
    if not top_candidates:
        return {
            "best_radius_mm": None,
            "best_radius_misfit": None,
            "next_radius_mm": None,
            "next_radius_misfit": None,
            "radius_margin_abs": None,
            "radius_margin_rel": None,
        }

    ordered = sorted(top_candidates, key=lambda item: item["misfit"])
    best = ordered[0]
    best_radius = float(best["params"]["radius_mm"])
    best_misfit = float(best["misfit"])
    next_item = None
    for item in ordered[1:]:
        radius = float(item["params"]["radius_mm"])
        if abs(radius - best_radius) > 1e-9:
            next_item = item
            break

    if next_item is None:
        return {
            "best_radius_mm": best_radius,
            "best_radius_misfit": best_misfit,
            "next_radius_mm": None,
            "next_radius_misfit": None,
            "radius_margin_abs": None,
            "radius_margin_rel": None,
        }

    next_misfit = float(next_item["misfit"])
    margin = next_misfit - best_misfit
    return {
        "best_radius_mm": best_radius,
        "best_radius_misfit": best_misfit,
        "next_radius_mm": float(next_item["params"]["radius_mm"]),
        "next_radius_misfit": next_misfit,
        "radius_margin_abs": margin,
        "radius_margin_rel": margin / max(abs(best_misfit), 1e-12),
    }


def summarize_single_rebar_summary(summary_path):
    """Flatten one `single_rebar_summary.json` into comparable metrics."""
    path = Path(summary_path)
    with path.open("r", encoding="utf-8") as handle:
        summary = json.load(handle)

    recovered = summary.get("recovered", {})
    truth = summary.get("true", {})
    optimizer_final = summary.get("optimizer_final", {})
    noise = summary.get("observed_noise") or {}
    grid_polish = summary.get("grid_polish") or {}
    top_candidates = grid_polish.get("top_candidates") or []
    margin = distinct_radius_margin(top_candidates)

    nrms_data = _primary_value(summary.get("nrms_data_by_frequency"))
    trace_shift = _primary_value(summary.get("trace_shift_by_frequency"))

    row = {
        "experiment": experiment_label(path),
        "summary_path": str(path),
        "backend": summary.get("backend"),
        "optimizer": summary.get("optimizer"),
        "frequencies_ghz": ",".join(str(value) for value in summary.get("frequencies_ghz", [])),
        "noise_fraction": noise.get("rms_fraction", 0.0),
        "noise_seed": noise.get("seed"),
        "objective_bandpass": summary.get("objective_bandpass"),
        "objective_frequency_weights": summary.get("objective_frequency_weights"),
        "grid_polish_enabled": bool(grid_polish),
        "grid_polish_evaluations": grid_polish.get("evaluations"),
        "elapsed_time_s": summary.get("elapsed_time_s"),
        "best_misfit": summary.get("best_misfit"),
        "nrms_data_primary": nrms_data,
        "nrms_model": summary.get("nrms_model"),
        "recovered_x_mm": recovered.get("x_mm"),
        "recovered_z_mm": recovered.get("z_mm"),
        "recovered_radius_mm": recovered.get("radius_mm"),
        "optimizer_radius_mm": optimizer_final.get("radius_mm"),
        "true_x_mm": truth.get("x_mm"),
        "true_z_mm": truth.get("z_mm"),
        "true_radius_mm": truth.get("radius_mm"),
        "x_error_mm": None,
        "z_error_mm": None,
        "radius_error_mm": None,
        "nrccc_primary": _safe_get(trace_shift, "nrccc_fraction_lt_half_period"),
        "max_rccc_primary": _safe_get(trace_shift, "max_rccc"),
    }
    for name in ("x", "z", "radius"):
        recovered_value = recovered.get(f"{name}_mm")
        true_value = truth.get(f"{name}_mm")
        if recovered_value is not None and true_value is not None:
            row[f"{name}_error_mm"] = float(recovered_value) - float(true_value)

    row.update(margin)
    return row


def find_single_rebar_summaries(root):
    """Find saved single-rebar summary JSON files under an experiment root."""
    return sorted(Path(root).glob("*/data/single_rebar_summary.json"))


def write_summary_csv(rows, path):
    """Write flattened rows to CSV."""
    rows = list(rows)
    if not rows:
        raise ValueError("no rows to write")
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
