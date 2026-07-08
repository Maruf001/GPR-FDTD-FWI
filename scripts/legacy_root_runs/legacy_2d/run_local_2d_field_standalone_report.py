"""Generate the PI-facing local 2D and field readiness report notebook."""

from __future__ import annotations

import argparse
import base64
import json
import math
import re
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import nbformat as nbf
import numpy as np
import pandas as pd
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


REPORT_DATE = "2026-06-19"
REPORT_STEM = "015_2026-06-19_local_2d_field_standalone_report"
NOTEBOOK_PATH = Path("docs/update/summary") / f"{REPORT_STEM}.ipynb"

PRIOR_NOTEBOOK = Path("docs/update/summary/007_2026-06-17_experiment_700_1259_holistic_evaluation.ipynb")
PRIOR_DATA = Path("outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data")
SUPPORT_ROOT = Path("outputs/summary_tables/133_local_2d_field_holistic_report_post_checkpoint")
SUPPORT_DATA = SUPPORT_ROOT / "data"
SUPPORT_FIGURES = SUPPORT_ROOT / "figures"
REPORT_FIGURES = SUPPORT_FIGURES / "pi_report"
EXPERIMENT_ROOT = Path("outputs/experiments")

SYNTHETIC_SCENE = Path(
    "outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
) / "figures" / "system_scene_geometry.png"
CUTOFF = 5.0e-4


def parse_run_id(name: str) -> int | None:
    match = re.match(r"^(\d+)_", name)
    return int(match.group(1)) if match else None


def parse_number(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text)
    if not match:
        return None
    token = match.group(1).replace("p", ".")
    return float(token)


def parse_int(pattern: str, text: str) -> int | None:
    value = parse_number(pattern, text)
    return int(value) if value is not None else None


def state_linf_mm(state: dict, truth_x: list[float], truth_z: list[float], truth_r: list[float]) -> float:
    values: list[float] = []
    for key, truth in [("x_values_mm", truth_x), ("z_values_mm", truth_z), ("radii_mm", truth_r)]:
        observed = state.get(key) or []
        values.extend(abs(float(a) - float(b)) for a, b in zip(observed, truth))
    return max(values) if values else math.nan


def target_error_mm(row: pd.Series, summary: dict) -> float:
    target = int(row.get("target_rebar_index", row.get("target", 0)))
    true_x = summary.get("true_x_values_mm") or []
    true_z = summary.get("true_z_values_mm") or []
    true_r = summary.get("truth_radius_values_mm") or []
    if target >= len(true_x) or target >= len(true_z) or target >= len(true_r):
        return math.nan
    errors = [
        abs(float(row["best_x_mm"]) - float(true_x[target])),
        abs(float(row["best_z_mm"]) - float(true_z[target])),
    ]
    if "best_radius_mm" in row and not pd.isna(row["best_radius_mm"]):
        errors.append(abs(float(row["best_radius_mm"]) - float(true_r[target])))
    return max(errors)


