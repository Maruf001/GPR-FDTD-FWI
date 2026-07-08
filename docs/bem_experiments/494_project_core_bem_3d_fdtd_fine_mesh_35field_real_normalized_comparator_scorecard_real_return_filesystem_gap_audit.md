# BEM Experiment 494: Real Return-File Filesystem Gap Audit

Date: 2026-06-29

## Purpose

Scan the BEM experiment tree for the four real return files required by the
run `488` acceptance gate.

This run distinguishes real returned files from blank templates and synthetic
reference files with the same filenames.

## Output

```text
outputs/bem_experiments/494_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_file_scan_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_candidate_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
required real return files:                  4
required real paths present:                 0
open filesystem gaps:                        4
matching filename candidates:                8
real return-file candidates:                 0
blank-template candidates:                   4
synthetic-reference candidates:              4
outside-contract candidates:                 0
accepted real files:                         0
accepted real entries:                       0
accepted real scorecard rows:                0
real BEM/FDTD comparison ready:              false
3D validation ready:                         false
GPU/HPC ready:                               false
field FWI ready:                             false
```

The eight matching filenames are non-evidence copies: four blank templates
from the return-file manifest and four synthetic reference files from the
consumer-smoke run. No `data/real_return_files/` directory currently contains
the four required real files.

## Decision

Keep the real BEM/FDTD comparison blocked until real files are returned under
the required `real_return_files` contract.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_normalized_comparator_scorecard_real_return_filesystem_gap_audit.py
4 passed
```

Figure check:

```text
3005x861, dynamic range=255
```
