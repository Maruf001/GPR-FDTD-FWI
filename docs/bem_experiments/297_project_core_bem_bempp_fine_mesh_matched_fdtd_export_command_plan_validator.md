# BEM Experiment 297: Bempp Fine-Mesh Matched FDTD Export Command Plan Validator

Date: 2026-06-28

## Purpose

Validate the saved run `296` non-executed command plan from output artifacts.

This run checks the command counts, current guard commands, future real-export
gates, no-execution state, blocked downstream readiness, figure validation, and
script snapshots.

It does not execute commands, run FDTD, ingest real FDTD traces, compute a real
BEM/FDTD comparison, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/297_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator_checks.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator.png
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                            7
passed checks:                    7
failed checks:                    0
validation ready:                 true
source command plan ready:        true
commands:                         7
current guard commands:           3
future FDTD export commands:      2
future comparison commands:       1
future threshold commands:        1
commands executed:                false
real BEM/FDTD comparison ready:   false
threshold calibration ready:      false
GPU/HPC ready:                    false
field FWI ready:                  false
```

## Interpretation

The saved run `296` command plan is internally consistent: current guard
commands are executable, future export/comparison/threshold commands are
real-export gated, no commands have been executed, and downstream states remain
blocked.

## Decision

Use runs `296-297` as the validated non-executed command plan. Sensitivity
testing remains required before treating the command-plan validator as guarded.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_validator.py
3 passed
```

Figure validation:

```text
2933x886, dynamic range=255
```
