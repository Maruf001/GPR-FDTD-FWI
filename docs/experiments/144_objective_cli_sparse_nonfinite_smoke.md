# Experiment 144: Objective CLI Sparse/Non-Finite Smoke

## Purpose

Exercise the hardened objective diagnostic CLI end-to-end on sparse diagnostic
geometry and non-finite optional margin values.

## 611: Objective CLI Sparse/Non-Finite Smoke

Output:

```text
outputs/experiments/611_objective_cli_sparse_nonfinite_smoke
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python run_coordinate_objective_diagnostic_report.py outputs/experiments/611_objective_cli_sparse_nonfinite_smoke/data/sparse_objective_input.json --outdir outputs/experiments/611_objective_cli_sparse_nonfinite_smoke
```

Artifacts:

```text
README.md
data/sparse_objective_input.json
data/coordinate_objective_diagnostic_ratios.csv
data/coordinate_objective_confidence_rows.csv
data/coordinate_objective_diagnostic_report.json
data/objective_cli_sparse_nonfinite_smoke_validation.json
figures/coordinate_objective_diagnostic_ratios.png
figures/FIGURE_NOTES.md
run_manifest.json
```

Validation:

```text
CLI exit code: 0
generated run_manifest.json parses as JSON
generated coordinate_objective_diagnostic_report.json parses as JSON
report non-finite numeric count: 0
ratio row variant_best_z_mm: null
ratio row margin_ratio_to_base: null
ratio row geometry_comparison_available: false
PNG dimensions: 2059 x 1005
PNG extrema span 0-255 for RGB channels
git diff --check: clean after run 611
```

## Interpretation

The objective diagnostic CLI now survives sparse geometry and non-finite
optional margin values through CSV, JSON, plot, and figure-note generation.
Unavailable geometry comparison and margin ratio values are represented as
explicit null/missing report values.

## Next Decision

Refresh current validation, commit-summary, and next-action queue pointers
after runs 609-611, or run a current-state audit first if preparing handoff.
