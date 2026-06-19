# Experiment 782: Guarded Archive Policy After Late-High Primary Probe

Date: 2026-06-17

## Purpose

CPU-only reporting guard after experiment 781. Run 1259 deliberately labels a
late/highband objective as the primary optimizer objective, so its confidence
CSV uses `base` for a noncanonical objective. That is useful for an
update-rule probe, but it must not contaminate archive-level "base objective"
policy summaries.

This experiment updates the holistic report generator and archive-policy
reducer so noncanonical-primary objective runs are visible in raw run tables
but excluded from canonical base-policy charts, series, and archive objective
policy rows.

## Outputs

Holistic guarded refresh:

```text
outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation
docs/update/summary/007_2026-06-17_experiment_700_1259_holistic_evaluation.ipynb
```

Archive objective-policy refresh:

```text
outputs/experiments/1260_archive_objective_policy_700_1259_guarded
```

## Implementation

The holistic report now records:

```text
primary_objective_label
primary_objective_family
base_margin_is_canonical
```

Run 1259 is classified as:

```text
primary_objective_label:  base
primary_objective_family: late_high_primary
base_margin_is_canonical: False
```

The raw coordinate summary still includes the run, but base-policy plots and
series use only canonical-base primary rows.

The archive objective-policy reducer also filters objective rows from
noncanonical-primary runs before assigning target policies. Older summary
tables that lack the flag default to canonical so restored 700-1218 behavior is
preserved.

## Result

Guarded holistic refresh:

```text
parseable coordinate runs:          443
canonical-base policy runs:         442
excluded noncanonical-primary runs:   1
detected series:                    123
validated figures:                  142
```

Guarded archive policy:

```text
input coordinate-run rows:             443
input objective-variant rows:         2660
excluded noncanonical-primary runs:      1
excluded noncanonical objective rows:    6
policy coordinate-run rows:            442
policy objective-variant rows:        2654
assigned objective rows:              2610
unassigned objective rows:              44
```

The policy recommendations remain unchanged from the 700-1257 guarded archive
because run 1259 is intentionally excluded from canonical base-policy evidence:

| Target | Base accepted fraction | Archive-scale confirmation objectives | Strongest secondary objective |
| --- | ---: | --- | --- |
| target0 | 0.6791 | `highband`, `veryhigh` | `highband` |
| target1 | 0.6791 | `highband`, `late`, `late_high` | `late_high` |
| target2 | 0.5210 | `late`, `late_high`, `veryhigh` | `late_high` |

## Interpretation

This closes a reporting integrity gap introduced by the useful experiment 781
update-rule probe. Run 1259 can be discussed as evidence that late/highband
weighting separates the target1 branch, while archive base-confidence claims
remain tied to the canonical base objective.

The manuscript distinction should stay explicit:

```text
canonical base confidence and late_high secondary confirmation are separate
evidence streams.
```

## Validation

Focused tests:

```text
tests/test_experiment_holistic_report_config.py
tests/test_archive_objective_policy_summary.py
11 passed
```

Guarded archive figure validation:

```text
archive_objective_policy_matrix.png nonwhite=0.4574, dynamic range=255
```

The guarded holistic refresh wrote `figure_validation_700_1259.csv` with 142
validated figure rows.

