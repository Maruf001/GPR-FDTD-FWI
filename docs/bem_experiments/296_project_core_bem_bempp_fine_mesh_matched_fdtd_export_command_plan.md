# BEM Experiment 296: Bempp Fine-Mesh Matched FDTD Export Command Plan

Date: 2026-06-28

## Purpose

Create a non-executed command plan for the guarded matched BEM/FDTD export
contract from runs `293-295`.

This plan separates commands that can run now as guard checks from future
commands that require real target/background FDTD frequency exports, paired
residual rows, and threshold calibration inputs.

It does not execute commands, run FDTD, ingest real FDTD traces, compute a real
BEM/FDTD comparison, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/296_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_rows.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_MATCHED_FDTD_EXPORT_COMMAND_PLAN.md
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands:                         7
current guard commands:           3
future FDTD export commands:      2
future comparison commands:       1
future threshold commands:        1
executable now:                   3
requires target FDTD export:      3
requires background FDTD export:  3
requires real comparison:         2
commands executed:                false
command plan ready:               true
real BEM/FDTD comparison ready:   false
threshold calibration ready:      false
GPU/HPC ready:                    false
field FWI ready:                  false
```

## Interpretation

The guarded matched-export contract now has a command plan: three current guard
commands can run now, while target/background FDTD export, paired residual, and
threshold commands remain future-gated by real exports.

## Decision

Use run `296` as the non-executed command plan for the first matched BEM/FDTD
export path. Do not execute future export/comparison/threshold commands until
real target and background FDTD exports are staged.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan.py
3 passed
```

Figure validation:

```text
2681x844, dynamic range=255
```
