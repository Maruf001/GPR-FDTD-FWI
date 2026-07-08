# Field Experiment 432: Direct Intake Pre-Ingest Contract Validator

Date: 2026-06-30

## Purpose

Validate run `431`, the direct-intake pre-ingest contract for the latest
33-slot field staging manifest.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/432_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
validation checks passed:                  6
blocking failures:                         0
pre-ingest contract validation ready:      true
source pre-ingest contract ready:          true
pre-ingest rows:                           33
required directories:                      5
actions:                                   6
current files present:                     0
current SHA-256 records present:           0
real packet files present:                 false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
```

## Decision

Use run `432` as the artifact guard for the run `431` pre-ingest contract.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract.py
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_preingest_contract_validator.py
8 passed
```

Figure check:

```text
2645x863, dynamic range=255
```
