"""Generate a holistic notebook report for output experiments 700-1218.

The report is intentionally generated from run artifacts instead of hand-edited
so later increments can extend the same tables and figures.
"""

from __future__ import annotations

import csv
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import nbformat as nbf
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from PIL import Image


RUN_MIN = 700
RUN_MAX = 1218
CUTOFF = 5.0e-4
REPORT_STEM = "004_2026-06-11_experiment_700_1218_holistic_evaluation"
REPORT_DIR = Path("outputs/summary_tables/experiment_700_1218_holistic_evaluation")
DATA_DIR = REPORT_DIR / "data"
FIG_DIR = REPORT_DIR / "figures"
SERIES_FIG_DIR = FIG_DIR / "series_charts"
NOTEBOOK_PATH = Path("docs/update/summary") / f"{REPORT_STEM}.ipynb"


OBJECTIVE_ORDER = [
    "base",
    "highband",
    "late",
    "late_high",
    "veryhigh",
    "early_high",
]

TARGET_NAMES = {
    0: "target0 shallow-left rebar",
    1: "target1 center rebar",
    2: "target2 deep-right rebar",
}


def parse_run_id(path_name: str) -> int | None:
    prefix = path_name.split("_", 1)[0]
    if not prefix.isdigit():
        return None
    return int(prefix)


def parse_seed(run_name: str) -> str:
    match = re.search(r"_seed([0-9]+)", run_name)
    return match.group(1) if match else ""


def parse_target(run_name: str) -> int | None:
    match = re.search(r"_target([0-9]+)", run_name)
    return int(match.group(1)) if match else None


def parse_ringdown_label(run_name: str) -> str:
    match = re.search(r"_ringdown([0-9]+)", run_name)
    return match.group(1) if match else ""


def ringdown_value(label: str) -> float:
    if not label:
        return math.nan
    if len(label) == 3:
        return int(label) / 100.0
    return int(label) / float(10 ** (len(label) - 1))


def tracker_number_for_output_run(run_id: int) -> int | None:
    """Best-effort tracker lookup by referenced output run path."""
    pattern = f"outputs/experiments/{run_id}_"
    for path in Path("docs/experiments").glob("*.md"):
        try:
            if pattern in path.read_text(errors="ignore"):
                tracker = parse_run_id(path.name)
                if tracker is not None:
                    return tracker
        except OSError:
            continue
    return None


def exact_geometry(summary: dict) -> bool | None:
    final = summary.get("final_state") or {}
    true_x = summary.get("true_x_values_mm")
    true_z = summary.get("true_z_values_mm")
    true_r = summary.get("truth_radius_values_mm") or summary.get("truth_radius_mm")
    final_x = final.get("x_values_mm")
    final_z = final.get("z_values_mm")
    final_r = final.get("radii_mm")
    if not (true_x and true_z and true_r and final_x and final_z and final_r):
        return None
    return bool(
        np.allclose(final_x, true_x, atol=1.0e-9)
        and np.allclose(final_z, true_z, atol=1.0e-9)
        and np.allclose(final_r, true_r, atol=1.0e-9)
    )


def read_csv_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def classify_phase(run_id: int) -> str:
    if run_id < 740:
        return "infrastructure/reporting outputs"
    if run_id <= 783:
        return "Tx/Rx and receiver-sampling diagnostics"
    if run_id <= 848:
        return "source-density and ringdown diagnostics"
    if run_id <= 1118:
        return "ringdown050 replication and rescue-policy development"
    if run_id == 1119:
        return "field-data QC baseline"
    return "extended ringdown050 replication and stop-point block"


def discover_coordinate_runs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows: list[dict] = []
    diag_rows: list[dict] = []
    top_rows: list[dict] = []

    for summary_path in sorted(
        Path("outputs/experiments").glob("*/data/multi_rebar_coordinate_optimizer_summary.json")
    ):
        run_dir = summary_path.parent.parent
        run_id = parse_run_id(run_dir.name)
        if run_id is None or not (RUN_MIN <= run_id <= RUN_MAX):
            continue
        summary = json.loads(summary_path.read_text())
        confidence_rows = read_csv_rows(run_dir / "data/coordinate_confidence_report.csv")
        if not confidence_rows:
            continue
        confidence = confidence_rows[0]
        target = int(confidence.get("target_rebar_index") or parse_target(run_dir.name) or -1)
        seed = parse_seed(run_dir.name)
        ring_label = parse_ringdown_label(run_dir.name)
        tx_rx = float(summary.get("tx_rx_offset_mm") or confidence.get("tx_rx_offset_mm") or 0.0)
        sources = int(summary.get("sources") or 0)
        margin = float(confidence.get("radius_margin_abs") or "nan")
        best_misfit = float(confidence.get("best_misfit") or "nan")
        next_misfit = float(confidence.get("next_radius_misfit") or "nan")
        elapsed = float(summary.get("elapsed_time_s") or summary.get("elapsed_seconds") or "nan")
        tracker = tracker_number_for_output_run(run_id)

        rows.append(
            {
                "run_id": run_id,
                "run_name": run_dir.name,
                "output_path": str(run_dir),
                "tracker_number": tracker,
                "seed": seed,
                "seed_label": f"seed{seed}" if seed else "",
                "target": target,
                "target_name": TARGET_NAMES.get(target, f"target{target}"),
                "sources": sources,
                "tx_rx_offset_mm": tx_rx,
                "ringdown_label": ring_label,
                "ringdown_value": ringdown_value(ring_label),
                "linear_receiver": "linear_receiver" in run_dir.name,
                "base_margin": margin,
                "margin_offset_from_cutoff": margin - CUTOFF,
                "confidence_label": confidence.get("confidence_label", ""),
                "fallback_warning": confidence.get("fallback_warning", ""),
                "best_misfit": best_misfit,
                "next_radius_misfit": next_misfit,
                "best_radius_mm": float(confidence.get("best_radius_mm") or "nan"),
                "next_radius_mm": float(confidence.get("next_radius_mm") or "nan"),
                "competing_geometry_radius_mm": float(
                    confidence.get("competing_geometry_radius_mm") or "nan"
                ),
                "elapsed_time_s": elapsed,
                "phase": classify_phase(run_id),
                "exact_geometry": exact_geometry(summary),
            }
        )

        for diag in read_csv_rows(run_dir / "data/coordinate_objective_diagnostics.csv"):
            label = diag.get("objective_label") or diag.get("variant") or ""
            diag_rows.append(
                {
                    "run_id": run_id,
                    "objective_label": label,
                    "objective_margin": float(diag.get("radius_margin_abs") or "nan"),
                    "objective_margin_offset": float(diag.get("radius_margin_abs") or "nan") - CUTOFF,
                    "best_x_mm": float(diag.get("best_x_mm") or "nan"),
                    "best_z_mm": float(diag.get("best_z_mm") or "nan"),
                    "best_radius_mm": float(diag.get("best_radius_mm") or "nan"),
                }
            )

        for top in read_csv_rows(run_dir / "data/coordinate_objective_top_candidates.csv"):
            if top.get("rank") == "1":
                top_rows.append(
                    {
                        "run_id": run_id,
                        "objective_label": top.get("objective_label", ""),
                        "x_mm": float(top.get("x_mm") or "nan"),
                        "z_mm": float(top.get("z_mm") or "nan"),
                        "radius_mm": float(top.get("radius_mm") or "nan"),
                    }
                )

    run_df = pd.DataFrame(rows).sort_values("run_id").reset_index(drop=True)
    diag_df = pd.DataFrame(diag_rows).sort_values(["run_id", "objective_label"]).reset_index(drop=True)
    top_df = pd.DataFrame(top_rows).sort_values(["run_id", "objective_label"]).reset_index(drop=True)
    return run_df, diag_df, top_df


