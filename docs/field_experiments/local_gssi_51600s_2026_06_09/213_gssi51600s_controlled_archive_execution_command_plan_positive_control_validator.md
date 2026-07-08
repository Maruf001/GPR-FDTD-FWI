# Field Experiment 213: Controlled Archive Command Plan Positive-Control Validator

Date: 2026-06-28

## Purpose

Validate the run `212` synthetic positive-control result from a consumer
perspective.

This run does not ingest real field files, execute shell command templates,
accept a real archive, run field FWI, launch GPU/HPC work, or run 3D
validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/213_gssi51600s_controlled_archive_execution_command_plan_positive_control_validator
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_positive_control_validation_checks.csv
data/field_controlled_archive_execution_command_plan_positive_control_validator_summary.json
figures/field_controlled_archive_execution_command_plan_positive_control_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_POSITIVE_CONTROL_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_positive_control_validator.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_positive_control_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
validation ready:                   true
source positive-control passes:     27
real archive acceptance ready:      false
checksum intake ready:              false
controlled evidence ready:          false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The positive-control result is internally consistent. It confirms that all
command groups pass on the synthetic archive, the synthetic files are not real
data, no shell command templates were executed, and real archive/downstream
states remain blocked.

## Decision

Use run `213` as the validator for run `212`. Sensitivity remains required
before treating the positive-control harness as fully guarded.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control_validator.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_command_plan_positive_control_validator.py: pass
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control_validator.py: pass
```

Figure check:

```text
2465x841, dynamic range=255
```
