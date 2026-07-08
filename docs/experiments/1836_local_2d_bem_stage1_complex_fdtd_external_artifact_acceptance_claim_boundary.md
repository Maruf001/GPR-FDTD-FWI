# Experiment 1836: BEM Stage-1 Complex FDTD External Artifact Acceptance Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the external artifact acceptance watchlist from
runs `1833-1835`.

This run does not write live approval files, write returned FDTD files, run
FDTD, compare BEM/FDTD, transfer to field, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1836_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary
```

Key artifacts:

```text
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_claim_rows.csv
data/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary_summary.json
figures/local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source watchlist ready:                true
source validation ready:               true
source sensitivity ready:              true
claims:                                8
guarded claims:                        3
blocked claims:                        5
required live files:                   2
present live files:                    0
accepted artifacts:                    0
FDTD producer authorized now:          false
FDTD executed now:                     false
real BEM/FDTD comparison ready:        false
field transfer ready:                  false
3D/HPC ready:                          false
gpu priority:                          none
```

## Interpretation

The watchlist, validator, and sensitivity result are guarded. The execution and
comparison claims remain blocked because the live approval JSON and the BEM
stage-1 partial-return CSV are still absent.

## Decision

Use run `1836` as the current claim boundary for the 2D-side external artifact
acceptance path. Keep FDTD execution, real BEM/FDTD comparison, field transfer,
and 3D/HPC blocked until the live artifacts pass acceptance.

## Validation

Focused tests:

```text
tests/test_local_2d_bem_stage1_complex_fdtd_external_artifact_acceptance_claim_boundary.py
3 passed
```

Figure check:

```text
2645x838, dynamic range=255
```
