"""Pure helpers for reporting-first multi-rebar coordinate searches."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoordinateState:
    """Current x/z/r estimate for a multi-rebar coordinate search."""

    x_values_mm: tuple[float, ...]
    z_values_mm: tuple[float, ...]
    radii_mm: tuple[float, ...]

    def __post_init__(self):
        if not (
                len(self.x_values_mm)
                == len(self.z_values_mm)
                == len(self.radii_mm)):
            raise ValueError("x, z, and radius values must have the same length")
        if len(self.x_values_mm) == 0:
            raise ValueError("at least one rebar is required")

    @classmethod
    def from_lists(cls, x_values_mm, z_values_mm, radii_mm):
        return cls(
            tuple(float(value) for value in x_values_mm),
            tuple(float(value) for value in z_values_mm),
            tuple(float(value) for value in radii_mm),
        )

    def as_dict(self):
        return {
            "x_values_mm": list(self.x_values_mm),
            "z_values_mm": list(self.z_values_mm),
            "radii_mm": list(self.radii_mm),
        }


def offset_window(center_mm, offsets_mm):
    """Return sorted unique window values around a center."""
    values = sorted({
        round(float(center_mm) + float(offset), 9)
        for offset in offsets_mm
    })
    if not values:
        raise ValueError("offset window must contain at least one value")
    return values


def target_window(state, target_index, x_offsets_mm, z_offsets_mm, radius_offsets_mm):
    """Build per-target x/z/r windows around the current coordinate state."""
    if target_index < 0 or target_index >= len(state.x_values_mm):
        raise ValueError("target_index must be a valid zero-based rebar index")
    return {
        "target_index": int(target_index),
        "x_values_mm": offset_window(state.x_values_mm[target_index], x_offsets_mm),
        "z_values_mm": offset_window(state.z_values_mm[target_index], z_offsets_mm),
        "radius_values_mm": offset_window(state.radii_mm[target_index], radius_offsets_mm),
    }


def update_state_from_candidate(state, candidate_params):
    """Return a new state after applying one target candidate."""
    target_index = int(candidate_params["target_index"])
    if target_index < 0 or target_index >= len(state.x_values_mm):
        raise ValueError("candidate target_index is outside the state")
    x_values = list(state.x_values_mm)
    z_values = list(state.z_values_mm)
    radii = list(state.radii_mm)
    x_values[target_index] = float(candidate_params["x_mm"])
    z_values[target_index] = float(candidate_params["z_mm"])
    radii[target_index] = float(candidate_params["radius_mm"])
    return CoordinateState.from_lists(x_values, z_values, radii)


def choose_case_label(case_labels, preferred_case_label=None):
    """Choose the case used to update the coordinate state."""
    labels = list(case_labels)
    if not labels:
        raise ValueError("case_labels must be non-empty")
    if preferred_case_label is None:
        return labels[0]
    if preferred_case_label not in labels:
        raise ValueError(f"preferred case {preferred_case_label!r} not found")
    return preferred_case_label


def _number_or_none(value):
    if value in ("", None):
        return None
    return float(value)


def is_weak_high_radius_branch(row, radius_tol_mm=1.0e-9):
    """
    Return True when a weak row selects the high-radius ambiguity endpoint.

    This is a conservative trigger for a confirmatory revisit. It does not say
    the high-radius branch is wrong; it says the optimizer should not commit it
    without another look because the reported ambiguity interval includes a
    smaller-radius branch.
    """
    if not row.get("fallback_warning"):
        return False
    best_radius = _number_or_none(row.get("best_radius_mm"))
    ambiguity_min = _number_or_none(row.get("ambiguity_radius_min_mm"))
    ambiguity_max = _number_or_none(row.get("ambiguity_radius_max_mm"))
    if best_radius is None or ambiguity_min is None or ambiguity_max is None:
        return False
    if ambiguity_max - ambiguity_min <= float(radius_tol_mm):
        return False
    return best_radius >= ambiguity_max - float(radius_tol_mm)


def weak_high_radius_revisit_targets(confidence_rows, case_label):
    """Return target indices that need a high-radius-branch revisit."""
    targets = []
    seen = set()
    for row in confidence_rows:
        if row.get("case_label") != case_label:
            continue
        target_index = int(row["step_target_index"])
        if target_index in seen:
            continue
        if is_weak_high_radius_branch(row):
            targets.append(target_index)
            seen.add(target_index)
    return targets


def interval_offsets(center_mm, lower_mm, upper_mm, step_mm):
    """Return offsets from center that cover an interval on a fixed step."""
    center = float(center_mm)
    lower = float(lower_mm)
    upper = float(upper_mm)
    step = float(step_mm)
    if step <= 0.0:
        raise ValueError("step_mm must be positive")
    if lower > upper:
        raise ValueError("interval lower bound must be <= upper bound")
    count = int(round((upper - lower) / step))
    values = [round(lower + idx * step, 10) for idx in range(count + 1)]
    if not values or values[-1] < upper - 1.0e-9:
        values.append(round(upper, 10))
    offsets = sorted({round(value - center, 10) for value in values})
    if 0.0 not in offsets and lower <= center <= upper:
        offsets.append(0.0)
        offsets = sorted(set(offsets))
    return offsets


def revisit_radius_offsets_from_row(row, current_radius_mm, step_mm=0.2):
    """Build radius offsets for a confirmatory revisit from an ambiguity row."""
    lower = _number_or_none(row.get("ambiguity_radius_min_mm"))
    upper = _number_or_none(row.get("ambiguity_radius_max_mm"))
    if lower is None or upper is None:
        return [0.0]
    return interval_offsets(current_radius_mm, lower, upper, step_mm)


def step_report(pass_index, target_index, case_label, state_before, state_after, result):
    """Create a compact serializable report for one coordinate update step."""
    best = result["top_candidates"][0]
    return {
        "pass_index": int(pass_index),
        "target_index": int(target_index),
        "update_case_label": case_label,
        "state_before": state_before.as_dict(),
        "state_after": state_after.as_dict(),
        "best_candidate": best,
        "margin": dict(result["margin"]),
    }
