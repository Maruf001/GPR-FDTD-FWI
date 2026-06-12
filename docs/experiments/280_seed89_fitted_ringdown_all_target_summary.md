# Experiment 280: Seed89 Fitted-Ringdown All-Target Summary

## Purpose

Run 747 summarizes the restored seed89 GPU sequence from runs 744-746. Those
runs added another independent source-mismatch/ringdown noise seed, seed89, to
the established Tx/Rx=50 mm variable-depth/radius final-state
fitted-ringdown branch.

This run is a decision-grade analysis artifact: it converts three substantive
GPU diagnostics into one compact table, one JSON summary, and two figures.

## 747: Seed89 Fitted-Ringdown All-Target Summary

Output:

```text
outputs/experiments/747_seed89_fitted_ringdown_all_target_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_seed21_fitted_ringdown_summary.py \
  --label seed89 \
  --run-name seed89_fitted_ringdown_all_target_summary \
  outputs/experiments/744_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/746_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/745_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Inputs:

```text
run 744 target 0 summary
run 746 target 1 summary
run 745 target 2 summary
```

Artifacts:

```text
README.md
data/seed89_fitted_ringdown_summary.json
data/seed89_objective_confidence_rows.csv
data/seed89_objective_ratios.csv
data/seed89_target_summary.csv
figures/seed89_base_margins_by_target.png
figures/seed89_objective_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All three base production rows are truth-geometry rows:

| Target | Truth x/z/r mm | Base margin | Base confidence | Strongest truth-preserving diagnostic | Ratio |
| ---: | --- | ---: | --- | --- | ---: |
| 0 | 150 / 80 / 5.0 | 5.798369e-04 | moderate | veryhigh | 1.355 |
| 1 | 250 / 100 / 6.0 | 5.982895e-04 | moderate | late_high | 1.432 |
| 2 | 350 / 120 / 8.0 | 9.935884e-04 | moderate | late_high | 1.516 |

Aggregate:

```text
target count: 3
base truth count: 3
base confidence labels: moderate=3
best truth-preserving objectives: veryhigh=1, late_high=2
objective ratio rows: 15
objective confidence rows: 18
diagnostic geometry changes: 0
```

Seed21-to-seed89 comparison:

| Target | Seed21 base margin | Seed89 base margin | Seed89 vs seed21 | Best diagnostic stayed same? |
| ---: | ---: | ---: | --- | --- |
| 0 | 5.385658e-04 | 5.798369e-04 | stronger | yes, veryhigh |
| 1 | 7.175881e-04 | 5.982895e-04 | weaker | yes, late_high |
| 2 | 8.000475e-04 | 9.935884e-04 | stronger | yes, late_high |

## Interpretation

The additional seed89 stress does not expose a new geometry failure in the
fitted-ringdown Tx/Rx=50 final-state branch. Base remains exact and moderate
on all targets.

The diagnostic objective pattern remains target-specific and matches seed21:

```text
target 0: veryhigh is strongest
targets 1 and 2: late_high is strongest
```

This strengthens the conservative rule rather than replacing it:

```text
Use base for coordinate updates.
Use diagnostic objective variants as reporting evidence.
Do not promote a single global diagnostic objective without a separate
branch-specific update-rule study.
```

The main caveat is target 1. Seed89 target 1 has a lower base margin than
seed21 target 1, despite exact geometry and a stronger late_high diagnostic
ratio. The cross-seed summary should preserve that nuance.

## Validation

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_seed21_fitted_ringdown_summary.py
5 passed

JSON parse:
run_manifest.json pass
seed89_fitted_ringdown_summary.json pass

CSV row counts:
seed89_target_summary.csv: 3
seed89_objective_ratios.csv: 15
seed89_objective_confidence_rows.csv: 18

Figure validation:
seed89_base_margins_by_target.png: 1243x733, dynamic range 255
seed89_objective_ratios_by_target.png: 1515x835, dynamic range 255
visual inspection: both summary figures are readable

git diff --check: clean before tracker write; rerun after final validation
```

## Next Decision

The immediate next step should be a cross-seed fitted-ringdown robustness
summary over seed21 and seed89. That would combine runs 743 and 747 into one
decision table, call out the target-1 seed sensitivity, and avoid launching a
new GPU branch before this result is integrated.
