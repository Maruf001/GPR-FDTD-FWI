# Experiment 826: Synthetic 2D Next-Question Matrix After Target1 Surface

Date: 2026-06-18

## Purpose

Refresh the CPU-only synthetic 2D next-question matrix after the target1
acquisition-confidence surface. This keeps the current local 2D decision
endpoint aware that target1 remains a confidence-policy/acquisition-design
result, not a closed GPU queue item.

## Output

```text
outputs/experiments/1313_synthetic_2d_next_question_matrix_post_target1_surface_refresh
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
candidate rows:                         9
cpu-first candidates:                   0
conditional GPU candidates:             0
target1 acquisition surface included:   true
top question:                           synthetic_publication_bundle_current
top readiness:                          no_gpu_required
gpu priority:                           none_now
```

Target1 row:

```text
run:               1312_target1_acquisition_confidence_surface
rows:              133
exact rows:        133
weak-exact rows:    43
late_high:         132 / 133
escalation helped:  10 branches
lower best:          7 branches
```

## Interpretation

The synthetic 2D decision endpoint remains no-GPU under the current local
questions. The target1 acquisition-confidence surface is now represented in the
matrix: exact geometry is stable, but source-density behavior is nonmonotonic,
so a broad target1 GPU sweep is not justified. Future synthetic GPU work needs
a new objective, geometry, acquisition hypothesis, or narrow exception probe.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
10 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903, dynamic range=255
```
