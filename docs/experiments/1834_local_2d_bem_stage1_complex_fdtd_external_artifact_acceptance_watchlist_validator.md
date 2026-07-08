# Experiment 1834: BEM Stage-1 Complex FDTD External Artifact Acceptance Watchlist Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1833` external artifact acceptance watchlist from
artifacts.

This validator does not write live files, run FDTD, compare BEM/FDTD, transfer
to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1834_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validator
```

## Result

```text
validation checks:                    6
passed checks:                        6
failed checks:                        0
watchlist artifacts:                  2
present live files:                   0
missing live files:                   2
accepted artifacts:                   0
FDTD producer authorized now:         false
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
3D/HPC ready:                         false
gpu priority:                         none
```

## Interpretation

The saved watchlist validates as two absent live artifacts and no FDTD
authorization.

## Decision

Keep FDTD execution blocked until both live artifacts pass acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validator.py
3 passed
```

Figure check:

```text
2358x835, dynamic range=255
```
