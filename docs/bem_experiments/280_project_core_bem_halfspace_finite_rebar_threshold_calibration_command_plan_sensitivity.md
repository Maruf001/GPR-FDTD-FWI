# BEM Experiment 280: Half-Space Finite-Rebar Threshold Calibration Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `279` threshold-calibration command-plan validator.

This run verifies that the validator accepts the exact run `278` command plan
and rejects controlled damage to command rows, summary counts, command
execution state, and false real/downstream readiness.

This run does not execute commands, ingest real FDTD traces, run a real BEM/FDTD
comparison, set thresholds, launch GPU/HPC work, run 3D validation, or run field
FWI.

## Output

```text
outputs/bem_experiments/280_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity_scenarios.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_COMMAND_PLAN_SENSITIVITY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                            32
expected pass scenarios:              1
observed pass scenarios:              1
expected failure scenarios:           31
observed failure scenarios:           31
unexpected outcomes:                  0
sensitivity ready:                    true
command plan ready:                   true
commands executed:                    false
threshold calibration ready:          false
real BEM/FDTD comparison ready:       false
ready for 3D validation:              false
field transfer ready:                 false
ready for GPU work:                   false
field FWI ready:                      false
```

The exact run `278` command plan passes. All 31 damaged variants fail as
expected for command-row drift, command-order drift, command-group drift,
current guard executability drift, future gate blocking drift, summary-count
drift, command-execution promotion, real-trace promotion, real-comparison
promotion, threshold promotion, and false 3D/field/GPU/FWI readiness.

## Interpretation

The first-real-pair BEM threshold-calibration command checklist is now guarded.
The current guard commands can be used to recheck the support package, but real
trace, real comparison, and threshold-setting commands remain blocked until
real paired BEM/FDTD data are staged.

## Decision

Use runs `278`-`280` as the guarded first-real-pair threshold-calibration
command checklist. Real paired BEM/FDTD data remain required before calibration,
BEM/FDTD agreement, 3D validation, inversion-scale claims, field transfer, GPU
work, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_sensitivity.py
6 passed
```

Figure validation:

```text
4301x879, dynamic range=255
```
