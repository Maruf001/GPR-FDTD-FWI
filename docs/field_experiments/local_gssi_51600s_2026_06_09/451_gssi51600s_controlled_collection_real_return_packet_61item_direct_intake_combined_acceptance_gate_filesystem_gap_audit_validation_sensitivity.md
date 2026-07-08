# Field Experiment 451: Combined Acceptance Gate Filesystem Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `450` validator.

The exact run `449` artifacts should pass. Damaged source readiness,
directory-count drift, missing directory, unexpected-file promotion, file-count
drift, live-file promotion, nonempty-file promotion, DZT and metadata missing
count drift, schema-acceptance promotion, action damage, downstream promotion,
figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/451_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     16
expected pass scenarios:                   1
expected failure scenarios:                15
unexpected scenarios:                      0
filesystem-gap sensitivity ready:          true
exact source artifacts pass:               true
directory damage rejected:                 true
file damage rejected:                      true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
real packet files present:                 false
real packet accepted:                      false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
directory_count_drift
directory_missing
unexpected_file_promotion
file_count_drift
file_present_promotion
file_nonempty_promotion
dzt_missing_count_drift
metadata_missing_count_drift
schema_acceptance_promotion
action_ready_promotion
action_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `449-451` as the current live field filesystem gap. The field branch
remains blocked until the 33 real files are copied into the staged return tree.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_filesystem_gap_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
3077x839, dynamic range=255
```
