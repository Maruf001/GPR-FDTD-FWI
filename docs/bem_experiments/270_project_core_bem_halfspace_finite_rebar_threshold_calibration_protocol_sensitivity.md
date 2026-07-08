# BEM Experiment 270: Half-Space Finite-Rebar Threshold Calibration Protocol Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `269` threshold-calibration protocol validator.

Run `269` validated the run `268` protocol under the exact expected state. This
run checks whether the validator fails closed when counts, statuses, metric
boundaries, synthetic negative-control exclusion, threshold readiness, or
downstream readiness flags are damaged.

It does not ingest real FDTD traces, calibrate thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/270_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_PROTOCOL_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity.py
```

## Result

```text
scenarios:                         31
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:        30
observed failure scenarios:        30
unexpected outcomes:                0
sensitivity ready:                  true
threshold calibration ready:        false
synthetic negative control usable:  false
real trace files present:           false
real FDTD extraction ready:         false
real BEM/FDTD comparison ready:     false
field FWI ready:                    false
```

The exact run `268` protocol passes. Thirty damaged variants fail as expected,
including protocol-count drift, metric-count drift, status-count drift, missing
rows, item-name drift, premature threshold readiness, synthetic
negative-control promotion, metric boundary drift, and false real/downstream
readiness.

## Interpretation

The threshold-calibration protocol is now guarded from the current consumer
side. It protects against two important failure modes:

1. Treating structural comparison mechanics as numerical agreement.
2. Treating the synthetic negative-control mismatch as a source of real
   agreement thresholds.

## Decision

Use runs `268-270` as the guarded threshold-calibration protocol. Real traces
and the first real paired BEM/FDTD return remain required before numerical
agreement thresholds can be set.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity.py
6 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_sensitivity.png
3581x886, dynamic range=255
```
