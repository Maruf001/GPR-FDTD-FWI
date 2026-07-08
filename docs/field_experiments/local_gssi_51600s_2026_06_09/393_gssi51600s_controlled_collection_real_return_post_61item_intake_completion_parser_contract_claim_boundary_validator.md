# Field Experiment 393: Post-Parser-Contract Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved claim-boundary artifacts from run `392`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/393_gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator.png
```

## Result

```text
validation checks:                 5
validation checks passed:          5
blocking failures:                 0
claim-boundary validation ready:   true
claims:                            23
guarded claims:                    19
blocked claims:                    4
worksheet rows:                    49
completion rules:                  6
required completion columns:       5
parser-accepted current rows:      0
current measured-evidence rows:    0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator confirms the claim count, parser-claim support range, parser
metrics, blocked downstream states, nonblank figure output, and script
snapshots.

## Decision

Use this validator as the artifact guard for run `392`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
