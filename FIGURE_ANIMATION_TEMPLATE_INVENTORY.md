# Figure And Animation Template Inventory

Last audited: 2026-06-18

This inventory documents the figure and animation generation scripts for the
GPR-FDTD-FWI experiment archive. It was reconstructed from the local repository
and output folders, with emphasis on later coordinate-optimizer outputs through
experiment `1218`.

No experiment outputs were deleted, moved, or regenerated during this audit.
The original generator scripts remain in their original locations. The folder
`tools/figure_animation_templates/` is a documentation index for migration and
future Codex sessions.

## Overview

The current experiment-native figure system has two layers:

1. Core coordinate-optimizer reporting, generated during
   `run_multi_rebar_coordinate_optimizer.py`.
2. Reusable context/backfill scripts that read
   `data/multi_rebar_coordinate_optimizer_summary.json` and add static figures,
   GIFs, validation summaries, and bounded sections in `figures/FIGURE_NOTES.md`.

The later full visual-context examples are:

- `outputs/experiments/1140_coordinate_optimizer_variable_depth_radius_seed2504730781961_target0_sources9_txrx60_ringdown050_objectives`
- `outputs/experiments/1158_coordinate_optimizer_variable_depth_radius_seed17167680207565_target2_sources9_txrx60_ringdown050_objectives`
- `outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives`

The latest core-reporting examples are:

- `outputs/experiments/1216_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources5_txrx60_ringdown050_objectives`
- `outputs/experiments/1217_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources9_txrx60_ringdown050_objectives`
- `outputs/experiments/1218_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources11_txrx60_ringdown050_objectives`

Important filename caveat: the current true FDTD GIF is named
`fdtd_wavefield_amplitude.gif` in the repository and outputs. No uppercase
`FDTD_wavefield_amplitude.gif` files were found.

## Expected Artifacts

| Artifact | Policy | Current canonical generator | Example output |
| --- | --- | --- | --- |
| `system_scene_geometry.png` | Core for every compatible coordinate experiment | `run_experiment_scene_visualization.py`, also called by `run_multi_rebar_coordinate_optimizer.py` | `outputs/experiments/1218_.../figures/system_scene_geometry.png` |
| `source_pulse_noise_context.png` | Core desired for future experiments, backfill where useful | `run_experiment_pulse_noise_visualization.py` | `outputs/experiments/1160_.../figures/source_pulse_noise_context.png` |
| `coordinate_confidence_margins.png` | Core, preserve legacy compact figure | `run_multi_rebar_coordinate_optimizer.py` | `outputs/experiments/1218_.../figures/coordinate_confidence_margins.png` |
| `coordinate_radius_decision_panel.png` | Core current reporting style | `run_multi_rebar_coordinate_optimizer.py` | `outputs/experiments/1218_.../figures/coordinate_radius_decision_panel.png` |
| `coordinate_objective_radius_candidates.png` | Core current reporting style when objective top-candidate rows exist | `run_multi_rebar_coordinate_optimizer.py` | `outputs/experiments/1218_.../figures/coordinate_objective_radius_candidates.png` |
| `FIGURE_NOTES.md` | Core, preserve and update | `run_multi_rebar_coordinate_optimizer.py` plus context-script upsert helpers | `outputs/experiments/1160_.../figures/FIGURE_NOTES.md` |
| `geometric_wave_propagation.gif` | Optional/selective schematic GIF | `run_experiment_wave_propagation_animation.py` | `outputs/experiments/1160_.../figures/geometric_wave_propagation.gif` |
| `fdtd_wavefield_amplitude.gif` | Optional/selective true FDTD GIF | `run_experiment_fdtd_wavefield_animation.py` | `outputs/experiments/1160_.../figures/fdtd_wavefield_amplitude.gif` |

## Coverage Snapshot

Across numbered experiments `700-1218`, the local audit found 519 run folders.

| Artifact | Count in `700-1218` |
| --- | ---: |
| `system_scene_geometry.png` | 425 |
| `source_pulse_noise_context.png` | 343 |
| `geometric_wave_propagation.gif` | 337 |
| `fdtd_wavefield_amplitude.gif` | 6 |
| `coordinate_confidence_margins.png` | 425 |
| `coordinate_radius_decision_panel.png` | 119 |
| `coordinate_objective_radius_candidates.png` | 119 |
| `FIGURE_NOTES.md` | 480 |

Combined status:

