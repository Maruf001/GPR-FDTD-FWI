# BEM Experiment 476: 35-Field Return-File Manifest

Date: 2026-06-29

## Purpose

Convert the staged 1116-cell real-return plan from run `470` into four concrete
file-level templates for future BEM/FDTD comparison returns.

This is a non-evidence manifest. No real BEM or FDTD values are filled.

## Output

```text
outputs/bem_experiments/476_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_file_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_template_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest_template_file_hashes.csv
data/templates/fdtd_source_hash_manifest.csv
data/templates/bem_source_hash_manifest.csv
data/templates/fdtd_scattered_norm_values.csv
data/templates/bem_scattered_norm_values.csv
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:                   true
source claim boundary ready:                 true
return-file manifest ready:                  true
required files:                              4
template files:                              4
template entries:                            1116
required real input cells:                   1116
filled template entries:                     0
missing template entries:                    1116
source-hash files:                           2
scattered-norm files:                        2
source-hash template entries:                558
scattered-norm template entries:             558
receivers:                                   31
frequencies:                                 9
worksheet rows:                              279
real return files present:                   false
real return values present:                  false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field transfer ready:                        false
field FWI ready:                             false
```

The staged return plan now has explicit file targets:

| File target | Rows | Purpose |
| --- | ---: | --- |
| `fdtd_source_hash_manifest.csv` | 279 | FDTD source-lineage hashes |
| `bem_source_hash_manifest.csv` | 279 | BEM source-lineage hashes |
| `fdtd_scattered_norm_values.csv` | 279 | FDTD scattered-field norms |
| `bem_scattered_norm_values.csv` | 279 | BEM scattered-field norms |

## Decision

Use these four templates as the required real-return file targets before any
real BEM/FDTD comparison evidence is promoted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_return_file_manifest.py
4 passed
```

Figure check:

```text
2969x873, dynamic range=255
```
