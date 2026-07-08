# 1862 Synthetic 2D Next Question Matrix Post Field Live Recheck Status V4 Refresh

Date: 2026-07-02

## Purpose

Refresh the synthetic 2D next-question matrix after the field live-receipt
recheck and status packet v4, using existing archive evidence only. No GPU,
FDTD, BEM/FDTD comparison, field transfer, or 3D/HPC work is launched.

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
GPU priority:                           none_now
```

## Decision

Use the refreshed synthetic paper-facing bundle and claim-boundary CSV as the
current synthetic 2D endpoint. No immediate or broad GPU run is justified;
future synthetic compute needs a new objective, geometry, or acquisition
question.

## Artifacts

```text
outputs/experiments/1862_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh
outputs/experiments/1862_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh/data/synthetic_2d_next_question_matrix_rows.csv
outputs/experiments/1862_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh/data/synthetic_2d_next_question_matrix_summary.json
outputs/experiments/1862_synthetic_2d_next_question_matrix_post_field_live_recheck_status_v4_refresh/figures/synthetic_2d_next_question_matrix.png
```
