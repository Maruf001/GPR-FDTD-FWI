# Experiment 864: Local 2D Manuscript Contribution Matrix Post Matched Source3 Policy

Date: 2026-06-19

## Purpose

Refresh the local 2D manuscript contribution matrix after summary table `121`
added the completed matched-source3 claim boundary.

This is CPU-only manuscript synthesis. It does not run FDTD/FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/122_local_2d_manuscript_contribution_matrix_post_matched_source3_policy
```

Key artifacts:

```text
data/local_2d_manuscript_contribution_rows.csv
data/local_2d_manuscript_contribution_summary.json
figures/local_2d_manuscript_contribution_matrix.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_manuscript_contribution_matrix_ready_no_gpu
contribution rows:                    11
ready rows:                           10
deferred rows:                        1
review rows:                          0
synthetic immediate GPU candidates:   0
synthetic conditional GPU candidates: 0
field ready for 2D QC:                true
field ready for FWI:                  false
field ready for 3D/HPC:               false
gpu priority:                         none
ready for manuscript positioning:     true
```

New contribution row:

```text
key:              matched_source3_acquisition_geometry_contrast
role:             acquisition_result
readiness:        ready
readiness score:  0.9
evidence:         close14 truth fraction=1.0;
                  close50 truth fraction=0.0;
                  close50 wrong branch=true;
                  spacing-only=false
next action:      use summary table 121 as the manuscript source-density claim gate
gpu priority:     none
```

## Interpretation

The manuscript-planning matrix now carries the matched-source3 result as an
acquisition/geometry contrast, not as spacing-only proof. The overall paper
position remains ready for drafting: controlled synthetic 2D identifiability
and ambiguity-margin evidence, with measured field data used only as scoped 2D
QC and collection-planning support.

No immediate or conditional GPU queue is exposed by this matrix.

## Validation

Focused tests:

```text
tests/test_local_2d_manuscript_contribution_matrix.py
3 passed
```

Figure validation:

```text
local_2d_manuscript_contribution_matrix.png: 2739x1379,
nonwhite=0.2622, dynamic range=255
```
