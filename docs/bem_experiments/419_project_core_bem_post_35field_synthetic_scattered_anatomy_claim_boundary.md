# BEM Experiment 419: Post 35-Field Synthetic Scattered Anatomy Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic scattered-anatomy block from runs `416-418` into the
BEM claim boundary.

This is a claim-boundary refresh. It does not run a real BEM/FDTD comparison,
create measured evidence, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/419_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary
```

## Result

```text
claim boundary ready:              true
claims:                            22
guarded claims:                    19
blocked claims:                    3
dominant component:                ez
peak receiver index:               30
peak frequency:                    3.0 GHz
real BEM/FDTD comparison ready:    false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The new guarded claim says the synthetic scattered table has structured
consumer anatomy: 31 receivers, nine frequencies, dominant `ez` component,
peak receiver `30`, peak frequency `3 GHz`, and peak scattered norm
`1.7743269146355192`.

## Decision

Use this as the current BEM claim boundary after the synthetic
scattered-anatomy block. Keep real comparison, 3D validation, GPU/HPC, field
transfer, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_scattered_anatomy_claim_boundary.py
4 passed
```

Figure check:

```text
3941x909, dynamic range=255
```
