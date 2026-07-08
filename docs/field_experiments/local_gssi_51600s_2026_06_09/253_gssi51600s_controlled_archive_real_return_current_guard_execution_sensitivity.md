# Field Experiment 253: Controlled Archive Real Return Current Guard Execution Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `252` current-guard execution validator.

This run does not execute commands, inspect real measured files, accept a real
archive, promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/253_gssi51600s_controlled_archive_real_return_current_guard_execution_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_current_guard_execution_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_current_guard_execution_sensitivity_summary.json
figures/field_controlled_archive_real_return_current_guard_execution_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_CURRENT_GUARD_EXECUTION_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_return_current_guard_execution_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_return_current_guard_execution_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         28
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        27
observed failure scenarios:        27
unexpected outcomes:               0
sensitivity ready:                 true
execution validation ready:        true
execution smoke ready:             true
future real-archive commands run:  false
real files present:                false
real archive acceptance ready:     false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The current-guard execution validator accepts the exact run `251` smoke and
rejects controlled damage to execution rows, source command-plan matching,
summary counts, execution state, and false real/downstream readiness.

## Decision

Use runs `251-253` as the guarded current-guard execution smoke for the
real-return archive checklist.

Real measured files remain required before real archive acceptance, field
evidence promotion, field FWI, field 3D/HPC, or GPU escalation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_current_guard_execution_sensitivity.py
6 passed
```

Figure validation:

```text
4121x889, dynamic range=255
```
