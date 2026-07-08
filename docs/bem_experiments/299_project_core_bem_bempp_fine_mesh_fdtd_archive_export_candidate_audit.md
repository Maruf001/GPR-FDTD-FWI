# BEM Experiment 299: Bempp Fine-Mesh FDTD Archive Export Candidate Audit

Date: 2026-06-28

## Purpose

Audit the existing 2D FDTD archive for files that could feed the guarded
matched BEM/FDTD export contract from run `293`.

This run distinguishes strict target/background frequency-export files from
time-domain B-scan files that may be convertible only after a dedicated export
adapter is written.

It does not run FDTD, create new target/background frequency exports, run the
BEM/FDTD comparator, set thresholds, launch GPU/HPC work, transfer to field
evidence, or run field FWI.

## Output

```text
outputs/bem_experiments/299_project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit
```

Key artifacts:

```text
data/project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_rows.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_class_counts.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_top_convertible.csv
data/project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit_summary.json
data/figure_validation.csv
figures/project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit.png
docs/PROJECT_CORE_BEM_BEMPP_FINE_MESH_FDTD_ARCHIVE_EXPORT_CANDIDATE_AUDIT.md
scripts/run_project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit.py
scripts/test_project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scanned files:                         4513
CSV files:                             4423
NPZ files:                               90
strict fine-mesh export candidates:       0
legacy 3D frequency-bin candidates:       0
convertible B-scan trace files:          80
experiments with convertible traces:     76
strict target export candidates:          0
strict background export candidates:      0
strict target/background pair ready:  false
new FDTD export adapter required:     true
real BEM/FDTD comparison ready:       false
threshold calibration ready:          false
3D validation claim ready:            false
GPU/HPC ready:                        false
field FWI ready:                      false
```

The archive is mostly optimizer and detector tables:

| Artifact class | Files |
| --- | ---: |
| optimizer_or_detector_table | 3874 |
| other_csv | 549 |
| time_domain_bscan_convertible_candidate | 80 |
| other_npz | 10 |

## Interpretation

The existing 2D archive contains time-domain B-scan files that may be useful as
raw material, but it does not contain a strict target/background FDTD
frequency-export pair matching the run `293` Bempp fine-mesh schema.

The best available raw candidates are detector B-scan NPZ files containing
`time`, `scan_x`, and B-scan arrays. Those are not enough by themselves because
the guarded BEM/FDTD comparison requires paired target and background frequency
rows with a locked source convention, receiver convention, frequency grid, and
schema.

## Decision

Do not run the real BEM/FDTD comparator from the archive as-is. The next useful
step is a dedicated FDTD frequency-export adapter that converts a selected 2D
time-domain case into target and background rows with the run `293` schema,
source lock, receiver lock, and frequency grid.

## Validation

Focused test:

```text
tests/test_project_core_bem_bempp_fine_mesh_fdtd_archive_export_candidate_audit.py
4 passed
```

Figure validation:

```text
3941x895, dynamic range=255
```
