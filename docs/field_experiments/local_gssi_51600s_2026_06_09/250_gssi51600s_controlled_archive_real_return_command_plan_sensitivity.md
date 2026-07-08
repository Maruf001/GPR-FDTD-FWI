# Field Experiment 250: Controlled Archive Real Return Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `249` real-return command-plan validator.

This run verifies that the validator accepts the exact run `248` command plan
and rejects controlled damage to command rows, summary counts, command
execution state, and false archive/downstream readiness.

This run does not execute commands, inspect real measured files, accept a real
archive, promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/250_gssi51600s_controlled_archive_real_return_command_plan_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_real_return_command_plan_sensitivity_scenarios.csv
data/field_controlled_archive_real_return_command_plan_sensitivity_summary.json
figures/field_controlled_archive_real_return_command_plan_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_COMMAND_PLAN_SENSITIVITY.md
scripts/run_gssi_field_controlled_archive_real_return_command_plan_sensitivity.py
scripts/test_gssi_field_controlled_archive_real_return_command_plan_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                            27
expected pass scenarios:              1
observed pass scenarios:              1
expected failure scenarios:           26
observed failure scenarios:           26
unexpected outcomes:                  0
sensitivity ready:                    true
command plan ready:                   true
commands executed:                    false
real files present:                   false
ready for real archive acceptance:    false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                         none
```

The exact run `248` command plan passes. All 26 damaged variants fail as
expected for command-row drift, command-order drift, command-group drift,
current guard executability drift, future real-archive gate blocking drift,
summary-count drift, command-execution promotion, real-file promotion,
real-archive acceptance promotion, and false field FWI/3D/GPU readiness.

## Interpretation

The real-return command checklist is now guarded. Current guard commands can be
used to recheck the support package, but real archive commands remain blocked
until real measured files are staged.

## Decision

Use runs `248`-`250` as the guarded real-return archive command checklist. Real
measured files remain required before archive acceptance, field evidence
promotion, field FWI, field 3D/HPC, or GPU escalation.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_command_plan_sensitivity.py
6 passed
```

Figure validation:

```text
3941x892, dynamic range=255
```
