# BEM Experiment 437: Post Threshold-Ladder Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `434-436` threshold-ladder result into the current BEM
claim boundary.

## Output

```text
outputs/bem_experiments/437_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_claim_rows.csv
data/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary_summary.json
figures/project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary.png
```

## Result

```text
claims:                            25
guarded claims:                    22
blocked claims:                    3
threshold ladder ready:            true
threshold-ladder sensitivity ready:true
scenarios:                         9
pass scenarios:                    5
fail scenarios:                    4
perturbed score rows:              2511
pass rows:                         1395
fail rows:                         1116
max passing relative residual:     9.50339903422461e-13
min failing relative residual:     1.0501746923583452e-12
threshold calibration ready:       true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
claim boundary ready:              true
```

The new guarded claim records the threshold behavior of the synthetic
normalized comparator. It does not promote real comparison, 3D validation,
GPU/HPC work, field transfer, or field FWI.

## Decision

Use this as the current BEM claim boundary after the threshold-ladder block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_post_35field_synthetic_normalized_comparator_threshold_ladder_claim_boundary.py
4 passed as part of the 12-test focused set
```

Figure check:

```text
3941x909, dynamic range=255
```
