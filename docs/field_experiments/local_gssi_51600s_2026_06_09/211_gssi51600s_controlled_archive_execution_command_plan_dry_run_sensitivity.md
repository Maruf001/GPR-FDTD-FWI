# Field Experiment 211: Controlled Archive Command Plan Dry-Run Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `210` dry-run validator with damaged variants of the run
`209` fail-closed dry-run result.

This is a CPU-only guard run. It does not ingest real field files, execute shell
command templates, modify a pending archive, run field FWI, launch GPU/HPC work,
or run 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/211_gssi51600s_controlled_archive_execution_command_plan_dry_run_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_dry_run_sensitivity_rows.csv
data/field_controlled_archive_execution_command_plan_dry_run_sensitivity_summary.json
figures/field_controlled_archive_execution_command_plan_dry_run_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_DRY_RUN_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_dry_run_sensitivity.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_dry_run_sensitivity.py
```

## Result

```text
sensitivity scenarios:              11
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         10
observed failure scenarios:         10
unexpected outcomes:                0
dry-run sensitivity ready:          true
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
field 3D/HPC ready:                 false
GPU priority:                       none
```

The exact fail-closed dry run passes. Ten damaged variants fail:

| Scenario | Expected | Observed | Failed checks |
| --- | --- | --- | --- |
| exact fail-closed dry run | pass | pass | none |
| missing dry-run row | fail | fail | command count, missing-file failures, per-group failures |
| wrong command group | fail | fail | command groups, per-group failures |
| unexpected dry-run pass | fail | fail | zero passes, missing-file failures, per-group failures |
| failure reason not missing file | fail | fail | all failures are missing files |
| missing-file count drift | fail | fail | nine file slots |
| fail-closed marked false | fail | fail | fail-closed state |
| row shell execution marked true | fail | fail | no shell execution |
| summary shell execution marked true | fail | fail | no shell execution |
| real archive marked ready | fail | fail | downstream block |
| field FWI marked ready | fail | fail | downstream block |

## Interpretation

The run `210` validator is sensitive to row loss, command-group drift,
unexpected dry-run passes, non-missing-file failures, shell execution flags, and
premature field/archive readiness.

## Decision

Use runs `209`-`211` as the guarded fail-closed dry-run package before real
archive intake. Real archive acceptance, checksum intake, controlled evidence,
field FWI, GPU work, and field 3D/HPC remain blocked until real files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_dry_run_sensitivity.py
4 passed
```

Figure validation:

```text
field_controlled_archive_execution_command_plan_dry_run_sensitivity.png
2717x847, dynamic range=255
```
