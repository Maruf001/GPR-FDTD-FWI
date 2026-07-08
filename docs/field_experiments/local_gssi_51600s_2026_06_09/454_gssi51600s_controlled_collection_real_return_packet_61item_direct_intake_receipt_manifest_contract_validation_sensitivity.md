# Field Experiment 454: Direct-Intake Receipt Manifest Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `453` validator with controlled damaged variants of the
run `452` artifacts.

The sensitivity set tests source damage, missing and duplicate receipt rows,
extension damage, directory damage, file promotion, schema-acceptance
promotion, action promotion, downstream field-evidence promotion, figure
damage, and script-snapshot damage.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/454_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source contract ready:                     true
source validator ready:                    true
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
source damage rejected:                    true
receipt damage rejected:                   true
directory damage rejected:                 true
file promotion rejected:                   true
schema promotion rejected:                 true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
sensitivity ready:                         true
GPU priority:                              none
```

## Decision

Runs `452-454` are the current guarded field receipt-manifest block before any
measured file copy, parser rerun, provenance rerun, archive acceptance, field
FWI, or field 3D/HPC escalation.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_receipt_manifest_contract_validation_sensitivity.py
2 passed
```

Figure check:

```text
2897x841, dynamic range=255
```
