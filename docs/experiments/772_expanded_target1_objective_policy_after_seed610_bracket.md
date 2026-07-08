# Experiment 772: Expanded Target1 Objective Policy After Seed610 Bracket

Date: 2026-06-17

## Purpose

CPU-only policy update after the seed610 target1 5-source Tx/Rx bracket in
experiment 771. This folds the new Tx/Rx 50, 55, and 57.5 mm rows into the
target1 objective-policy evidence, then refreshes the cross-target objective
matrix.

No FDTD, FWI, or GPU command was run for this experiment.

## Outputs

```text
outputs/experiments/1237_coordinate_objective_diagnostic_target1_expanded_policy
outputs/experiments/1238_coordinate_objective_policy_matrix_expanded_target1
```

## Inputs

Expanded target1 objective synthesis:

```text
seed610 target1:              runs 897, 898, 899, 1224, 1234, 1235, 1236
seed5527939710754757 target1: runs 1216, 1217, 1218, 1223
```

Cross-target matrix:

```text
target0: outputs/experiments/1231_coordinate_objective_diagnostic_target0_policy
target1: outputs/experiments/1237_coordinate_objective_diagnostic_target1_expanded_policy
target2: outputs/experiments/1230_coordinate_objective_diagnostic_target2_txrx50_policy
```

## Target1 Result

The expanded target1 set has 11 rows. Every objective preserves exact rank-1
truth geometry in every row.

| Objective | Rows | Truth rows | Rows clearing `5.0e-4` | Weak rows | Mean margin | Mean ratio to base |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `base` | 11 | 11 | 0 | 11 | 4.561161e-4 | 1.0000 |
| `early_high` | 11 | 11 | 1 | 10 | 4.444366e-4 | 0.9763 |
| `highband` | 11 | 11 | 10 | 1 | 6.097422e-4 | 1.3369 |
| `late` | 11 | 11 | 10 | 1 | 6.654046e-4 | 1.4541 |
| `late_high` | 11 | 11 | 11 | 0 | 7.728177e-4 | 1.6901 |
| `veryhigh` | 11 | 11 | 9 | 2 | 5.586454e-4 | 1.2234 |

All objective-specific confidence rows report zero x/z/r ambiguity width.

## Cross-Target Policy

The refreshed matrix keeps the same target-specific recommendations:

| Target | Base accepted fraction | Full-acceptance secondary objectives | Strongest secondary objective | Mean ratio |
| --- | ---: | --- | --- | ---: |
| target0 | 0.2778 | `highband`, `veryhigh` | `highband` | 1.3327 |
| target1 | 0.0000 | `late_high` | `late_high` | 1.6901 |
| target2 | 0.1111 | `highband`, `late`, `late_high` | `late_high` | 1.6499 |

## Interpretation

The seed610 Tx/Rx bracket strengthens, rather than changes, the target1
interpretation:

```text
target1 weak rows are exact-geometry, base-confidence-limited rows.
late_high is the only audited target1 secondary objective that clears the
cutoff for every row in the expanded set.
the base objective remains the production acceptance gate.
```

For manuscript language, target1 should be reported as:

```text
Strict base confidence remains unresolved in the tested weak branches, but the
true radius/location branch is stable under the late_high diagnostic objective.
```

This distinction is the current cleanest version of the paper argument:
point recovery and branch identifiability are separable from strict objective
margin confidence.

## Validation

Figures were validated as nonblank:

```text
1237 coordinate_objective_diagnostic_ratios.png: nonwhite=0.2596, dynamic range=255
1238 objective_policy_matrix.png:               nonwhite=0.4561, dynamic range=255
```