@dataclass
class SeriesSpec:
    series_id: str
    series_type: str
    title: str
    run_ids: list[int]
    varied_col: str
    conclusion: str
    seed: str = ""
    target: int | None = None


def values_text(values: Iterable[object]) -> str:
    return ", ".join(str(v) for v in values)


def make_series_summary(spec: SeriesSpec, run_df: pd.DataFrame) -> dict:
    subset = run_df[run_df["run_id"].isin(spec.run_ids)].sort_values("run_id")
    best = subset.loc[subset["base_margin"].idxmax()]
    accepted = subset[subset["base_margin"] >= CUTOFF]
    return {
        "series_id": spec.series_id,
        "series_type": spec.series_type,
        "title": spec.title,
        "run_ids": values_text(subset["run_id"].astype(int).tolist()),
        "seed": spec.seed,
        "target": "" if spec.target is None else int(spec.target),
        "varied_col": spec.varied_col,
        "varied_values": values_text(subset[spec.varied_col].tolist()),
        "n_runs": len(subset),
        "accepted_runs": values_text(accepted["run_id"].astype(int).tolist()),
        "weak_runs": values_text(
            subset.loc[subset["base_margin"] < CUTOFF, "run_id"].astype(int).tolist()
        ),
        "best_run": int(best["run_id"]),
        "best_margin": float(best["base_margin"]),
        "all_exact_geometry": bool(subset["exact_geometry"].fillna(False).all()),
        "conclusion": spec.conclusion,
    }


def detect_series(run_df: pd.DataFrame) -> list[SeriesSpec]:
    specs: list[SeriesSpec] = []

    def add_grouped(
        series_type: str,
        group_cols: list[str],
        varied_col: str,
        title_prefix: str,
    ) -> None:
        grouped = run_df.groupby(group_cols, dropna=False)
        for key, group in grouped:
            if group[varied_col].nunique(dropna=True) < 2 or len(group) < 2:
                continue
            group = group.sort_values("run_id")
            key_dict = dict(zip(group_cols, key if isinstance(key, tuple) else (key,)))
            seed = str(key_dict.get("seed", ""))
            target = int(key_dict.get("target", -1))
            run_ids = group["run_id"].astype(int).tolist()
            best = group.loc[group["base_margin"].idxmax()]
            accepted = group[group["base_margin"] >= CUTOFF]
            if accepted.empty:
                conclusion = (
                    f"All tested rows stayed below the strict {CUTOFF:.1e} base-margin cutoff; "
                    f"best tested run is {int(best.run_id)}."
                )
            elif len(accepted) == len(group):
                conclusion = (
                    f"All tested rows cleared the strict {CUTOFF:.1e} base-margin cutoff; "
                    f"best tested run is {int(best.run_id)}."
                )
            else:
                conclusion = (
                    f"At least one row cleared the strict {CUTOFF:.1e} base-margin cutoff; "
                    f"best tested run is {int(best.run_id)}."
                )
            varied_values = values_text(group[varied_col].tolist())
            series_id = (
                f"{series_type}_seed{seed}_target{target}_runs{run_ids[0]}_{run_ids[-1]}"
            ).replace(".", "p")
            title = (
                f"{title_prefix}: seed{seed} target{target}, runs "
                f"{run_ids[0]}-{run_ids[-1]}, {varied_col}={varied_values}"
            )
            specs.append(
                SeriesSpec(
                    series_id=series_id,
                    series_type=series_type,
                    title=title,
                    run_ids=run_ids,
                    varied_col=varied_col,
                    conclusion=conclusion,
                    seed=seed,
                    target=target,
                )
            )

    add_grouped(
        "source_density",
        ["seed", "target", "ringdown_label", "tx_rx_offset_mm", "linear_receiver"],
        "sources",
        "Source-density series",
    )
    add_grouped(
        "tx_rx_offset",
        ["seed", "target", "ringdown_label", "sources", "linear_receiver"],
        "tx_rx_offset_mm",
        "Tx/Rx-offset series",
    )
    add_grouped(
        "ringdown",
        ["seed", "target", "sources", "tx_rx_offset_mm", "linear_receiver"],
        "ringdown_value",
        "Ringdown-parameter series",
    )
    return sorted(specs, key=lambda spec: (spec.series_type, min(spec.run_ids), spec.series_id))


def curated_series(run_df: pd.DataFrame) -> list[SeriesSpec]:
    specs = [
        SeriesSpec(
            "curated_seed5527939710754757_target1_sources_1216_1218",
            "curated",
            "Seed5527939710754757 target1 source-density rescue did not resolve radius confidence",
            [1216, 1217, 1218],
            "sources",
            (
                "The exact target1 geometry is preserved, but base margin rises at 9 sources "
                "and then drops at 11 sources. This supports stopping the source-density ladder."
            ),
            "5527939710754757",
            1,
        ),
        SeriesSpec(
            "curated_seed5527939710754757_target0_txrx_1211_1214",
            "curated",
            "Seed5527939710754757 target0 Tx/Rx acquisition bracket found a stronger lower offset",
            [1211, 1212, 1213, 1214],
            "tx_rx_offset_mm",
            (
                "Target0 base margin improves as Tx/Rx offset is reduced from 60 to 45 mm, "
                "making 45 mm the strongest tested point for this seed."
            ),
            "5527939710754757",
            0,
        ),
        SeriesSpec(
            "curated_seed3416454629006707_target2_sources_1207_1209",
            "curated",
            "Seed3416454629006707 target2 source-density ladder rescued a weak control",
            [1207, 1208, 1209],
            "sources",
            (
                "Target2 is weak at 5 and 7 sources but crosses the base cutoff at 9 sources, "
                "supporting the 5/7/9 source-density ladder for this target."
            ),
            "3416454629006707",
            2,
        ),
        SeriesSpec(
            "curated_seed2111485081748050_target2_sources_1203_1204",
            "curated",
            "Seed2111485081748050 target2 7-source bracket rescued a near-miss control",
            [1203, 1204],
            "sources",
            (
                "The 5-source target2 run is a near-miss, and the 7-source bracket clears the "
                "strict base-margin cutoff without a 9-source escalation."
            ),
            "2111485081748050",
            2,
        ),
        SeriesSpec(
            "curated_seed365435296162_target0_txrx_1120_1123",
            "curated",
            "Seed365435296162 target0 Tx/Rx bracket established the lower-offset rescue pattern",
            [1120, 1121, 1122, 1123],
            "tx_rx_offset_mm",
            (
                "This earlier bracket shows the same target0 behavior: lowering Tx/Rx offset "
                "turns a weak exact row into an accepted row with better reserve."
            ),
            "365435296162",
            0,
        ),
        SeriesSpec(
            "curated_seed139583862445_target1_sources_1114_1115",
            "curated",
            "Seed139583862445 target1 9-source rescue converted a weak control",
            [1114, 1115],
            "sources",
            (
                "A 9-source target1 rescue can work: the weak 5-source row becomes accepted "
                "and all objective variants rank the true geometry."
            ),
            "139583862445",
            1,
        ),
        SeriesSpec(
            "curated_seed72723460378141_target1_sources_1172_1173",
            "curated",
            "Seed72723460378141 target1 9-source rescue produced a clean acceptance",
            [1172, 1173],
            "sources",
            (
                "This branch is a clean target1 rescue example, contrasting with the later "
                "seed5527939710754757 unresolved branch."
            ),
            "72723460378141",
            1,
        ),
        SeriesSpec(
            "curated_seed89_target2_txrx_threshold_759_769",
            "curated",
            "Seed89 target2 Tx/Rx threshold and linear-receiver sensitivity",
            [759, 760, 761, 762, 763, 765, 766, 767, 769],
            "tx_rx_offset_mm",
            (
                "The target2 confidence drop around 50-60 mm Tx/Rx offset motivated later "
                "acquisition and receiver-sampling checks."
            ),
            "89",
            2,
        ),
    ]
    available = set(run_df["run_id"].astype(int).tolist())
    return [spec for spec in specs if set(spec.run_ids).issubset(available)]


def ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    SERIES_FIG_DIR.mkdir(parents=True, exist_ok=True)
    NOTEBOOK_PATH.parent.mkdir(parents=True, exist_ok=True)


def target_color(target: int) -> str:
    return {0: "#4477AA", 1: "#CC6677", 2: "#228833"}.get(int(target), "#777777")


def save_overview_plots(run_df: pd.DataFrame, series_df: pd.DataFrame) -> dict[str, Path]:
    paths: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(15, 5.5))
    for target, group in run_df.groupby("target"):
        ax.scatter(
            group["run_id"],
            group["base_margin"],
            s=26,
            alpha=0.78,
            label=f"target{int(target)}",
            color=target_color(int(target)),
        )
    ax.axhline(CUTOFF, color="black", linestyle="--", linewidth=1.2, label="strict cutoff")
    ax.set_title("Base radius-confidence margin by output experiment ID")
    ax.set_xlabel("Output experiment ID")
    ax.set_ylabel("Base margin: best radius minus next radius objective gap")
    ax.legend(ncol=4, frameon=False)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    paths["overview_margin_by_run"] = FIG_DIR / "overview_margin_by_run.png"
    fig.savefig(paths["overview_margin_by_run"], dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    accept_df = (
        run_df.assign(accepted=run_df["base_margin"] >= CUTOFF)
        .groupby("target")["accepted"]
        .agg(["mean", "count"])
        .reset_index()
    )
    ax.bar(
        [f"target{int(t)}" for t in accept_df["target"]],
        accept_df["mean"] * 100.0,
        color=[target_color(int(t)) for t in accept_df["target"]],
    )
    for idx, row in accept_df.iterrows():
        ax.text(idx, row["mean"] * 100.0 + 1.2, f"n={int(row['count'])}", ha="center")
    ax.set_ylim(0, 105)
    ax.set_ylabel("Rows clearing strict cutoff [%]")
    ax.set_title("Acceptance rate by target rebar")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    paths["acceptance_rate_by_target"] = FIG_DIR / "acceptance_rate_by_target.png"
    fig.savefig(paths["acceptance_rate_by_target"], dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5.2))
    data = [run_df.loc[run_df["target"] == target, "base_margin"].dropna() for target in [0, 1, 2]]
    ax.boxplot(data, tick_labels=["target0", "target1", "target2"], showmeans=True)
    ax.axhline(CUTOFF, color="black", linestyle="--", linewidth=1.2)
    ax.set_ylabel("Base margin")
    ax.set_title("Base-margin distribution by target")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    paths["margin_distribution_by_target"] = FIG_DIR / "margin_distribution_by_target.png"
    fig.savefig(paths["margin_distribution_by_target"], dpi=180)
    plt.close(fig)

    phase_counts = (
        run_df.groupby("phase")["run_id"].count().sort_values(ascending=True)
    )
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.barh(phase_counts.index, phase_counts.values, color="#667788")
    for idx, value in enumerate(phase_counts.values):
        ax.text(value + 1, idx, str(int(value)), va="center")
    ax.set_xlabel("Parseable coordinate-optimizer runs")
    ax.set_title("Report coverage by experiment phase")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    paths["phase_coverage"] = FIG_DIR / "phase_coverage.png"
    fig.savefig(paths["phase_coverage"], dpi=180)
    plt.close(fig)

    if not series_df.empty:
        counts = series_df.groupby("series_type")["series_id"].count().sort_values()
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(counts.index, counts.values, color="#AA7744")
        for idx, value in enumerate(counts.values):
            ax.text(value + 0.5, idx, str(int(value)), va="center")
        ax.set_xlabel("Detected multi-run series")
        ax.set_title("Automatically detected experiment-series families")
        ax.grid(axis="x", alpha=0.25)
        fig.tight_layout()
        paths["detected_series_counts"] = FIG_DIR / "detected_series_counts.png"
        fig.savefig(paths["detected_series_counts"], dpi=180)
        plt.close(fig)

    return paths


def plot_series(
    spec: SeriesSpec,
    run_df: pd.DataFrame,
    diag_df: pd.DataFrame,
    out_dir: Path,
    detailed: bool = False,
) -> Path:
    subset = run_df[run_df["run_id"].isin(spec.run_ids)].sort_values("run_id")
    if spec.varied_col == "ringdown_value":
        x = subset["ringdown_value"].to_numpy(dtype=float)
        x_label = "Ringdown coefficient"
    elif spec.varied_col == "tx_rx_offset_mm":
        x = subset["tx_rx_offset_mm"].to_numpy(dtype=float)
        x_label = "Tx/Rx offset [mm]"
    elif spec.varied_col == "sources":
        x = subset["sources"].to_numpy(dtype=float)
        x_label = "Number of source positions"
    else:
        x = np.arange(len(subset))
        x_label = spec.varied_col

    if detailed:
        fig, axes = plt.subplots(2, 1, figsize=(10.5, 8.2), gridspec_kw={"height_ratios": [1.0, 1.1]})
        ax = axes[0]
    else:
        fig, ax = plt.subplots(figsize=(8, 4.8))

    color = target_color(int(subset["target"].iloc[0]))
    ax.plot(x, subset["base_margin"], marker="o", color=color, linewidth=2)
    ax.axhline(CUTOFF, color="black", linestyle="--", linewidth=1.1)
    for xi, (_, row) in zip(x, subset.iterrows()):
        ax.text(xi, row["base_margin"], str(int(row["run_id"])), fontsize=8, ha="center", va="bottom")
    ax.set_title(spec.title)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Base margin")
    ax.grid(True, alpha=0.25)
    if len(set(x)) == len(x):
        ax.set_xticks(x)

    if detailed:
        heat = []
        labels = []
        for run_id in subset["run_id"].astype(int).tolist():
            row = []
            labels.append(str(run_id))
            dsub = diag_df[diag_df["run_id"] == run_id].set_index("objective_label")
            for objective in OBJECTIVE_ORDER:
                if objective in dsub.index:
                    row.append(float(dsub.loc[objective, "objective_margin"]))
                else:
                    row.append(np.nan)
            heat.append(row)
        arr = np.array(heat).T
        hax = axes[1]
        image = hax.imshow(arr, aspect="auto", cmap="viridis", vmin=0.0, vmax=max(0.001, np.nanmax(arr)))
        hax.set_yticks(np.arange(len(OBJECTIVE_ORDER)))
        hax.set_yticklabels(OBJECTIVE_ORDER)
        hax.set_xticks(np.arange(len(labels)))
        hax.set_xticklabels(labels)
        hax.set_xlabel("Output experiment ID")
        hax.set_title("Objective-variant radius margins; cutoff is 5.0e-4")
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                if np.isfinite(arr[i, j]):
                    text_color = "white" if arr[i, j] < 0.00055 else "black"
                    hax.text(j, i, f"{arr[i, j]:.1e}", ha="center", va="center", fontsize=7, color=text_color)
        fig.colorbar(image, ax=hax, label="Margin")

    fig.tight_layout()
    path = out_dir / f"{spec.series_id}.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


