# Experiment 766: Target1 Objective-Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only diagnostic-objective synthesis for the two unresolved target1 branches
that remain exact but weak under the base confidence rule:

```text
seed610 target1:              runs 897, 898, 899, 1224
seed5527939710754757 target1: runs 1216, 1217, 1218, 1223
```

This checks whether the weak target1 result is specific to the base objective,
or whether diagnostic objectives also fail to separate the true radius branch.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1229_coordinate_objective_diagnostic_target1_unresolved_policy
```

Artifacts:

```text
data/coordinate_objective_diagnostic_ratios.csv
data/coordinate_objective_confidence_rows.csv
data/coordinate_objective_diagnostic_report.json
figures/coordinate_objective_diagnostic_ratios.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Result

The report compares five diagnostic objectives against the matching base row
for each of the eight target1 summaries.

Ratio summary:

| Objective | Rows | Truth-preserving rows | Geometry changes | Mean margin ratio | Min ratio | Max ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `early_high` | 8 | 8 | 0 | 0.9869 | 0.9090 | 1.0363 |
| `highband` | 8 | 8 | 0 | 1.3416 | 1.2936 | 1.4047 |
| `late` | 8 | 8 | 0 | 1.4251 | 1.2861 | 1.5422 |
| `late_high` | 8 | 8 | 0 | 1.6923 | 1.5022 | 1.9173 |
| `veryhigh` | 8 | 8 | 0 | 1.2234 | 1.1688 | 1.3383 |

Objective-specific confidence rows:

| Objective | Truth rows | Rows clearing `5.0e-4` | Weak rows | Mean margin | Min margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `base` | 8 | 0 | 8 | 4.437210e-4 | 3.632038e-4 | 4.962451e-4 |
| `early_high` | 8 | 1 | 7 | 4.372036e-4 | 3.716681e-4 | 5.020206e-4 |
| `highband` | 8 | 7 | 1 | 5.954149e-4 | 4.853719e-4 | 6.847261e-4 |
| `late` | 8 | 7 | 1 | 6.340016e-4 | 4.957468e-4 | 7.653059e-4 |
| `late_high` | 8 | 8 | 0 | 7.536607e-4 | 5.455900e-4 | 9.346139e-4 |
| `veryhigh` | 8 | 6 | 2 | 5.437009e-4 | 4.327113e-4 | 6.523762e-4 |

Every objective row has zero x/z/r ambiguity width in the saved confidence
rows.

## Interpretation

The target1 unresolved branches are base-objective confidence failures, not
geometry failures. All diagnostic objectives preserve exact truth geometry in
all eight rows, and `late_high` clears the strict radius-margin cutoff in all
eight rows.

This does not justify silently replacing the production/base objective. It does
justify a narrower next research question:

```text
Can a late/highband confirmation rule be used as secondary evidence for exact
target1 branches, while preserving the base objective as the primary acceptance
rule?
```

For now, keep the production label as exact-but-unresolved when the base margin
is below `5.0e-4`. In paper language, report the diagnostic evidence separately:
the late/highband objectives indicate that the true radius branch is stable
under later-window/high-frequency weighting, but the base objective remains the
strict acceptance gate.

## Validation

The diagnostic-ratio figure was validated as nonblank:

```text
coordinate_objective_diagnostic_ratios.png nonwhite=0.2590
```
