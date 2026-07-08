# BEM Experiment 470: 35-Field Scorecard Return Staging Plan

Date: 2026-06-29

## Purpose

Convert the 1116-cell scorecard intake worksheet from run `464` into an
ordered return and dependency plan.

## Output

```text
outputs/bem_experiments/470_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_stage_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_action_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_dependency_edges.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source worksheet ready:                      true
source claim boundary ready:                 true
return staging plan ready:                   true
worksheet rows:                              279
required real-return cells:                  1116
stage actions:                               6
cell-stage groups:                           4
dependency edges:                            7
filled real-return cells:                    0
missing real-return cells:                   1116
source-hash stage cells:                     558
scattered-norm stage cells:                  558
computed comparator rows:                    279
evidence-review rows:                        279
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The plan groups the worksheet into four real-return intake stages: FDTD source
hashes, BEM source hashes, FDTD scattered norms, and BEM scattered norms. Those
stages feed computed normalized-comparator rows and then evidence review.

## Decision

Use this as the staging plan for future real 35-field scorecard returns. The
plan is ready, but real comparison and downstream work remain blocked until
values are returned.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_staging_plan.py
4 passed
```

Figure check:

```text
2933x927, dynamic range=255
```
