# Field Experiment 448: Direct Intake Combined Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `447` validator.

The exact run `446` combined gate should pass. Damaged source readiness, total
file counts, DZT file counts, metadata file counts, DZT check counts, metadata
field counts, total requirement counts, live-file promotion, accepted-file
promotion, parser acceptance, provenance acceptance, archive acceptance, action
readiness, downstream promotion, figure damage, and script-snapshot damage
should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/448_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     18
expected pass scenarios:                   1
expected failure scenarios:                17
unexpected scenarios:                      0
combined gate sensitivity ready:           true
exact source artifacts pass:               true
count damage rejected:                     true
file or acceptance promotion rejected:     true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
real packet accepted:                      false
provenance acceptance ready:               false
archive acceptance ready:                  false
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
total_file_count_drift
dzt_file_count_drift
metadata_file_count_drift
dzt_check_count_drift
metadata_field_count_drift
total_requirement_count_drift
dzt_file_promotion
metadata_file_promotion
accepted_file_promotion
parser_acceptance_promotion
provenance_acceptance_promotion
archive_acceptance_promotion
action_damage
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `446-448` as the guarded combined direct-intake acceptance-gate block.
No field parser, provenance gate, archive acceptance, field FWI, or field 3D/HPC
run is justified until the real 33-file packet exists and passes this gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_combined_acceptance_gate_validation_sensitivity.py
4 passed
```

Figure check:

```text
3311x839, dynamic range=255
```
