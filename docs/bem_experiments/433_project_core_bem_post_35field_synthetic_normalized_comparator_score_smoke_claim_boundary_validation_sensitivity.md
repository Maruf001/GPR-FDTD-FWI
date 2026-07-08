# BEM Experiment 433: Post 35-Field Synthetic Normalized Comparator Score Smoke Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `432` validator with controlled damaged variants of the
run `431` post-score-smoke claim boundary.

## Output

```text
outputs/bem_experiments/433_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         21
expected pass scenarios:           1
expected failure scenarios:        20
observed pass scenarios:           1
observed failure scenarios:        20
unexpected outcomes:               0
boundary sensitivity ready:        true
validator accepts exact run 431:   true
validator rejects damaged variants:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `431` boundary and rejects controlled
damage to claim counts, score readiness, score metrics, evidence text, blocked
rows, downstream state, figure validation, and script snapshots.

## Decision

Use runs `431-433` as the guarded BEM post-score-smoke claim-boundary block.
Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work, field transfer, and
field FWI blocked until real returned files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_score_smoke_claim_boundary_validation_sensitivity.py
3 passed as part of the 23-test focused set
```

Figure check:

```text
3581x889, dynamic range=255
```
