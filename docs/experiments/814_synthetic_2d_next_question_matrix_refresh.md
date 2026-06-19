# Experiment 814: Synthetic 2D Next-Question Matrix Refresh

Date: 2026-06-17

## Purpose

CPU-only refresh of the synthetic 2D next-question matrix after experiments
811-813 identified the actionable objective-uniqueness gap as target2 close14
source5 / Tx/Rx=45 mm, not target1 archive rows or close50 reruns.

This run does not launch FDTD, FWI, GPU kernels, or new inversion experiments.

## Output

```text
outputs/experiments/1292_synthetic_2d_next_question_matrix
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
candidate count:                   8
cpu-first count:                   1
immediate GPU-priority count:      0
conditional GPU candidates:        2
top question:                      target2_close14_source5_threshold_gate
top question GPU readiness:        cpu_first
gpu priority:                      none_now
```

Top recommended action:

```text
Define the exact narrow target2 close14 source5/TxRx45 probe contract and
manuscript decision rule before any GPU run.
```

## Interpretation

The next synthetic work remains CPU-first. A new GPU run is not justified until
there is a fixed probe contract and decision rule. If that later happens, the
candidate should be narrow: target2, close14, source5, Tx/Rx=45 mm, fixed
threshold decision, skip-existing. Broad close50 reruns, target1 archive
reruns, and target0 exception extensions are not current priorities.

## Validation

Focused tests:

```text
tests/test_synthetic_2d_next_question_matrix.py: 3 passed
```

Figure validation:

```text
synthetic_2d_next_question_matrix.png: 2501x903,
nonwhite=0.1736, dynamic range=255
```
