"""Generate the local 2D plus field holistic report notebook.

This report is intentionally built from preserved output artifacts. It does not
launch simulations or GPU work.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import nbformat as nbf
import pandas as pd
from PIL import Image


REPORT_DATE = "2026-06-19"
REPORT_STEM = "014_2026-06-19_local_2d_field_holistic_report"
NOTEBOOK_PATH = Path("docs/update/summary") / f"{REPORT_STEM}.ipynb"
REPORT_DIR = Path("outputs/summary_tables/133_local_2d_field_holistic_report_post_checkpoint")
DATA_DIR = REPORT_DIR / "data"
FIG_DIR = REPORT_DIR / "figures"

SYNTHETIC_ROOT = Path("outputs/experiments")
FIELD_ROOT = Path("outputs/field_experiments/local_gssi_51600s_2026_06_09")
SYNTHETIC_RUN_MIN = 1200

TABLE_PACK_ROOT = Path(
    "outputs/summary_tables/132_local_2d_field_manuscript_table_pack_post_fixed_radius_locking_validation"
)
LOCK_DESIGN_ROOT = Path("outputs/summary_tables/130_local_2d_detector_fixed_radius_locking_policy_design")
LOCK_VALIDATION_ROOT = Path(
    "outputs/summary_tables/131_local_2d_detector_fixed_radius_locking_policy_validation_post_unlock_probe"
)
LOCK_SECOND_PASS_ROOT = Path(
    "outputs/experiments/1357_local2d_fixed_radius_second_pass_target2_close14_seed21_nominal_gpu"
)
LOCK_UNLOCK_PROBE_ROOT = Path(
    "outputs/experiments/1358_local2d_fixed_radius_locking_target2_unlock_probe_target2_close14_seed21_nominal_gpu"
)
FIELD_CRITICAL_ROOT = FIELD_ROOT / "156_gssi51600s_controlled_collection_critical_path"


def parse_run_id(name: str) -> int | None:
    """Parse the numeric run prefix from an output directory name."""
    match = re.match(r"^(\d+)(?:_|$)", name)
    return int(match.group(1)) if match else None


def classify_recent_synthetic_phase(run_id: int, run_name: str = "") -> str:
    """Group recent synthetic output IDs into report-level phases."""
    if run_id <= 1259:
        return "1200-1259 prior holistic tail and stop-point context"
    if run_id <= 1279:
        return "1260-1279 weak-exact confidence policy closure"
    if run_id <= 1293:
        return "1280-1293 ambiguity, objective, and reporting policy maps"
    if run_id <= 1307:
        return "1294-1307 close-spacing threshold probes and claim refresh"
    if run_id <= 1325:
        return "1308-1325 publication bundle and acquisition surfaces"
    if run_id <= 1338:
        return "1326-1338 local detector baselines and sampling boundary"
    if run_id <= 1343:
        return "1339-1343 fixed-radius controlled-prior diagnostics"
    if run_id <= 1356:
        return "1344-1356 matched source-count close-spacing probes"
    if run_id <= 1358:
        return "1357-1358 fixed-radius locking validation endpoint"
    return "post-checkpoint synthetic context"


def classify_recent_synthetic_type(run_name: str) -> str:
    """Assign a coarse artifact type from the recent output directory name."""
    if "coordinate_optimizer" in run_name:
        return "coordinate optimizer run"
    if "coordinate_confidence" in run_name:
        return "coordinate aggregate"
    if "local2d_detector_baseline" in run_name:
        return "detector baseline"
    if "fixed_radius" in run_name or "controlled_fixed_radius" in run_name:
        return "fixed-radius detector"
    if any(token in run_name for token in ["publication", "claim", "matrix", "table_pack"]):
        return "publication synthesis"
    if any(token in run_name for token in ["policy", "audit", "synthesis", "map"]):
        return "policy/audit synthesis"
    return "other recent output"


def classify_field_phase(run_id: int, run_name: str = "") -> str:
    """Group field experiment IDs into report-level phases."""
    if run_id <= 4:
        return "001-004 archive intake and initial status"
    if run_id <= 17:
        return "005-017 phase-anchor and synthetic waveform probes"
    if run_id <= 23:
        return "018-023 repeatability, alignment, and profile network"
    if run_id <= 42:
        return "024-042 short-profile timing and content anchoring"
    if run_id <= 58:
        return "043-058 corrected stacks and long-profile transfer"
    if run_id <= 81:
        return "059-081 publication bundle, event tiers, and timing conflict"
    if run_id <= 118:
        return "100-118 timing discriminants, cue support, and dimensionality"
    if run_id <= 136:
        return "119-136 short-anchor inversion-readiness blockers"
    if run_id <= 156:
        return "137-156 controlled 2D collection packet and critical path"
    return "post-critical-path field context"


def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text())


def read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def discover_synthetic_runs(run_min: int = SYNTHETIC_RUN_MIN) -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(SYNTHETIC_ROOT.iterdir(), key=lambda p: (parse_run_id(p.name) or 10**9, p.name)):
        if not path.is_dir():
            continue
        run_id = parse_run_id(path.name)
        if run_id is None or run_id < run_min:
            continue
        run_name = path.name.split("_", 1)[1] if "_" in path.name else path.name
        rows.append(
            {
                "run_id": run_id,
                "run_name": run_name,
                "phase": classify_recent_synthetic_phase(run_id, run_name),
                "artifact_type": classify_recent_synthetic_type(run_name),
                "has_manifest": (path / "run_manifest.json").exists(),
                "path": str(path),
            }
        )
    return pd.DataFrame(rows)


def discover_field_runs() -> pd.DataFrame:
    rows: list[dict] = []
    for path in sorted(FIELD_ROOT.iterdir(), key=lambda p: (parse_run_id(p.name) or 10**9, p.name)):
        if not path.is_dir():
            continue
        run_id = parse_run_id(path.name)
        if run_id is None:
            continue
        run_name = path.name.split("_", 1)[1] if "_" in path.name else path.name
        rows.append(
            {
                "run_id": run_id,
                "run_name": run_name,
                "phase": classify_field_phase(run_id, run_name),
                "has_manifest": (path / "run_manifest.json").exists(),
                "path": str(path),
            }
        )
    return pd.DataFrame(rows)


def phase_summary(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["phase", "first_run", "last_run", "run_count", "manifest_count"])
    return (
        df.groupby("phase", sort=False)
        .agg(
            first_run=("run_id", "min"),
            last_run=("run_id", "max"),
            run_count=("run_id", "count"),
            manifest_count=("has_manifest", "sum"),
        )
        .reset_index()
        .sort_values("first_run")
    )


def state_linf_mm(state: dict, truth_x: list[float], truth_z: list[float], truth_r: list[float]) -> float:
    """Max absolute x/z/r geometry error in millimeters for a state dict."""
    values: list[float] = []
    for key, truth in [
        ("x_values_mm", truth_x),
        ("z_values_mm", truth_z),
        ("radii_mm", truth_r),
    ]:
        observed = state.get(key) or []
        values.extend(abs(float(a) - float(b)) for a, b in zip(observed, truth))
    return max(values) if values else float("nan")


def build_locking_endpoint_rows() -> pd.DataFrame:
    rows: list[dict] = []
    for run_id, root, label in [
        (1357, LOCK_SECOND_PASS_ROOT, "second pass before lock"),
        (1358, LOCK_UNLOCK_PROBE_ROOT, "target2 unlock after target1 lock"),
    ]:
        summary = read_json(root / "data" / "multi_rebar_coordinate_optimizer_summary.json")
        truth_x = [float(v) for v in summary["true_x_values_mm"]]
        truth_z = [float(v) for v in summary["true_z_values_mm"]]
        truth_r = [float(v) for v in summary["truth_radius_values_mm"]]
        rows.append(
            {
                "run_id": run_id,
                "label": label,
                "run_name": summary.get("run_name", root.name),
                "initial_linf_error_mm": state_linf_mm(summary["initial_state"], truth_x, truth_z, truth_r),
                "final_linf_error_mm": state_linf_mm(summary["final_state"], truth_x, truth_z, truth_r),
                "initial_state": compact_state(summary["initial_state"]),
                "final_state": compact_state(summary["final_state"]),
                "truth_state": compact_truth(truth_x, truth_z, truth_r),
                "path": str(root),
            }
        )
    return pd.DataFrame(rows)


def compact_state(state: dict) -> str:
    x = ",".join(f"{float(v):.0f}" for v in state.get("x_values_mm", []))
    z = ",".join(f"{float(v):.0f}" for v in state.get("z_values_mm", []))
    r = ",".join(f"{float(v):.0f}" for v in state.get("radii_mm", []))
    return f"x=[{x}], z=[{z}], r=[{r}]"


def compact_truth(x: Iterable[float], z: Iterable[float], r: Iterable[float]) -> str:
    return (
        f"x=[{','.join(f'{float(v):.0f}' for v in x)}], "
        f"z=[{','.join(f'{float(v):.0f}' for v in z)}], "
        f"r=[{','.join(f'{float(v):.0f}' for v in r)}]"
    )


def bool_label(value: object) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_key_metrics(
    synthetic_runs: pd.DataFrame,
    field_runs: pd.DataFrame,
    table_summary: dict,
    lock_design: dict,
    lock_validation: dict,
    field_summary: dict,
    endpoint_rows: pd.DataFrame,
) -> pd.DataFrame:
    rows = [
        ("synthetic_2d", "recent_window_first_run", synthetic_runs["run_id"].min(), "report window lower bound"),
        ("synthetic_2d", "recent_window_last_run", synthetic_runs["run_id"].max(), "latest synthetic output in scope"),
        ("synthetic_2d", "recent_output_dir_count", len(synthetic_runs), "numbered output directories from run 1200 onward"),
        (
            "synthetic_2d",
            "recent_manifest_count",
            int(synthetic_runs["has_manifest"].sum()),
            "recent output directories with run_manifest.json",
        ),
        (
            "synthetic_2d",
            "claim_table_rows",
            table_summary.get("claim_table_row_count"),
            "paper-facing claim rows in latest table pack",
        ),
        (
            "synthetic_2d",
            "synthetic_publication_figures",
            table_summary.get("synthetic_figure_count"),
            "synthetic figures in latest table pack",
        ),
        (
            "synthetic_2d",
            "lock_selected_target_index",
            lock_design.get("selected_lock_target_index"),
            "truth-free lock candidate selected before unlock probe",
        ),
        (
            "synthetic_2d",
            "lock_objective_penalty_rel",
            lock_design.get("selected_lock_objective_penalty_rel"),
            "relative objective penalty for locking target1 to exact truth branch",
        ),
        (
            "synthetic_2d",
            "downstream_truth_clearance_before_mm",
            lock_design.get("selected_lock_downstream_truth_clearance_before_mm"),
            "target2 clearance before target1 lock",
        ),
        (
            "synthetic_2d",
            "downstream_truth_clearance_after_mm",
            lock_design.get("selected_lock_downstream_truth_clearance_after_mm"),
            "target2 clearance after target1 lock",
        ),
        (
            "synthetic_2d",
            "unlock_probe_final_linf_error_mm",
            float(endpoint_rows.loc[endpoint_rows["run_id"] == 1358, "final_linf_error_mm"].iloc[0]),
            "final geometry error after guarded unlock probe",
        ),
        (
            "synthetic_2d",
            "locking_mechanism_claim_ready",
            lock_validation.get("ready_for_locking_mechanism_claim"),
            "single-branch mechanism evidence is usable",
        ),
        (
            "synthetic_2d",
            "general_detector_policy_ready",
            lock_validation.get("ready_for_general_detector_policy_claim"),
            "general detector policy claim status",
        ),
        (
            "synthetic_2d",
            "broad_gpu_queue_ready",
            lock_validation.get("ready_for_broad_gpu_queue"),
            "whether current endpoint opens broad GPU queue",
        ),
        (
            "field", "field_first_run", field_runs["run_id"].min(), "first field output in local archive"
        ),
        ("field", "field_last_run", field_runs["run_id"].max(), "latest field output in scope"),
        ("field", "field_run_count", len(field_runs), "numbered field output directories"),
        (
            "field",
            "field_manifest_count",
            int(field_runs["has_manifest"].sum()),
            "field output directories with run_manifest.json",
        ),
        ("field", "field_geometry_type", field_summary.get("field_geometry_type"), "survey geometry classification"),
        ("field", "is_3d_survey", field_summary.get("is_3d_survey"), "whether the current field archive is a 3D survey"),
        ("field", "field_gate_count", field_summary.get("gate_count"), "acceptance gates at critical path checkpoint"),
        ("field", "field_ready_gate_count", field_summary.get("ready_gate_count"), "gates ready at checkpoint"),
        (
            "field",
            "field_current_archive_unblockable_gate_count",
            field_summary.get("current_archive_unblockable_gate_count"),
            "gates the existing archive can unblock alone",
        ),
        (
            "field",
            "field_critical_new_data_action_count",
            field_summary.get("critical_new_data_action_count"),
            "critical actions requiring new controlled data",
        ),
        (
            "field",
            "packet_missing_required_value_count",
            field_summary.get("missing_required_value_count"),
            "missing required values in controlled packet",
        ),
        (
            "field",
            "ready_for_collection_execution",
            field_summary.get("ready_for_collection_execution"),
            "whether the next action is collection execution",
        ),
        (
            "field",
            "ready_for_current_archive_field_fwi",
            field_summary.get("ready_for_current_archive_field_fwi"),
            "whether current archive is sufficient for field FWI",
        ),
        (
            "field",
            "ready_for_field_3d_hpc",
            field_summary.get("ready_for_field_3d_hpc"),
            "whether current field archive calls for 3D/HPC",
        ),
    ]
    return pd.DataFrame(rows, columns=["domain", "metric", "value", "interpretation"])


def notebook_rel(path: Path) -> str:
    return os.path.relpath(path, NOTEBOOK_PATH.parent)


def figure_block(alt: str, path: Path, caption: str) -> str:
    return f"![{alt}]({notebook_rel(path)})\n\n*Figure: {caption}*"


def md_value(value: object) -> str:
    if pd.isna(value):
        return ""
    if isinstance(value, float):
        if abs(value) >= 1000:
            return f"{value:,.0f}"
        if abs(value) < 0.01 and value != 0:
            return f"{value:.3e}"
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(df: pd.DataFrame, columns: list[tuple[str, str]], max_rows: int | None = None) -> str:
    if df.empty:
        return "_No rows._"
    selected = df.loc[:, [key for key, _ in columns]].head(max_rows) if max_rows else df.loc[:, [key for key, _ in columns]]
    header = "| " + " | ".join(label for _, label in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_value(row[key]) for key, _ in columns) + " |"
        for _, row in selected.iterrows()
    ]
    if max_rows is not None and len(df) > max_rows:
        body.append(f"| ... | {len(df) - max_rows} more rows omitted; see generated CSV. |")
    return "\n".join([header, sep] + body)


def write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def plot_scope_counts(
    synthetic_runs: pd.DataFrame,
    field_runs: pd.DataFrame,
    table_summary: dict,
    field_summary: dict,
    path: Path,
) -> None:
    labels = [
        "2D outputs\n1200-1358",
        "2D manifests",
        "Field outputs\n001-156",
        "Field manifests",
        "Claim rows",
        "Figure rows",
        "Field gates",
    ]
    values = [
        len(synthetic_runs),
        int(synthetic_runs["has_manifest"].sum()),
        len(field_runs),
        int(field_runs["has_manifest"].sum()),
        int(table_summary.get("claim_table_row_count", 0)),
        int(table_summary.get("figure_inventory_row_count", 0)),
        int(field_summary.get("gate_count", 0)),
    ]
    colors = ["#2a6f97", "#61a5c2", "#7b2cbf", "#c77dff", "#2d6a4f", "#74c69d", "#9d0208"]
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    bars = ax.bar(labels, values, color=colors)
    ax.set_ylabel("Count")
    ax.set_title("Report Scope And Preserved Artifact Counts")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + max(values) * 0.015, str(value), ha="center")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_phase_summary(df: pd.DataFrame, title: str, path: Path, color: str) -> None:
    summary = phase_summary(df)
    fig, ax = plt.subplots(figsize=(11, max(4.8, len(summary) * 0.55)))
    y = range(len(summary))
    ax.barh(y, summary["run_count"], color=color, alpha=0.88)
    ax.set_yticks(list(y))
    ax.set_yticklabels(summary["phase"])
    ax.invert_yaxis()
    ax.set_xlabel("Output directories")
    ax.set_title(title)
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    for idx, row in summary.iterrows():
        label = f"{int(row['run_count'])} runs ({int(row['first_run'])}-{int(row['last_run'])})"
        ax.text(float(row["run_count"]) + 0.4, list(summary.index).index(idx), label, va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_synthetic_endpoint(endpoint_rows: pd.DataFrame, lock_design: dict, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw={"width_ratios": [1.1, 1.0]})
    ax = axes[0]
    x = range(len(endpoint_rows))
    ax.bar([i - 0.18 for i in x], endpoint_rows["initial_linf_error_mm"], width=0.36, label="initial", color="#b56576")
    ax.bar([i + 0.18 for i in x], endpoint_rows["final_linf_error_mm"], width=0.36, label="final", color="#2a9d8f")
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{int(r)}" for r in endpoint_rows["run_id"]])
    ax.set_ylabel("Max geometry error (mm)")
    ax.set_title("Fixed-Radius Endpoint Error")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    for i, value in enumerate(endpoint_rows["final_linf_error_mm"]):
        ax.text(i + 0.18, float(value) + 0.05, f"{float(value):.0f}", ha="center", fontsize=9)

    ax = axes[1]
    labels = ["before lock", "after lock"]
    values = [
        float(lock_design.get("selected_lock_downstream_truth_clearance_before_mm", 0)),
        float(lock_design.get("selected_lock_downstream_truth_clearance_after_mm", 0)),
    ]
    colors = ["#e76f51" if v < 0 else "#2a9d8f" for v in values]
    ax.bar(labels, values, color=colors)
    ax.axhline(0, color="#333333", linewidth=1)
    ax.set_ylim(min(values) - 0.18, 0.16)
    ax.set_ylabel("Target2 truth clearance (mm)")
    ax.set_title("Target1 Lock Unblocks Target2 Truth Branch")
    for i, value in enumerate(values):
        if value < 0:
            ax.text(i, value / 2.0, f"{value:.3f}", ha="center", va="center", color="white", fontsize=10)
        else:
            ax.text(i, 0.04, f"{value:.3f}", ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_claim_inventory(claims: pd.DataFrame, figures: pd.DataFrame, path: Path) -> None:
    claim_counts = claims.groupby(["domain", "paper_use_tier"]).size().reset_index(name="count")
    figure_counts = figures.groupby(["domain", "paper_role"]).size().reset_index(name="count")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))
    for ax, frame, category, title in [
        (axes[0], claim_counts, "paper_use_tier", "Claim Rows By Domain And Tier"),
        (axes[1], figure_counts, "paper_role", "Figure Rows By Domain And Role"),
    ]:
        pivot = frame.pivot(index="domain", columns=category, values="count").fillna(0)
        pivot.plot(kind="bar", stacked=True, ax=ax, colormap="tab20")
        ax.set_xlabel("")
        ax.set_ylabel("Count")
        ax.set_title(title)
        ax.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(1.02, 1.0))
        ax.grid(axis="y", color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_field_gates(gates: pd.DataFrame, path: Path) -> None:
    frame = gates.copy()
    for col in [
        "required_action_count",
        "current_archive_resolvable_action_count",
        "new_controlled_data_action_count",
        "missing_required_total",
    ]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)
    frame["priority_sort"] = pd.to_numeric(frame["highest_priority"], errors="coerce").fillna(999)
    frame = frame.sort_values(["priority_sort", "gate_key"])
    fig, ax = plt.subplots(figsize=(11, 5.4))
    y = range(len(frame))
    ax.barh(y, frame["required_action_count"], color="#adb5bd", label="required actions")
    ax.barh(y, frame["new_controlled_data_action_count"], color="#d00000", alpha=0.76, label="new controlled data")
    ax.barh(y, frame["current_archive_resolvable_action_count"], color="#2a9d8f", label="current archive resolvable")
    ax.set_yticks(list(y))
    ax.set_yticklabels(frame["gate_key"])
    ax.invert_yaxis()
    ax.set_xlabel("Action count")
    ax.set_title("Field Critical-Path Gates: Existing Archive Cannot Unblock The Gates")
    ax.set_xlim(0, float(frame["required_action_count"].max()) + 1.0)
    ax.legend(frameon=False)
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    for i, row in enumerate(frame.itertuples(index=False)):
        ax.text(float(row.required_action_count) + 0.08, i, f"missing={int(row.missing_required_total)}", va="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_field_phase_plan(phases: pd.DataFrame, path: Path) -> None:
    frame = phases.copy()
    for col in ["action_count", "minimum_rows_or_repeats_total", "missing_required_total"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0)
    frame = frame.sort_values("phase_order")
    x = range(len(frame))
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.plot(x, frame["minimum_rows_or_repeats_total"], marker="o", linewidth=2.2, color="#2a6f97", label="minimum rows/repeats")
    ax.plot(x, frame["missing_required_total"], marker="s", linewidth=2.2, color="#d00000", label="missing required values")
    ax.bar(x, frame["action_count"], width=0.38, color="#80ed99", alpha=0.75, label="action count")
    ax.set_xticks(list(x))
    ax.set_xticklabels(frame["collection_phase"], rotation=25, ha="right")
    ax.set_ylabel("Count")
    ax.set_title("Controlled 2D Field Collection Phase Plan")
    ax.legend(frameon=False)
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def validate_figures(paths: Iterable[Path]) -> pd.DataFrame:
    rows: list[dict] = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        sample = image.resize((min(image.width, 256), min(image.height, 256)))
        colors = sample.getcolors(maxcolors=1_000_000) or []
        nonwhite = sum(count for count, color in colors if color != (255, 255, 255)) / (
            sample.width * sample.height
        )
        rows.append(
            {
                "path": str(path),
                "width": image.width,
                "height": image.height,
                "sampled_unique_colors": len(colors),
                "nonwhite_fraction": nonwhite,
            }
        )
    return pd.DataFrame(rows)


def write_notebook(context: dict) -> None:
    synthetic_runs = context["synthetic_runs"]
    field_runs = context["field_runs"]
    synthetic_phase = context["synthetic_phase"]
    field_phase = context["field_phase"]
    endpoint_rows = context["endpoint_rows"]
    key_metrics = context["key_metrics"]
    claims = context["claims"]
    figures = context["figures"]
    gates = context["gates"]
    actions = context["actions"]
    phases = context["phases"]
    figure_validation = context["figure_validation"]
    field_summary = context["field_summary"]
    lock_design = context["lock_design"]
    lock_validation = context["lock_validation"]
    paths = context["paths"]

    nb = nbf.v4.new_notebook()
    cells = []

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""# Local 2D And Field Holistic Report

Generated: {REPORT_DATE}.

Scope:

- Recent synthetic 2D outputs: `outputs/experiments/{SYNTHETIC_RUN_MIN}_...` through `outputs/experiments/{int(synthetic_runs['run_id'].max())}_...`.
- Field outputs: `{FIELD_ROOT}` runs `001` through `{int(field_runs['run_id'].max()):03d}`.
- Primary field checkpoint: `{FIELD_CRITICAL_ROOT}`.

This notebook is report-facing. It summarizes the recent synthetic 2D work and
the full local GSSI field sequence without launching more experiments.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Executive Summary

The synthetic 2D campaign did not close because the 3D work started elsewhere.
It reached a local mechanism checkpoint: a fixed-radius target1 branch lock
converted the target2 close14 repaired branch from a residual 1 mm state into
exact geometry in one guarded unlock probe. This is usable as a narrow
mechanism result, not as a general detector policy or detector-seeded FWI claim.

The field campaign also reached a natural checkpoint, not an abrupt stop. Runs
`137-156` close a complete field-side logic block: controlled acquisition
design, existing-archive manifest, packet template, validation, metadata
recovery, handoff, and gate-level critical path. The current archive is
classified as independent 2D line profiles, not a 3D survey, and it cannot
unblock any acceptance gate by itself.

The next report should treat the two domains separately: synthetic 2D supports
an acquisition-aware resolution/ambiguity study; the field archive supports
QC, timing-risk analysis, and a controlled 2D collection protocol, but not
field FWI or heavy GPU work from the current archive alone.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Scope Counts

{figure_block(
    "Report scope counts",
    paths["scope_counts"],
    "Counts of recent synthetic outputs, field outputs, manifests, claim rows, figure rows, and field acceptance gates included in this report.",
)}

Key metrics:

{md_table(
    key_metrics,
    [("domain", "Domain"), ("metric", "Metric"), ("value", "Value"), ("interpretation", "Interpretation")],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Recent Synthetic 2D Window

{figure_block(
    "Recent synthetic 2D phase coverage",
    paths["synthetic_phase"],
    "Output-directory coverage from run 1200 through the fixed-radius locking checkpoint, grouped by report-level phase.",
)}

{md_table(
    synthetic_phase,
    [("phase", "Phase"), ("first_run", "First"), ("last_run", "Last"), ("run_count", "Runs"), ("manifest_count", "Manifests")],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Synthetic 2D Endpoint: Fixed-Radius Locking Mechanism

{figure_block(
    "Fixed-radius synthetic endpoint",
    paths["synthetic_endpoint"],
    "Run 1357 leaves a 1 mm residual after the second pass. The CPU-side lock policy chooses target1=[250,90] with a 3.4 percent relative objective penalty and clears target2 truth geometry in run 1358.",
)}

Endpoint rows:

{md_table(
    endpoint_rows,
    [
        ("run_id", "Run"),
        ("label", "Role"),
        ("initial_linf_error_mm", "Initial Linf mm"),
        ("final_linf_error_mm", "Final Linf mm"),
        ("initial_state", "Initial"),
        ("final_state", "Final"),
        ("truth_state", "Truth"),
    ],
)}

Lock-design decision:

- Selected lock target: `{lock_design.get("selected_lock_target_index")}` at
  `[x,z]=[{lock_design.get("selected_lock_x_mm")}, {lock_design.get("selected_lock_z_mm")}]`.
- Relative objective penalty: `{float(lock_design.get("selected_lock_objective_penalty_rel", 0)):.6f}`.
- Downstream target2 truth clearance changed from
  `{float(lock_design.get("selected_lock_downstream_truth_clearance_before_mm", 0)):.6f}` mm to
  `{float(lock_design.get("selected_lock_downstream_truth_clearance_after_mm", 0)):.6f}` mm.
- Validation exact geometry recovered: `{bool_label(lock_validation.get("exact_geometry_recovered"))}`.
- Guard maximum GPU/RAM during validation: `{lock_validation.get("guard_max_gpu_util_percent")}` percent GPU,
  `{float(lock_validation.get("guard_max_ram_used_percent", 0)):.3f}` percent RAM.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Synthetic 2D Interpretation

What is reportable:

- The fixed-radius branch-locking result demonstrates a mechanism: a
  truth-free near-tie lock can improve downstream geometry clearance on one
  repaired target2 close14 branch.
- The recent synthetic window strengthens the paper framing around
  identifiability, ambiguity margins, and acquisition choices rather than a
  generic claim that rebar detection is solved.
- The current table pack preserves the claim boundary: point recovery,
  strict confidence, near-tie ambiguity, and publication readiness should stay
  separate.

What remains blocked:

- The validated lock is one branch, so it is not a deployable detector policy.
- It does not justify broad GPU queues, detector-seeded FWI, or field transfer.
- The target1/target2 close-spacing question still needs careful CPU-side
  policy synthesis before any future narrow probe.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Full Field Experiment Chain

{figure_block(
    "Field phase coverage",
    paths["field_phase"],
    "All local GSSI field outputs through run 156, grouped by field-side logic phase.",
)}

{md_table(
    field_phase,
    [("phase", "Phase"), ("first_run", "First"), ("last_run", "Last"), ("run_count", "Runs"), ("manifest_count", "Manifests")],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Field Critical Path

{figure_block(
    "Field gate critical path",
    paths["field_gates"],
    "Run 156 shows seven acceptance gates, zero ready gates, and zero gates that can be unblocked by the existing archive alone.",
)}

Gate table:

{md_table(
    gates,
    [
        ("gate_key", "Gate"),
        ("ready_now", "Ready"),
        ("highest_priority", "Priority"),
        ("required_action_count", "Required Actions"),
        ("current_archive_resolvable_action_count", "Archive-Resolvable"),
        ("new_controlled_data_action_count", "New Data Actions"),
        ("missing_required_total", "Missing Required"),
        ("critical_path", "Critical Path"),
    ],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Field Collection Plan

{figure_block(
    "Controlled 2D field collection phase plan",
    paths["field_phase_plan"],
    "The next field work is controlled 2D collection: target truth, time-zero and amplitude references, survey geometry, controlled repeats, and documentation overlay.",
)}

Collection phases:

{md_table(
    phases,
    [
        ("phase_order", "Order"),
        ("collection_phase", "Phase"),
        ("blocker_groups", "Blockers"),
        ("action_count", "Actions"),
        ("minimum_rows_or_repeats_total", "Min Rows/Repeats"),
        ("missing_required_total", "Missing Required"),
        ("acceptance_gates_touched", "Gates Touched"),
    ],
)}

Critical actions:

{md_table(
    actions,
    [
        ("priority", "Priority"),
        ("collection_phase", "Phase"),
        ("blocker_group", "Blocker"),
        ("planned_ids_or_repeats", "Planned IDs/Repeats"),
        ("minimum_rows_or_repeats", "Minimum"),
        ("missing_required_count", "Missing"),
        ("requires_new_controlled_data", "Needs New Data"),
        ("current_archive_can_resolve", "Archive Can Resolve"),
    ],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Publication Claim And Figure Inventory

{figure_block(
    "Claim and figure inventory",
    paths["claim_inventory"],
    "Latest manuscript table pack: {int(context['table_summary'].get('claim_table_row_count', 0))} claim rows and {int(context['table_summary'].get('figure_inventory_row_count', 0))} figure rows, split between synthetic and field domains.",
)}

Selected high-signal figure rows:

{md_table(
    figures.sort_values(["domain", "figure_order"]).head(14),
    [
        ("domain", "Domain"),
        ("figure_order", "Order"),
        ("figure_key", "Figure"),
        ("paper_role", "Role"),
        ("source_run", "Source Run"),
        ("policy_or_status", "Status"),
        ("metric_summary", "Metric Summary"),
    ],
)}

Selected claim rows:

{md_table(
    claims.sort_values(["domain", "claim_order"]).head(16),
    [
        ("domain", "Domain"),
        ("claim_order", "Order"),
        ("claim_area", "Area"),
        ("paper_use_tier", "Tier"),
        ("allowed_claim", "Allowed Claim"),
        ("not_allowed", "Not Allowed"),
    ],
)}
"""
        )
    )

    source_rows = pd.DataFrame(
        [
            {
                "artifact": "Notebook report",
                "path": str(NOTEBOOK_PATH),
                "role": "primary report artifact",
            },
            {
                "artifact": "Generated report tables and figures",
                "path": str(REPORT_DIR),
                "role": "reproducible support directory",
            },
            {
                "artifact": "Recent checkpoint summary",
                "path": "docs/update/summary/013_2026-06-19_local_2d_field_report_checkpoint.md",
                "role": "natural-checkpoint narrative",
            },
            {
                "artifact": "Latest manuscript table pack",
                "path": str(TABLE_PACK_ROOT),
                "role": "claim, figure, and metric inventory",
            },
            {
                "artifact": "Synthetic fixed-radius lock design",
                "path": str(LOCK_DESIGN_ROOT),
                "role": "CPU-side lock policy",
            },
            {
                "artifact": "Synthetic fixed-radius lock validation",
                "path": str(LOCK_VALIDATION_ROOT),
                "role": "guarded unlock validation",
            },
            {
                "artifact": "Field critical-path checkpoint",
                "path": str(FIELD_CRITICAL_ROOT),
                "role": "field natural checkpoint and next collection plan",
            },
        ]
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Source Artifacts And Reproducibility

{md_table(source_rows, [("artifact", "Artifact"), ("path", "Path"), ("role", "Role")])}

Generated figure validation:

{md_table(
    figure_validation,
    [
        ("path", "Figure"),
        ("width", "Width"),
        ("height", "Height"),
        ("sampled_unique_colors", "Unique Colors"),
        ("nonwhite_fraction", "Nonwhite Fraction"),
    ],
)}
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Recommended Next Steps

For the synthetic 2D side:

- Write the report around acquisition-aware identifiability and ambiguity, not
  around a universal rebar spacing limit.
- Present run `1358` as a single-branch fixed-radius locking mechanism
  validation, with run `1357` and summary tables `130-132` as the evidence
  chain.
- Keep broad GPU queues and detector-seeded FWI closed until CPU-side policy
  synthesis identifies a narrow, falsifiable next probe.

For the field side:

- Treat the archive as independent 2D line profiles. Current field geometry:
  `{field_summary.get("field_geometry_type")}`; 3D survey status:
  `{bool_label(field_summary.get("is_3d_survey"))}`.
- Execute the controlled 2D collection packet before attempting packet
  acceptance, field FWI, heavy GPU work, or field-side HPC work.
- Use run `156` as the resumption point because it states which gates are
  blocked and which new measurements are required.
"""
        )
    )

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {"display_name": "Python 3 (gpr-fdtd-fwi)", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.write_text(nbf.writes(nb))


def build_report() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    synthetic_runs = discover_synthetic_runs()
    field_runs = discover_field_runs()
    synthetic_phase = phase_summary(synthetic_runs)
    field_phase = phase_summary(field_runs)

    table_summary = read_json(TABLE_PACK_ROOT / "data" / "local_2d_field_manuscript_table_pack_summary.json")
    lock_design = read_json(LOCK_DESIGN_ROOT / "data" / "local_2d_detector_fixed_radius_locking_policy_summary.json")
    lock_validation = read_json(
        LOCK_VALIDATION_ROOT / "data" / "local_2d_detector_fixed_radius_locking_policy_validation_summary.json"
    )
    field_summary = read_json(FIELD_CRITICAL_ROOT / "data" / "field_controlled_collection_critical_path_summary.json")

    claims = read_csv(TABLE_PACK_ROOT / "data" / "local_2d_field_manuscript_claim_table.csv")
    figures = read_csv(TABLE_PACK_ROOT / "data" / "local_2d_field_manuscript_figure_inventory.csv")
    metrics = read_csv(TABLE_PACK_ROOT / "data" / "local_2d_field_manuscript_result_metrics.csv")
    gates = read_csv(FIELD_CRITICAL_ROOT / "data" / "field_controlled_collection_gate_critical_path.csv")
    actions = read_csv(FIELD_CRITICAL_ROOT / "data" / "field_controlled_collection_critical_actions.csv")
    phases = read_csv(FIELD_CRITICAL_ROOT / "data" / "field_controlled_collection_phase_plan.csv")
    endpoint_rows = build_locking_endpoint_rows()

    key_metrics = build_key_metrics(
        synthetic_runs=synthetic_runs,
        field_runs=field_runs,
        table_summary=table_summary,
        lock_design=lock_design,
        lock_validation=lock_validation,
        field_summary=field_summary,
        endpoint_rows=endpoint_rows,
    )

    paths = {
        "scope_counts": FIG_DIR / "local_2d_field_scope_counts.png",
        "synthetic_phase": FIG_DIR / "recent_synthetic_2d_phase_coverage.png",
        "field_phase": FIG_DIR / "field_phase_coverage_001_156.png",
        "synthetic_endpoint": FIG_DIR / "synthetic_fixed_radius_locking_endpoint.png",
        "claim_inventory": FIG_DIR / "claim_figure_inventory.png",
        "field_gates": FIG_DIR / "field_critical_path_gates.png",
        "field_phase_plan": FIG_DIR / "field_controlled_collection_phase_plan.png",
    }

    plot_scope_counts(synthetic_runs, field_runs, table_summary, field_summary, paths["scope_counts"])
    plot_phase_summary(synthetic_runs, "Recent Synthetic 2D Phase Coverage", paths["synthetic_phase"], "#2a6f97")
    plot_phase_summary(field_runs, "Field Experiment Phase Coverage", paths["field_phase"], "#7b2cbf")
    plot_synthetic_endpoint(endpoint_rows, lock_design, paths["synthetic_endpoint"])
    plot_claim_inventory(claims, figures, paths["claim_inventory"])
    plot_field_gates(gates, paths["field_gates"])
    plot_field_phase_plan(phases, paths["field_phase_plan"])

    figure_validation = validate_figures(paths.values())

    write_csv(synthetic_runs, DATA_DIR / "recent_synthetic_runs_1200_1358.csv")
    write_csv(synthetic_phase, DATA_DIR / "recent_synthetic_phase_summary.csv")
    write_csv(field_runs, DATA_DIR / "field_runs_001_156.csv")
    write_csv(field_phase, DATA_DIR / "field_phase_summary.csv")
    write_csv(endpoint_rows, DATA_DIR / "synthetic_fixed_radius_endpoint_rows.csv")
    write_csv(key_metrics, DATA_DIR / "local_2d_field_holistic_key_metrics.csv")
    write_csv(metrics, DATA_DIR / "source_table_pack_result_metrics.csv")
    write_csv(figure_validation, DATA_DIR / "figure_validation.csv")

    context = {
        "synthetic_runs": synthetic_runs,
        "field_runs": field_runs,
        "synthetic_phase": synthetic_phase,
        "field_phase": field_phase,
        "table_summary": table_summary,
        "lock_design": lock_design,
        "lock_validation": lock_validation,
        "field_summary": field_summary,
        "claims": claims,
        "figures": figures,
        "metrics": metrics,
        "gates": gates,
        "actions": actions,
        "phases": phases,
        "endpoint_rows": endpoint_rows,
        "key_metrics": key_metrics,
        "figure_validation": figure_validation,
        "paths": paths,
    }
    write_notebook(context)
    return context


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--print-summary", action="store_true", help="Print generated artifact paths.")
    args = parser.parse_args()

    context = build_report()
    if args.print_summary:
        print(f"Wrote notebook: {NOTEBOOK_PATH}")
        print(f"Wrote report support directory: {REPORT_DIR}")
        print(
            "Scope: "
            f"{len(context['synthetic_runs'])} recent synthetic runs, "
            f"{len(context['field_runs'])} field runs, "
            f"{len(context['paths'])} generated figures."
        )


if __name__ == "__main__":
    main()
