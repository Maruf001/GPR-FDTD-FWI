# BEM Experiment 377: Post Staging Dependency Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded return-packet staging dependency block from runs
`374-376` into the current BEM claim boundary.

This run uses saved artifacts only. It does not run BEM solves, FDTD exports,
real comparison, threshold calibration, GPU work, field transfer, field FWI, or
3D validation.

## Output

```text
outputs/bem_experiments/377_project_core_bem_real_pair_post_staging_dependency_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_claim_rows.csv
data/project_core_bem_real_pair_post_staging_dependency_claim_boundary_summary.json
figures/project_core_bem_real_pair_post_staging_dependency_claim_boundary.png
scripts/
```

## Result

```text
claims:                              14
guarded claims:                      11
blocked claims:                      3
base claims:                         13
base guarded claims:                 10
base blocked claims:                 3
staging sensitivity ready:           true
accepts exact run 374:               true
rejects damaged variants:            true
stages:                              4
dependency edges:                    3
missing packet items:                34
real packet files present:           false
real BEM/FDTD comparison ready:      false
threshold calibration ready:         false
broad BEM replacement ready:         false
field transfer ready:                false
GPU work ready:                      false
3D validation ready:                 false
```

## Interpretation

The BEM claim boundary now includes the guarded four-stage staging dependency
plan. The plan is useful as an execution sequence, but it does not promote the
branch to evidence because the real return packet is still absent.

## Decision

Use run `377` as the current BEM claim boundary after the staging dependency
block. Do not run real comparison or threshold calibration until the real
packet passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_real_pair_post_staging_dependency_claim_boundary.py
3 passed
```

Figure validation:

```text
3581x961, dynamic range=255
```
