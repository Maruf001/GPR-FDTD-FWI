# Field Experiment 206: Controlled Archive Execution Command Plan

Date: 2026-06-27

## Purpose

Convert the controlled archive execution packet from run `203` into explicit
command templates for a future real archive intake.

This is a CPU-only planning run. It does not ingest real DZT files, execute the
commands, modify any archive, accept field evidence, run field FWI, launch GPU
work, run field 3D/HPC, or train a neural network.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/206_gssi51600s_controlled_archive_execution_command_plan
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_rows.csv
data/field_controlled_archive_execution_command_plan_summary.json
figures/field_controlled_archive_execution_command_plan.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN.md
scripts/run_gssi_field_controlled_archive_execution_command_plan.py
scripts/test_gssi_field_controlled_archive_execution_command_plan.py
```

## Result

```text
source file slots:                  9
command groups:                     3
commands:                          27
commands per file slot:             3
file-exists commands:               9
DZT signature commands:             9
checksum commands:                  9
execution command plan ready:       true
real files present:                 false
commands executed:                  false
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The command plan attaches three checks to each required DZT slot:

| Command group | Count | Purpose |
| --- | ---: | --- |
| `file_exists` | 9 | Confirm the expected archive-relative DZT file exists. |
| `dzt_signature_guard` | 9 | Confirm the DZT size floor and GSSI header prefix guard. |
| `sha256_checksum` | 9 | Produce a checksum for intake provenance. |

## Interpretation

The field intake path is now operationally explicit. When a real controlled
archive exists, there is a concrete command plan for checking all three
controlled profile repeats, all three time-zero reference files, and all three
amplitude-reference files.

This run does not reduce the evidence blocker by itself. It only turns the
previous packet into reproducible command templates. The real archive still
needs measured files and measured metadata, followed by command execution,
checksum intake, structural validation, provenance validation, and downstream
acceptance gates.

## Decision

Use run `206` as the command-template companion to the execution packet from
run `203`. Keep real archive acceptance, checksum intake, controlled evidence,
field FWI, heavy GPU work, field 3D/HPC, and neural-network training blocked
until the commands are executed on real files and all integrated gates pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan.py
3 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan.png
2248x789, dynamic range=255
```
