# Experiment 827: Target1 Source-Density Exception Map

Date: 2026-06-18

## Purpose

Build a CPU-only branch-level action map for the target1 source-density
surface from run 1312. This checks whether the weak-but-exact target1 branches
actually justify a narrow GPU rerun, or whether they are already explained by
secondary confirmation and legacy-policy boundaries.

No FDTD, FWI, optimizer, or GPU experiment was launched.

## Output

```text
outputs/experiments/1314_target1_source_density_exception_map
```

Artifacts:

```text
data/target1_source_density_exception_branches.csv
data/target1_source_density_exception_runs.csv
data/target1_source_density_exception_map_summary.json
data/figure_validation.csv
figures/target1_source_density_exception_map.png
run_manifest.json
```

## Result

Policy label:

```text
target1_source_density_exception_map_no_gpu
```

Summary:

```text
source-density series:                 17
source-density run rows:               42
all late_high-confirmed series:        16
legacy exception series:                1
modern exception series:                0
terminal 11-source series:              2
terminal 11-source worse:               2
terminal 11-source late_high confirmed: 2
source escalation helped:              10
lower source count best/equal:          7
all-base-weak series:                   3
legacy exception run IDs:             785
gpu priority:                         none
recommended GPU action:               none_target1_source_density
```

Action counts:

```text
accepted_branch_no_rerun:              9
lower_source_count_best_no_rerun:      4
secondary_confirmed_no_source_rescue:  1
do_not_extend_source_density:          2
legacy_exception_no_gpu:               1
```

## Interpretation

The branch-level audit closes the practical target1 source-density question
under the current hypothesis. All modern source-density branches preserve exact
geometry and are `late_high` confirmed. The only `late_high` exception is
legacy ringdown025 run 785.

Both terminal 11-source branches are worse than their first setting, even
though they are `late_high` confirmed. That makes source-density escalation a
bad rescue rule for target1. The next target1 GPU run would need a genuinely
new hypothesis, not a continuation of the current source-count sweep.

## Validation

Focused tests:

```text
tests/test_target1_source_density_exception_map.py
4 passed
```

Figure validation:

```text
target1_source_density_exception_map.png: 2535x1413,
nonwhite=0.1846, dynamic range=255
```
