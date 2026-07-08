# BEM Experiment 464: 35-Field Real Normalized Comparator Scorecard Intake Worksheet

Date: 2026-06-29

## Purpose

Convert the storage-refreshed 35-field normalized-comparator scorecard from run
`458` into a non-evidence intake worksheet for future real BEM/FDTD returns.

## Output

```text
outputs/bem_experiments/464_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_worksheet_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_requirement_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_acceptance_rule_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source storage refresh ready:               true
scorecard intake worksheet ready:           true
worksheet rows:                             279
receivers:                                  31
frequencies:                                9
required real-return fields per row:        4
required real-return cells:                 1116
filled real-return cells:                   0
missing real-return cells:                  1116
completed worksheet rows:                   0
comparison-ready rows:                      0
template rows currently evidence:           0
hash requirements:                          558
norm requirements:                          558
expected hash length:                       64
reference coefficient text:                 0.019078784028338909
recommended storage significant digits:     17
minimum safe scorecard significant digits:  13
preferred storage rows:                     279
real return values present:                 false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
```

The worksheet makes the next BEM handoff concrete: each of the 279
receiver-frequency rows needs two returned scattered-norm values and two
source hashes before any row can become comparison evidence.

## Decision

Use this worksheet for future real 35-field BEM/FDTD normalized-comparator
returns. Real comparison, 3D validation, GPU/HPC, field transfer, and field
FWI remain blocked until the worksheet is filled with real values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_intake_worksheet.py
4 passed
```

Figure check:

```text
2789x880, dynamic range=255
```
