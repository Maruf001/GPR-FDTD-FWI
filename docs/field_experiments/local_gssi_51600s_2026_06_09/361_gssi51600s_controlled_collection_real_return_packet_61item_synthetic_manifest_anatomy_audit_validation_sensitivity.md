# Field Experiment 361: 61-Item Synthetic Manifest Anatomy Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `360` validator with controlled damaged variants of the
run `359` manifest anatomy audit.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/361_gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validation_sensitivity.png
```

## Result

```text
scenarios:                         19
expected pass scenarios:           1
expected failure scenarios:        18
observed pass scenarios:           1
observed failure scenarios:        18
unexpected outcomes:               0
manifest anatomy sensitivity ready:true
measured-evidence payloads:        0
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The validator accepts the exact run `359` manifest anatomy and rejects
controlled damage to readiness, packet counts, duplicate metadata burden,
measured-evidence promotion, downstream promotion, figure validation, and
script snapshots.

## Decision

Use runs `359-361` as the guarded field synthetic manifest-anatomy block. Keep
measured evidence, provenance, archive acceptance, field FWI, GPU, and field
3D/HPC blocked until real measured files replace the synthetic payloads.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_synthetic_manifest_anatomy_audit_validation_sensitivity.py
3 passed as part of the 11-test focused set
```

Figure check:

```text
3581x885, dynamic range=255
```
