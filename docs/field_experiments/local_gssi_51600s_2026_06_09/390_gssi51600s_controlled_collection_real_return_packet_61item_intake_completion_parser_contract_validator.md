# Field Experiment 390: Intake Completion Parser Contract Validator

Date: 2026-06-29

## Purpose

Validate the saved parser-contract artifacts from run `389`.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/390_gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator.png
```

## Result

```text
validation checks:                 5
validation checks passed:          5
blocking failures:                 0
parser-contract validation ready:  true
worksheet rows:                    49
completion rules:                  6
status rules:                      8
blank completion cells:            294
parser-accepted current rows:      0
parser-rejected current rows:      49
current measured-evidence rows:    0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator confirms the worksheet shape, required completion rules, current
blank-row rejection, no current measured evidence, no downstream readiness,
nonblank figure output, and script snapshots.

## Decision

Use this validator as the artifact guard for run `389`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_intake_completion_parser_contract_validator.py
9 passed
```

Figure check:

```text
2645x839, dynamic range=255
```
