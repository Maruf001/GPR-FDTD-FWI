# BEM Experiment 269: Half-Space Finite-Rebar Threshold Calibration Protocol Validator

Date: 2026-06-28

## Purpose

Validate the run `268` threshold-calibration protocol from a consumer
perspective.

Run `268` separated pre-data structural gates from real-data agreement
thresholds. This run checks that the protocol item set, metric rollup, synthetic
negative-control exclusion, and downstream no-go states are internally
consistent.

It does not ingest real FDTD traces, calibrate thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/269_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_PROTOCOL_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator.py
```

## Result

```text
validation checks:                  5
validation passes:                  5
blocking failures:                  0
validation ready:                   true
source protocol items:              10
source metric rows:                 6
threshold calibration ready:        false
synthetic negative control usable:  false
real trace files present:           false
real FDTD extraction ready:         false
real BEM/FDTD comparison ready:     false
field FWI ready:                    false
```

The validator checks:

| Check | Result |
| --- | --- |
| Protocol summary counts are consistent | pass |
| Protocol items and statuses match contract | pass |
| Synthetic negative control is excluded from thresholds | pass |
| Metric rollup preserves threshold boundary | pass |
| Real comparison and downstream states blocked | pass |

## Interpretation

The threshold-calibration protocol is internally consistent. Structural gates
remain separate from agreement thresholds, the synthetic negative control is
not allowed to become a threshold source, and real comparison plus downstream
states remain blocked.

## Decision

Use run `269` as the positive validator for the threshold-calibration protocol.
Sensitivity remains required before treating the protocol as fully guarded.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_validator.png
2573x840, dynamic range=255
```
