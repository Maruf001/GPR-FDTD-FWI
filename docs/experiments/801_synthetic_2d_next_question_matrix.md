# Experiment 801: Synthetic 2D Next-Question Matrix

Date: 2026-06-17

## Purpose

CPU-only ranking of candidate next synthetic 2D research questions after the
publication figure bundle. This makes the future-GPU gate explicit without
launching FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1279_synthetic_2d_next_question_matrix
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
candidate count:                  5
cpu-first count:                  1
immediate GPU-priority count:     0
conditional GPU candidates:       1
top question:                     x_ambiguity_objective_design
top question GPU readiness:       cpu_first
gpu priority:                     none_now
```

Top recommended action:

```text
Design and test an ambiguity-aware objective or reporting metric on existing
rows before any new GPU run.
```

## Interpretation

The next synthetic work should stay CPU-side. The close50 sub-30 linear branch
is exact and strong, but seed13 remains x-ambiguous at both tested offsets.
That is a better objective/reporting-design question than an immediate GPU
question.

The only conditional GPU candidate is a future seed-frequency estimate for the
sub-30 ambiguity, and only if the manuscript explicitly needs that statistic
after the objective/reporting scope is defined.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py: 2 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1985, dynamic range=255
```
