# Field Experiment 210: Controlled Archive Command Plan Dry-Run Validator

Date: 2026-06-28

## Purpose

Validate the run `209` fail-closed command-plan dry run from a consumer
perspective.

This is a CPU-only validation run. It does not ingest real field files, execute
shell command templates, modify a pending archive, run field FWI, launch
GPU/HPC work, or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/210_gssi51600s_controlled_archive_execution_command_plan_dry_run_validator
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_dry_run_validation_checks.csv
data/field_controlled_archive_execution_command_plan_dry_run_validator_summary.json
figures/field_controlled_archive_execution_command_plan_dry_run_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_DRY_RUN_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_dry_run_validator.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_dry_run_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
source dry-run commands:            27
source dry-run failures:            27
source missing files:               9
source fail-closed ready:           true
dry-run validation ready:           true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The validator confirms:

| Check family | Result |
| --- | --- |
| Dry-run command count | Passed |
| Command groups | Passed |
| Nine required file slots | Passed |
| Zero dry-run passes | Passed |
| All failures are missing files | Passed |
| Nine failures per command group | Passed |
| Dry run evaluated and fail-closed | Passed |
| No shell command templates executed | Passed |
| Real archive and downstream states remain blocked | Passed |

## Interpretation

The fail-closed dry-run result is consumer-valid. All command groups are
present, all 27 checks fail for missing files, no shell templates are executed,
and no downstream field acceptance is inferred.

## Decision

Use runs `209`-`210` as the fail-closed dry-run guard before real archive
intake. Real archive acceptance, checksum intake, controlled evidence, field
FWI, GPU work, and field 3D/HPC remain blocked until real files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_dry_run_validator.py
5 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan_dry_run_validator.png
2537x841, dynamic range=255
```
