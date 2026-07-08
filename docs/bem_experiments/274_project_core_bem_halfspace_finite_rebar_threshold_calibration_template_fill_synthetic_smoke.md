# BEM Experiment 274: Half-Space Finite-Rebar Threshold Calibration Template Fill Synthetic Smoke

Date: 2026-06-28

## Purpose

Fill the run `271` threshold-calibration template with deterministic synthetic
values as a mechanics smoke test. The goal is to prove that future filled
threshold rows, metadata rows, hash fields, frequency-grid fields, and shared
calibration-pair IDs can be checked without claiming real threshold
calibration.

This run does not ingest real FDTD traces, set real thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/274_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_thresholds.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_metadata.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_smoke_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_FILL_SYNTHETIC_SMOKE.md
```

## Result

```text
threshold rows:                    4
synthetic threshold values:        4
real calibrated thresholds:        0
metadata rows:                     8
metadata ready rows:               8
synthetic metadata values:         8
real metadata values:              0
synthetic checks passed:           13 / 13
synthetic template-fill ready:     true
synthetic negative control usable: false
threshold calibration ready:       false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
field FWI ready:                   false
```

The 13 checks confirm threshold row count, nonblank finite positive threshold
values, consistent synthetic calibration-pair IDs, synthetic negative-control
exclusion, no real-threshold promotion, metadata row count, nonblank metadata
values, ready metadata rows, matching pair ID, SHA-256-shaped hash fields,
parseable frequency grid, and no real-metadata promotion.

## Interpretation

The threshold-calibration template can be filled and checked mechanically. The
synthetic filled template is a positive control for future intake logic, not a
calibration result.

Real paired BEM/FDTD data remain required before setting numerical thresholds,
claiming BEM/FDTD agreement, validating 3D, promoting inversion-scale
half-space use, transferring to field data, launching GPU/HPC work, or running
field FWI.

## Decision

Use run `274` as a positive-control fill smoke for future real threshold
intake. Real threshold calibration remains blocked until real paired BEM/FDTD
data pass the same filled-template checks.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_smoke.py
5 passed
```

Figure validation:

```text
2753x842, dynamic range=255
```
