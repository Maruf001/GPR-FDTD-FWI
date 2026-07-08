# BEM Experiment 556: Matched-FDTD Return Command Plan

Date: 2026-06-30

## Purpose

Convert the run `555` producer checklist into non-executed validation commands
for the two matched-FDTD return CSV files.

The source-hash CSV command checks that the file is nonempty, has 279 rows, and
contains lowercase SHA-256 return values. The scattered-norm CSV command checks
that the file is nonempty, has 279 rows, and contains positive finite numeric
return values.

This run does not execute the commands, create real FDTD return files, or
promote BEM/FDTD comparison evidence, 3D validation, GPU/HPC work, field
transfer, or field FWI.

## Output

```text
outputs/bem_experiments/556_project_core_bem_35field_matched_fdtd_return_command_plan
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_command_plan_command_rows.csv
data/project_core_bem_35field_matched_fdtd_return_command_plan_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_command_plan_summary.json
figures/project_core_bem_35field_matched_fdtd_return_command_plan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source checklist ready:                    true
commands:                                  2
source-hash commands:                      1
positive-float commands:                   1
required return rows:                      558
commands executed:                         0
return-file checks ready:                  0
command actions:                           3
command plan ready:                        true
GPU priority:                              none
```

## Decision

Run these commands only after both real matched-FDTD return CSV files are
produced. Then rerun row-identity, value-domain, and BEM/FDTD comparison
acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_command_plan.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
