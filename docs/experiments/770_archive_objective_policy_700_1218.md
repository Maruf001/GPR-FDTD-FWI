# Experiment 770: Archive Objective-Policy Summary, Runs 700-1218

Date: 2026-06-17

## Purpose

CPU-only archive-level check of the cross-target objective-policy matrix using
the holistic summary tables for experiments 700-1218. This tests whether the
curated objective-policy results from experiments 766-769 also appear at wider
archive scale.

No FDTD, FWI, or GPU command was run for this synthesis.

## Output

```text
outputs/experiments/1233_archive_objective_policy_700_1218
```

Artifacts:

```text
data/archive_objective_assignment_rows.csv
data/archive_objective_policy_matrix.csv
data/archive_objective_policy_recommendations.csv
data/archive_objective_policy_summary.json
data/figure_validation.csv
figures/archive_objective_policy_matrix.png
run_manifest.json
```

## Inputs

```text
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/coordinate_run_summary_700_1218.csv
outputs/summary_tables/wk03_experiment_700_1218_holistic_evaluation/data/objective_variant_summary_700_1218.csv
```

The reducer handles the all-target summary-table edge case by assigning
single-target runs from `coordinate_run_summary_700_1218.csv` and multi-target
objective rows by exact known target geometry.

## Result

Archive rows:

```text
coordinate-run rows:       425
objective-variant rows:   2562
assigned objective rows:  2562
unassigned rows:             0
```

Archive-scale secondary confirmation policy, using `accepted_fraction >= 0.95`
and exact geometry for all rows:

| Target | Base accepted fraction | Archive-scale confirmation objectives | Strongest secondary objective | Strongest accepted fraction | Mean ratio for strongest |
| --- | ---: | --- | --- | ---: | ---: |
| target0 | 0.6791 | `highband`, `veryhigh` | `highband` | 0.9925 | 1.2842 |
| target1 | 0.7109 | `highband`, `late`, `late_high` | `late_high` | 0.9922 | 1.6846 |
| target2 | 0.5212 | `late`, `late_high`, `veryhigh` | `late_high` | 1.0000 | 1.5913 |

Selected matrix rows:

| Target | Objective | Rows | Truth rows | Accepted fraction | Mean margin | Mean ratio to base |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| target0 | `base` | 134 | 134 | 0.6791 | 5.204965e-4 | 1.0000 |
| target0 | `highband` | 134 | 134 | 0.9925 | 6.675877e-4 | 1.2842 |
| target0 | `veryhigh` | 134 | 134 | 0.9925 | 6.485766e-4 | 1.2472 |
| target1 | `base` | 128 | 128 | 0.7109 | 5.271683e-4 | 1.0000 |
| target1 | `highband` | 128 | 128 | 0.9844 | 6.788732e-4 | 1.2899 |
| target1 | `late` | 128 | 128 | 0.9766 | 7.859170e-4 | 1.4898 |
| target1 | `late_high` | 128 | 128 | 0.9922 | 8.880321e-4 | 1.6846 |
| target2 | `base` | 165 | 165 | 0.5212 | 5.157226e-4 | 1.0000 |
| target2 | `late` | 165 | 165 | 1.0000 | 7.648895e-4 | 1.4818 |
| target2 | `late_high` | 165 | 165 | 1.0000 | 8.208830e-4 | 1.5913 |
| target2 | `veryhigh` | 165 | 165 | 0.9697 | 6.647121e-4 | 1.2879 |

## Interpretation

The archive-level result supports the curated target-specific policy:

```text
target0: highband/veryhigh are the reliable secondary confirmers.
target1: late_high is strongest; highband and late also clear at archive scale.
target2: late and late_high are strongest; veryhigh is also archive-scale
         confirmatory, while highband is useful but below the 0.95 threshold.
```

This should be framed as secondary confirmation evidence, not as a replacement
for the base production acceptance rule. The broader archive also clarifies a
paper-level claim: target2 has the weakest base accepted fraction, but its late
window diagnostics are the most consistently confirmatory.

## Validation

The archive objective-policy matrix figure was validated as nonblank:

```text
archive_objective_policy_matrix.png nonwhite=0.4573
```
