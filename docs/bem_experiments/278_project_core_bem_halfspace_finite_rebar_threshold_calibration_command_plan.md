# BEM Experiment 278: Half-Space Finite-Rebar Threshold Calibration Command Plan

Date: 2026-06-28

## Purpose

Convert the guarded threshold-calibration intake boundary from run `277` into a
non-executed command checklist for the first real paired BEM/FDTD calibration
path.

This run answers a practical execution question:

```text
Which BEM threshold-calibration commands can run now, and which commands must
wait for real paired BEM/FDTD data?
```

This run does not ingest real FDTD traces, run a real BEM/FDTD comparison, set
thresholds, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/278_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_COMMAND_PLAN.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source boundary guarded:                true
commands:                               7
current guard commands:                 3
future real-pair commands:              4
executable now:                         3
requires real trace root:               4
requires real paired comparison:        2
requires real thresholds:               1
commands executed:                      false
threshold-calibration plan ready:       true
real trace files present:               false
real FDTD frequency extraction ready:   false
real BEM/FDTD comparison ready:         false
threshold calibration ready:            false
ready for 3D validation:                false
field FWI ready:                        false
```

The seven commands are split into two groups:

| Order | Command group | Command name | Executable now | Requires real trace root | Requires real pair |
| ---: | --- | --- | ---: | ---: | ---: |
| 1 | current guard validation | threshold template pack guard tests | true | false | false |
| 2 | current guard validation | synthetic threshold fill guard tests | true | false | false |
| 3 | current guard validation | threshold intake boundary guard tests | true | false | false |
| 4 | future real pair gate | real FDTD trace root preflight | false | true | false |
| 5 | future real pair gate | real FDTD frequency extraction | false | true | false |
| 6 | future real pair gate | real paired BEM/FDTD comparison | false | true | true |
| 7 | future real pair gate | real threshold template fill and validator | false | true | true |

## Interpretation

The threshold-calibration path now has an execution checklist without pretending
that real paired data already exist. The runnable commands only recheck the
existing guards. The real trace, real comparison, and threshold-setting commands
remain blocked until the first real paired BEM/FDTD dataset is staged.

## Decision

Use run `278` as the command checklist for first-real-pair threshold
calibration. Do not set numerical thresholds or promote BEM/FDTD agreement from
synthetic support artifacts.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_command_plan.py
3 passed
```

Figure validation:

```text
2681x826, dynamic range=255
```
