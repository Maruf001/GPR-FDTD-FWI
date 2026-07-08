# BEM Experiment 728: Producer Input Strict-Mode Live-Route Rescan Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `727` strict-mode live-route rescan validator.

The sensitivity audit checks that the validator accepts the exact empty-live
route state and rejects false live-file presence, false row counts, false
strict acceptance, completed-action promotion, and false exporter/GPU
readiness.

This is CPU-only validator sensitivity auditing. It does not run FDTD, execute
the exporter on live files, create real evidence, run a real BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation claims.

## Output

```text
outputs/bem_experiments/728_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validation_sensitivity_case_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                   15
expected pass cases:                  1
expected fail cases:                 14
actual pass cases:                    1
actual fail cases:                   14
unexpected outcomes:                  0
damaged cases:                       14
exporter execution ready:         false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                    false
```

## Interpretation

The validator accepts only the exact empty-live-route strict-mode state. It
rejects false file presence, false strict acceptance, and false downstream
promotion.

## Decision

Keep exporter execution and BEM/FDTD comparison blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validation_sensitivity.py
2 passed
```

Figure check:

```text
2645x859, dynamic range=255
```
