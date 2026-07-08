# Field Experiment 249: Controlled Archive Real Return Command Plan Validator

Date: 2026-06-28

## Purpose

Validate the run `248` real-return command plan from saved artifacts.

This run verifies that the command checklist preserves the current real-archive
boundary: current guard commands are runnable now, while real archive commands
remain blocked until a real archive root with real measured files exists.

This run does not execute commands, inspect real measured files, accept a real
archive, promote field evidence, run field FWI, or launch field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/249_gssi51600s_controlled_archive_real_return_command_plan_validator
```

Key artifacts:

```text
data/field_controlled_archive_real_return_command_plan_validator_checks.csv
data/field_controlled_archive_real_return_command_plan_validator_summary.json
figures/field_controlled_archive_real_return_command_plan_validator.png
docs/FIELD_CONTROLLED_ARCHIVE_REAL_RETURN_COMMAND_PLAN_VALIDATOR.md
scripts/run_gssi_field_controlled_archive_real_return_command_plan_validator.py
scripts/test_gssi_field_controlled_archive_real_return_command_plan_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  6
validation checks passed:           6
blocking failures:                  0
command-plan validation ready:      true
command plan ready:                 true
commands executed:                  false
real files present:                 false
ready for real archive acceptance:  false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The six checks confirm source readiness, command partition counts, current
guard command executability, future real-archive gate blocking, summary/table
count consistency, and blocked archive/downstream states.

## Interpretation

The saved real-return command plan is internally consistent and keeps the
real-archive boundary intact. It is now consumer-validated, but not yet
stress-tested against damaged command-plan variants.

## Decision

Use runs `248`-`249` as the consumer-validated command checklist for real-return
archive acceptance. Sensitivity remains required before treating the checklist
as fully guarded.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_archive_real_return_command_plan_validator.py
6 passed
```

Figure validation:

```text
2627x814, dynamic range=255
```
