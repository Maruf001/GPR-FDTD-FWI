# 1874 Synthetic 2D Next Question Matrix Post Synthetic Status-V6 Field BEM Guard Refresh

Date: 2026-07-02

## Purpose

Refresh the synthetic 2D next-question matrix after the post-synthetic-status-v6
field BEM recheck and archive guard. This consumes the advertised next safe
experiment ID `1874` without launching 3D FDTD, GPU work, field transfer, or
new simulations.

## Result

```text
candidate questions:              10
top synthetic question:           synthetic_publication_bundle_current
immediate GPU candidates:         0
conditional GPU candidates:       0
open immediate GPU rows:          0
target1 acquisition surface:      included
target1 exception map:            included
matched source3 policy:           not included
gpu priority:                     none_now
```

## Decision

Use the refreshed synthetic paper bundle and its claim-boundary CSV as the
current endpoint. No immediate GPU run, 3D FDTD run, or broad synthetic sweep is
justified by this matrix; further work requires a new objective, geometry, or
acquisition question.

## Artifacts

```text
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh/data/synthetic_2d_next_question_matrix_rows.csv
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh/data/synthetic_2d_next_question_matrix_summary.json
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh/figures/synthetic_2d_next_question_matrix.png
outputs/experiments/1874_synthetic_2d_next_question_matrix_post_synthetic_status_v6_field_bem_guard_refresh/scripts/script_snapshot_manifest.json
```
