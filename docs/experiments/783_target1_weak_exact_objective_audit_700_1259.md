# Experiment 783: Target1 Weak-Exact Objective Audit 700-1259

Date: 2026-06-17

## Purpose

CPU-only synthesis over the guarded 700-1259 holistic report. This audits
canonical target1 rows where the recovered geometry is exact but the base
margin remains weak, then checks whether diagnostic objective variants confirm
the same truth branch.

No FDTD, FWI, or GPU command was run.

## Output

```text
outputs/experiments/1261_target1_weak_exact_objective_audit_700_1259
```

Artifacts:

```text
data/target1_weak_exact_runs.csv
data/target1_weak_exact_objective_per_run.csv
data/target1_weak_exact_objective_summary.csv
data/target1_weak_exact_subset_policy.csv
data/target1_weak_exact_objective_audit_summary.json
data/figure_validation.csv
figures/target1_weak_exact_objective_audit.png
run_manifest.json
```

## Inputs

```text
outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data/coordinate_run_summary_700_1259.csv
outputs/summary_tables/wk03_experiment_700_1259_holistic_evaluation/data/objective_variant_summary_700_1259.csv
```

Only canonical-base primary rows are included. The noncanonical late-high
primary run 1259 is excluded from the policy evidence by the guarded holistic
summary.

## Result

Policy label:

```text
target1_ringdown050_latehigh_secondary_confirmed
```

Target1 canonical weak-exact rows:

```text
all archive rows:          43
ringdown050 rows:          36
modern seed610/seed552:    12
```

Objective summary across all 43 weak-exact rows:

| Objective | Truth rows | Rows clearing 5e-4 | Mean margin | Median ratio to base |
| --- | ---: | ---: | ---: | ---: |
| `base` | 43/43 | 0/43 | 4.622347e-4 | 1.0000 |
| `highband` | 43/43 | 41/43 | 6.010488e-4 | 1.3201 |
| `late` | 43/43 | 40/43 | 6.767550e-4 | 1.4762 |
| `late_high` | 43/43 | 42/43 | 7.711391e-4 | 1.6879 |
| `veryhigh` | 43/43 | 33/43 | 5.505481e-4 | 1.1914 |

Subset policy:

| Subset | Weak-exact rows | `late_high` accepted | Exception |
| --- | ---: | ---: | --- |
| all | 43 | 42 | run 785 |
| ringdown050 | 36 | 36 | none |
| ringdown025 | 4 | 3 | run 785 |
| modern seed610/seed552 | 12 | 12 | none |

## Interpretation

The broader archive audit refines the earlier target1 policy:

```text
For canonical weak-but-exact target1 rows, late_high is a strong secondary
confirmation objective, not a replacement for the base production gate.
```

For the modern ringdown050 branch, `late_high` confirms every weak-exact
target1 row and preserves exact truth geometry. Across the full archive, the
only `late_high` exception is legacy ringdown025 run 785, where no secondary
objective clears the strict cutoff.

This argues against another broad target1 GPU sweep right now. The cleaner
paper statement is that point recovery and base-margin confidence are separable:
target1 geometry is stable, while strict base confidence remains conservative.

## Validation

Focused tests:

```text
tests/test_target1_weak_exact_objective_audit.py: 4 passed
```

Figure validation:

```text
target1_weak_exact_objective_audit.png nonwhite=0.1649, dynamic range=255
```
