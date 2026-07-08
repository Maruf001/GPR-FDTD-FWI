# Experiment 1835: BEM Stage-1 Complex FDTD External Artifact Acceptance Watchlist Validation Sensitivity

Date: 2026-07-01

## Purpose

Sensitivity-harden the run `1834` validator for the external artifact
acceptance watchlist.

This run checks that the validator accepts only the exact current state: two
required live artifacts are absent, no artifact is accepted, and no FDTD
execution or BEM/FDTD comparison is authorized.

This run does not write live approval files, write returned FDTD files, run
FDTD, compare BEM/FDTD, transfer to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1835_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validation_sensitivity_scenario_rows.csv
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validation_sensitivity_summary.json
figures/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
sensitivity scenarios:               19
expected pass scenarios:             1
expected fail scenarios:             18
observed pass scenarios:             1
observed fail scenarios:             18
unexpected outcomes:                 0
damaged scenarios:                   18
FDTD executed now:                   false
real BEM/FDTD comparison ready:      false
field transfer ready:                false
3D/HPC ready:                        false
gpu priority:                        none
script snapshots:                    2
```

The exact watchlist state passes. All damaged states fail as expected,
including false live-file promotion, false artifact acceptance, damaged parent
or template counts, false live approval, false partial return, false FDTD
authorization/execution, false BEM/FDTD comparison, false field/3D promotion,
figure damage, and missing script snapshots.

## Interpretation

The watchlist validator is fail-closed. It does not allow the 2D BEM/FDTD
bridge to advance from an absent-artifact state into FDTD execution or real
comparison by changing one summary flag, row field, figure field, or snapshot
field.

## Decision

Use runs `1833-1835` as the current 2D-side external artifact acceptance block.
Keep FDTD execution blocked until both live artifacts exist and pass
acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_watchlist_validation_sensitivity.py
3 passed
```

Figure check:

```text
2861x871, dynamic range=255
```
