# Field Experiment 252: Controlled Archive Real Return Current Guard Execution Validator

Date: 2026-06-28

## Purpose

Validate the run `251` current-guard execution smoke from saved artifacts.

This run does not execute commands, inspect real measured files, accept a real
archive, promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/252_gssi51600s_controlled_archive_real_return_current_guard_execution_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_current_guard_execution_validator_checks.csv
data/field_controlled_archive_real_return_current_guard_execution_validator_summary.json
figures/field_controlled_archive_real_return_current_guard_execution_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_CURRENT_GUARD_EXECUTION_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_return_current_guard_execution_validator.py
scripts/test_gssi_field_controlled_archive_real_return_current_guard_execution_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                    6
validation checks passed:             6
blocking failures:                    0
current-guard validation ready:       true
current-guard execution smoke ready:  true
future real-archive commands run:     false
real files present:                   false
real archive acceptance ready:        false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

The saved current-guard execution smoke is internally consistent and matches
the runnable current-guard subset of the real-return command plan.

## Decision

Use runs `251-252` as the consumer-validated current-guard execution smoke.
Sensitivity remains required before treating the smoke as fully guarded.

Real measured files remain required before real archive acceptance, field
evidence promotion, field FWI, field 3D/HPC, or GPU escalation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_current_guard_execution_validator.py
6 passed
```

Figure validation:

```text
2717x814, dynamic range=255
```
