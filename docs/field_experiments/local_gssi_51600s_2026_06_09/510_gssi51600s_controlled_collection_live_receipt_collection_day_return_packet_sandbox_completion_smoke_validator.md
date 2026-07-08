# Field Experiment 510: Return-Packet Sandbox Completion Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `509`, the output-local sandbox completion smoke for the
collection-day return-packet intake contract.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/510_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator.png
scripts/
```

## Result

```text
validation checks:                 5
failed checks:                     0
sandbox files:                     33
sandbox receipt-ready files:       33
sandbox receipt checks:            183
sandbox complete families:         5
original live files present:       0
measured field evidence files:     0
live receipt ready:                false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source sandbox completion smoke ready | pass |
| 2 | sandbox packet shape complete | pass |
| 3 | receipt report is internally consistent | pass |
| 4 | sandbox remains non-evidence and live paths empty | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `510` confirms that the sandbox completion smoke is a valid
positive-path receipt-mechanics artifact. The pass is limited to output-local
synthetic placeholders and does not promote the live field archive.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_sandbox_completion_smoke_validator.py

6 passed
```

Figure check:

```text
2285x832, dynamic range=255
```
