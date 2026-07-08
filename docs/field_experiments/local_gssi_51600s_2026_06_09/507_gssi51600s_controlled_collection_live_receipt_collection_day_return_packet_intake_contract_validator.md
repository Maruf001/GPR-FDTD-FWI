# Field Experiment 507: Return Packet Intake Contract Validator

Date: 2026-06-30

## Purpose

Validate run `506`, the unified collection-day return-packet intake contract.

This validator checks that the 33-file contract has the expected family shape,
that all twenty-four metadata templates remain linked but do not count as live
receipt, and that live receipt, parser/provenance/archive promotion, field FWI,
and field 3D/HPC remain blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/507_gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator_check_rows.csv
data/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator.png
scripts/
```

## Result

```text
validation checks:                    5
failed checks:                        0
contract files:                       33
file families:                        5
DZT files:                            9
metadata JSON files:                  24
metadata templates linked:            24
metadata templates unlinked:          0
template files written locally:       24
templates accepted as live receipt:   0
required receipt checks:              183
current live files present:           0
current live receipt-ready files:     0
parser input-ready files:             0
all files required before parser:     true
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source return-packet contract ready | pass |
| 2 | contract rows preserve 33-file shape | pass |
| 3 | metadata templates remain linked but non-receipt | pass |
| 4 | live receipt and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `507` guards the run `506` intake contract. The contract can be used as the
real collection-day return checklist, but the current archive still has zero
live receipt files. The next promotion step still requires all 33 live files to
exist and pass receipt before parser/provenance/archive gates can be rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract.py
tests/test_gssi_field_controlled_collection_live_receipt_collection_day_return_packet_intake_contract_validator.py

6 passed
```

Figure check:

```text
2285x834, dynamic range=255
```
