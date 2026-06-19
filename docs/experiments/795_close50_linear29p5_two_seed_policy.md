# Experiment 795: Close50 Linear 29.5 mm Two-Seed Policy

Date: 2026-06-17

## Purpose

CPU-only synthesis of the two close50 target2 linear receiver runs at 29.5 mm:

```text
seed21: outputs/experiments/1271_coordinate_optimizer_close50_seed21_sources4_txrx29p5_linear_receiver_objectives
seed13: outputs/experiments/1272_coordinate_optimizer_close50_seed13_sources4_txrx29p5_linear_receiver_objectives
```

This run did not launch FDTD, FWI, or GPU kernels. It reads the optimizer
summaries and objective diagnostics to decide whether the linear 29.5 mm point
can be called clean-replicated.

## Output

```text
outputs/experiments/1273_close50_linear_receiver_policy
```

Artifacts:

```text
data/close50_linear_receiver_policy_summary.json
data/close50_linear_receiver_run_rows.csv
data/close50_linear_receiver_confidence_rows.csv
data/close50_linear_receiver_objective_diagnostics.csv
data/figure_validation.csv
figures/close50_linear_receiver_policy.png
run_manifest.json
```

## Result

Policy label:

```text
close50_linear29p5_two_seed_exact_strong_not_clean_replicated
```

Aggregate counts:

| Metric | Value |
| --- | ---: |
| seed count | 2 |
| confidence rows | 4 |
| truth geometry rows | 4 |
| strong-confidence rows | 4 |
| strict clean rows | 3 |
| x-ambiguity rows | 1 |
| radius-ambiguity rows | 0 |
| min primary radius margin | 1.4692e-03 |
| highband truth rows | 4 / 4 |
| min highband margin | 5.9946e-04 |

Per-seed policy rows:

| Seed | Result |
| --- | --- |
| seed21 | `single_seed_clean` |
| seed13 | `single_seed_exact_strong_x_ambiguous` |

## Interpretation

Linear receiver sampling at 29.5 mm improves on the nearest-sampled effective
29 mm branch and is exact/strong across the two tested seeds. It still should
not be reported as a clean replicated below-30 mm threshold because the nominal
seed13 row retains a one-grid-cell x ambiguity at 300-301 mm.

The nearest-sampled paper-safe threshold remains:

```text
close50 target2 sources4: first clean replicated nearest-sampled Tx/Rx offset is 30 mm.
```

The linear-sampled statement is narrower:

```text
close50 target2 sources4 linear 29.5 mm: exact/strong across seeds 21 and 13,
but not clean-replicated under the no-x-ambiguity rule.
```

Useful next GPU work should answer one specific question. A seed34 linear 29.5
run estimates ambiguity frequency, while a seed13 linear 29.75 mm bracket tests
where the known seed13 x ambiguity clears. Do not run both as an unfocused
sweep.

## Validation

Focused tests:

```text
tests/test_close50_linear_receiver_policy.py: 4 passed
```

Figure validation:

```text
close50_linear_receiver_policy.png: 2263x835, nonwhite=0.3659, dynamic range=255
```
