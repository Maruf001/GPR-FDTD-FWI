# BEM Experiment 320: Receiver Operator Holdout Execution Command Plan Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `319` validator for the saved run `318` receiver-operator
holdout execution command plan.

This is an artifact-only sensitivity run. It mutates saved command-plan rows,
summary values, figure metadata, script snapshots, and command-script text in
memory. It does not run Bempp, FDTD, GPU/HPC, field transfer, field FWI, or 3D
validation.

## Output

```text
outputs/bem_experiments/320_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity_scenarios.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_EXECUTION_COMMAND_PLAN_SENSITIVITY.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                         16
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        15
observed failure scenarios:        15
unexpected outcomes:               0
sensitivity ready:                 true
exact run 318 accepted:            true
damaged variants rejected:         true
holdout data present:              false
receiver operator holdout ready:   false
physical claim ready:              false
real BEM/FDTD comparison ready:    false
3D validation claim ready:         false
field transfer ready:              false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The damaged variants cover source-count drift, phase drift, no-refit contract
drift, accidental execution, GPU/HPC requirement drift, command-script drift,
downstream promotion, figure drift, and script-snapshot drift.

## Interpretation

The receiver-operator holdout command plan is now guarded as a non-executed
future work plan. The exact run `318` no-refit plan passes, while every damaged
variant fails as expected.

This does not promote the receiver-operator shortcut. It only preserves the
contract for a future independent holdout: define new geometry/data, export the
BEM and FDTD traces, apply the frozen operator without refitting, then validate.

## Decision

Use runs `318-320` as the guarded non-executed BEM receiver-operator holdout
command-plan block. Do not promote the receiver-operator shortcut until
independent holdout artifacts exist and pass the no-refit validation plan.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_sensitivity.py
3 passed
```

Figure validation:

```text
3437x891, dynamic range=255
```
