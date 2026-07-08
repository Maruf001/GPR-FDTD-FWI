# Experiment 1838: BEM Stage-1 Complex FDTD External Artifact Acceptance Claim Boundary Validation Sensitivity

Date: 2026-07-01

## Purpose

Sensitivity-harden the run `1837` validator for the external artifact
acceptance claim boundary.

This run checks that the validator accepts only the exact current state: the
watchlist/validator/sensitivity claims are guarded, two live artifacts are
absent, zero artifacts are accepted, and all downstream execution claims remain
blocked.

This run does not write live approval files, write returned FDTD files, run
FDTD, compare BEM/FDTD, transfer to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1838_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:               true
sensitivity scenarios:                19
expected pass scenarios:              1
expected fail scenarios:              18
observed pass scenarios:              1
observed fail scenarios:              18
unexpected outcomes:                  0
damaged scenarios:                    18
damaged scenarios rejected:           18
FDTD executed now:                    false
real BEM/FDTD comparison ready:       false
field transfer ready:                 false
3D/HPC ready:                         false
gpu priority:                         none
script snapshots:                     2
```

The exact claim boundary passes. All damaged states fail as expected, including
claim count drift, guarded/blocked key drift, false live-artifact acceptance,
false FDTD authorization/execution, false BEM/FDTD comparison, false field/3D
promotion, figure damage, and missing script snapshots.

## Interpretation

The claim-boundary validator is fail-closed for the current absent-artifact
state. It does not allow the 2D BEM/FDTD bridge to advance into FDTD execution
or real comparison by changing one saved summary flag, row field, figure field,
or snapshot field.

## Decision

Use runs `1836-1838` as the current guarded external artifact acceptance claim
boundary block. Keep FDTD execution blocked until both live artifacts exist and
pass acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
2933x889, dynamic range=255
```