def make_seed_branch_plot(run_df: pd.DataFrame) -> Path:
    ring = run_df[(run_df["ringdown_label"] == "050") & (run_df["seed"] != "")]
    rows = []
    for (seed, target), group in ring.groupby(["seed", "target"]):
        best = group.loc[group["base_margin"].idxmax()]
        latest = group.sort_values("run_id").iloc[-1]
        rows.append(
            {
                "seed": seed,
                "target": int(target),
                "best_margin": float(best["base_margin"]),
                "best_run": int(best["run_id"]),
                "latest_margin": float(latest["base_margin"]),
                "latest_run": int(latest["run_id"]),
                "accepted": float(best["base_margin"]) >= CUTOFF,
            }
        )
    branch = pd.DataFrame(rows)
    # Keep the later replication block readable.
    branch = branch[branch["best_run"] >= 900].copy()
    branch["seed_num"] = branch["seed"].astype("int64")
    branch = branch.sort_values("seed_num")
    seeds = branch["seed"].drop_duplicates().tolist()
    matrix = np.full((len(seeds), 3), np.nan)
    labels = [["" for _ in range(3)] for _ in seeds]
    for i, seed in enumerate(seeds):
        for target in [0, 1, 2]:
            row = branch[(branch["seed"] == seed) & (branch["target"] == target)]
            if row.empty:
                continue
            value = float(row.iloc[0]["best_margin"])
            matrix[i, target] = value
            labels[i][target] = str(int(row.iloc[0]["best_run"]))
    fig_height = max(8, len(seeds) * 0.28)
    fig, ax = plt.subplots(figsize=(8.4, fig_height))
    image = ax.imshow(matrix, aspect="auto", cmap="viridis", vmin=0.0, vmax=max(0.001, np.nanmax(matrix)))
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(["target0", "target1", "target2"])
    ax.set_yticks(np.arange(len(seeds)))
    ax.set_yticklabels([f"seed{s}" for s in seeds], fontsize=7)
    ax.set_title("Best accepted-or-tested base margin by seed and target, ringdown050 runs >=900")
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if np.isfinite(matrix[i, j]):
                color = "white" if matrix[i, j] < 0.00055 else "black"
                ax.text(j, i, f"{labels[i][j]}\n{matrix[i,j]:.1e}", ha="center", va="center", fontsize=6, color=color)
    fig.colorbar(image, ax=ax, label="Best base margin")
    fig.tight_layout()
    path = FIG_DIR / "seed_branch_best_margin_grid.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def summarize_intervention_series(specs: list[SeriesSpec], run_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for spec in specs:
        subset = run_df[run_df["run_id"].isin(spec.run_ids)].copy()
        if subset.empty:
            continue
        sort_cols = [spec.varied_col, "run_id"] if spec.varied_col in subset.columns else ["run_id"]
        ordered = subset.sort_values(sort_cols)
        accepted = subset[subset["base_margin"] >= CUTOFF]
        weak = subset[subset["base_margin"] < CUTOFF]
        best = subset.loc[subset["base_margin"].idxmax()]
        worst = subset.loc[subset["base_margin"].idxmin()]
        first = ordered.iloc[0]
        last = ordered.iloc[-1]
        if len(accepted) == len(subset):
            outcome = "all accepted"
        elif accepted.empty:
            outcome = "all weak"
        else:
            outcome = "mixed: accepted setting exists"
        rows.append(
            {
                "series_id": spec.series_id,
                "series_type": spec.series_type,
                "run_ids": values_text(subset.sort_values("run_id")["run_id"].astype(int).tolist()),
                "first_run": int(subset["run_id"].min()),
                "last_run": int(subset["run_id"].max()),
                "seed": spec.seed,
                "target": "" if spec.target is None else int(spec.target),
                "varied_col": spec.varied_col,
                "n_runs": len(subset),
                "n_accepted": len(accepted),
                "n_weak": len(weak),
                "outcome_category": outcome,
                "first_setting": first[spec.varied_col] if spec.varied_col in first.index else math.nan,
                "last_setting": last[spec.varied_col] if spec.varied_col in last.index else math.nan,
                "best_setting": best[spec.varied_col] if spec.varied_col in best.index else math.nan,
                "worst_setting": worst[spec.varied_col] if spec.varied_col in worst.index else math.nan,
                "first_margin": float(first["base_margin"]),
                "last_margin": float(last["base_margin"]),
                "best_run": int(best["run_id"]),
                "worst_run": int(worst["run_id"]),
                "best_margin": float(best["base_margin"]),
                "worst_margin": float(worst["base_margin"]),
                "best_minus_worst_margin": float(best["base_margin"] - worst["base_margin"]),
                "best_minus_first_margin": float(best["base_margin"] - first["base_margin"]),
                "all_exact_geometry": bool(subset["exact_geometry"].fillna(False).all()),
            }
        )
    return pd.DataFrame(rows).sort_values(["series_type", "first_run"]).reset_index(drop=True)


def make_source_count_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    return (
        run_df.groupby(["target", "sources"])
        .agg(
            run_count=("run_id", "count"),
            accepted_fraction=("base_margin", lambda s: float((s >= CUTOFF).mean())),
            median_margin=("base_margin", "median"),
            q25_margin=("base_margin", lambda s: float(s.quantile(0.25))),
            q75_margin=("base_margin", lambda s: float(s.quantile(0.75))),
            first_run=("run_id", "min"),
            last_run=("run_id", "max"),
        )
        .reset_index()
        .sort_values(["target", "sources"])
    )


def make_txrx_summary(run_df: pd.DataFrame) -> pd.DataFrame:
    return (
        run_df.groupby(["target", "tx_rx_offset_mm"])
        .agg(
            run_count=("run_id", "count"),
            accepted_fraction=("base_margin", lambda s: float((s >= CUTOFF).mean())),
            median_margin=("base_margin", "median"),
            q25_margin=("base_margin", lambda s: float(s.quantile(0.25))),
            q75_margin=("base_margin", lambda s: float(s.quantile(0.75))),
            first_run=("run_id", "min"),
            last_run=("run_id", "max"),
        )
        .reset_index()
        .sort_values(["target", "tx_rx_offset_mm"])
    )