| Status group | Count | Latest run |
| --- | ---: | ---: |
| Core reporting without pulse/noise | 119 | 1218 |
| Core reporting with pulse/noise | 37 | 1160 |
| Full visual context including both GIFs | 3 | 1160 |

Sample comparison:

| Run | Scene | Pulse/noise | Geometric GIF | FDTD GIF | Confidence | Decision panel | Candidate panel | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1140 | yes | yes | yes | yes, lowercase | yes | yes | yes | yes |
| 1158 | yes | yes | yes | yes, lowercase | yes | yes | yes | yes |
| 1160 | yes | yes | yes | yes, lowercase | yes | yes | yes | yes |
| 1216 | yes | missing | missing | missing | yes | yes | yes | yes |
| 1217 | yes | missing | missing | missing | yes | yes | yes | yes |
| 1218 | yes | missing | missing | missing | yes | yes | yes | yes |

Reference dimensions from `1160`:

| Artifact | Size / frames |
| --- | --- |
| `system_scene_geometry.png` | 1769 x 1065 |
| `source_pulse_noise_context.png` | 2484 x 1892 |
| `geometric_wave_propagation.gif` | 977 x 621, 36 frames |
| `fdtd_wavefield_amplitude.gif` | 1000 x 600, 43 frames |
| `coordinate_confidence_margins.png` | 1804 x 665 |
| `coordinate_radius_decision_panel.png` | 2127 x 1583 |
| `coordinate_objective_radius_candidates.png` | 2025 x 1026 |

## Canonical Scripts

### `run_multi_rebar_coordinate_optimizer.py`

Purpose:

- Runs the coordinate/radius optimizer.
- Writes the three coordinate/reporting figures.
- Writes the initial `figures/FIGURE_NOTES.md`.
- Calls `write_scene_artifacts()` from `run_experiment_scene_visualization.py`
  so new compatible optimizer runs also get `system_scene_geometry.png`.

Inputs:

- CLI experiment parameters such as backend, grid step, true/initial geometry,
  target indices, source/receiver layout, source cases, and diagnostic objective
  variants.
- During the run it creates confidence rows, objective diagnostic rows, top
  candidate rows, and state history.

Outputs:

- `figures/coordinate_confidence_margins.png`
- `figures/coordinate_radius_decision_panel.png`
- `figures/coordinate_objective_radius_candidates.png` when top-candidate rows exist
- `figures/system_scene_geometry.png`
- `figures/FIGURE_NOTES.md`
- `data/coordinate_confidence_report.csv`
- `data/coordinate_objective_diagnostics.csv`
- `data/coordinate_objective_top_candidates.csv`
- `data/coordinate_state_history.csv`
- `data/multi_rebar_coordinate_optimizer_summary.json`
- `data/system_scene_geometry_summary.json`

Reusable status:

- Canonical for new coordinate experiments.
- Do not rerun existing experiments just to regenerate figures unless the user
  explicitly asks to rerun the optimizer.
- The plotting functions are importable and tested, but there is no standalone
  regenerate-from-CSV CLI for the coordinate panels.

Real data status:

- Uses real optimizer rows and actual experiment configuration.

Key functions:

- `plot_coordinate_margins`
- `plot_coordinate_radius_decision_panel`
- `plot_coordinate_objective_radius_candidates`
- `write_coordinate_figure_notes`

Tests:

- `tests/test_multi_rebar_coordinate_optimizer.py`

### `run_experiment_scene_visualization.py`

Purpose:

- Generates the physical setup/context figure for an experiment.
- Can run one summary-backed generation, explicit geometry generation, or a
  skip-existing backfill audit over numbered experiment folders.

Inputs:

- Preferred: `data/multi_rebar_coordinate_optimizer_summary.json`.
- Alternative: explicit CLI geometry vectors.
- Requires true x/z/radius geometry and scan-position metadata for safe
  summary-backed backfill.

Outputs:

- `figures/system_scene_geometry.png`
- `data/system_scene_geometry_summary.json`
- `figures/FIGURE_NOTES.md` section bounded by:
  `<!-- system_scene_geometry:start -->` and
  `<!-- system_scene_geometry:end -->`
- Optional audit JSON/CSV in `outputs/visualization_audits/...`.

Reusable status:

- Canonical and reusable as-is.
- Backfill mode skips existing valid artifacts unless `--refresh-existing` is
  provided.

Real data status:

