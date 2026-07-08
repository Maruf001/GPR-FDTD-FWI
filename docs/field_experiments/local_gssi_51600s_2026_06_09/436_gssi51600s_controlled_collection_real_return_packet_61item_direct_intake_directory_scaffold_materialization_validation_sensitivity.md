# Field Experiment 436: Direct Intake Directory Scaffold Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `435` validator.

The exact run `434` scaffold should pass. Damaged source readiness, missing
directories, false file or hash promotion, template or synthetic file creation,
pre-ingest acceptance promotion, field-evidence promotion, action damage,
figure damage, and script-snapshot damage should fail.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/436_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     12
expected pass scenarios:                   1
expected failure scenarios:                11
unexpected scenarios:                      0
directory scaffold sensitivity ready:      true
exact source artifacts pass:               true
directory damage rejected:                 true
file or hash promotion rejected:           true
evidence promotion rejected:               true
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

## Decision

Use runs `434-436` as the guarded empty-directory scaffold block before copying
measured field files. This block closes directory setup only; it does not close
the real-file, checksum, parser, provenance, archive, or field-evidence gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validation_sensitivity.py
3 passed
```

Figure check:

```text
2897x859, dynamic range=255
```
