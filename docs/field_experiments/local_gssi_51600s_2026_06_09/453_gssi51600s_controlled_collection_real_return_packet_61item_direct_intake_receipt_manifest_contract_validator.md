# Field Experiment 453: Direct-Intake Receipt Manifest Contract Validator

Date: 2026-06-30

## Purpose

Validate run `452` from its saved artifacts.

This run checks that the receipt manifest has 33 unique file identities, the
expected 9/24 DZT/metadata split, the five required directories, 183 file-level
checks, zero accepted measured files, and no downstream field promotion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/453_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         5
validation passes:                         5
blocking failures:                         0
required receipt rows:                     33
unique receipt identities:                 33
total required file-level checks:          183
required directories:                      5
receipt actions:                           4
receipt manifest validation ready:         true
GPU priority:                              none
```

## Decision

Run `452` validates as the current field receipt-manifest lock. It is ready to
guard copied measured files, but it does not itself provide measured evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validator.py
4 passed
```

Figure check:

```text
2285x841, dynamic range=255
```
