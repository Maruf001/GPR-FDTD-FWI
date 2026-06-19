# Experiment 823: Synthetic 2D Next-Question Matrix After Publication Bundle Refresh

Date: 2026-06-18

## Purpose

Refresh the synthetic 2D next-question matrix after run 1309 made the
paper-facing publication bundle current. This is a CPU-only reporting synthesis
over existing outputs; it does not launch FDTD, FWI, GPU kernels, or new
inversion experiments.

## Output

```text
outputs/experiments/1310_synthetic_2d_next_question_matrix_post_publication_bundle_refresh
```

Artifacts:

```text
data/synthetic_2d_next_question_matrix_rows.csv
data/synthetic_2d_next_question_matrix_summary.json
data/figure_validation.csv
figures/synthetic_2d_next_question_matrix.png
run_manifest.json
```

## Result

Policy label:

```text
synthetic_2d_next_question_matrix_cpu_first_no_gpu
```

Summary:

```text
candidate count:                 8
cpu-first count:                 0
immediate GPU-priority count:    0
conditional GPU candidates:      0
top question:                    synthetic_publication_bundle_current
top readiness:                   no_gpu_required
gpu priority:                    none_now
```

The top action is to use the refreshed synthetic paper bundle and its
claim-boundary CSV. No GPU work follows from this completed reporting endpoint.

## Interpretation

Run 1310 supersedes run 1306 as the current local synthetic next-question
endpoint. The matrix now recognizes that run 1309 already includes the current
resolution claim map and close50 legacy midpoint refresh.

Under the already-posed local 2D questions, there are no CPU-first or
conditional GPU candidates left. Future synthetic GPU work should start from a
new objective, geometry, acquisition question, or deliberately narrow exception
probe rather than from broad reruns of the current tracker family.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
9 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1429, dynamic range=255
```