def save_policy_plots(
    run_df: pd.DataFrame,
    policy_df: pd.DataFrame,
    source_summary_df: pd.DataFrame,
    txrx_summary_df: pd.DataFrame,
    target1_source_policy_df: pd.DataFrame,
) -> dict[str, Path]:
    paths: dict[str, Path] = {}

    outcome_order = ["all accepted", "mixed: accepted setting exists", "all weak"]
    outcome_colors = {
        "all accepted": "#228833",
        "mixed: accepted setting exists": "#CCBB44",
        "all weak": "#CC6677",
    }
    type_order = ["source_density", "tx_rx_offset", "ringdown"]
    pivot = (
        policy_df.groupby(["series_type", "outcome_category"])["series_id"]
        .count()
        .unstack(fill_value=0)
        .reindex(type_order)
        .fillna(0)
    )
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    bottom = np.zeros(len(pivot))
    x = np.arange(len(pivot))
    for outcome in outcome_order:
        values = pivot[outcome].to_numpy() if outcome in pivot.columns else np.zeros(len(pivot))
        ax.bar(x, values, bottom=bottom, color=outcome_colors[outcome], label=outcome)
        bottom += values
    for idx, total in enumerate(bottom):
        ax.text(idx, total + 0.6, str(int(total)), ha="center", va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels(["source-density", "Tx/Rx offset", "ringdown"])
    ax.set_ylabel("Detected series")
    ax.set_title("Intervention-series outcomes")
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    paths["intervention_outcome_counts"] = FIG_DIR / "intervention_outcome_counts.png"
    fig.savefig(paths["intervention_outcome_counts"], dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    data = [
        policy_df.loc[policy_df["series_type"] == series_type, "best_minus_worst_margin"].dropna()
        for series_type in type_order
    ]
    ax.boxplot(data, tick_labels=["source-density", "Tx/Rx offset", "ringdown"], showmeans=True)
    rng = np.random.default_rng(17)
    for idx, values in enumerate(data, start=1):
        if values.empty:
            continue
        jitter = rng.normal(0.0, 0.035, size=len(values))
        ax.scatter(np.full(len(values), idx) + jitter, values, s=18, alpha=0.45, color="#556677")
    ax.set_ylabel("Best minus worst base margin within series")
    ax.set_title("How much each intervention family can move the margin")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    paths["intervention_margin_spread"] = FIG_DIR / "intervention_margin_spread.png"
    fig.savefig(paths["intervention_margin_spread"], dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(10.2, 7.4), sharex=True)
    for target, group in source_summary_df.groupby("target"):
        color = target_color(int(target))
        axes[0].plot(
            group["sources"],
            group["median_margin"],
            marker="o",
            linewidth=2,
            color=color,
            label=f"target{int(target)}",
        )
        axes[1].plot(
            group["sources"],
            group["accepted_fraction"] * 100.0,
            marker="o",
            linewidth=2,
            color=color,
            label=f"target{int(target)}",
        )
        for _, row in group.iterrows():
            axes[0].text(
                row["sources"],
                row["median_margin"],
                f"n={int(row['run_count'])}",
                fontsize=7,
                ha="center",
                va="bottom",
            )
    axes[0].axhline(CUTOFF, color="black", linestyle="--", linewidth=1.1)
    axes[0].set_ylabel("Median base margin")
    axes[0].set_title("Source-count evidence by target")
    axes[0].grid(True, alpha=0.25)
    axes[0].legend(frameon=False, ncol=3)
    axes[1].set_ylabel("Rows clearing cutoff [%]")
    axes[1].set_xlabel("Number of source positions")
    axes[1].set_ylim(-3, 103)
    axes[1].grid(True, alpha=0.25)
    fig.tight_layout()
    paths["source_count_by_target_policy"] = FIG_DIR / "source_count_by_target_policy.png"
    fig.savefig(paths["source_count_by_target_policy"], dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.2), sharey=True)
    for target, ax in zip([0, 1, 2], axes):
        raw = run_df[run_df["target"] == target]
        summary = txrx_summary_df[txrx_summary_df["target"] == target]
        color = target_color(target)
        ax.scatter(
            raw["tx_rx_offset_mm"],
            raw["base_margin"],
            s=22,
            alpha=0.28,
            color=color,
            label="individual runs",
        )
        ax.plot(
            summary["tx_rx_offset_mm"],
            summary["median_margin"],
            marker="D",
            linewidth=1.8,
            color="black",
            label="median by offset",
        )
        for _, row in summary.iterrows():
            if int(row["run_count"]) >= 2:
                ax.text(
                    row["tx_rx_offset_mm"],
                    row["median_margin"],
                    f"n={int(row['run_count'])}",
                    fontsize=7,
                    ha="center",
                    va="bottom",
                )
        ax.axhline(CUTOFF, color="black", linestyle="--", linewidth=1.0)
        ax.set_title(f"target{target}")
        ax.set_xlabel("Tx/Rx offset [mm]")
        ax.grid(True, alpha=0.25)
    axes[0].set_ylabel("Base margin")
    axes[2].legend(frameon=False, loc="upper right")
    fig.suptitle("Tx/Rx-offset evidence by target", y=0.98)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.94])
    paths["txrx_offset_by_target_policy"] = FIG_DIR / "txrx_offset_by_target_policy.png"
    fig.savefig(paths["txrx_offset_by_target_policy"], dpi=180)
    plt.close(fig)

    if not target1_source_policy_df.empty:
        t1 = target1_source_policy_df.sort_values("first_run").reset_index(drop=True)
        fig_height = max(5.5, len(t1) * 0.42)
        fig, ax = plt.subplots(figsize=(11.5, fig_height))
        y = np.arange(len(t1))
        colors = [
            outcome_colors.get(outcome, "#777777")
            for outcome in t1["outcome_category"].tolist()
        ]
        ax.hlines(y, t1["worst_margin"], t1["best_margin"], color="#8899AA", linewidth=2)
        ax.scatter(t1["best_margin"], y, s=50, color=colors, label="best setting")
        ax.scatter(t1["worst_margin"], y, s=35, facecolors="white", edgecolors="#445566", label="worst setting")
        labels = [
            f"{row.first_run}-{row.last_run} seed{str(row.seed)[:8]}"
            for row in t1.itertuples(index=False)
        ]
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=8)
        ax.axvline(CUTOFF, color="black", linestyle="--", linewidth=1.1)
        ax.set_xlabel("Base margin")
        ax.set_title("Target1 source-density branches: rescue successes and unresolved cases")
        ax.grid(axis="x", alpha=0.25)
        legend_handles = [
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor=outcome_colors["all accepted"],
                markeredgecolor=outcome_colors["all accepted"],
                markersize=7,
                label="all accepted",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor=outcome_colors["mixed: accepted setting exists"],
                markeredgecolor=outcome_colors["mixed: accepted setting exists"],
                markersize=7,
                label="mixed; accepted exists",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor=outcome_colors["all weak"],
                markeredgecolor=outcome_colors["all weak"],
                markersize=7,
                label="all weak",
            ),
            Line2D(
                [0],
                [0],
                marker="o",
                color="none",
                markerfacecolor="white",
                markeredgecolor="#445566",
                markersize=7,
                label="worst setting",
            ),
        ]
        ax.legend(handles=legend_handles, frameon=False, loc="lower right")
        fig.tight_layout()
        paths["target1_source_density_rescue_map"] = FIG_DIR / "target1_source_density_rescue_map.png"
        fig.savefig(paths["target1_source_density_rescue_map"], dpi=180)
        plt.close(fig)

    return paths


def validate_figures(paths: Iterable[Path]) -> pd.DataFrame:
    rows = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        sample = image.resize((min(image.width, 256), min(image.height, 256)))
        colors = sample.getcolors(maxcolors=1_000_000)
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


def notebook_rel(path: Path) -> str:
    return str(path.relative_to(NOTEBOOK_PATH.parent, walk_up=True))


def figure_block(alt: str, path: Path, caption: str) -> str:
    return f"![{alt}]({notebook_rel(path)})\n\n*Figure: {caption}*"


