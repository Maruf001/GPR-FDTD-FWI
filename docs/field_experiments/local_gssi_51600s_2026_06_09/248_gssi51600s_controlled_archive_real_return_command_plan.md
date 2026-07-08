# Field Experiment 248: Controlled Archive Real Return Command Plan

Date: 2026-06-28

## Purpose

Convert the guarded real-return acceptance boundary from runs `245`-`247` into
a non-executed command checklist for future real archive intake.

This run answers a practical handoff question:

```text
Which commands can be run now, and which commands must wait until real measured
files exist?
```

This run does not execute commands, inspect real measured files, accept a real
archive, promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/248_gssi51600s_controlled_archive_real_return_command_plan
```

Key artifacts:

```text
data/field_controlled_archive_real_return_command_plan_rows.csv
data/field_controlled_archive_real_return_command_plan_summary.json
figures/field_controlled_archive_real_return_command_plan.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_COMMAND_PLAN.md
scripts/run_gssi_field_controlled_archive_real_return_command_plan.py
scripts/test_gssi_field_controlled_archive_real_return_command_plan.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source boundary guarded:               true
commands:                              6
current guard commands:                3
future real-archive commands:          3
executable now:                        3
requires real archive root:            3
requires real files:                   3
commands executed:                     false
real-return command plan ready:        true
real files present:                    false
ready for real archive acceptance:     false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

The six commands are split into two groups:

| Order | Command group | Command name | Executable now | Requires real archive root |
| ---: | --- | --- | ---: | ---: |
| 1 | current guard validation | real return boundary focused tests | true | false |
| 2 | current guard validation | empty skeleton validator | true | false |
| 3 | current guard validation | synthetic positive-control validator | true | false |
| 4 | future real archive gate | real archive preflight | false | true |
| 5 | future real archive gate | real file checksum intake | false | true |
| 6 | future real archive gate | rerun structural and provenance gates | false | true |

## Interpretation

The real-return path now has an execution checklist without pretending that the
current archive is ready. The runnable commands only recheck the existing guard
state. The three real archive commands remain blocked until a real archive root
with real measured files is staged.

## Decision

Use run `248` as the command checklist for the real-return acceptance path. Do
not execute real archive commands against missing or synthetic data. Real
archive acceptance, field FWI, field 3D/HPC, and GPU escalation remain blocked.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_command_plan.py
3 passed
```

Figure validation:

```text
2465x826, dynamic range=255
```
