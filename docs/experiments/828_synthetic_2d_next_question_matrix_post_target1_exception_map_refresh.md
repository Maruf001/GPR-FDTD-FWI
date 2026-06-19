# Experiment 828: Synthetic 2D Next-Question Matrix After Target1 Exception Map

Date: 2026-06-18

## Purpose

Refresh the local synthetic 2D next-question matrix after run 1314 closed the
target1 source-density exception map. This is CPU-only planning synthesis; it
does not launch FDTD, FWI, optimizer, or GPU experiments.

This tracker has now been superseded by experiment 830 / run 1321, which keeps
the same no-GPU decision boundary after the close50 28.75 mm replicated
midpoint refresh and the target1-aware publication-bundle refresh.

## Output

```text
outputs/experiments/1315_synthetic_2d_next_question_matrix_post_target1_exception_map_refresh
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
candidate rows:                     10
cpu-first candidates:                0
immediate GPU candidates:            0
conditional GPU candidates:          0
target1 acquisition surface included true
target1 exception map included       true
top question:                        synthetic_publication_bundle_current
top readiness:                       no_gpu_required
gpu priority:                        none_now
```

Top included rows:

```text
synthetic_publication_bundle_current
target1_acquisition_confidence_surface_current
synthetic_claim_boundaries_current
target1_source_density_exception_map_current
```

## Interpretation

Run 1315 keeps the local 2D decision boundary unchanged but makes it current
through run 1314. The target1 acquisition-confidence surface remains useful as
a manuscript table, and the target1 source-density exception map now closes the
source-count branch under the current hypothesis: zero modern exceptions, one
legacy ringdown025 exception, and no target1 source-count GPU rerun.

No immediate, conditional, or CPU-first synthetic GPU candidate remains in the
current matrix. Future GPU work should require a new objective, geometry, or
acquisition hypothesis.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
11 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1519, dynamic range=255
```
