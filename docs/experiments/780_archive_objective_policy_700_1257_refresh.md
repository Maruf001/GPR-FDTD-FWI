# Experiment 780: Archive Objective-Policy Refresh, Runs 700-1257

Date: 2026-06-17

## Purpose

Refresh the CPU-side archive objective-policy evidence after the post-1218
target1, close-spacing, and physical-spacing work. This extends the holistic
tables from the old 700-1218 cutoff through output 1257, then reruns the
archive objective-policy reducer.

No FDTD, FWI, or GPU command was run for this synthesis.

## Outputs

Holistic summary refresh:

```text
outputs/summary_tables/wk03_experiment_700_1257_holistic_evaluation
docs/update/summary/006_2026-06-17_experiment_700_1257_holistic_evaluation.ipynb
```

Archive objective-policy synthesis:

```text
outputs/experiments/1258_archive_objective_policy_700_1257
```

## Method

The holistic report runner was parameterized so the same report machinery can
generate range-specific outputs without overwriting the restored 700-1218
tables. The 700-1257 refresh wrote range-specific CSVs, figures, and a
notebook.

The archive objective-policy reducer used:

```text
outputs/summary_tables/wk03_experiment_700_1257_holistic_evaluation/data/coordinate_run_summary_700_1257.csv
outputs/summary_tables/wk03_experiment_700_1257_holistic_evaluation/data/objective_variant_summary_700_1257.csv
```

## Holistic Refresh Result

```text
parseable coordinate runs: 442
detected series:          123
validated figures:        142
```

The refreshed notebook and tables include the latest target1 policy rows,
close-spacing target2 rows, and the close14 non-overlap guard probe.

## Archive Objective-Policy Result

Archive-policy rows:

```text
coordinate-run rows:       442
objective-variant rows:   2654
assigned objective rows:  2610
unassigned rows:            44
```

The 44 unassigned objective rows are the newer close-spacing geometry rows.
The reducer assigns archive-scale objective policy by the default
variable-depth three-rebar geometry, so those rows remain outside this
particular archive-policy matrix and should be interpreted through the
separate close-spacing policy syntheses.

Archive-scale secondary confirmation policy:

| Target | Base accepted fraction | Archive-scale confirmation objectives | Strongest secondary objective | Strongest accepted fraction | Mean ratio |
| --- | ---: | --- | --- | ---: | ---: |
| target0 | 0.6791 | `highband`, `veryhigh` | `highband` | 0.9925 | 1.2842 |
| target1 | 0.6791 | `highband`, `late`, `late_high` | `late_high` | 0.9925 | 1.6846 |
| target2 | 0.5210 | `late`, `late_high`, `veryhigh` | `late_high` | 1.0000 | 1.5937 |

## Interpretation

The 700-1257 refresh preserves the earlier policy structure while adding the
new target1 rows:

```text
target1 remains a base-confidence-limited branch at archive scale.
late_high remains the strongest target1 secondary confirmation objective.
diagnostic objectives are secondary reporting evidence, not a replacement for
the base production gate.
```

For manuscript framing, the updated archive-scale result supports saying that
strict base confidence and geometry identifiability are separable: some target1
branches are exact but weak under the base rule, while late/high-frequency
diagnostics consistently confirm the true branch.

## Validation

Focused tests:

```text
tests/test_experiment_holistic_report_config.py
tests/test_archive_objective_policy_summary.py
7 passed
```

Archive objective-policy figure validation:

```text
archive_objective_policy_matrix.png: nonwhite=0.4574, dynamic range=255
```

The holistic refresh wrote `figure_validation_700_1257.csv` with 142 validated
figure rows.