def md_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, (float, np.floating)):
        if value != 0 and abs(value) < 0.01:
            return f"{value:.3e}"
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(df: pd.DataFrame, columns: list[tuple[str, str]], max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows._"
    selected = df.loc[:, [key for key, _ in columns]].head(max_rows) if max_rows else df.loc[:, [key for key, _ in columns]]
    header = "| " + " | ".join(label for _, label in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    rows = [
        "| " + " | ".join(md_value(row[key]) for key, _ in columns) + " |"
        for _, row in selected.iterrows()
    ]
    if max_rows is not None and len(df) > max_rows:
        rows.append(f"| ... | {len(df) - max_rows} more rows omitted; see source tables. |")
    return "\n".join([header, sep] + rows)


def attachment_image_cell(figure_number: int, title: str, path: Path, caption: str) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    attachment_name = f"figure_{figure_number:02d}_{path.name}"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    cell = nbf.v4.new_markdown_cell(
        f"### Figure {figure_number}. {title}\n\n"
        f"![Figure {figure_number}. {title}](attachment:{attachment_name})\n\n"
        f"*Figure {figure_number}. {caption}*"
    )
    cell["attachments"] = {attachment_name: {"image/png": encoded}}
    return cell


def decode_experiment_name(name: str) -> pd.DataFrame:
    rows = [
        {
            "term": "local2d",
            "meaning": "A local two-dimensional synthetic experiment, not a measured-field run.",
        },
        {
            "term": "fixed_radius",
            "meaning": "The rebar radii are treated as known values, so the experiment isolates position ambiguity.",
        },
        {
            "term": "target2",
            "meaning": "The final optimization step is focused on the right rebar in the three-rebar scene.",
        },
        {
            "term": "close14",
            "meaning": (
                "The center and right rebar centers are 14 mm apart in horizontal position. "
                "Here target1 has radius 6 mm and target2 has radius 8 mm, so their radii sum to 14 mm. "
                "That makes this a deliberately hard close-spacing case. It is not the transmitter-receiver offset."
            ),
        },
        {
            "term": "seed21",
            "meaning": "The repeatable random-noise setting used for this synthetic test.",
        },
        {
            "term": "nominal",
            "meaning": "The run uses the intended source model, rather than a source-mismatch stress test.",
        },
        {
            "term": "gpu",
            "meaning": "The guarded run used the local graphics processing unit while staying under the resource limits.",
        },
    ]
    return pd.DataFrame([row for row in rows if row["term"] in name])


def discover_current_coordinate_rows(run_min: int = 1260) -> pd.DataFrame:
    rows: list[dict] = []
    for csv_path in sorted(EXPERIMENT_ROOT.glob("*/data/coordinate_confidence_report.csv")):
        run_dir = csv_path.parents[1]
        run_id = parse_run_id(run_dir.name)
        if run_id is None or run_id < run_min:
            continue
        summary_path = run_dir / "data" / "multi_rebar_coordinate_optimizer_summary.json"
        summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
        frame = pd.read_csv(csv_path)
        for _, row in frame.iterrows():
            run_name = str(row.get("run_name") or run_dir.name)
            target = int(row.get("target_rebar_index", parse_int(r"_target(\d+)", run_name) or 0))
            scenario = "variable-depth/radius"
            for token in ["close10", "close12", "close14", "close50"]:
                if token in run_name:
                    scenario = token
                    break
            radius_margin = pd.to_numeric(pd.Series([row.get("radius_margin_abs")]), errors="coerce").iloc[0]
            best_misfit = pd.to_numeric(pd.Series([row.get("best_misfit")]), errors="coerce").iloc[0]
            competing_misfit = pd.to_numeric(pd.Series([row.get("competing_geometry_misfit")]), errors="coerce").iloc[0]
            rows.append(
                {
                    "run_id": run_id,
                    "run_name": run_name,
                    "scenario": scenario,
                    "target": target,
                    "sources": parse_int(r"_sources(\d+)", run_name),
                    "tx_rx_offset_mm": parse_number(r"_txrx([0-9p.]+)", run_name),
                    "linear_receiver": "linear_receiver" in run_name,
                    "noise_label": "noise" if "noise" in run_name else "default noise",
                    "best_misfit": best_misfit,
                    "competing_geometry_misfit": competing_misfit,
                    "competitor_gap_abs": competing_misfit - best_misfit if pd.notna(competing_misfit) else math.nan,
                    "base_margin": radius_margin,
                    "accepted": bool(pd.notna(radius_margin) and radius_margin >= CUTOFF),
                    "ambiguity_candidate_count": pd.to_numeric(
                        pd.Series([row.get("ambiguity_candidate_count")]), errors="coerce"
                    ).iloc[0],
                    "candidate_count": pd.to_numeric(pd.Series([row.get("candidate_count")]), errors="coerce").iloc[0],
                    "target_error_mm": target_error_mm(row, summary) if summary else math.nan,
                    "is_fixed_radius": pd.isna(radius_margin),
                    "path": str(run_dir),
                }
            )
    return pd.DataFrame(rows).sort_values(["run_id", "target"])


def fixed_radius_stage_rows() -> pd.DataFrame:
    stages = [
        (1340, "source-mismatch seed refine"),
        (1341, "repaired exact-radius seed refine"),
        (1342, "counterfactual target2 unlock"),
        (1357, "second pass before lock"),
        (1358, "target2 unlock after target1 lock"),
    ]
    rows: list[dict] = []
    for run_id, label in stages:
        matches = list(EXPERIMENT_ROOT.glob(f"{run_id}_*/data/multi_rebar_coordinate_optimizer_summary.json"))
        if not matches:
            continue
        summary = json.loads(matches[0].read_text())
        truth_x = [float(v) for v in summary["true_x_values_mm"]]
        truth_z = [float(v) for v in summary["true_z_values_mm"]]
        truth_r = [float(v) for v in summary["truth_radius_values_mm"]]
        rows.append(
            {
                "run_id": run_id,
                "label": label,
                "initial_linf_error_mm": state_linf_mm(summary["initial_state"], truth_x, truth_z, truth_r),
                "final_linf_error_mm": state_linf_mm(summary["final_state"], truth_x, truth_z, truth_r),
                "run_name": summary.get("run_name", matches[0].parents[1].name),
            }
        )
    return pd.DataFrame(rows)


def load_inputs() -> dict:
    return {
        "prior_coordinate": pd.read_csv(PRIOR_DATA / "coordinate_run_summary_700_1259.csv"),
        "prior_policy": pd.read_csv(PRIOR_DATA / "intervention_series_policy_700_1259.csv"),
        "key_metrics": pd.read_csv(SUPPORT_DATA / "local_2d_field_holistic_key_metrics.csv"),
        "result_metrics": pd.read_csv(SUPPORT_DATA / "source_table_pack_result_metrics.csv"),
        "current_coordinate": discover_current_coordinate_rows(),
        "fixed_radius_stages": fixed_radius_stage_rows(),
        "endpoint_rows": pd.read_csv(SUPPORT_DATA / "synthetic_fixed_radius_endpoint_rows.csv"),
        "field_gates": pd.read_csv(
            "outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path/data/field_controlled_collection_gate_critical_path.csv"
        ),
        "field_phases": pd.read_csv(
            "outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path/data/field_controlled_collection_phase_plan.csv"
        ),
        "field_actions": pd.read_csv(
            "outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path/data/field_controlled_collection_critical_actions.csv"
        ),
        "claim_rows": pd.read_csv(
            "outputs/summary_tables/132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation/data/local_2d_field_manuscript_claim_table.csv"
        ),
        "lock_candidates": pd.read_csv(
            "outputs/summary_tables/130_local_2d_detector_fixed_radius_locking_policy_design/data/local_2d_detector_fixed_radius_lock_candidates.csv"
        ),
        "validation_rows": pd.read_csv(
            "outputs/summary_tables/131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe/data/local_2d_detector_fixed_radius_locking_policy_validation_rows.csv"
        ),
    }


def metric_lookup(metrics: pd.DataFrame) -> dict[str, str]:
    return {str(row["metric"]): str(row["value"]) for _, row in metrics.iterrows()}


def metric_float(metrics: dict[str, str], key: str, default: float = 0.0) -> float:
    try:
        return float(metrics.get(key, default))
    except (TypeError, ValueError):
        return default


def plot_margin_comparison(data: dict, path: Path) -> None:
    prior = data["prior_coordinate"].copy()
    prior = prior[prior["base_margin_is_canonical"].fillna(True)]
    current = data["current_coordinate"].copy()
    current_ranked = current[current["base_margin"].notna()]

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.5), gridspec_kw={"width_ratios": [1.0, 1.25]})
    ax = axes[0]
    labels = ["target0", "target1", "target2"]
    prior_groups = [prior.loc[prior["target"] == i, "base_margin"].dropna().values for i in range(3)]
    cur_groups = [current_ranked.loc[current_ranked["target"] == i, "base_margin"].dropna().values for i in range(3)]
    positions = np.arange(3)
    ax.boxplot(
        prior_groups,
        positions=positions - 0.16,
        widths=0.24,
        patch_artist=True,
        boxprops={"facecolor": "#bdd7e7", "edgecolor": "#333333"},
        medianprops={"color": "#1d3557"},
    )
    ax.boxplot(
        cur_groups,
        positions=positions + 0.16,
        widths=0.24,
        patch_artist=True,
        boxprops={"facecolor": "#fdae6b", "edgecolor": "#333333"},
        medianprops={"color": "#7f2704"},
    )
    ax.axhline(CUTOFF, color="#333333", linestyle="--", linewidth=1.2)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Base objective margin")
    ax.set_title("Prior milestone versus post-1259 probes")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.legend(
        handles=[
            Line2D([0], [0], color="#333333", linestyle="--", label="strict cutoff"),
            Patch(facecolor="#bdd7e7", edgecolor="#333333", label="prior 700-1259"),
            Patch(facecolor="#fdae6b", edgecolor="#333333", label="post-1259"),
        ],
        frameon=False,
        loc="upper left",
    )

    ax = axes[1]
    colors = {"close10": "#bdbdbd", "close12": "#9ecae1", "close14": "#3182bd", "close50": "#e6550d", "variable-depth/radius": "#31a354"}
    markers = {0: "o", 1: "s", 2: "^"}
    for scenario, subset in current_ranked.groupby("scenario"):
        for target, target_subset in subset.groupby("target"):
            ax.scatter(
                target_subset["run_id"],
                target_subset["base_margin"],
                label=scenario,
                s=55,
                marker=markers.get(int(target), "o"),
                color=colors.get(scenario, "#444444"),
                edgecolor="black",
                linewidth=0.4,
                alpha=0.86,
            )
    ax.axhline(CUTOFF, color="#333333", linestyle="--", linewidth=1.2)
    ax.set_xlabel("Output experiment ID")
    ax.set_ylabel("Base objective margin")
    ax.set_title("Post-1259 coordinate-optimizer probes")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    handles, labels_seen = ax.get_legend_handles_labels()
    by_label = dict(zip(labels_seen, handles))
    ax.legend(by_label.values(), by_label.keys(), fontsize=8, frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_current_setup_outcomes(data: dict, path: Path) -> None:
    current = data["current_coordinate"].copy()
    current = current[current["base_margin"].notna()]
    current["setup"] = current.apply(
        lambda r: (
            f"{r['scenario']} | target {int(r['target']) if pd.notna(r['target']) else '?'} | "
            f"sources {int(r['sources']) if pd.notna(r['sources']) else '?'} | "
            f"Tx/Rx {r['tx_rx_offset_mm'] if pd.notna(r['tx_rx_offset_mm']) else '?'}"
            + (" | linear Rx" if bool(r["linear_receiver"]) else "")
        ),
        axis=1,
    )
    summary = (
        current.groupby("setup")
        .agg(
            median_margin=("base_margin", "median"),
            min_margin=("base_margin", "min"),
            max_margin=("base_margin", "max"),
            row_count=("base_margin", "count"),
            accepted_count=("accepted", "sum"),
            first_run=("run_id", "min"),
            last_run=("run_id", "max"),
        )
        .reset_index()
    )
    summary["accepted_fraction"] = summary["accepted_count"] / summary["row_count"]
    summary = summary.sort_values(["median_margin", "max_margin"], ascending=[False, False])
    fig, ax = plt.subplots(figsize=(13.5, 6.8))
    x = np.arange(len(summary))
    colors = ["#2a9d8f" if row.accepted_fraction == 1 else "#f4a261" if row.accepted_fraction > 0 else "#d62828" for row in summary.itertuples()]
    ax.bar(x, summary["median_margin"], color=colors, alpha=0.86)
    ax.errorbar(
        x,
        summary["median_margin"],
        yerr=[summary["median_margin"] - summary["min_margin"], summary["max_margin"] - summary["median_margin"]],
        fmt="none",
        ecolor="#333333",
        elinewidth=1,
        capsize=3,
    )
    ax.axhline(CUTOFF, color="#333333", linestyle="--", linewidth=1.2)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{r.setup}\nruns {int(r.first_run)}-{int(r.last_run)}" for r in summary.itertuples()], rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Median base objective margin")
    ax.set_xlabel("Post-1259 setup group")
    ax.set_title("Post-1259 Setup Groups: Median Margin And Within-Group Range")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    for idx, row in enumerate(summary.itertuples()):
        ax.text(idx, row.median_margin + 5.0e-5, f"{int(row.accepted_count)}/{int(row.row_count)}", ha="center", va="bottom", fontsize=8)
    ax.legend(
        handles=[
            Patch(facecolor="#2a9d8f", label="all rows clear cutoff"),
            Patch(facecolor="#f4a261", label="mixed"),
            Patch(facecolor="#d62828", label="none clear cutoff"),
            Line2D([0], [0], color="#333333", linestyle="--", label="strict cutoff"),
        ],
        frameon=False,
        loc="upper right",
    )
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_fixed_radius_progression(data: dict, metrics: dict[str, str], path: Path) -> None:
    stages = data["fixed_radius_stages"].copy()
    validation = data["validation_rows"].copy()
    lock_candidates = data["lock_candidates"].copy()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))

    ax = axes[0]
    x = np.arange(len(stages))
    ax.plot(x, stages["initial_linf_error_mm"], marker="o", color="#a44a3f", linewidth=2.0, label="initial")
    ax.plot(x, stages["final_linf_error_mm"], marker="o", color="#2a9d8f", linewidth=2.0, label="final")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{int(r.run_id)}\n{r.label}" for r in stages.itertuples()], rotation=20, ha="right", fontsize=8)
    ax.set_ylabel("Maximum x/z/r geometry error (mm)")
    ax.set_title("Fixed-radius branch error progression")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.legend(frameon=False)

    ax = axes[1]
    rows = []
    target1 = lock_candidates[lock_candidates["target_index"] == 1].iloc[0]
    rows.append(("target1 lock penalty", float(target1["lock_objective_penalty_rel"])))
    if not validation.empty:
        rows.append(("target2 next competitor gap", float(validation.iloc[0]["competing_minus_best_rel"])))
    values = [row[1] for row in rows]
    ax.bar([row[0] for row in rows], values, color=["#f4a261", "#457b9d"])
    ax.set_ylabel("Relative objective gap")
    ax.set_title("Exact endpoint remains a near-tie mechanism")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    for i, value in enumerate(values):
        ax.text(i, value + 0.001, f"{100*value:.2f}%", ha="center", va="bottom")
    note = (
        f"Target2 truth clearance: {metric_float(metrics, 'downstream_truth_clearance_before_mm'):.3f} mm "
        f"to {metric_float(metrics, 'downstream_truth_clearance_after_mm'):.3f} mm."
    )
    ax.text(0.5, -0.22, note, transform=ax.transAxes, ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_detector_progression(metrics: dict[str, str], path: Path) -> None:
    rows = pd.DataFrame(
        [
            ("All triples objective", "top-1 all truth", metric_float(metrics, "detector_alltriples_best_top1_all_truth_cases")),
            ("All triples objective", "top-50 all truth", metric_float(metrics, "detector_alltriples_best_top50_all_truth_cases")),
            ("Component waveform gate", "top-50 all truth", metric_float(metrics, "detector_component_gate_best_top50_cases")),
            ("Geometry selector", "leave-one-case top-1", metric_float(metrics, "detector_geometry_selector_leave_one_case_cases")),
            ("Depth/slot prior", "best top-1", metric_float(metrics, "detector_depth_slot_prior_best_all_truth_cases")),
            ("Slot component assembly", "upper-bound slot hits", metric_float(metrics, "detector_slot_component_best_slot_cases")),
            ("Blind envelope", "leave-one all-slot hits", metric_float(metrics, "detector_blind_envelope_leave_one_cases")),
            ("Reliability gate", "stable accepted cases", metric_float(metrics, "detector_blind_envelope_reliability_stable_cases")),
            ("Reliability gate", "review cases", metric_float(metrics, "detector_blind_envelope_reliability_review_cases")),
        ],
        columns=["stage", "metric", "cases"],
    )
    fig, ax = plt.subplots(figsize=(12.5, 6))
    y = np.arange(len(rows))
    colors = ["#d62828" if "top-1" in m and c <= 3 else "#2a9d8f" if c >= 10 else "#f4a261" for m, c in zip(rows["metric"], rows["cases"])]
    ax.barh(y, rows["cases"], color=colors)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{r.stage}\n{r.metric}" for r in rows.itertuples()], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Cases recovered or flagged")
    ax.set_title("Detector Evidence Progressed To Guardrails, Not A Deployable Full-Waveform Inversion Trigger")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    for i, value in enumerate(rows["cases"]):
        ax.text(value + 0.15, i, f"{value:.0f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_field_gate_blockers(data: dict, path: Path) -> None:
    gates = data["field_gates"].copy()
    for col in ["required_action_count", "current_archive_resolvable_action_count", "new_controlled_data_action_count", "missing_required_total"]:
        gates[col] = pd.to_numeric(gates[col], errors="coerce").fillna(0)
    gates["priority"] = pd.to_numeric(gates["highest_priority"], errors="coerce").fillna(99)
    gates = gates.sort_values(["priority", "gate_key"])
    fig, ax = plt.subplots(figsize=(12, 6.2))
    y = np.arange(len(gates))
    ax.barh(y, gates["new_controlled_data_action_count"], color="#d62828", label="requires new controlled data")
    ax.barh(y, gates["current_archive_resolvable_action_count"], color="#2a9d8f", label="resolvable from current archive")
    ax.set_yticks(y)
    gate_labels = (
        gates["gate_key"]
        .str.replace("_", " ", regex=False)
        .str.replace("fwi", "full-waveform inversion", regex=False)
    )
    ax.set_yticklabels(gate_labels)
    ax.invert_yaxis()
    ax.set_xlabel("Required action count")
    ax.set_title("Field Acceptance Gates Are Blocked By Missing Controlled Measurements")
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    for i, row in enumerate(gates.itertuples()):
        ax.text(row.new_controlled_data_action_count + 0.08, i, f"missing values={int(row.missing_required_total)}", va="center", fontsize=8)
    ax.set_xlim(0, max(4, gates["new_controlled_data_action_count"].max() + 1.3))
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_field_collection_requirements(data: dict, path: Path) -> None:
    actions = data["field_actions"].copy()
    actions["missing_required_count"] = pd.to_numeric(actions["missing_required_count"], errors="coerce").fillna(0)
    actions["minimum_rows_or_repeats"] = pd.to_numeric(actions["minimum_rows_or_repeats"], errors="coerce").fillna(0)
    actions["priority"] = pd.to_numeric(actions["priority"], errors="coerce").fillna(99)
    actions = actions.sort_values("priority")
    fig, ax1 = plt.subplots(figsize=(13, 5.8))
    x = np.arange(len(actions))
    ax1.bar(x, actions["missing_required_count"], color="#d62828", alpha=0.82, label="missing required fields")
    ax1.set_ylabel("Missing required fields (red bars)", color="#d62828")
    ax1.set_xticks(x)
    ax1.set_xticklabels(
        [
            f"P{int(r.priority)}\n{str(r.collection_phase).replace('_', ' ')}\n{str(r.blocker_group).replace('_', ' ')}"
            for r in actions.itertuples()
        ],
        rotation=20,
        ha="right",
        fontsize=8,
    )
    ax1.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax2 = ax1.twinx()
    ax2.plot(x, actions["minimum_rows_or_repeats"], color="#1d3557", marker="o", linewidth=2, label="minimum rows/repeats")
    ax2.set_ylabel("Minimum rows or repeats (blue line)", color="#1d3557")
    ax1.set_title("Controlled Field Collection Requirements Before Inversion Can Be Reconsidered")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_field_qc_status(metrics: dict[str, str], path: Path) -> None:
    rows = pd.DataFrame(
        [
            ("Short-profile relative timing quality control", metric_float(metrics, "field_time_zero_ladder_ready_short_qc")),
            ("Apparent-depth scale quality control", metric_float(metrics, "field_inversion_readiness_ready_depth_scale_qc")),
            ("Short-to-long timing transfer", metric_float(metrics, "field_inversion_readiness_ready_long_transfer")),
            ("Spatial calibration", metric_float(metrics, "field_inversion_readiness_ready_spatial_calibration")),
            ("Calibrated cover-depth recovery", metric_float(metrics, "field_inversion_readiness_ready_cover_depth")),
            ("Radius recovery", metric_float(metrics, "field_inversion_readiness_ready_radius")),
            ("Field full-waveform inversion", metric_float(metrics, "field_inversion_readiness_ready_field_fwi")),
            ("Field three-dimensional/high-performance-computing job", metric_float(metrics, "field_dimensionality_ready_for_3d_hpc")),
        ],
        columns=["capability", "ready"],
    )
    colors = rows["ready"].map({1.0: "#2a9d8f", 0.0: "#d62828"}).fillna("#999999")
    fig, ax = plt.subplots(figsize=(11.5, 5.7))
    y = np.arange(len(rows))
    ax.barh(y, np.ones(len(rows)), color=colors)
    ax.set_yticks(y)
    ax.set_yticklabels(rows["capability"])
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    ax.set_title("Measured-Field Archive Supports Quality Control, Not Calibrated Inversion")
    for i, ready in enumerate(rows["ready"]):
        ax.text(0.5, i, "supported" if ready else "blocked", color="white", va="center", ha="center", weight="bold")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def generate_figures(data: dict) -> dict[str, Path]:
    REPORT_FIGURES.mkdir(parents=True, exist_ok=True)
    for old_figure in REPORT_FIGURES.glob("*.png"):
        old_figure.unlink()
    metrics = metric_lookup(pd.concat([data["key_metrics"], data["result_metrics"]], ignore_index=True))
    paths = {
        "margin_comparison": REPORT_FIGURES / "fig02_prior_current_margin_comparison.png",
        "current_setups": REPORT_FIGURES / "fig03_current_close_spacing_setup_outcomes.png",
        "fixed_radius": REPORT_FIGURES / "fig04_fixed_radius_progression.png",
        "detector": REPORT_FIGURES / "fig05_detector_guardrail_progression.png",
        "field_qc": REPORT_FIGURES / "fig06_field_qc_status.png",
        "field_gates": REPORT_FIGURES / "fig07_field_gate_blockers.png",
        "field_collection": REPORT_FIGURES / "fig08_field_collection_requirements.png",
    }
    plot_margin_comparison(data, paths["margin_comparison"])
    plot_current_setup_outcomes(data, paths["current_setups"])
    plot_fixed_radius_progression(data, metrics, paths["fixed_radius"])
    plot_detector_progression(metrics, paths["detector"])
    plot_field_qc_status(metrics, paths["field_qc"])
    plot_field_gate_blockers(data, paths["field_gates"])
    plot_field_collection_requirements(data, paths["field_collection"])
    return paths


def build_notebook() -> None:
    data = load_inputs()
    metrics = metric_lookup(pd.concat([data["key_metrics"], data["result_metrics"]], ignore_index=True))
    figures = generate_figures(data)
    prior = data["prior_coordinate"]
    prior_canonical = prior[prior["base_margin_is_canonical"].fillna(True)]
    prior_exact = int(prior_canonical["exact_geometry"].fillna(False).sum())
    prior_total = len(prior_canonical)
    prior_accepted = int((prior_canonical["base_margin"] >= CUTOFF).sum())
    current = data["current_coordinate"]
    current_ranked = current[current["base_margin"].notna()]
    current_best = current_ranked.loc[current_ranked["base_margin"].idxmax()]
    current_accepted = int(current_ranked["accepted"].sum())
    current_total = len(current_ranked)

    nb = nbf.v4.new_notebook()
    cells: list[dict] = []

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""# Local Two-Dimensional Ground-Penetrating Radar Experiments And Field-Data Readiness

Generated: {REPORT_DATE}.

## Executive Summary

Notebook `007` established the main state of the synthetic coordinate-optimizer
archive through output experiment 1259: the optimizer usually recovered the
known geometry, but many exact recoveries still had weak objective margins. In
that canonical milestone set, `{prior_exact}` of `{prior_total}` parseable rows
preserved exact geometry, while `{prior_accepted}` cleared the strict margin
cutoff.

The current batch did not overturn that conclusion. Its main contribution is
more specific: it stress-tested close-spacing acquisition choices, showed that
saved detector evidence is useful as a guardrail rather than a deployable
selector, diagnosed the remaining fixed-radius close14 failure mode, and
validated one narrow branch-locking mechanism in a guarded run.

The measured-field work reached a separate checkpoint. The current GSSI 51600s
archive supports selected two-dimensional quality-control statements, but it is
not ready for field full-waveform inversion, calibrated radius/depth recovery,
three-dimensional high-performance-computing work, or broad graphics-processor
runs. The next field step is controlled two-dimensional collection with known
target truth, references, profile geometry, repeats, and complete metadata.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Scientific Objective

The project studies how reliably ground-penetrating radar can distinguish
closely spaced reinforcing bars in concrete. The central question is not simply
whether a rebar can be detected. The more specific question is whether the
inversion can distinguish the true geometry from nearby wrong geometries when
multiple rebars are close enough that their radar responses overlap.

This distinction matters because an inversion can return the correct geometry
while still having a weak margin over a nearly equivalent wrong geometry. Such a
case is useful evidence for ambiguity, but it should not be reported as a clean
resolution result.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Methods And Terms

| Term | Meaning in this report |
| --- | --- |
| Ground-penetrating radar | A radar method that sends a short electromagnetic pulse into a material and records reflections from embedded objects such as steel reinforcement. |
| Synthetic experiment | A computer-generated radar experiment with known rebar position, depth, and radius. It is used to test whether the inversion returns the known truth. |
| Measured-field experiment | A real data experiment from the local GSSI 51600s archive. The true target geometry and timing references are not automatically known. |
| Finite-difference time-domain simulation | A numerical wave-propagation method used here to generate radar-like waveforms for candidate rebar geometries. |
| Full-waveform inversion | An optimization approach that compares simulated waveforms with observed waveforms and adjusts the model to reduce the mismatch. |
| Parametric inversion | An inversion that estimates a small set of parameters, such as rebar horizontal position, depth, and radius. |
| Objective margin | The score gap between the selected geometry and the nearest competing geometry. A small margin indicates ambiguity. |
| Candidate solution | One tested rebar geometry, or one tested combination of rebar geometries, that the optimizer or detector can rank against alternatives. |
| Top-1 and top-50 recovery | Top-1 means the true candidate is ranked first. Top-50 means the true candidate appears somewhere within the 50 best-ranked candidates. |
| Guardrail | A check that can flag reliable or risky cases before a larger inversion run. In this report, a guardrail is not the same as an automatic launch policy. |
| Transmitter-receiver offset | The distance between the transmitting antenna position and receiving antenna position. Some labels abbreviate this as Tx/Rx offset. |
| Two-dimensional (2D) | A cross-sectional model or line-profile interpretation with horizontal position and depth, but not a full volume. |
| Three-dimensional (3D) | A volumetric survey or inversion design. The local GSSI field archive is not treated as a 3D survey in this report. |
| Graphics processing unit (GPU) | The accelerator used for guarded simulation or optimization runs on the local workstation. |
| High-performance computing (HPC) | Cluster-scale computing, distinct from the local workstation. |
| GSSI 51600s archive | The local measured-field data set used in the field-data track. GSSI is the instrument/archive label; 51600s is the local session identifier. |
"""
        )
    )

    cells.append(
        attachment_image_cell(
            1,
            "Final Close-Spacing Synthetic Geometry",
            SYNTHETIC_SCENE,
            (
                "This scene comes from output experiment 1358. The horizontal axis is lateral position in millimeters and the vertical axis is depth in millimeters. "
                "The final validation uses three rebars, with the center and right rebars separated by 14 mm center-to-center. Because their radii are 6 mm and 8 mm, their cross sections touch in this two-dimensional model. This figure explains why the close14 case is a difficult ambiguity test rather than a routine localization case."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Interpreting The Final Experiment Name

The final validation run is:

`1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu`

{md_table(
    decode_experiment_name("local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"),
    [("term", "Name part"), ("meaning", "Meaning")],
)}
"""
        )
    )

    cells.append(
        attachment_image_cell(
            2,
            "Prior Milestone Versus Current Coordinate-Optimizer Margins",
            figures["margin_comparison"],
            (
                "The left panel compares the base objective margin distributions from the prior milestone notebook 007, experiments 700-1259, with post-1259 coordinate-optimizer probes. The dashed horizontal line is the strict 5.0e-4 confidence cutoff; values above it are stronger separations from the nearest candidate radius. The right panel shows each post-1259 coordinate-optimizer probe by experiment ID and target. The current batch remains concentrated around the same cutoff boundary, so it mainly confirms and refines the prior ambiguity boundary rather than producing a broad new improvement."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## What Changed After Notebook 007

Notebook `007` had already shown that geometry recovery was strong but
confidence separation was incomplete. The post-1259 coordinate-optimizer probes
therefore tested boundary conditions rather than starting from scratch.

Across the post-1259 coordinate-optimizer rows with a base-margin value,
`{current_accepted}` of `{current_total}` cleared the strict cutoff. The strongest
post-1259 row in this parsed set is output experiment `{int(current_best['run_id'])}`,
scenario `{current_best['scenario']}`, target `{int(current_best['target'])}`,
with margin `{float(current_best['base_margin']):.3e}`. That best row is useful,
but the broader pattern in Figure 2 is more important: many newer close-spacing
tests remain near the cutoff, so the current batch mainly refines the resolution
boundary rather than replacing it.
"""
        )
    )

    cells.append(
        attachment_image_cell(
            3,
            "Post-1259 Close-Spacing Setup Outcomes",
            figures["current_setups"],
            (
                "Each bar is a setup group aggregated from post-1259 coordinate_confidence_report.csv rows. The y-axis is the median base objective margin, and the error bar spans the weakest to strongest row in that group. The dashed line is the strict 5.0e-4 confidence cutoff. The number above each bar is accepted rows over total rows; green means every row cleared the cutoff, orange means mixed behavior, and red means no row cleared the cutoff. The labels give spacing family, target, source count, transmitter-receiver offset, receiver sampling when relevant, and the experiment-ID range. This plot shows which newer close-spacing acquisition choices improved confidence and which stayed weak or unstable."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Close-Spacing Interpretation

The post-1259 close-spacing runs did not create a universal clean-spacing rule.
Instead, they showed that the outcome depends on acquisition setup, target,
source count, receiver sampling, and noise/source condition. Some close-spacing
rows clear the margin cutoff, while others remain weak even when the selected
geometry is correct.

That is a useful result. It supports a paper framing around acquisition-aware
identifiability: the method can often recover the right geometry, but the margin
must be checked before calling a case resolved.
"""
        )
    )

    cells.append(
        attachment_image_cell(
            4,
            "Fixed-Radius Branch Progression And Remaining Ambiguity",
            figures["fixed_radius"],
            (
                "The left panel plots the maximum geometry error, in millimeters, for the fixed-radius close14 branch stages. The final guarded validation, experiment 1358, reaches zero final error. The right panel plots relative objective gaps: the target1 lock required a 3.41 percent relative objective penalty, and the exact target2 endpoint still had a close next competitor with a 1.19 percent relative gap. The conclusion is that the branch-locking mechanism worked, but it remains a narrow near-tie result rather than a broad detector-policy result."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Fixed-Radius Mechanism Result

The fixed-radius sequence narrowed a specific failure mode. Before locking, the
branch could end with a 1 mm residual because the center rebar and right rebar
were coupled by a near-tie geometry. The CPU-side policy selected a target1 lock
at x=250 mm, z=90 mm. That lock changed target2 truth clearance from
`{metric_float(metrics, 'downstream_truth_clearance_before_mm'):.3f}` mm to
`{metric_float(metrics, 'downstream_truth_clearance_after_mm'):.3f}` mm, and the
guarded target2 unlock probe ended with
`{metric_float(metrics, 'unlock_probe_final_linf_error_mm'):.1f}` mm maximum
geometry error.

The result is reportable, but the claim must stay narrow:

- Supported: this fixed-radius close14 branch can be repaired by a specific
  target1 lock and target2 unlock sequence.
- Not supported: a general detector policy.
- Not supported: detector-seeded full-waveform inversion.
- Not supported: direct transfer of this synthetic mechanism to measured field
  data.
"""
        )
    )

    cells.append(
        attachment_image_cell(
            5,
            "Detector Evidence Progression",
            figures["detector"],
            (
                "Bars summarize detector-side metrics from the current manuscript table pack. The y-axis lists successive detector or selector analyses; the x-axis is the number of cases recovered or flagged. Top-1 means the true candidate was ranked first; top-50 means it appeared somewhere within the 50 best-ranked candidates. The detector evidence improves from weak top-1 all-truth recovery to useful upper-bound and reliability-gate evidence, but it still does not justify detector-seeded full-waveform inversion because the robust output is a guardrail and seed table, not a complete deployable selector."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Detector Interpretation

The detector studies are useful because they identify where candidate selection
is stable and where it should be reviewed. They do not yet provide a complete
inversion launch contract. The all-triples objective remains weak at top-1
selection, while later blind-envelope and reliability-gate analyses recover or
screen more cases. That progression supports detector guardrails and
upper-bound statements, but not a broad full-waveform inversion launch.
"""
        )
    )

    cells.append(
        attachment_image_cell(
            6,
            "Measured-Field Archive Readiness",
            figures["field_qc"],
            (
                "Each row is a field-data capability from the current readiness metrics. Green rows are supported by the current archive and red rows are blocked. The current field archive supports short-profile relative timing quality control and apparent-depth scale quality control, but blocks timing transfer, spatial calibration, calibrated cover-depth recovery, radius recovery, field full-waveform inversion, and field three-dimensional or high-performance-computing escalation."
            ),
        )
    )

    cells.append(
        attachment_image_cell(
            7,
            "Field Acceptance Gate Blockers",
            figures["field_gates"],
            (
                "Each horizontal bar is an acceptance gate from field run 156. The x-axis is the number of required action groups. Red portions require new controlled data; green portions would be resolvable from the current archive. The labels show missing required metadata values. The current archive cannot unblock the field acceptance gates by itself, especially the field full-waveform inversion or heavy-work gate."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Field-Data Interpretation

The field data are valuable, but the supported claims are currently limited to
quality control and collection planning. The data are independent two-dimensional
line profiles, not a three-dimensional survey. Without known target truth,
absolute time-zero references, amplitude references, profile-target geometry,
repeat measurements, and complete metadata, field full-waveform inversion would
be underconstrained.
"""
        )
    )

    cells.append(
        attachment_image_cell(
            8,
            "Controlled Field Collection Requirements",
            figures["field_collection"],
            (
                "Each bar is a required field action from run 156, ordered by priority. Red bars show missing required values; the blue line shows the minimum number of rows or repeats needed for that action. The plot shows that the next field milestone is controlled two-dimensional collection, not immediate inversion."
            ),
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Required Field Work Before Inversion

The next field work should collect the missing controls and then re-run the
acceptance gates. The highest-priority requirements are target truth, time-zero
references, amplitude references, survey geometry, controlled repeats, session
metadata, and reference registry rows.

{md_table(
    data["field_actions"],
    [
        ("priority", "Priority"),
        ("collection_phase", "Phase"),
        ("blocker_group", "Blocker"),
        ("planned_ids_or_repeats", "Planned IDs or repeats"),
        ("minimum_rows_or_repeats", "Minimum"),
        ("done_when", "Done when"),
    ],
)}
"""
        )
    )

    claim_subset = data["claim_rows"].sort_values(["domain", "claim_order"]).head(12)
    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Publication Positioning

The defensible contribution is an acquisition-aware identifiability study for
closely spaced rebars. The paper should emphasize when the true geometry is
distinguishable from nearby alternatives, when that distinction becomes
ambiguous, and why measured-field data require controlled references before
inversion.

The paper should not claim that all close-spacing cases are cleanly resolvable,
that the detector is deployable as a general policy, or that the local field
archive is ready for field full-waveform inversion.

Selected claim boundaries:

{md_table(
    claim_subset,
    [
        ("domain", "Domain"),
        ("claim_area", "Claim area"),
        ("paper_use_tier", "Use tier"),
        ("allowed_claim", "Allowed claim"),
        ("not_allowed", "Not allowed"),
    ],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Recommended Next Steps

For synthetic two-dimensional work:

1. Treat the fixed-radius close14 endpoint as a bounded mechanism result.
2. Continue CPU-side confidence-policy synthesis before any new graphics-processor
   run.
3. If another synthetic run is justified, make it a single guarded probe with a
   predeclared hypothesis and a predeclared decision rule.

For measured-field work:

1. Keep the current field archive in the quality-control and planning lane.
2. Execute the controlled two-dimensional collection packet.
3. Collect known target truth, time-zero references, amplitude references, profile
   geometry, controlled repeats, and required metadata.
4. Re-run the field acceptance gates after collection before considering field
   inversion, heavy graphics-processor work, or high-performance-computing work.
"""
        )
    )

    source_rows = pd.DataFrame(
        [
            {
                "artifact": "Prior milestone notebook",
                "path": str(PRIOR_NOTEBOOK),
                "purpose": "Baseline result through output experiment 1259.",
            },
            {
                "artifact": "Current report notebook",
                "path": str(NOTEBOOK_PATH),
                "purpose": "Result-focused synthesis of the current 2D and field checkpoint.",
            },
            {
                "artifact": "Current generated figures and tables",
                "path": str(SUPPORT_ROOT),
                "purpose": "Support files and regenerated report figures.",
            },
            {
                "artifact": "Final synthetic probe",
                "path": "outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu",
                "purpose": "Evidence for the fixed-radius locking endpoint.",
            },
            {
                "artifact": "Field critical-path checkpoint",
                "path": "outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path",
                "purpose": "Evidence for the field collection-readiness checkpoint.",
            },
        ]
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            "## Source Artifacts\n\n"
            + md_table(source_rows, [("artifact", "Artifact"), ("path", "Path"), ("purpose", "Purpose")])
        )
    )

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3 (gpr-fdtd-fwi)", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(nbf.writes(nb))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args()
    build_notebook()
    if args.print_summary:
        print(f"Wrote notebook: {NOTEBOOK_PATH}")
        print("Embedded figures: 8")


if __name__ == "__main__":
    main()
