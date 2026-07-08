# BEM Experiment 781: Complex Metric Preflight Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the guarded BEM/FDTD complex-metric preflight
block from runs `778-780`.

This run separates what is now guarded from what remains blocked. The schema,
staging plan, preflight gate, validator, and sensitivity checks are guarded.
The real BEM/FDTD comparison remains blocked because no real producer CSV file
has passed preflight.

## Output

```text
outputs/bem_experiments/781_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_claim_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight gate ready:      true
source validation ready:          true
source sensitivity ready:         true
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight files:                  5
required metric rows:             279
required columns:                 13
producer files present:           0
preflight-passed files:           0
ready-to-stage files:             0
executed commands:                0
sensitivity scenarios:            15
unexpected sensitivity outcomes:  0
real BEM/FDTD comparison ready:   false
field FWI ready:                  false
3D/HPC ready:                     false
gpu priority:                     none
```

## Interpretation

The BEM/FDTD complex-metric return path is guarded as a contract and preflight
mechanism. It is not real agreement evidence yet. The current packet has zero
real producer CSV files and zero preflight-passed files.

## Decision

Use run `781` to prevent the pre-return gate mechanics from being cited as real
BEM/FDTD agreement, detector evidence, field transfer, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validator.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_gate_validation_sensitivity.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_real_return_preflight_claim_boundary.py

12 passed
```

Figure check:

```text
3401x938, dynamic range=255
```
