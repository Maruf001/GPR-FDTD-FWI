# BEM Experiment 767: Complex Metric Consumer Positive Control Validator

Date: 2026-07-01

## Purpose

Validate the saved run `766` complex metric consumer positive-control artifacts.

This run does not use real FDTD exports, does not accept synthetic files as real
addendum returns, and does not promote real BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/767_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source positive control ready:        true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
synthetic addendum files:             5
computed metric rows:                 279
real FDTD exported true rows:         0
synthetic positive-control rows:      279
uses real BEM/FDTD values:            false
real BEM/FDTD comparison ready:       false
gpu priority:                         none
```

Validation checks:

| Check | Result |
| --- | --- |
| source positive control ready | pass |
| five files and 279 metric rows represented | pass |
| stage row shape is preserved | pass |
| synthetic files preserve schema shape without real export | pass |
| metric values are positive and finite | pass |
| real comparison remains blocked | pass |
| figure and script snapshots are present | pass |

## Interpretation

The saved run `766` artifacts are internally consistent. The positive-control
consumer covers the full five-stage, 279-row complex metric shape and computes
finite nonzero amplitude, phase, and complex errors.

The validator also confirms the guardrail: these values remain synthetic-only.
No real FDTD-exported row is present, and real BEM/FDTD comparison remains
blocked.

## Decision

Use run `767` as the saved-artifact validator for the run `766` consumer
positive control.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py
7 passed
```

Python compile check:

```text
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
run_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control.py: pass
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_consumer_positive_control_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
