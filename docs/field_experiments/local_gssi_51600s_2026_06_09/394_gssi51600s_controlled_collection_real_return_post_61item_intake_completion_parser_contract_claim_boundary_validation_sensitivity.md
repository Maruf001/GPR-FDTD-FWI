# Field Experiment 394: Post-Parser-Contract Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `393` validator against controlled damage to the
post-parser-contract field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/394_gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validation_sensitivity.png
```

## Result

```text
scenarios:                          33
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         32
observed failure scenarios:         32
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 392:    true
validator rejects damaged variants: true
real packet files present:          false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The damaged variants cover claim-count drift, parser-claim support drift,
parser-metric drift, current-row acceptance promotion, measured-evidence
promotion, downstream promotion, GPU-priority drift, blank figures, and
missing script snapshots.

## Decision

Use runs `392-394` as the current guarded field post-parser-contract
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validator.py
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_completion_parser_contract_claim_boundary_validation_sensitivity.py
12 passed
```

Figure check:

```text
3581x885, dynamic range=255
```
