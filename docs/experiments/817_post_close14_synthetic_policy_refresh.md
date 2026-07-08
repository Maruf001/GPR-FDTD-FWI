# Experiment 817: Post-Close14 Synthetic Policy Refresh

Date: 2026-06-18

## Purpose

CPU-only policy refresh after experiment 816 completed the target2 close14
source5 / Tx/Rx=45 mm three-seed probe.

This refresh moves the completed close14 probe out of the launch queue and into
the synthetic manuscript claim-boundary table. No FDTD, FWI, GPU kernels, or
new inversion experiments were launched.

## Output

```text
outputs/experiments/1298_synthetic_2d_next_question_matrix_post_close14_probe
outputs/experiments/1299_synthetic_2d_publication_claim_boundary_refresh_post_close14_probe
```

Key artifacts:

```text
1298/data/synthetic_2d_next_question_matrix_summary.json
1298/data/synthetic_2d_next_question_matrix_rows.csv
1298/figures/synthetic_2d_next_question_matrix.png
1299/data/synthetic_2d_publication_claim_boundary_refresh_summary.json
1299/data/synthetic_2d_publication_claim_boundaries_refreshed.csv
1299/figures/synthetic_2d_publication_claim_boundary_refresh.png
```

## Result

Run 1298 policy:

```text
synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate count:                 8
top question:                    post_close14_claim_boundary_refresh
immediate GPU-priority count:    0
conditional GPU candidates:      1
gpu priority:                    none_now
```

Run 1299 policy:

```text
synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu
claim boundary count:             8
close14 probe included:           true
close14 0.5x near-tie count:      6
ready for manuscript claim table: true
gpu priority:                     none
```

## Interpretation

The close14 source5 / Tx/Rx=45 mm question is no longer a pending GPU action.
The current paper-facing interpretation is:

```text
Target2 close14 selects truth with strong radius confidence across the
three-seed probe, but the +1 mm lateral competitor remains inside the strict
0.5x ambiguity gate in every row. Report this as a robust objective-uniqueness
limit, not as clean lateral resolution.
```

Future synthetic GPU work should require a new objective, geometry, acquisition
question, or explicitly different manuscript need.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
tests/test_synthetic_2d_publication_claim_boundary_refresh.py
9 passed
```

Figure validation:

```text
1298 synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1544, dynamic range=255

1299 synthetic_2d_publication_claim_boundary_refresh.png: 2127x835,
nonwhite=0.5331, dynamic range=255
```
