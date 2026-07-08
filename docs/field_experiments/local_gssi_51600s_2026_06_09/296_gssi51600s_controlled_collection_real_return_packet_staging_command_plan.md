# Field Experiment 296: Real Return Packet Staging Command Plan

Date: 2026-06-29

## Purpose

Convert the guarded run `293` field real-return packet contract into an ordered,
non-executed staging command plan.

Runs `293-295` define and guard the packet contents. This run answers the next
practical question:

```text
What exact staging phases must happen before the measured field return packet
can be accepted?
```

This run does not stage real DZT files, promote field evidence, run field FWI,
launch 3D/HPC work, or start GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/296_gssi51600s_controlled_collection_real_return_packet_staging_command_plan
```

Key artifacts:

```text
data/field_controlled_collection_real_return_packet_staging_command_plan_command_rows.csv
data/field_controlled_collection_real_return_packet_staging_command_plan_commands.sh
data/field_controlled_collection_real_return_packet_staging_command_plan_summary.json
figures/field_controlled_collection_real_return_packet_staging_command_plan.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_PACKET_STAGING_COMMAND_PLAN.md
scripts/script_snapshot_manifest.json
```

## Result

```text
packet contract guarded:           true
phases:                            8
commands:                          8
all commands non-executed:          true
command script comment-only:        true
packet items:                       57
acceptance checks:                  189
measured requirements:              50
measured requirements complete:     0
real DZT files:                     9
controlled profile repeats:         3
time-zero references:               3
amplitude references:               3
metadata values:                    32
checksum rows:                      9
acceptance gates:                   7
real packet files present:          false
real return execution ready:        false
provenance acceptance ready:        false
real archive acceptance ready:      false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
figure size:                        3365x927
figure dynamic range:               255
```

The eight staging phases are:

| Order | Phase | Expected output count | Executed |
| ---: | --- | ---: | --- |
| 1 | create return packet directories | 7 | no |
| 2 | stage controlled profile repeats | 3 | no |
| 3 | stage time-zero references | 3 | no |
| 4 | stage amplitude references | 3 | no |
| 5 | write measured metadata | 32 | no |
| 6 | compute and record checksums | 9 | no |
| 7 | run packet acceptance checks | 189 | no |
| 8 | write acceptance gate results | 7 | no |

## Interpretation

The guarded field return packet now has a concrete non-executed staging
sequence. The plan remains a handoff artifact only: it does not stage measured
files or make field evidence ready.

## Decision

Use run `296` as the field real-return packet staging command plan. Keep
provenance acceptance, real archive acceptance, controlled field evidence,
field FWI, field 3D/HPC, and GPU work blocked until the measured packet is
staged and validators pass.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_packet_staging_command_plan.py
3 passed
```
