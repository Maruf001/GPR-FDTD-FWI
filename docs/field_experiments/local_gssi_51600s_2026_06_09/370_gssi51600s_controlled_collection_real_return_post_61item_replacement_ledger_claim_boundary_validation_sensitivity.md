# Field Experiment 370: Post-61-Item Replacement Ledger Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `369` validator with controlled damaged variants of the
run `368` claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/370_gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validation_sensitivity.png
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
validator accepts exact run 368:   true
validator rejects damaged variants:true
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator accepts the exact run `368` boundary and rejects controlled
damage to claim counts, ledger metrics, evidence state, blocked rows,
downstream promotion, figure validation, and script snapshots.

## Decision

Use runs `368-370` as the guarded field post-replacement-ledger
claim-boundary block. Keep measured evidence, provenance, archive acceptance,
field FWI, GPU work, and field 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x889, dynamic range=255
```
