"""Confidence summaries for ranked inversion candidates."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConfidenceThresholds:
    """Thresholds for labeling best-vs-next-radius candidate separation."""

    moderate_abs: float = 5.0e-4
    moderate_rel: float = 5.0e-3
    strong_abs: float = 1.0e-3
    strong_rel: float = 1.0e-2
    ambiguity_rel: float = 1.5e-2

    def as_dict(self):
        return {
            "moderate_abs": self.moderate_abs,
            "moderate_rel": self.moderate_rel,
            "strong_abs": self.strong_abs,
            "strong_rel": self.strong_rel,
            "ambiguity_rel": self.ambiguity_rel,
        }


def confidence_label(radius_margin_abs, radius_margin_rel, thresholds=None):
    """Return a conservative confidence label for a distinct-radius margin."""
    thresholds = thresholds or ConfidenceThresholds()
    if radius_margin_abs is None or radius_margin_rel is None:
        return "missing"
    margin_abs = float(radius_margin_abs)
    margin_rel = float(radius_margin_rel)
    if margin_abs <= 0.0 or margin_rel <= 0.0:
        return "ambiguous"
    if margin_abs >= thresholds.strong_abs and margin_rel >= thresholds.strong_rel:
        return "strong"
    if margin_abs >= thresholds.moderate_abs and margin_rel >= thresholds.moderate_rel:
        return "moderate"
    return "weak"


def _float_or_none(value):
    if value is None:
        return None
    return float(value)


def _params(candidate):
    if not isinstance(candidate, dict):
        return {}
    params = candidate.get("params")
    return params if isinstance(params, dict) else {}


def _source_profile(candidate):
    if not isinstance(candidate, dict):
        return {}
    profile = candidate.get("source_profile")
    return profile if isinstance(profile, dict) else {}


def _same_position(params, reference, tol_mm):
    for key in ("x_mm", "z_mm"):
        if key not in params or key not in reference:
            return True
        if abs(float(params[key]) - float(reference[key])) > tol_mm:
            return False
    return True


def first_competing_geometry(top_candidates, position_tol_mm=1.0e-9):
    """Return the first top candidate that moves in x or z from the best."""
    if not top_candidates:
        return None
    best_params = _params(top_candidates[0])
    if "x_mm" not in best_params and "z_mm" not in best_params:
        return None
    for candidate in top_candidates[1:]:
        params = _params(candidate)
        if not _same_position(params, best_params, position_tol_mm):
            return candidate
    return None


def ambiguity_interval(top_candidates, thresholds=None):
    """
    Return x/z/r spans for candidates close enough to the best objective.

    The default tolerance is intentionally conservative for noisy GPR radius
    reporting: it includes candidates within 1.5% of the best objective, which
    captures the recurring deeper/larger-radius branch seen in Stage 6.
    """
    thresholds = thresholds or ConfidenceThresholds()
    if not top_candidates:
        return {
            "ambiguity_candidate_count": 0,
            "ambiguity_misfit_threshold": None,
            "ambiguity_x_min_mm": None,
            "ambiguity_x_max_mm": None,
            "ambiguity_z_min_mm": None,
            "ambiguity_z_max_mm": None,
            "ambiguity_radius_min_mm": None,
            "ambiguity_radius_max_mm": None,
        }

    ordered = sorted(top_candidates, key=lambda item: item["misfit"])
    best_misfit = float(ordered[0]["misfit"])
    threshold = best_misfit + abs(best_misfit) * float(thresholds.ambiguity_rel)
    close = [
        item
        for item in ordered
        if float(item["misfit"]) <= threshold
    ]

    def values_for(key):
        values = [
            _float_or_none(_params(item).get(key))
            for item in close
            if _params(item).get(key) is not None
        ]
        return values

    x_values = values_for("x_mm")
    z_values = values_for("z_mm")
    radius_values = values_for("radius_mm")
    return {
        "ambiguity_candidate_count": len(close),
        "ambiguity_misfit_threshold": threshold,
        "ambiguity_x_min_mm": None if not x_values else min(x_values),
        "ambiguity_x_max_mm": None if not x_values else max(x_values),
        "ambiguity_z_min_mm": None if not z_values else min(z_values),
        "ambiguity_z_max_mm": None if not z_values else max(z_values),
        "ambiguity_radius_min_mm": None if not radius_values else min(radius_values),
        "ambiguity_radius_max_mm": None if not radius_values else max(radius_values),
    }


def summarize_case_confidence(run_name, case_label, case_result, summary_meta=None, thresholds=None):
    """Flatten one ranked case into confidence and ambiguity fields."""
    summary_meta = summary_meta or {}
    thresholds = thresholds or ConfidenceThresholds()
    top_candidates = list(case_result.get("top_candidates") or [])
    best = top_candidates[0] if top_candidates else {}
    best_params = _params(best)
    best_profile = _source_profile(best)
    margin = case_result.get("margin") or {}
    competing = first_competing_geometry(top_candidates)
    competing_params = _params(competing)
    ambiguity = ambiguity_interval(top_candidates, thresholds)

    margin_abs = margin.get("radius_margin_abs")
    margin_rel = margin.get("radius_margin_rel")
    label = confidence_label(margin_abs, margin_rel, thresholds)
    row = {
        "run_name": run_name,
        "case_label": case_label,
        "backend": summary_meta.get("backend"),
        "grid_step_mm": summary_meta.get("grid_step_mm"),
        "target_rebar_index": summary_meta.get("target_rebar_index"),
        "candidate_count": summary_meta.get("candidate_count"),
        "case_count": summary_meta.get("case_count"),
        "best_x_mm": best_params.get("x_mm"),
        "best_z_mm": best_params.get("z_mm"),
        "best_radius_mm": margin.get("best_radius_mm", best_params.get("radius_mm")),
        "next_radius_mm": margin.get("next_radius_mm"),
        "radius_margin_abs": margin_abs,
        "radius_margin_rel": margin_rel,
        "confidence_label": label,
        "fallback_warning": "radius_weak_confidence" if label in ("weak", "ambiguous") else "",
        "best_misfit": margin.get("best_radius_misfit", best.get("misfit")),
        "next_radius_misfit": margin.get("next_radius_misfit"),
        "competing_geometry_x_mm": competing_params.get("x_mm"),
        "competing_geometry_z_mm": competing_params.get("z_mm"),
        "competing_geometry_radius_mm": competing_params.get("radius_mm"),
        "competing_geometry_misfit": None if competing is None else competing.get("misfit"),
        "source_frequency_scale": best_profile.get("frequency_scale"),
        "source_time_shift_ps": best_profile.get("time_shift_ps"),
        "source_amplitude_scale": best_profile.get("amplitude_scale"),
    }
    row.update(ambiguity)
    return row


def summarize_profile_summary(summary, thresholds=None):
    """Return confidence rows from a saved profile-style summary dictionary."""
    thresholds = thresholds or ConfidenceThresholds()
    run_name = summary.get("run_name")
    meta = {
        "backend": summary.get("backend"),
        "grid_step_mm": summary.get("grid_step_mm"),
        "target_rebar_index": summary.get("target_rebar_index"),
        "candidate_count": summary.get("candidate_count"),
        "case_count": summary.get("case_count"),
    }
    results = summary.get("results") or {}
    return [
        summarize_case_confidence(run_name, label, result, meta, thresholds)
        for label, result in results.items()
    ]


def load_profile_confidence_rows(summary_path, thresholds=None):
    """Load a profile-style summary JSON and return confidence rows."""
    with Path(summary_path).open("r", encoding="utf-8") as handle:
        summary = json.load(handle)
    rows = summarize_profile_summary(summary, thresholds)
    for row in rows:
        row["summary_path"] = str(summary_path)
    return rows


def write_confidence_csv(rows, path):
    """Write confidence rows to CSV."""
    rows = list(rows)
    if not rows:
        raise ValueError("no confidence rows to write")
    fieldnames = list(rows[0].keys())
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