- Summary-backed mode uses actual experiment geometry and acquisition metadata.
- Explicit CLI mode is a template/manual mode; only use it when real values are
  supplied.

Example single-run command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --summary outputs/experiments/1218_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources11_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Example skip-existing audit/backfill:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_scene_visualization.py \
  --backfill-root outputs/experiments \
  --min-run-number 1216 \
  --max-run-number 1218 \
  --audit-json outputs/visualization_audits/YYYYMMDD/scene_geometry_1216_1218.json \
  --audit-csv outputs/visualization_audits/YYYYMMDD/scene_geometry_1216_1218.csv
```

Tests:

- `tests/test_experiment_scene_visualization.py`

### `run_experiment_pulse_noise_visualization.py`

Purpose:

- Generates a source-pulse/noise context PNG from coordinate-optimizer metadata.
- Shows configured Ricker source pulse, source mismatch, delayed ringdown,
  additive Gaussian observed-data noise settings, pulse-plus-noise proxy, seed
  fingerprint, and noise distribution.

Inputs:

- `data/multi_rebar_coordinate_optimizer_summary.json`.
- Optional `--case-label`; defaults to the first `replication_cases` entry.

Outputs:

- `figures/source_pulse_noise_context.png`
- `data/source_pulse_noise_context_summary.json`
- `figures/FIGURE_NOTES.md` section bounded by:
  `<!-- source_pulse_noise_context:start -->` and
  `<!-- source_pulse_noise_context:end -->`
- Optional audit JSON/CSV in `outputs/visualization_audits/...`.

Reusable status:

- Canonical and reusable as-is.
- Backfill mode skips existing valid artifacts unless `--refresh-existing` is
  provided.
- Older outputs may have pre-schema-v2 pulse/noise summaries; do not overwrite
  them unless asked.

Real data status:

- Uses actual source/noise metadata from the experiment summary.
- The plotted noise trace is a deterministic proxy generated from the saved
  Gaussian noise seed and RMS fraction; observed B-scan noise statistics are
  included from summary metadata when available.
- It does not run FDTD or FWI.

Example command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --summary outputs/experiments/1218_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources11_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Example selective backfill:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_pulse_noise_visualization.py \
  --backfill-root outputs/experiments \
  --min-run-number 1216 \
  --max-run-number 1218 \
  --audit-json outputs/visualization_audits/YYYYMMDD/pulse_noise_1216_1218.json \
  --audit-csv outputs/visualization_audits/YYYYMMDD/pulse_noise_1216_1218.csv
```

Tests:

- `tests/test_experiment_context_visualizations.py`

### `run_experiment_wave_propagation_animation.py`

Purpose:

- Generates the schematic/geometric wave-propagation GIF.
- Uses straight-ray concrete travel-time estimates to show outgoing wavefronts,
  rebar reflections, target highlight, and approximate echo arrivals.

Inputs:

- `data/multi_rebar_coordinate_optimizer_summary.json`.
- Requires geometry and scan-position metadata.
- Optional `--frames` and `--fps`.

Outputs:

- `figures/geometric_wave_propagation.gif`
- `data/geometric_wave_propagation_summary.json`
- `figures/FIGURE_NOTES.md` section bounded by:
  `<!-- geometric_wave_propagation:start -->` and
  `<!-- geometric_wave_propagation:end -->`
- Optional audit JSON/CSV in `outputs/visualization_audits/...`.

Reusable status:

- Canonical schematic GIF generator.
- Selective/backfill use is recommended. Do not generate for every experiment
  by default unless explicitly requested.
- Backfill mode skips existing valid artifacts unless `--refresh-existing` is
  provided.

Real data status:

- Uses real experiment geometry and Tx/Rx scan metadata.
- It is a travel-time schematic, not an FDTD wavefield.

Example command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_wave_propagation_animation.py \
  --summary outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --frames 36 \
  --fps 8
