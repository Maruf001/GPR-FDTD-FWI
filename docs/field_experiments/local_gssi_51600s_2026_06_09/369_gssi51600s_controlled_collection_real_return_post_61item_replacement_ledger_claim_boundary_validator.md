# Field Experiment 369: Post-61-Item Replacement Ledger Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate run `368` from saved artifacts.

The validator checks claim counts, the inserted replacement-ledger claim,
ledger metrics, blocked downstream rows, figure validation, and script
snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/369_gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
passed checks:                     5
failed checks:                     0
claim-boundary validation ready:   true
claims:                            19
guarded claims:                    15
blocked claims:                    4
direct collection input files:     33
generated verification files:      16
field evidence ready:              false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Decision

Use this validator as the artifact guard for run `368`. Sensitivity testing
remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_replacement_ledger_claim_boundary_validator.py
4 passed as part of the 11-test focused set
```

Figure check:

```text
2645x839, dynamic range=255
```
