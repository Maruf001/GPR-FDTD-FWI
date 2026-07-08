# BEM Experiment 439: Post Threshold-Ladder Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `438` validator with controlled damaged variants of the
run `437` claim boundary.

## Output

```text
outputs/bem_experiments/439_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validation_sensitivity_scenario_rows.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         27
expected pass scenarios:           1
expected failure scenarios:        26
observed pass scenarios:           1
observed failure scenarios:        26
unexpected outcomes:               0
threshold-boundary sensitivity ready:true
validator accepts exact run 437:   true
validator rejects damaged variants:true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The validator accepts the exact run `437` boundary and rejects controlled
damage to claim counts, threshold-claim support, threshold metrics, blocked
rows, downstream promotions, figure validation, and script snapshots.

## Decision

Use runs `437-439` as the current guarded BEM post-threshold-ladder
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
