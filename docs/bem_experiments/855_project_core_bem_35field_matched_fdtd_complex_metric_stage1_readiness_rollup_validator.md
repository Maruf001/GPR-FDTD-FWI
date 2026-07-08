# BEM Experiment 855: Stage-1 Readiness Rollup Validator

Date: 2026-07-01

## Purpose

Validate the saved run `854` stage-1 readiness rollup from artifacts.

The validator checks summary readiness, rollup row shape, target identity,
fail-closed execution/downstream state, figure metadata, and frozen script
snapshots.

## Output

```text
outputs/bem_experiments/855_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup_validator
```

## Result

```text
validation checks:               6
checks passed:                   6
checks failed:                   0
source runs:                    16
source runs ready:              16
rollup blocks:                   6
ready blocks:                    6
clean blocked-state blocks:      6
receiver index:                 15
frequency:            1000000000 Hz
live approval file present:  false
accepted live approvals:         0
stage-1 partial file present: false
FDTD producer authorized:     false
FDTD executed now:            false
real BEM/FDTD comparison:     false
field transfer ready:         false
ready for 3D/HPC:             false
gpu priority:                 none
```

## Interpretation

The saved run `854` rollup validates as internally ready but fail-closed. It is
safe to use as the current stage-1 readiness statement, but it does not
authorize producer execution.

## Decision

Use run `854` as the current stage-1 readiness rollup. Keep execution blocked
until live approval is supplied and accepted by the six-gate 2D approval check.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup.py
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_readiness_rollup_validator.py
4 passed
```

Figure check:

```text
2861x838, dynamic range=255
```
