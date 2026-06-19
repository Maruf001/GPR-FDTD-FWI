# Experiment 784: Weak-Exact Secondary Confirmation Audit 700-1259

Date: 2026-06-17

## Purpose

CPU-only synthesis over the guarded 700-1259 holistic report. This audits
canonical base-weak rows where the recovered geometry is exact, then checks
whether diagnostic objective variants confirm the same target-specific truth
branch.

No FDTD, FWI, or GPU command was run.

## Output

```text
outputs/experiments/1262_coordinate_weak_exact_secondary_confirmation_audit_700_1259
```

Artifacts:

```text
data/weak_exact_base_rows.csv
data/weak_exact_secondary_per_run.csv
data/weak_exact_secondary_objective_summary.csv
data/weak_exact_secondary_target_policy.csv
data/weak_exact_secondary_confirmation_audit_summary.json
data/figure_validation.csv
figures/weak_exact_secondary_confirmation_audit.png
run_manifest.json
```

## Inputs

```text
outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data/coordinate_run_summary_700_1259.csv
outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data/objective_variant_summary_700_1259.csv
```

The reducer selects the objective row matching each target's truth geometry.
This avoids overcounting older all-target rows where one run ID contains
target0, target1, and target2 objective entries.

## Result

Policy label:

```text
weak_exact_secondary_confirmation_audit
```

Canonical base-weak exact rows:

```text
target0: 43
target1: 43
target2: 80
total:   166
```

Target policy:

| Target | Weak-exact rows | Strongest secondary | Accepted | Policy |
| --- | ---: | --- | ---: | --- |
| target0 | 43 | `highband` | 42/43 | near confirmation; exception run 1136 |
| target1 | 43 | `late_high` | 42/43 | near confirmation; exception run 785 |
| target2 | 80 | `late_high` | 80/80 | full confirmation |

Objective highlights:

| Target | Objective | Truth rows | Accepted | Median ratio to base |
| --- | --- | ---: | ---: | ---: |
| target0 | `highband` | 43/43 | 42/43 | 1.2960 |
| target0 | `veryhigh` | 43/43 | 42/43 | 1.2358 |
| target1 | `late_high` | 43/43 | 42/43 | 1.6879 |
| target2 | `late` | 80/80 | 80/80 | 1.4781 |
| target2 | `late_high` | 80/80 | 80/80 | 1.5940 |

## Interpretation

This audit strengthens the manuscript framing:

```text
Canonical base remains the production confidence gate.
Diagnostic secondary objectives can confirm many base-weak exact recoveries.
Point recovery, branch identity, and strict base-margin confidence are
separable outcomes.
```

The result does not justify replacing the base gate. It supports reporting
secondary objectives as diagnostic confirmation:

```text
target0: highband confirms all but one weak-exact row.
target1: late_high confirms all but one weak-exact row.
target2: late and late_high confirm all weak-exact rows.
```

The immediate local decision is to avoid broad GPU sweeps for this question.
If a new GPU run is justified later, it should be a narrow exception probe for
run 1136 or run 785, not another unconstrained target sweep.

## Validation

Focused tests:

```text
tests/test_coordinate_weak_exact_secondary_confirmation_audit.py: 4 passed
```

The audit figure was validated as nonblank:

```text
weak_exact_secondary_confirmation_audit.png nonwhite=0.3773, dynamic range=255
```
