# BEM Experiment 318: Receiver Operator Holdout Execution Command Plan

Date: 2026-06-28

## Purpose

Turn the guarded holdout design packet from runs `315-317` into an ordered,
non-executed command plan.

This run uses saved artifacts only. It does not run Bempp, FDTD, GPU/HPC,
field transfer, field FWI, or 3D validation.

## Output

```text
outputs/bem_experiments/318_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_commands.sh
data/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_RECEIVER_OPERATOR_HOLDOUT_EXECUTION_COMMAND_PLAN.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan.py
scripts/script_snapshot_manifest.json
```

## Result

```text
required artifacts:                 9
command phases:                     7
commands executing now:             0
commands requiring GPU/HPC now:     0
independent pair required:          true
apply without refit required:       true
command plan ready:                 true
holdout data present:               false
receiver operator holdout ready:    false
physical claim ready:               false
real BEM/FDTD comparison ready:     false
3D validation claim ready:          false
field transfer ready:               false
GPU/HPC ready:                      false
field FWI ready:                    false
```

Command phases:

| Phase | Produces |
| ---: | --- |
| 1 | holdout pair metadata |
| 2 | three BEM holdout reference exports |
| 3 | FDTD target frequency rows |
| 4 | FDTD background frequency rows |
| 5 | derived FDTD scattered rows |
| 6 | no-refit receiver-operator apply-only rows |
| 7 | holdout operator validation summary |

## Interpretation

The independent receiver-operator holdout now has an ordered command plan, but
every command is non-executed. The plan preserves the key rule that frozen
run `311` operators must be applied to a new holdout without refitting.

## Decision

Use run `318` as the BEM holdout execution plan. Do not execute or promote the
holdout branch until an independent pair id and geometry are selected and
reviewed.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_receiver_operator_holdout_execution_command_plan.py
3 passed
```

Figure validation:

```text
3005x933, dynamic range=255
```
