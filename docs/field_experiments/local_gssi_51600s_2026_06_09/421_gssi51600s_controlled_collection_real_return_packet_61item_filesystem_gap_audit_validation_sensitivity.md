# Field Experiment 421: 61-Item Real-Packet Filesystem Gap-Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `420` validator against controlled damage to the filesystem
gap audit.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/421_gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_filesystem_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       24
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  23
observed failure scenarios:                  23
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 419:             true
validator rejects damaged variants:          true
real packet files present:                   false
real packet accepted:                        false
controlled field evidence ready:             false
field FWI ready:                             false
field 3D/HPC ready:                          false
GPU priority:                                none
```

The damaged variants cover scan-count drift, real-file promotion,
template/synthetic misclassification, measured-evidence promotion, downstream
promotion, GPU-priority drift, figure damage, and script-snapshot damage.

## Decision

Use runs `419-421` as the guarded field filesystem gap-audit block.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_filesystem_gap_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3617x918, dynamic range=255
```
