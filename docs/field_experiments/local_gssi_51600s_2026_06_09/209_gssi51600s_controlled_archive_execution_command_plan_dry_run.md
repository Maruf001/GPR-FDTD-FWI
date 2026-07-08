# Field Experiment 209: Controlled Archive Execution Command Plan Dry Run

Date: 2026-06-28

## Purpose

Evaluate the run `206` controlled archive command plan against an empty
run-local archive root to confirm that missing real files fail closed.

This is a CPU-only field-side dry run. It does not ingest real field files,
execute shell command templates, modify a pending archive, run field FWI, launch
GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/209_gssi51600s_controlled_archive_execution_command_plan_dry_run
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_dry_run_rows.csv
data/field_controlled_archive_execution_command_plan_dry_run_summary.json
figures/field_controlled_archive_execution_command_plan_dry_run.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_DRY_RUN.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_dry_run.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_dry_run.py
```

## Result

```text
source commands:                    27
dry-run commands:                   27
command groups:                     3
dry-run passes:                     0
dry-run failures:                   27
missing files:                      9
dry-run evaluated:                  true
shell commands executed:            false
fail-closed ready:                  true
real files present:                 false
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

All 27 dry-run command checks fail for the expected reason: the nine required
DZT files are absent from the empty archive root.

| Command group | Expected count | Dry-run passes | Dry-run failures |
| --- | ---: | ---: | ---: |
| file_exists | 9 | 0 | 9 |
| dzt_signature_guard | 9 | 0 | 9 |
| sha256_checksum | 9 | 0 | 9 |

## Interpretation

The command plan fails closed against an empty archive root. Missing files do
not produce archive acceptance, checksum intake, controlled evidence, field FWI
readiness, or 3D/HPC readiness. The shell command templates are not executed in
this run; the dry-run harness evaluates the equivalent safe checks directly.

## Decision

Use this dry-run harness as the fail-closed precheck before real archive intake.
Real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC remain blocked until the same checks pass on real
measured files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_dry_run.py
5 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan_dry_run.png
2284x807, dynamic range=255
```
