# Experiment 767: Target2 Objective-Policy Synthesis

Date: 2026-06-17

## Purpose

CPU-only diagnostic-objective synthesis for the two recent target2
branch-sensitive acquisition branches:

```text
seed20365011074 target2:      runs 1090, 1091, 1092, 1093, 1225
seed308061521720129 target2:  runs 1184, 1185, 1186, 1226
```

This checks whether the Tx/Rx=50 rescue/failure distinction is specific to the
base objective, or whether diagnostic objectives also remain branch-sensitive.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1230_coordinate_objective_diagnostic_target2_txrx50_policy
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
for each of the nine target2 summaries.

Ratio summary:

| Objective | Rows | Truth-preserving rows | Geometry changes | Mean margin ratio | Min ratio | Max ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `early_high` | 9 | 9 | 0 | 0.9255 | 0.8509 | 1.0270 |
| `highband` | 9 | 9 | 0 | 1.2992 | 1.2112 | 1.3750 |
| `late` | 9 | 9 | 0 | 1.5164 | 1.3972 | 1.7176 |
| `late_high` | 9 | 9 | 0 | 1.6499 | 1.4783 | 1.8458 |
| `veryhigh` | 9 | 9 | 0 | 1.3552 | 1.2206 | 1.5038 |

Objective-specific confidence rows:

| Objective | Truth rows | Rows clearing `5.0e-4` | Weak rows | Mean margin | Min margin | Max margin |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `base` | 9 | 1 | 8 | 4.719057e-4 | 4.033775e-4 | 5.181019e-4 |
| `early_high` | 9 | 2 | 7 | 4.375427e-4 | 3.742475e-4 | 5.202965e-4 |
| `highband` | 9 | 9 | 0 | 6.133120e-4 | 5.072260e-4 | 7.020086e-4 |
| `late` | 9 | 9 | 0 | 7.178250e-4 | 5.662041e-4 | 8.899153e-4 |
| `late_high` | 9 | 9 | 0 | 7.807500e-4 | 5.963000e-4 | 9.562918e-4 |
| `veryhigh` | 9 | 8 | 1 | 6.409763e-4 | 4.923526e-4 | 7.791240e-4 |

Every objective row has zero x/z/r ambiguity width in the saved confidence
rows.

## Interpretation

The target2 Tx/Rx=50 rescue result is branch-sensitive under the base
objective, but not under the highband/late diagnostic objectives. The base
objective clears only one of nine target2 rows; highband, late, and late_high
clear all nine while preserving exact geometry.

This supports two separate policy statements:

```text
1. Keep Tx/Rx=50 as a selective target2 base-objective probe, not a universal
   rescue rule.
2. Treat highband/late/late_high as strong secondary confirmation evidence for
   exact target2 branches, while retaining the base objective as the production
   acceptance gate.
```

For manuscript framing, this reinforces that the current ambiguity is a
confidence-policy issue around radius-branch separation, not a target2
localization failure in the tested synthetic setup.

## Validation

The diagnostic-ratio figure was validated as nonblank:

```text
coordinate_objective_diagnostic_ratios.png nonwhite=0.2776
```