```

Tests:

- `tests/test_experiment_context_visualizations.py`

### `run_experiment_fdtd_wavefield_animation.py`

Purpose:

- Generates the true FDTD wavefield-amplitude GIF for one selected experiment.
- Reads the coordinate-optimizer summary, builds the selected model state,
  picks a representative Tx/Rx pair near the target rebar, reconstructs the
  configured source including ringdown, runs one forward FDTD simulation, and
  animates sparse Ez snapshots.

Inputs:

- Required: `--summary data/multi_rebar_coordinate_optimizer_summary.json`.
- Optional: `--case-label`, `--model-state truth|initial|final`, `--backend`,
  `--grid-step-mm`, `--frames`, `--save-every`, `--fps`,
  `--geometry-mode hard|subcell`, `--subcell-samples`, `--max-updates`.

Outputs:

- `figures/fdtd_wavefield_amplitude.gif`
- `data/fdtd_wavefield_amplitude_summary.json`
- `figures/FIGURE_NOTES.md` section bounded by:
  `<!-- fdtd_wavefield_amplitude:start -->` and
  `<!-- fdtd_wavefield_amplitude:end -->`

Reusable status:

- Canonical true FDTD animation generator for current coordinate-optimizer
  outputs.
- Selective use only; there is no broad backfill mode, and it may be expensive.
- Default backend is CPU. Use `--backend gpu-cpml` on the DGX Spark only after
  confirming the GPU environment.

Real data status:

- Uses real summary geometry, scan positions, source/ringdown settings, and a
  forward FDTD simulation.
- Observed-data Gaussian noise is not injected into the wavefield animation;
  that noise is added after forward simulation to B-scans.

Example command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_experiment_fdtd_wavefield_animation.py \
  --summary outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  --backend cpu
```

Selected runs already generated:

- `1004`
- `1006`
- `1007`
- `1140`
- `1158`
- `1160`

Audit files:

- `outputs/visualization_audits/20260611/fdtd_wavefield_amplitude_targets_1004_1006_1007_1140_1158_1160.json`
- `outputs/visualization_audits/20260611/fdtd_wavefield_amplitude_targets_1004_1006_1007_1140_1158_1160.csv`

Tests:

- `tests/test_experiment_fdtd_wavefield_animation.py`
- `tests/test_wavefield_animation.py`

## Supporting And Legacy Scripts

### `run_wavefield_animation.py`

Purpose:

- Manual explicit-geometry FDTD wavefield GIF generator.

Inputs:

- Explicit geometry vectors and source location from the CLI.

Outputs:

- `figures/<label>_wavefield.gif`
- `data/<label>_wavefield_animation_summary.json`

Status:

- Reusable for ad hoc/manual studies.
- Not canonical for current experiment-summary-driven coordinate runs because
  it can use explicit geometry without reading the experiment summary.
- `run_experiment_fdtd_wavefield_animation.py` is the current wrapper for
  summary-grounded true FDTD GIFs.

### `visualization/plot_wavefield.py`

Purpose:

- Shared `animate_wavefield()` helper used by true FDTD animation scripts.

Status:

- Reusable plotting utility, not a standalone experiment template.

### `run_existing_wavefield_animation_backfill.py`

Purpose:

- Discovers, validates, inventories, and annotates already-saved true wavefield
  GIFs.
- Never runs FDTD/FWI.

Outputs:

- `data/existing_true_wavefield_animations_summary.json`
- `figures/FIGURE_NOTES.md` section bounded by:
  `<!-- existing_true_wavefield_animations:start -->` and
  `<!-- existing_true_wavefield_animations:end -->`
- Optional audit JSON/CSV.

Status:

- Useful migration/backfill audit tool.
- Not a generator for new wavefield GIFs.

Example command:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python run_existing_wavefield_animation_backfill.py \
  --backfill-root outputs/experiments \
  --min-run-number 1000 \
  --max-run-number 1160 \
  --audit-json outputs/visualization_audits/YYYYMMDD/existing_wavefields_1000_1160.json \
  --audit-csv outputs/visualization_audits/YYYYMMDD/existing_wavefields_1000_1160.csv
