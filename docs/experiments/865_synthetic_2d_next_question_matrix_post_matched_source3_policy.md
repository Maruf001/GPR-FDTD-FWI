# Experiment 865: Synthetic 2D Next-Question Matrix Post Matched Source3 Policy

Date: 2026-06-19

## Purpose

Refresh the synthetic 2D next-question matrix after the matched-source3 policy
synthesis in summary table `121`.

This is CPU-only synthetic planning. It does not run FDTD/FWI, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/experiments/1356_synthetic_2d_next_question_matrix_post_matched_source3_policy
```

Key artifacts:

```text
data/synthetic_2d_next_question_matrix_rows.csv
data/synthetic_2d_next_question_matrix_summary.json
figures/synthetic_2d_next_question_matrix.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate count:                      11
cpu-first count:                      0
immediate GPU-priority count:         0
conditional GPU candidates:           0
target1 acquisition surface included: true
target1 exception map included:       true
matched-source3 policy included:      true
top question:                         synthetic_publication_bundle_current
top readiness:                        no_gpu_required
gpu priority:                         none_now
```

The matched-source3 row is now closed:

```text
close14 truth fraction:        1.0
close50 truth fraction:        0.0
close50 wrong branch:          true
spacing-only causal claim:     false
recommended action:            use as guarded acquisition/geometry contrast
```

## Interpretation

The synthetic matrix exposes no immediate or conditional GPU candidate under
the current 2D hypotheses. The next work is manuscript synthesis and claim
discipline unless a new objective, geometry, or acquisition question is defined.

The old close50 270/280 family remains a claim caveat, not a default rerun
branch. Target1 source-density work remains closed under the current
hypothesis. The completed matched-source3 queue should be written as a guarded
acquisition/geometry contrast, not as spacing-only causal proof.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py
13 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1573, dynamic range=255
```
