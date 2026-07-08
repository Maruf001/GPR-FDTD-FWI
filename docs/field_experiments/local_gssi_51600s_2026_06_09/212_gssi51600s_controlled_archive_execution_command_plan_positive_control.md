# Field Experiment 212: Controlled Archive Command Plan Positive Control

Date: 2026-06-28

## Purpose

Evaluate the run `206` command plan against a run-local synthetic archive that
contains dummy DZT files with the expected size floor and header prefix.

This is a positive control for the evaluator. It does not ingest real field
files, execute shell command templates, accept a real archive, run field FWI,
launch GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/212_gssi51600s_controlled_archive_execution_command_plan_positive_control
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_positive_control_rows.csv
data/field_controlled_archive_execution_command_plan_positive_control_files.csv
data/field_controlled_archive_execution_command_plan_positive_control_summary.json
figures/field_controlled_archive_execution_command_plan_positive_control.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_POSITIVE_CONTROL.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_positive_control.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_positive_control.py
```

## Result

```text
source commands:                    27
positive-control commands:          27
positive-control passes:            27
positive-control failures:          0
synthetic files:                    9
file-existence passes:              9
DZT-signature passes:               9
SHA-256 passes:                     9
synthetic positive control ready:   true
synthetic files are real data:      false
shell commands executed:            false
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
3D/HPC ready:                       false
```

Each synthetic DZT slot is `65536` bytes and begins with header prefix `ff07`.
The run-local synthetic files are only evaluator fixtures.

## Interpretation

The command-plan evaluator now has both sides of a basic guard:

```text
run 209-211: empty archive fails closed
run 212:     synthetic valid archive shape passes the command checks
```

This proves the evaluator can fail when required files are absent and pass when
the expected file/size/header/checksum conditions are present. It still does not
prove real field archive acceptance.

## Decision

Use run `212` with runs `209`-`211` to guard future real archive intake.

Real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC remain blocked until real measured files pass the same
checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_command_plan_positive_control.py: pass
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control.py: pass
```

Figure check:

```text
2284x807, dynamic range=255
```
