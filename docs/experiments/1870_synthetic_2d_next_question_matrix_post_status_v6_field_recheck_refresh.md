# 1870 Synthetic 2D Next Question Matrix Post Status-V6 Field Recheck Refresh

Date: 2026-07-02

## Purpose

Refresh the synthetic 2D next-question matrix after the post-status-v6 field
live-receipt recheck, using existing archive evidence only. No GPU, FDTD,
BEM/FDTD comparison, field transfer, or 3D/HPC work is launched.

## Result

```text
candidate questions:                   10
top question:                           synthetic_publication_bundle_current
top question readiness:                 no_gpu_required
immediate GPU candidates:               0
conditional GPU candidates:             0
open immediate GPU rows:                0
target1 acquisition surface included:   True
target1 exception map included:         True
matched source3 policy included:        False
GPU priority:                           none_now
```

## Decision

Use the refreshed synthetic paper-facing bundle and claim-boundary CSV as the
current synthetic 2D endpoint. No immediate or broad GPU run is justified;
future synthetic compute needs a new objective, geometry, or acquisition
question.

## Artifacts

```text
outputs/experiments/1870_synthetic_2d_next_question_matrix_post_status_v6_field_recheck_refresh
outputs/experiments/1870_synthetic_2d_next_question_matrix_post_status_v6_field_recheck_refresh/data/synthetic_2d_next_question_matrix_rows.csv
outputs/experiments/1870_synthetic_2d_next_question_matrix_post_status_v6_field_recheck_refresh/data/synthetic_2d_next_question_matrix_summary.json
outputs/experiments/1870_synthetic_2d_next_question_matrix_post_status_v6_field_recheck_refresh/figures/synthetic_2d_next_question_matrix.png
```
