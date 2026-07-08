# Field Experiment 376: Post 61-Item Collection Execution Checklist Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `375` validator with controlled damaged variants of the
run `374` post-checklist claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/376_gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         22
expected pass scenarios:           1
expected failure scenarios:        21
observed pass scenarios:           1
observed failure scenarios:        21
unexpected outcomes:               0
claim-boundary sensitivity ready:  true
validator accepts exact run 374:   true
validator rejects damaged variants:true
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The validator accepts the exact run `374` boundary and rejects controlled
damage to counts, checklist metrics, evidence text, blocked rows, downstream
state, figure validation, and script snapshots.

## Decision

Use runs `374-376` as the guarded field post-checklist claim-boundary block.
Keep measured evidence, provenance, archive acceptance, field FWI, GPU work,
and field 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_collection_execution_checklist_claim_boundary_validation_sensitivity.py
3 passed as part of the 22-test focused set
```

Figure check:

```text
3581x889, dynamic range=255
```
