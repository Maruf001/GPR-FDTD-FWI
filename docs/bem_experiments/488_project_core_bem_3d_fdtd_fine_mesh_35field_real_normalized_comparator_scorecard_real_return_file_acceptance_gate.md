# BEM Experiment 488: Real Return-File Acceptance Gate

Date: 2026-06-29

## Purpose

Define the pass/fail gate for replacing the synthetic return-file smoke with
real returned BEM/FDTD files.

## Output

```text
outputs/bem_experiments/488_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_file_gate_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_entry_gate_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_scorecard_gate_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
acceptance gate ready:                       true
required real return files:                  4
accepted real return files:                  0
required real entries:                       1116
accepted real entries:                       0
required real scorecard rows:                279
accepted real scorecard rows:                0
source-hash requirements:                    558
scattered-norm requirements:                 558
receiver count:                              31
frequency count:                             9
real return packet accepted:                 false
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

## Interpretation

The gate is now explicit. Four real return files must replace the synthetic
files, all 1116 real entries must be accepted, and all 279 scorecard rows must
be accepted before any real BEM/FDTD comparison can be promoted.

## Decision

Use this gate as the real-file replacement contract. The current packet has no
accepted real files or values.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_file_acceptance_gate.py
4 passed
```

Figure check:

```text
2825x842, dynamic range=255
```
