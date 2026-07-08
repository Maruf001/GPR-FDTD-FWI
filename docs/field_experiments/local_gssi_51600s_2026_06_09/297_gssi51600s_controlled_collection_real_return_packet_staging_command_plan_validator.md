# Field Experiment 297: Real Return Packet Staging Command Plan Validator

Date: 2026-06-29

## Purpose

Validate the saved run `296` field real-return packet staging command plan from
artifacts.

Run `296` converted the guarded field packet contract into a non-executed
staging command plan. This run checks whether that plan is internally
consistent and still correctly blocked from real execution.

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/297_gssi51600s_controlled_collection_real_return_packet_staging_command_plan_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_staging_command_plan_validator_checks.csv
data/field_controlled_collection_real_return_packet_staging_command_plan_validator_summary.json
figures/field_controlled_collection_real_return_packet_staging_command_plan_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_STAGING_COMMAND_PLAN_VALIDATOR.md
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:             9
passed checks:                 9
failed checks:                 0
staging plan validation ready: true
phases:                        8
commands:                      8
packet items:                  57
acceptance checks:             189
measured requirements:         50
measured complete:             0
real DZT files:                9
metadata values:               32
checksum rows:                 9
acceptance gates:              7
real packet files present:     false
real return execution ready:   false
provenance acceptance ready:   false
real archive acceptance ready: false
controlled evidence ready:     false
field FWI ready:               false
field 3D/HPC ready:            false
GPU priority:                  none
figure size:                   3401x896
figure dynamic range:          255
```

The nine checks all passed:

| Check | Passed |
| --- | --- |
| source policy and plan counts | yes |
| phase order and dependencies | yes |
| expected output counts stable | yes |
| commands remain non-executed | yes |
| source contract links present | yes |
| current archive empty state stable | yes |
| field execution states blocked | yes |
| figure validation present | yes |
| script snapshots present | yes |

## Interpretation

The saved field packet staging command plan is internally consistent and
remains non-executing. It validates the handoff plan but does not create real
packet files or make field evidence ready.

## Decision

Use run `297` as the validator for the run `296` field packet staging command
plan. Keep provenance acceptance, real archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, and GPU work blocked until the measured
packet is staged and validators pass.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_command_plan_validator.py
4 passed
```
