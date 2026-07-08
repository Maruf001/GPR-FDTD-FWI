# Field Experiment 382: Post Operator-Handoff Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `381` validator with controlled damaged variants of the
run `380` claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/382_gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                         26
expected pass scenarios:           1
expected failure scenarios:        25
observed pass scenarios:           1
observed failure scenarios:        25
unexpected outcomes:               0
handoff-boundary sensitivity ready:true
validator accepts exact run 380:   true
validator rejects damaged variants:true
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
GPU priority:                      none
```

The validator accepts the exact run `380` boundary and rejects controlled
damage to claim counts, handoff-claim support, handoff metrics, blocked rows,
downstream promotions, figure validation, and script snapshots.

## Decision

Use runs `380-382` as the current guarded field post-handoff claim-boundary
block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_operator_handoff_manifest_claim_boundary_validation_sensitivity.py
3 passed as part of the 12-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
