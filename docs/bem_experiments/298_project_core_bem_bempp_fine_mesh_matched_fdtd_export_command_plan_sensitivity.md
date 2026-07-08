# BEM Experiment 298: Bempp Fine-Mesh Matched FDTD Export Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `297` command-plan validator with controlled damage cases.

This run checks whether the validator accepts only the exact run `296`
non-executed command plan and rejects plausible artifact drift: missing command
rows, current guard executability drift, future real-export gate drift,
accidental command execution, summary drift, downstream promotion, figure
validation drift, and script-snapshot drift.

It does not execute commands, run FDTD, ingest real FDTD traces, compute a real
BEM/FDTD comparison, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/298_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_MATCHED_FDTD_EXPORT_COMMAND_PLAN_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          38
expected pass scenarios:             1
observed pass scenarios:             1
expected failure scenarios:          37
observed failure scenarios:          37
unexpected outcomes:                  0
sensitivity ready:                 true
exact run 296 accepted:            true
damaged variants rejected:         true
real BEM/FDTD comparison ready:    false
threshold calibration ready:       false
3D validation claim ready:         false
GPU/HPC ready:                     false
field FWI ready:                   false
```

## Interpretation

The command-plan validator accepts the exact run `296` command plan and rejects
every damaged variant. The rejected cases cover missing commands, current-guard
executability drift, future real-export gating drift, command-execution
promotion, summary drift, downstream promotion, figure-validation drift, and
script-snapshot drift.

## Decision

Use runs `296-298` as the guarded non-executed command plan for the first
matched BEM/FDTD export path. Future export, comparison, and threshold commands
remain blocked until real target/background FDTD exports and paired residual
rows are staged.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_matched_fdtd_export_command_plan_sensitivity.py
3 passed
```

Figure validation:

```text
4031x883, dynamic range=255
```
