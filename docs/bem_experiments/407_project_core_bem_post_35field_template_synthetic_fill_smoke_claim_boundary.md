# BEM Experiment 407: Post-Synthetic-Fill-Smoke Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded synthetic consumer-smoke result from runs `404-406` into the
current BEM claim boundary.

This run does not stage real returned FDTD files, run a real BEM/FDTD
comparison, calibrate thresholds, transfer to field evidence, launch GPU work,
or make a 3D validation claim.

## Output

```text
outputs/bem_experiments/407_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary_summary.json
figures/project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary.png
```

## Result

```text
claims:                              20
guarded claims:                      17
blocked claims:                      3
synthetic smoke sensitivity ready:   true
synthetic packet preflight ready:    true
synthetic packet is evidence:        false
frequency rows filled:               558
frequency component cells filled:    3348
metadata fields:                     35
preflight checks:                    25
blank component cells after fill:    0
blank metadata values after fill:    0
real external FDTD data ready:       false
real BEM/FDTD comparison ready:      false
3D validation claim ready:           false
GPU/HPC ready:                       false
```

## Interpretation

The claim boundary now includes the consumer-smoke result: the 35-field return
templates are fillable and preflight-compatible when copied into an isolated
synthetic packet.

The claim is still not a real-data claim. The synthetic packet remains
non-evidence, and real comparison remains blocked until real returned FDTD
files replace it.

## Decision

Use run `407` as the post-synthetic-fill-smoke BEM claim boundary. Validate and
sensitivity-harden it before treating the boundary as closed.

## Validation

Focused test:

```text
tests/test_project_core_bem_post_35field_template_synthetic_fill_smoke_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x916, dynamic range=255
```