```

### `run_wavefield_comparison_animation.py`

Purpose:

- Generates side-by-side true/candidate/difference FDTD wavefield comparison
  GIFs.

Status:

- Historical/ad hoc diagnostic utility.
- Uses explicit truth/candidate geometry. Not canonical for the current
  expected artifact list.

### `run_residual_backprop_animation.py`

Purpose:

- Generates FWI-style residual back-propagation wavefield GIFs.

Status:

- Historical/ad hoc diagnostic utility.
- Not part of the current core or selective expected artifacts.

### `tool/codex/presentation_visuals.py`

Purpose:

- Generates presentation/context figures and one scan-path animation under
  presentation output folders.

Status:

- Presentation-only. It does not replace experiment-native figures.
- Documented in `tool/codex/README.md`.

### `run_experiment_archive_health_report.py`

Purpose:

- Audits numbered experiment outputs for artifact hygiene, manifests, figure
  notes, and run-type drift.

Status:

- Useful archive audit support.
- Not a generator for the expected per-experiment figure set.

### `run_experiment_700_1218_holistic_report.py`

Purpose:

- Builds the holistic report/notebook for experiments `700-1218` from existing
  outputs.

Status:

- Summary/report generator, not a per-run figure template.

## Figure Notes Format

`figures/FIGURE_NOTES.md` is the expected notes file for experiment-native
figures.

The coordinate optimizer writes top-level Markdown sections for:

- `coordinate_radius_decision_panel.png`
- `coordinate_confidence_margins.png`
- `coordinate_objective_radius_candidates.png`

The context/backfill scripts append or replace bounded sections with HTML
markers:

- `<!-- system_scene_geometry:start -->` to
  `<!-- system_scene_geometry:end -->`
- `<!-- source_pulse_noise_context:start -->` to
  `<!-- source_pulse_noise_context:end -->`
- `<!-- geometric_wave_propagation:start -->` to
  `<!-- geometric_wave_propagation:end -->`
- `<!-- fdtd_wavefield_amplitude:start -->` to
  `<!-- fdtd_wavefield_amplitude:end -->`
- `<!-- existing_true_wavefield_animations:start -->` to
  `<!-- existing_true_wavefield_animations:end -->`

The marker-based sections are idempotent. Re-running a context script should
replace only its own bounded section. Do not hand-delete older note content
during migration.

## 2026-06-18 Figure-Notes Policy Addendum

The original inventory snapshot emphasized coordinate-optimizer outputs through
experiment `1218`. The refreshed archive-health audit in
`outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh`
now covers numbered synthetic outputs through `1325`. It reports that
image-bearing runs without `figures/FIGURE_NOTES.md` are still the dominant
artifact-hygiene issue:

```text
figure_images_missing_figure_notes: 125
missing_run_manifest:               5
```

This does not mean old experiments should be regenerated. The current policy is:

- New image-bearing synthetic output generators should write
  `figures/FIGURE_NOTES.md` and include that path in the run summary/manifest.
- Paper-facing summary/report generators are not exempt just because they do
  not run FDTD/FWI; if they create a figure, they should document the figure's
  source CSVs, scope, and no-new-simulation boundary.
- Existing old outputs should be left intact unless they are selected for a
  manuscript figure, handoff package, or targeted skip-existing backfill.
- Current manuscript-facing endpoints have figure notes or targeted source-note
  coverage:
  `1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation`,
  `1323_synthetic_2d_next_question_matrix_post_claim_boundary_reconciliation`,
  `1325_synthetic_publication_source_figure_notes_backfill_report`,
  field bundle
  `102_gssi51600s_field_publication_claim_bundle_post_timing_window_family`,
  field source-note audit
  `104_gssi51600s_field_publication_source_figure_notes_backfill_post_timing_window_family`,
  `outputs/summary_tables/008_local_2d_field_manuscript_evidence_audit_post_timing_window_family`,
  and
  `outputs/summary_tables/009_local_2d_field_manuscript_table_pack_post_timing_window_family`.

Do not broad-generate optional GIFs or true FDTD animations to fix note hygiene.
For current publication work, fix notes at the generator level or use targeted
skip-existing backfills only.

## Current Best Versions By Artifact

| Artifact | Best current source | Why |
| --- | --- | --- |
| `system_scene_geometry.png` | `run_experiment_scene_visualization.py`, called by optimizer | Uses actual summary geometry, scan positions, target highlight, validation JSON, and note markers. Later style is visible in `1218` and `1160`. |
| `source_pulse_noise_context.png` | `run_experiment_pulse_noise_visualization.py` | Schema-v2 design distinguishes pulse shape, common-scale noise proxy, and seed fingerprint. Later full example: `1160`. |
| `geometric_wave_propagation.gif` | `run_experiment_wave_propagation_animation.py` | Uses real geometry and representative Tx/Rx pair, but remains explicitly schematic and cheap. |
| `fdtd_wavefield_amplitude.gif` | `run_experiment_fdtd_wavefield_animation.py` | Summary-driven true FDTD wrapper with source ringdown, selected Tx/Rx, validation summary, and notes. |
| `coordinate_confidence_margins.png` | `run_multi_rebar_coordinate_optimizer.py` | Legacy compact optimizer margin summary. Keep it. |
| `coordinate_radius_decision_panel.png` | `run_multi_rebar_coordinate_optimizer.py` | Primary current decision panel. |
| `coordinate_objective_radius_candidates.png` | `run_multi_rebar_coordinate_optimizer.py` | Current objective-variant candidate panel. |

## Recommended Future Workflow

For a new coordinate experiment:

1. Run `run_multi_rebar_coordinate_optimizer.py` with the desired experiment
   parameters. This should create the coordinate/reporting figures, scene
   geometry, summaries, manifest, and initial figure notes.
2. Verify these core files exist:
   - `figures/system_scene_geometry.png`
   - `figures/coordinate_confidence_margins.png`
   - `figures/coordinate_radius_decision_panel.png`
   - `figures/coordinate_objective_radius_candidates.png`, when objective
     top-candidate rows exist
   - `figures/FIGURE_NOTES.md`
   - `data/multi_rebar_coordinate_optimizer_summary.json`
   - `data/system_scene_geometry_summary.json`
3. Generate `source_pulse_noise_context.png` from the summary unless the run is
   intentionally excluded.
4. Generate `geometric_wave_propagation.gif` only for selected or
   decision-critical runs.
5. Generate `fdtd_wavefield_amplitude.gif` only for selected runs, after
   confirming compute cost and backend.
6. Preserve older figures. Do not overwrite existing artifacts unless the user
   explicitly requests refresh/regeneration.
7. Read `figures/FIGURE_NOTES.md` and confirm it describes all figures that
   exist in the run folder.
8. Record any generated/backfilled outputs in a tracker under
   `docs/experiments/` and write audit JSON/CSV under
   `outputs/visualization_audits/YYYYMMDD/` when doing batch work.

## Migration Notes For Next DGX Spark

The numbered synthetic output archive is local artifact data, not normal Git
source history. The migration audit at
`docs/migration/2026-06-14_project_audit.md` states that
`outputs/experiments/` is intentionally not tracked by Git and must be migrated
with the local artifact archive.

After migrating to the next DGX Spark machine:

1. Confirm the project source tree and local output archive are both present.
2. Confirm these directories exist:
   - `outputs/experiments/`
   - `outputs/visualization_audits/`
   - `docs/experiments/`
3. Confirm the later reference runs are present:
   - `outputs/experiments/1160_coordinate_optimizer_variable_depth_radius_seed17167680207565_target1_sources9_txrx60_ringdown050_objectives`
   - `outputs/experiments/1218_coordinate_optimizer_variable_depth_radius_seed5527939710754757_target1_sources11_txrx60_ringdown050_objectives`
4. Use the FNO environment or an equivalent environment with NumPy, Matplotlib,
   Pillow, pandas, nbformat, pytest, and GPU/CuPy dependencies when using
   `--backend gpu-cpml`.
5. Run focused tests before regeneration work:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q \
  tests/test_experiment_scene_visualization.py \
  tests/test_experiment_context_visualizations.py \
  tests/test_experiment_fdtd_wavefield_animation.py \
  tests/test_wavefield_animation.py \
  tests/test_multi_rebar_coordinate_optimizer.py
```

6. Use skip-existing backfill modes first. Add `--refresh-existing` only after
   explicit approval.
7. Do not broad-generate true FDTD GIFs. Select run IDs and record why those
   runs were chosen.
8. Validate generated images/GIFs via the scripts' summary JSON and existing
   validators before relying on them.

## Existing Visualization Audits

Useful audit files already present:

- `outputs/visualization_audits/20260610/scene_geometry_backfill_audit_20260610_final.json`
- `outputs/visualization_audits/20260610/pulse_noise_seed_fingerprint_skip_existing_audit_20260610.json`
- `outputs/visualization_audits/20260610/geometric_wave_backfill_audit_20260610.json`
- `outputs/visualization_audits/20260610/existing_true_wavefield_backfill_audit_20260610.json`
- `outputs/visualization_audits/20260611/fdtd_wavefield_amplitude_targets_1004_1006_1007_1140_1158_1160.json`

Their recorded counts include:

- scene backfill final: `refreshed=488`, `skipped=632`
- pulse/noise skip-existing audit: `skipped=1133`
- geometric wave backfill: `generated=493`, `skipped=632`
- existing true wavefield inventory: `generated=18`, `skipped=1109`
- FDTD amplitude selected targets: `generated=6`