def md_table(rows: list[dict], columns: list[tuple[str, str]], max_rows: int | None = None) -> str:
    selected = rows[:max_rows] if max_rows is not None else rows
    header = "| " + " | ".join(label for _, label in columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in selected:
        cells = []
        for key, _ in columns:
            value = row.get(key, "")
            if isinstance(value, float):
                if abs(value) < 0.01:
                    value = f"{value:.3e}"
                else:
                    value = f"{value:.3f}"
            cells.append(str(value).replace("\n", " "))
        body.append("| " + " | ".join(cells) + " |")
    if max_rows is not None and len(rows) > max_rows:
        body.append(f"| ... | {len(rows) - max_rows} more rows omitted here; see CSV. |")
    return "\n".join([header, sep] + body)


def write_notebook(
    run_df: pd.DataFrame,
    series_df: pd.DataFrame,
    policy_df: pd.DataFrame,
    source_summary_df: pd.DataFrame,
    txrx_summary_df: pd.DataFrame,
    target1_source_policy_df: pd.DataFrame,
    overview_paths: dict[str, Path],
    policy_paths: dict[str, Path],
    curated_specs: list[SeriesSpec],
    curated_paths: dict[str, Path],
    appendix_specs: list[SeriesSpec],
    appendix_paths: dict[str, Path],
    seed_branch_path: Path,
) -> None:
    nb = nbf.v4.new_notebook()
    cells = []

    total_output_dirs = sum(
        1
        for path in Path("outputs/experiments").iterdir()
        if path.is_dir()
        and (rid := parse_run_id(path.name)) is not None
        and RUN_MIN <= rid <= RUN_MAX
    )
    accepted_count = int((run_df["base_margin"] >= CUTOFF).sum())
    exact_count = int(run_df["exact_geometry"].fillna(False).sum())
    weak_count = int((run_df["base_margin"] < CUTOFF).sum())

    cells.append(
        nbf.v4.new_markdown_cell(
            f"""# Holistic Technical Evaluation: Output Experiments {RUN_MIN}-{RUN_MAX}

Generated: 2026-06-11.

This notebook evaluates the coordinate-optimizer experiment archive from output
experiment IDs `{RUN_MIN}` through `{RUN_MAX}`. The scope includes
`{total_output_dirs}` numbered output folders and `{len(run_df)}` parseable
coordinate-optimizer runs with confidence CSV files.

The goal is not to repeat each individual run report. It is to show how groups
of experiments support decisions: when a source-density ladder works, when a
transmitter/receiver spacing probe works, and where a branch should stop.
"""
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Terms Used In This Notebook

- Ground-penetrating radar (GPR): the simulated radar measurement modality.
- Full-waveform inversion (FWI): an inverse method that compares simulated and
  observed waveforms to recover rebar geometry.
- Coordinate optimizer: the search routine that tests candidate rebar
  coordinates and radii, then selects the candidate with the best score.
- Objective, or objective function: the scoring rule used to compare a
  candidate model against the reference data. In this archive the score is a
  waveform mismatch, also called a misfit. Lower misfit is better. When the
  report says a candidate "wins" an objective, it means that candidate produced
  the smallest mismatch under that scoring rule.
- Base objective: the main/default scoring rule used for the acceptance
  decision.
- Objective variants: diagnostic scoring rules that use different signal
  windows or frequency bands, such as late-time or high-frequency content.
  They are not separate experiments; they are alternate checks on the same
  run. Agreement across variants gives stronger evidence than the base
  objective alone.
- Target rebar: the specific rebar being evaluated in a run. The synthetic
  three-rebar geometry used here is fixed unless stated otherwise.
- `target0`: the shallow-left rebar, x=150 mm, z=80 mm, radius=5 mm.
- `target1`: the center rebar, x=250 mm, z=100 mm, radius=6 mm.
- `target2`: the deeper-right rebar, x=350 mm, z=120 mm, radius=8 mm.
- Tx/Rx offset: transmitter-to-receiver spacing in millimeters.
- Source-density ladder: rerunning the same target with more source positions,
  for example 5, 7, 9, or 11 sources.
- Acquisition-offset bracket: rerunning the same target at different Tx/Rx
  offsets, for example 60, 52.5, 50, and 45 mm.
- `seed...`: the pseudo-random seed controlling the repeatable synthetic
  noise/source-mismatch draw. It is not a different physical rebar geometry.
  Unless explicitly stated, the true rebar geometry remains x=[150, 250, 350]
  mm, z=[80, 100, 120] mm, radius=[5, 6, 8] mm.
- Base margin: the gap, under the base objective, between the selected radius
  and the next-best competing radius. A larger margin means the radius choice
  is more clearly separated from the alternative. The strict
  moderate-confidence cutoff used here is 5.0e-4.
- Exact geometry: the selected x position, z depth, and radius match the known
  synthetic truth. Several weak rows still have exact geometry; they are weak
  because the confidence margin is small, not because the location is wrong.
- Accepted row: a run whose base margin is at or above 5.0e-4.
- Weak row: a run whose base margin is below 5.0e-4.
"""
        )
    )

    cells.append(
        nbf.v4.new_code_cell(
            """# This notebook is generated by run_experiment_700_1218_holistic_report.py.
# The supporting tables are in:
# outputs/summary_tables/experiment_700_1218_holistic_evaluation/data
import pandas as pd
run_summary = pd.read_csv("../../../outputs/summary_tables/experiment_700_1218_holistic_evaluation/data/coordinate_run_summary_700_1218.csv")
series_summary = pd.read_csv("../../../outputs/summary_tables/experiment_700_1218_holistic_evaluation/data/series_summary_700_1218.csv")
run_summary.head()"""
        )
    )

    overview_md = f"""## Archive-Level Summary

Across the `{len(run_df)}` parseable coordinate-optimizer runs:

- `{exact_count}` runs preserve the exact final x/z/r geometry.
- `{accepted_count}` runs clear the strict base-margin cutoff.
- `{weak_count}` runs remain below the strict base-margin cutoff.
- The weak rows are mostly radius-confidence limitations, not localization
  failures, because the selected geometry usually remains exact and diagnostic
  scoring variants often rank the true geometry first.

{figure_block(
    "Base margin by output experiment ID",
    overview_paths["overview_margin_by_run"],
    "Each point is one parseable coordinate-optimizer run. The dashed line is the strict 5.0e-4 base-margin cutoff; points below it are exact-geometry rows whose radius confidence is still too weak.",
)}

{figure_block(
    "Acceptance rate by target",
    overview_paths["acceptance_rate_by_target"],
    "The bars show the fraction of rows for each target rebar that clear the strict cutoff. This separates target-specific confidence behavior from overall archive size.",
)}

{figure_block(
    "Margin distribution by target",
    overview_paths["margin_distribution_by_target"],
    "The boxes summarize base-margin spread for each target rebar. A target with many values close to the dashed cutoff is sensitive to acquisition settings or scoring-rule changes.",
)}

{figure_block(
    "Phase coverage",
    overview_paths["phase_coverage"],
    "This horizontal bar chart shows how many parseable coordinate-optimizer runs came from each experiment phase, so later conclusions can be tied back to run coverage.",
)}

{figure_block(
    "Detected series counts",
    overview_paths["detected_series_counts"],
    "The bars count automatically detected multi-run series by intervention family: source density, Tx/Rx offset, and ringdown parameter.",
)}

{figure_block(
    "Seed branch grid",
    seed_branch_path,
    "Each cell shows the best base margin and run ID for a seed-target branch in the later ringdown050 replication block. It is a compact map of which branches remained close to the cutoff.",
)}
"""
    cells.append(nbf.v4.new_markdown_cell(overview_md))

    phase_rows = (
        run_df.groupby("phase")
        .agg(
            run_count=("run_id", "count"),
            first_run=("run_id", "min"),
            last_run=("run_id", "max"),
            accepted_rate=("base_margin", lambda s: float((s >= CUTOFF).mean())),
            median_margin=("base_margin", "median"),
        )
        .reset_index()
        .sort_values("first_run")
        .to_dict("records")
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            "## Phase Table\n\n"
            + md_table(
                phase_rows,
                [
                    ("phase", "Phase"),
                    ("first_run", "First run"),
                    ("last_run", "Last run"),
                    ("run_count", "Runs"),
                    ("accepted_rate", "Accepted fraction"),
                    ("median_margin", "Median margin"),
                ],
            )
        )
    )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Main Conclusions From The Grouped Experiments

1. Exact geometry recovery is robust in this archive. The harder problem is
   radius-confidence separation against the next candidate radius.
2. Target0 weak rows are often acquisition-sensitive. The Tx/Rx offset bracket
   repeatedly improves confidence, especially when moving from 60 mm toward
   52.5, 50, or 45 mm.
3. Target2 weak rows are often source-density-sensitive. The 5/7/9 source
   ladder repeatedly converts exact-but-weak rows into accepted rows.
4. Target1 weak rows are mixed. Some seeds are rescued cleanly by 9 sources,
   while seed5527939710754757 worsens at 11 sources. That is a policy signal:
   do not keep increasing source density blindly.
"""
        )
    )

    outcome_rows = (
        policy_df.groupby(["series_type", "outcome_category"])["series_id"]
        .count()
        .unstack(fill_value=0)
        .reset_index()
        .to_dict("records")
    )
    policy_rows = (
        policy_df.sort_values(["series_type", "best_minus_worst_margin"], ascending=[True, False])
        .head(18)
        .to_dict("records")
    )
    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Policy Synthesis Increment

This section compresses the `{len(series_df)}` detected multi-run series into
intervention evidence. An intervention means a controlled rerun that changes
one acquisition or modeling setting while keeping the synthetic rebar geometry
fixed.

The key caution is that these are not independent laboratory measurements:
several rows share the same seed, target, and run family. The plots are still
useful because they show which intervention types repeatedly changed the
radius-confidence margin enough to matter.

{figure_block(
    "Intervention outcome counts",
    policy_paths["intervention_outcome_counts"],
    "Stacked bars count whether each detected intervention series was always accepted, always weak, or mixed with at least one accepted setting. This summarizes which intervention families most often produced usable confidence.",
)}

{figure_block(
    "Intervention margin spread",
    policy_paths["intervention_margin_spread"],
    "Each distribution shows the within-series gap between the best and worst tested setting. Larger spreads mean the intervention can materially change the radius-confidence decision.",
)}

Outcome counts by intervention family:

"""
            + md_table(
                outcome_rows,
                [
                    ("series_type", "Series type"),
                    ("all accepted", "All accepted"),
                    ("mixed: accepted setting exists", "Mixed with accepted setting"),
                    ("all weak", "All weak"),
                ],
            )
            + f"""

Largest within-series margin movements:

"""
            + md_table(
                policy_rows,
                [
                    ("series_type", "Type"),
                    ("run_ids", "Runs"),
                    ("seed", "Seed"),
                    ("target", "Target"),
                    ("varied_col", "Varied"),
                    ("best_run", "Best run"),
                    ("best_setting", "Best setting"),
                    ("best_margin", "Best margin"),
                    ("worst_run", "Worst run"),
                    ("worst_setting", "Worst setting"),
                    ("worst_margin", "Worst margin"),
                    ("best_minus_worst_margin", "Spread"),
                    ("outcome_category", "Outcome"),
                ],
            )
        )
    )

    source_rows = source_summary_df.to_dict("records")
    txrx_rows = txrx_summary_df[txrx_summary_df["run_count"] >= 2].to_dict("records")
    cells.append(
        nbf.v4.new_markdown_cell(
            f"""## Source Count And Tx/Rx Evidence

Source count is the number of transmitter source positions used for the
synthetic survey. Tx/Rx offset is the transmitter-to-receiver spacing in
millimeters. The median plots below are aggregate summaries, so individual
seed-level examples should still be checked before choosing a new marathon
branch.

{figure_block(
    "Source-count policy evidence",
    policy_paths["source_count_by_target_policy"],
    "The top panel shows median base margin versus number of source positions for each target; the lower panel shows the percentage clearing the cutoff. This distinguishes source-count settings that improve confidence from settings that add cost without reliable benefit.",
)}

Source-count summary:

"""
            + md_table(
                source_rows,
                [
                    ("target", "Target"),
                    ("sources", "Sources"),
                    ("run_count", "Runs"),
                    ("accepted_fraction", "Accepted fraction"),
                    ("median_margin", "Median margin"),
                    ("first_run", "First run"),
                    ("last_run", "Last run"),
                ],
            )
            + f"""

{figure_block(
    "Tx/Rx policy evidence",
    policy_paths["txrx_offset_by_target_policy"],
    "Each panel shows individual run margins and median margins by transmitter/receiver spacing for one target. Offsets whose medians move above the dashed cutoff are acquisition settings worth reusing.",
)}

Tx/Rx summary for offsets with at least two runs:

"""
            + md_table(
                txrx_rows,
                [
                    ("target", "Target"),
                    ("tx_rx_offset_mm", "Tx/Rx mm"),
                    ("run_count", "Runs"),
                    ("accepted_fraction", "Accepted fraction"),
                    ("median_margin", "Median margin"),
                    ("first_run", "First run"),
                    ("last_run", "Last run"),
                ],
            )
        )
    )

    if "target1_source_density_rescue_map" in policy_paths:
        target1_rows = target1_source_policy_df.to_dict("records")
        cells.append(
            nbf.v4.new_markdown_cell(
                f"""## Target1 Source-Density Stop Point

Target1 is the center rebar. Its source-density branches are important because
they include both clean rescues and unresolved exact-geometry runs. The figure
draws a line from the worst to best margin within each target1 source-density
series; the vertical dashed line is the strict 5.0e-4 cutoff.

{figure_block(
    "Target1 source-density rescue map",
    policy_paths["target1_source_density_rescue_map"],
    "Each horizontal line spans the worst-to-best margin within one target1 source-density series. Green or mixed outcomes show branches where a tested source count cleared the cutoff; red unresolved lines show branches where more sources did not solve confidence.",
)}

Target1 source-density series:

"""
                + md_table(
                    target1_rows,
                    [
                        ("run_ids", "Runs"),
                        ("seed", "Seed"),
                        ("n_runs", "Runs in series"),
                        ("n_accepted", "Accepted"),
                        ("best_run", "Best run"),
                        ("best_setting", "Best sources"),
                        ("best_margin", "Best margin"),
                        ("worst_run", "Worst run"),
                        ("worst_setting", "Worst sources"),
                        ("worst_margin", "Worst margin"),
                        ("outcome_category", "Outcome"),
                    ],
                )
            )
        )

    cells.append(nbf.v4.new_markdown_cell("## Curated Series Deep Dives"))
    for spec in curated_specs:
        subset = run_df[run_df["run_id"].isin(spec.run_ids)].sort_values("run_id")
        rows = subset[
            [
                "run_id",
                "target",
                "sources",
                "tx_rx_offset_mm",
                "ringdown_label",
                "base_margin",
                "confidence_label",
                "fallback_warning",
                "exact_geometry",
            ]
        ].to_dict("records")
        cells.append(
            nbf.v4.new_markdown_cell(
                f"""### {spec.title}

Runs: `{values_text(spec.run_ids)}`.

{spec.conclusion}

{figure_block(
    spec.title,
    curated_paths[spec.series_id],
    f"The upper panel compares base margins across runs {values_text(spec.run_ids)}; the dashed line is the strict cutoff. The lower heatmap shows radius margins under several scoring-rule variants, also called objective variants. If several rows in the heatmap are strong, the conclusion is supported by more than the default base scoring rule. {spec.conclusion}",
)}

"""
                + md_table(
                    rows,
                    [
                        ("run_id", "Run"),
                        ("target", "Target"),
                        ("sources", "Sources"),
                        ("tx_rx_offset_mm", "Tx/Rx mm"),
                        ("ringdown_label", "Ringdown"),
                        ("base_margin", "Base margin"),
                        ("confidence_label", "Label"),
                        ("fallback_warning", "Fallback"),
                        ("exact_geometry", "Exact geometry"),
                    ],
                )
            )
        )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Automatically Detected Series Index

The table below is the systematic index of multi-run series detected from
output experiment IDs 700-1218. Each row has a corresponding plot in the
appendix and a CSV row in `series_summary_700_1218.csv`.
"""
            + "\n\n"
            + md_table(
                series_df.sort_values(["series_type", "best_run"]).to_dict("records"),
                [
                    ("series_type", "Type"),
                    ("run_ids", "Runs"),
                    ("seed", "Seed"),
                    ("target", "Target"),
                    ("varied_col", "Varied"),
                    ("varied_values", "Values"),
                    ("best_run", "Best run"),
                    ("best_margin", "Best margin"),
                    ("conclusion", "Conclusion"),
                ],
                max_rows=80,
            )
        )
    )

    cells.append(nbf.v4.new_markdown_cell("## Appendix: All Detected Series Plots"))
    for spec in appendix_specs:
        cells.append(
            nbf.v4.new_markdown_cell(
                f"""### {spec.series_type}: runs {values_text(spec.run_ids)}

{spec.conclusion}

{figure_block(
    spec.title,
    appendix_paths[spec.series_id],
    f"This automatically generated series plot compares the varied setting against base margin for runs {values_text(spec.run_ids)}. The dashed cutoff shows which tested settings reach moderate radius confidence. {spec.conclusion}",
)}
"""
            )
        )

    cells.append(
        nbf.v4.new_markdown_cell(
            """## Recommended Next Increment

The next report increment should add a target1-specific synthesis before any
new GPU marathon:

1. Compare all target1 weak/rescue branches after output experiment 900.
2. Separate source-density rescue successes from unresolved cases.
3. Decide whether unresolved exact-geometry target1 rows should use Tx/Rx
   acquisition probes, a revised confidence threshold, or a broader source/noise
   model before more Fibonacci seed replication.

This notebook deliberately stops at the seed5527939710754757 branch because
that branch produced a negative 11-source escalation and needs interpretation,
not more blind queueing.
"""
        )
    )

    nb["cells"] = cells
    nb["metadata"] = {
        "kernelspec": {
            "display_name": "Python 3 (FNO)",
            "language": "python",
            "name": "python3",
        },
        "language_info": {"name": "python", "pygments_lexer": "ipython3"},
    }
    NOTEBOOK_PATH.write_text(nbf.writes(nb))


