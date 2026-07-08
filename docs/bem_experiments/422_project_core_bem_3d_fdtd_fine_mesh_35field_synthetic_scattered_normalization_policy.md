# BEM Experiment 422: 35-Field Synthetic Scattered Normalization Policy

Date: 2026-06-29

## Purpose

Derive a comparison-normalization policy from the guarded 35-field synthetic
scattered table.

This is a policy and metric-design run. It does not create measured evidence,
run a real BEM/FDTD comparison, launch GPU/HPC work, run 3D validation, or run
field FWI.

## Output

```text
outputs/bem_experiments/422_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_normalization_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_axis_summary.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_policy_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy.png
```

## Result

```text
normalization policy ready:        true
scattered rows:                    279
receiver count:                    31
frequency count:                   9
axis summary rows:                 40
raw norm span ratio:               232.50000000000006
raw frequency mean monotonic:      true
raw receiver mean monotonic:       true
normalized coefficient mean:       0.01907878402833891
normalized coefficient std:        3.984575489992671e-18
normalized coefficient cv:         2.0884850334665626e-16
normalized coefficient range:      1.0408340855860843e-17
normalization collapses scaling:   true
synthetic packet is evidence:      false
real comparison ready:             false
3D validation ready:               false
GPU/HPC ready:                     false
field FWI ready:                   false
```

The raw synthetic scattered norm spans `232.5x` across the receiver-frequency
grid. Dividing each row by frequency in GHz and receiver index plus one
collapses the synthetic scale to a nearly constant coefficient.

## Decision

Use this as a comparison-policy guard for future real BEM/FDTD return packets.
Carry raw scattered norm for diagnostics, but do not treat it as calibrated
evidence without the normalized metric and real returned FDTD files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_synthetic_scattered_normalization_policy.py
4 passed
```

Figure check:

```text
3941x889, dynamic range=255
```
