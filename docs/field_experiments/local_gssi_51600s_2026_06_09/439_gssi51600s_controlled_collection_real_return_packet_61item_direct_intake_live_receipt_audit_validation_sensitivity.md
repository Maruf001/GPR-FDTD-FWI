# Field Experiment 439: Direct-Intake Live Receipt Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `438` validator.

The exact run `437` live receipt audit should pass. Damaged source readiness,
directory counts, missing directories, file/receipt promotion, unexpected-file
promotion, parser/downstream promotion, action damage, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/439_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
live receipt audit sensitivity ready:      true
exact source artifacts pass:               true
directory damage rejected:                 true
file/receipt promotion rejected:           true
acceptance/downstream promotion rejected:  true
action damage rejected:                    true
figure damage rejected:                    true
script-snapshot damage rejected:           true
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use runs `437-439` as the guarded live-receipt audit block before any parser,
provenance, archive, field FWI, or field 3D/HPC rerun.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_live_receipt_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
2717x839, dynamic range=255
```
