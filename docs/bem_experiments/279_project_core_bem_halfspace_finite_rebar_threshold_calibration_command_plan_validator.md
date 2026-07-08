# BEM Experiment 279: Half-Space Finite-Rebar Threshold Calibration Command Plan Validator

Date: 2026-06-28

## Purpose

Validate the run `278` threshold-calibration command plan from saved artifacts.

This run verifies that the command checklist preserves the current real-data
boundary: guard commands are runnable now, while real trace, real comparison,
and threshold-setting commands remain blocked until real paired BEM/FDTD data
exist.

This run does not execute commands, ingest real FDTD traces, run a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/279_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator_checks.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_COMMAND_PLAN_VALIDATOR.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                       6
validation checks passed:                6
blocking failures:                       0
command-plan validation ready:           true
command plan ready:                      true
commands executed:                       false
threshold calibration ready:             false
real BEM/FDTD comparison ready:          false
ready for 3D validation:                 false
field transfer ready:                    false
ready for GPU work:                      false
field FWI ready:                         false
```

The six checks confirm source readiness, command partition counts, current
guard command executability, future real-pair gate blocking, summary/table
count consistency, and blocked real-comparison/downstream states.

## Interpretation

The saved threshold-calibration command plan is internally consistent and keeps
the real-data boundary intact. It is now consumer-validated, but not yet
stress-tested against damaged command-plan variants.

## Decision

Use runs `278`-`279` as the consumer-validated command checklist for
first-real-pair threshold calibration. Sensitivity remains required before
treating the checklist as fully guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_validator.py
6 passed
```

Figure validation:

```text
2717x814, dynamic range=255
```
