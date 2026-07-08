# Field Experiment 214: Controlled Archive Command Plan Positive-Control Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `213` positive-control validator with damaged summary
variants.

This run does not ingest real field files, execute shell command templates,
accept a real archive, run field FWI, launch GPU/HPC work, or run 3D
validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/214_gssi51600s_controlled_archive_execution_command_plan_positive_control_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_execution_command_plan_positive_control_sensitivity_scenarios.csv
data/field_controlled_archive_execution_command_plan_positive_control_sensitivity_summary.json
figures/field_controlled_archive_execution_command_plan_positive_control_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_EXECUTION_COMMAND_PLAN_POSITIVE_CONTROL_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_execution_command_plan_positive_control_sensitivity.py
scripts/test_gssi_field_controlled_archive_execution_command_plan_positive_control_sensitivity.py
```

## Result

```text
scenarios:                         14
expected pass scenarios:           1
expected failure scenarios:        13
observed pass scenarios:           1
observed failure scenarios:        13
unexpected outcomes:               0
sensitivity ready:                 true
real archive acceptance ready:     false
checksum intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
3D/HPC ready:                      false
```

The exact positive-control summary passes. Damaged summaries fail for the
intended reasons: command-count drift, command failure, synthetic-file count
drift, file/signature/checksum group pass-count drift, positive-control not
ready, synthetic files marked real, real files present, shell command execution,
real archive ready, checksum intake ready, and field FWI ready.

## Interpretation

Runs `212`-`214` form a guarded synthetic positive-control harness for the field
command-plan evaluator. Together with the fail-closed package from runs
`209`-`211`, the evaluator now has both expected failure and expected pass
coverage.

## Decision

Use runs `212`-`214` as the guarded positive-control command-plan harness.

Real archive acceptance, checksum intake, controlled evidence, field FWI, GPU
work, and field 3D/HPC remain blocked until real measured files pass.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control_sensitivity.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_archive_execution_command_plan_positive_control_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_execution_command_plan_positive_control_sensitivity.py: pass
```

Figure check:

```text
2933x859, dynamic range=255
```
