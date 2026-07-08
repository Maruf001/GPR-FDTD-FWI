# BEM Experiment 281: Half-Space Finite-Rebar Threshold Calibration Current Guard Execution Smoke

Date: 2026-06-28

## Purpose

Execute only the current guard-validation commands from the guarded run `278`
threshold-calibration command checklist.

This run does not execute future real-pair commands, ingest real FDTD traces,
run a real BEM/FDTD comparison, set thresholds, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/281_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_CURRENT_GUARD_EXECUTION_SMOKE.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_smoke.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source sensitivity guarded:           true
executable guard commands:            3
executed commands:                    3
passed commands:                      3
failed commands:                      0
current guard execution smoke ready:  true
future real-pair commands executed:   false
real trace files present:             false
real BEM/FDTD comparison ready:       false
threshold calibration ready:          false
field FWI ready:                      false
```

Executed guard commands:

| Command | Return code | Passed |
| --- | ---: | ---: |
| threshold template pack guard tests | 0 | true |
| synthetic threshold fill guard tests | 0 | true |
| threshold intake boundary guard tests | 0 | true |

## Interpretation

The current BEM threshold-calibration guard commands execute cleanly. Future
real-pair commands remain unexecuted and blocked because real paired BEM/FDTD
data are still missing.

## Decision

Use run `281` as the current-guard execution smoke for the first-real-pair
threshold-calibration checklist. Real paired BEM/FDTD data remain required
before calibration, BEM/FDTD agreement, 3D validation, inversion-scale claims,
field transfer, GPU work, or field FWI.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_current_guard_execution_smoke.py
4 passed
```

Executed guard commands:

```text
15 passed
16 passed
3 passed
```

Figure validation:

```text
2465x822, dynamic range=255
```
