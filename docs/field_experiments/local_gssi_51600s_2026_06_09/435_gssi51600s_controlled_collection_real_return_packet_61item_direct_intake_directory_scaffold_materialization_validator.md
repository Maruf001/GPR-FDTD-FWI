# Field Experiment 435: Direct Intake Directory Scaffold Validator

Date: 2026-06-30

## Purpose

Validate run `434` from saved artifacts.

The validator checks that only the directory scaffold was materialized, all 33
file slots remain open, no hashes or templates were created, and all downstream
field evidence states remain blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/435_gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validator_checks.csv
data/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validator_summary.json
figures/gssi51600s_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
validation passes:                         6
blocking failures:                         0
directory scaffold validation ready:       true
directories present after run:             5
files present after scaffold:              0
remaining pre-ingest blockers:             4
controlled field evidence ready:           false
field FWI ready:                           false
field 3D/HPC ready:                        false
GPU priority:                              none
```

Validated checks:

| Check | Result |
| --- | --- |
| Source chain ready | pass |
| Directories materialized without file creation | pass |
| Field file requirements remain open | pass |
| Action state advances only directory step | pass |
| Downstream states remain blocked | pass |
| Figure and script snapshots are present | pass |

## Decision

Use this validator as the artifact guard for run `434`.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_61item_direct_intake_directory_scaffold_materialization_validator.py
4 passed
```

Figure check:

```text
2645x860, dynamic range=255
```
