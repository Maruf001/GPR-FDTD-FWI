# BEM Experiment 275: Half-Space Finite-Rebar Threshold Calibration Template Fill Synthetic Validator

Date: 2026-06-28

## Purpose

Validate the run `274` synthetic template-fill smoke from saved artifacts. The
goal is to confirm that a downstream consumer can read the filled threshold
rows, metadata rows, synthetic check rows, and summary while preserving the
synthetic-vs-real threshold boundary.

This run does not ingest real FDTD traces, set real thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/275_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_TEMPLATE_FILL_SYNTHETIC_VALIDATOR.md
```

## Result

```text
validation checks:                 5
validation checks passed:          5
blocking failures:                 0
synthetic fill validation ready:   true
synthetic fill smoke ready:        true
threshold calibration ready:       false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The five validation checks confirm:

| Check | Result |
| --- | --- |
| Threshold rows are filled synthetic, not real | pass |
| Metadata rows are filled synthetic, not real | pass |
| Synthetic checks all pass | pass |
| Summary counts are consistent | pass |
| Real comparison and downstream states are blocked | pass |

## Interpretation

The saved synthetic template-fill smoke is internally consistent. It is useful
as a positive control for future real threshold intake, but it is not a real
calibration result.

Real paired BEM/FDTD data remain required before threshold calibration,
BEM/FDTD agreement, 3D validation, inversion-scale use, field transfer, GPU/HPC
work, or field FWI can be claimed.

## Decision

Use runs `274`-`275` as the consumer-validated positive-control threshold-fill
smoke. Sensitivity remains required before treating it as fully guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_template_fill_synthetic_validator.py
5 passed
```

Figure validation:

```text
2717x821, dynamic range=255
```