def main() -> None:
    ensure_dirs()
    run_df, diag_df, top_df = discover_coordinate_runs()
    if run_df.empty:
        raise RuntimeError("No coordinate optimizer runs found in requested range")

    detected_specs = detect_series(run_df)
    curated_specs = curated_series(run_df)
    all_specs = detected_specs

    series_rows = [make_series_summary(spec, run_df) for spec in all_specs]
    series_df = pd.DataFrame(series_rows).sort_values(["series_type", "best_run"])
    policy_df = summarize_intervention_series(all_specs, run_df)
    source_summary_df = make_source_count_summary(run_df)
    txrx_summary_df = make_txrx_summary(run_df)
    target1_source_policy_df = policy_df[
        (policy_df["series_type"] == "source_density") & (policy_df["target"] == 1)
    ].copy()

    run_df.to_csv(DATA_DIR / "coordinate_run_summary_700_1218.csv", index=False)
    diag_df.to_csv(DATA_DIR / "objective_variant_summary_700_1218.csv", index=False)
    top_df.to_csv(DATA_DIR / "rank1_candidate_summary_700_1218.csv", index=False)
    series_df.to_csv(DATA_DIR / "series_summary_700_1218.csv", index=False)
    policy_df.to_csv(DATA_DIR / "intervention_series_policy_700_1218.csv", index=False)
    source_summary_df.to_csv(DATA_DIR / "source_count_target_policy_700_1218.csv", index=False)
    txrx_summary_df.to_csv(DATA_DIR / "txrx_target_policy_700_1218.csv", index=False)
    target1_source_policy_df.to_csv(DATA_DIR / "target1_source_density_policy_700_1218.csv", index=False)

    overview_paths = save_overview_plots(run_df, series_df)
    seed_branch_path = make_seed_branch_plot(run_df)
    policy_paths = save_policy_plots(
        run_df,
        policy_df,
        source_summary_df,
        txrx_summary_df,
        target1_source_policy_df,
    )

    curated_paths = {
        spec.series_id: plot_series(spec, run_df, diag_df, FIG_DIR, detailed=True)
        for spec in curated_specs
    }
    appendix_paths = {
        spec.series_id: plot_series(spec, run_df, diag_df, SERIES_FIG_DIR, detailed=False)
        for spec in all_specs
    }

    validation_df = validate_figures(
        list(overview_paths.values())
        + list(policy_paths.values())
        + [seed_branch_path]
        + list(curated_paths.values())
        + list(appendix_paths.values())
    )
    validation_df.to_csv(DATA_DIR / "figure_validation_700_1218.csv", index=False)

    write_notebook(
        run_df=run_df,
        series_df=series_df,
        policy_df=policy_df,
        source_summary_df=source_summary_df,
        txrx_summary_df=txrx_summary_df,
        target1_source_policy_df=target1_source_policy_df,
        overview_paths=overview_paths,
        policy_paths=policy_paths,
        curated_specs=curated_specs,
        curated_paths=curated_paths,
        appendix_specs=all_specs,
        appendix_paths=appendix_paths,
        seed_branch_path=seed_branch_path,
    )

    print(f"Wrote notebook: {NOTEBOOK_PATH}")
    print(f"Wrote run summary: {DATA_DIR / 'coordinate_run_summary_700_1218.csv'}")
    print(f"Wrote series summary: {DATA_DIR / 'series_summary_700_1218.csv'}")
    print(f"Wrote policy summary: {DATA_DIR / 'intervention_series_policy_700_1218.csv'}")
    print(f"Wrote figures: {FIG_DIR}")
    print(f"Parseable coordinate runs: {len(run_df)}")
    print(f"Detected series: {len(series_df)}")
    print(f"Validated figures: {len(validation_df)}")


if __name__ == "__main__":
    main()
