# Experiment 769: Cross-Target Objective-Policy Matrix

Date: 2026-06-17

## Purpose

CPU-only consolidation of the target0, target1, and target2 diagnostic-objective
policy syntheses:

```text
target0 report: outputs/experiments/1231_coordinate_objective_diagnostic_target0_policy
target1 report: outputs/experiments/1229_coordinate_objective_diagnostic_target1_unresolved_policy
target2 report: outputs/experiments/1230_coordinate_objective_diagnostic_target2_txrx50_policy
```

This creates one cross-target policy table so the diagnostic objective rules are
not overgeneralized.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1232_coordinate_objective_policy_matrix
```

Artifacts:

```text
data/objective_policy_matrix.csv
data/objective_policy_recommendations.csv
data/objective_policy_matrix_summary.json
data/figure_validation.csv
figures/objective_policy_matrix.png
run_manifest.json
```

## Result

Recommended secondary confirmation objectives:

| Target | Base accepted fraction | Full-acceptance secondary objectives | Strongest secondary objective | Mean ratio for strongest |
| --- | ---: | --- | --- | ---: |
| target0 | 0.2778 | `highband`, `veryhigh` | `highband` | 1.3327 |
| target1 | 0.0000 | `late_high` | `late_high` | 1.6923 |
| target2 | 0.1111 | `highband`, `late`, `late_high` | `late_high` | 1.6499 |

Selected matrix details:

| Target | Objective | Rows | Truth rows | Accepted fraction | Mean margin | Mean ratio to base |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| target0 | `base` | 18 | 18 | 0.2778 | 4.871635e-4 | 1.0000 |
| target0 | `highband` | 18 | 18 | 1.0000 | 6.495129e-4 | 1.3327 |
| target0 | `veryhigh` | 18 | 18 | 1.0000 | 6.334062e-4 | 1.2982 |
| target0 | `late_high` | 18 | 18 | 0.0556 | 4.191154e-4 | 0.8611 |
| target1 | `base` | 8 | 8 | 0.0000 | 4.437210e-4 | 1.0000 |
| target1 | `late_high` | 8 | 8 | 1.0000 | 7.536607e-4 | 1.6923 |
| target2 | `base` | 9 | 9 | 0.1111 | 4.719057e-4 | 1.0000 |
| target2 | `highband` | 9 | 9 | 1.0000 | 6.133120e-4 | 1.2992 |
| target2 | `late` | 9 | 9 | 1.0000 | 7.178250e-4 | 1.5164 |
| target2 | `late_high` | 9 | 9 | 1.0000 | 7.807500e-4 | 1.6499 |

## Interpretation

The secondary objective policy is target-specific:

```text
target0: highband/veryhigh are useful secondary confirmers; late_high is not.
target1: late_high is the only audited full-acceptance secondary confirmer.
target2: highband, late, and late_high all fully confirm; late_high is strongest.
```

This is useful for paper positioning because it separates exact geometry from
strict base-objective confidence without pretending that one diagnostic
objective is universally best. The base objective remains the production
acceptance gate; these objectives are secondary confirmation/reporting
evidence.

## Validation

The policy-matrix figure was validated as nonblank:

```text
objective_policy_matrix.png nonwhite=0.4561
```
