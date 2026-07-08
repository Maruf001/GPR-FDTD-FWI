# Field Experiment 375: Post 61-Item Collection Execution Checklist Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `374` from saved artifacts.

The validator checks claim counts, checklist-claim insertion, checklist
metrics, blocked downstream states, figure validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/375_gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation passes:                 5
blocking failures:                 0
claim-boundary validation ready:   true
claims:                            20
guarded claims:                    16
blocked claims:                    4
stages:                            4
dependency edges:                  6
direct collection input files:     33
generated verification files:      16
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

## Decision

Use this validator as the artifact guard for run `374`. Sensitivity testing
remains required before closing the post-checklist claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validator.py
4 passed as part of the 22-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
