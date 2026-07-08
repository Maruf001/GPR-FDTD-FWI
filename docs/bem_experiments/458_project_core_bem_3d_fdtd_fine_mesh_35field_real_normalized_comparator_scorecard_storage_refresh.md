# BEM Experiment 458: Real Normalized-Comparator Scorecard Storage Refresh

Date: 2026-06-29

## Purpose

Refresh the non-evidence real-return scorecard template from run `440` with
the reference-coefficient storage rule from runs `452-454`.

This is a template and storage-format run. It does not run BEM, FDTD, GPU/HPC,
3D validation, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/458_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_scorecard_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_acceptance_rule_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source template ready:                         true
source serialization ready:                    true
scorecard storage refresh ready:               true
scorecard rows:                                279
receivers:                                     31
frequencies:                                   9
reference coefficient:                         0.01907878402833891
serialized reference coefficient:              0.019078784028338909
relative tolerance:                            1e-12
recommended storage significant digits:        17
minimum safe scorecard significant digits:     13
preferred-storage rows:                        279
minimum-safe-digit rows:                       279
required real input cells:                     1116
filled real input cells:                       0
generated score cells:                         1116
filled generated score cells:                  0
template rows currently evidence:              0
real BEM/FDTD comparison ready:                false
3D validation ready:                           false
GPU/HPC ready:                                 false
field FWI ready:                               false
```

The refresh converts the earlier display value into the preferred
17-significant-digit serialized text used by the storage guard. The scorecard
remains a blank return template, not comparison evidence.

## Decision

Use this as the storage-refreshed non-evidence scorecard template for future
real returned BEM/FDTD values and source hashes.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_storage_refresh.py
4 passed
```

Figure check:

```text
3221x883, dynamic range=255
```
