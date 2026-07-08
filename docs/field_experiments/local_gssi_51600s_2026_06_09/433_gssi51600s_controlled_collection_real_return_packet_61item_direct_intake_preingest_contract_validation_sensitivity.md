# Field Experiment 433: Direct Intake Pre-Ingest Contract Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `432` validator for the direct-intake pre-ingest contract.

Run `431` created the 33-row pre-ingest contract. Run `432` validated it. This
run verifies that the validator accepts the exact saved state and rejects
damaged paths, fake files, fake hashes, action drift, and downstream promotion.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/433_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validation_sensitivity_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                    12
expected pass scenarios:                  1
expected failure scenarios:               11
unexpected scenarios:                     0
pre-ingest sensitivity ready:             true
exact source artifacts pass:              true
file promotion rejected:                  true
SHA-256 promotion rejected:               true
downstream promotion rejected:            true
real packet files present:                false
real packet accepted:                     false
controlled field evidence ready:          false
field FWI ready:                          false
field 3D/HPC ready:                       false
```

The exact run `431` artifacts pass. Eleven damaged variants fail as expected:

| Scenario | Expected result | Failed check |
| --- | --- | --- |
| row count drift | fail | pre-ingest shape and counts |
| DZT count drift | fail | pre-ingest shape and counts |
| extension damage | fail | path extension and check rules |
| file promotion | fail | current files and hashes remain absent |
| SHA-256 promotion | fail | current files and hashes remain absent |
| directory promotion | fail | directory and action state |
| action order damage | fail | directory and action state |
| evidence promotion | fail | downstream states |
| field FWI promotion | fail | downstream states |
| figure damage | fail | figure and script snapshots |
| script snapshot damage | fail | figure and script snapshots |

## Decision

Use runs `431-433` as the guarded direct-intake pre-ingest contract block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validation_sensitivity.py
12 passed
```

Figure check:

```text
2717x869, dynamic range=255
```
