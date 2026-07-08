# BEM Experiment 268: Half-Space Finite-Rebar Threshold Calibration Protocol

Date: 2026-06-28

## Purpose

Define the threshold-calibration protocol for the first real matched BEM/FDTD
comparison pair.

Runs `265-267` established the current real-comparison readiness boundary. One
remaining blocker is threshold calibration after a real paired return exists.
This run makes that blocker explicit so later real data cannot be judged by
ad hoc thresholds or by thresholds borrowed from synthetic plumbing.

It does not ingest real FDTD traces, set numerical agreement thresholds, claim
BEM/FDTD agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/268_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_metric_rollup.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_PROTOCOL.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol.py
```

## Result

```text
protocol items:                     10
metric rollup rows:                  6
ready pre-data gates:                3
ready guards:                        2
ready contract records:              1
blocked until first real pair:       3
blocked until time-zero reference:   1
first-real-pair required items:      6
calibrated thresholds:               0
protocol ready:                      true
threshold calibration ready:         false
synthetic negative control usable:   false
real trace files present:            false
real FDTD extraction ready:          false
real BEM/FDTD comparison ready:      false
field FWI ready:                     false
```

The source negative-control mismatch remains:

```text
normalized L2 error:                 1.0000000672667073
maximum scattered relative error:    1.000208702121816
```

That mismatch is useful as a false-promotion guard. It is not a calibration
source for real agreement thresholds.

## Interpretation

The comparison path now separates two kinds of checks:

1. Structural gates that can be checked as soon as paired files exist: receiver
   and frequency key completeness, duplicate/missing key guards, and finite
   complex frequency bins.
2. Agreement thresholds that must wait for a real matched pair and explicit
   time-zero convention: normalized L2 error, maximum relative error,
   scan-peak location tolerance, and phase residual tolerance.

## Decision

Use run `268` to govern the first real BEM/FDTD comparison. Do not set
normalized-L2, maximum-error, peak-location, or phase-residual acceptance
thresholds from synthetic trace-root plumbing.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_protocol.png
3220x853, dynamic range=255
```
