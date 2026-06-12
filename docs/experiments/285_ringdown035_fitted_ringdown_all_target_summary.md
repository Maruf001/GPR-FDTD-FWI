# Experiment 285: Ringdown035 Fitted-Ringdown All-Target Summary

## Purpose

Run 752 summarizes the restored ringdown035 GPU sequence from runs 749-751.
Those runs increased the seed89 fitted-ringdown scale from 0.25 to 0.35 while
keeping the established Tx/Rx=50 mm variable-depth/radius final-state branch,
source-fit grid, and objective diagnostics.

This run is a decision-grade analysis artifact: it converts three substantive
GPU diagnostics into one compact table, one JSON summary, and two figures.

## 752: Ringdown035 Fitted-Ringdown All-Target Summary

Output:

```text
outputs/experiments/752_ringdown035_fitted_ringdown_all_target_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_seed21_fitted_ringdown_summary.py \
  --label ringdown035 \
  --run-name ringdown035_fitted_ringdown_all_target_summary \
  outputs/experiments/751_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx50_ringdown035_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/749_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx50_ringdown035_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/750_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx50_ringdown035_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Inputs:

```text
run 751 target 0 summary
run 749 target 1 summary
run 750 target 2 summary
```

Artifacts:

```text
README.md
data/ringdown035_fitted_ringdown_summary.json
data/ringdown035_objective_confidence_rows.csv
data/ringdown035_objective_ratios.csv
data/ringdown035_target_summary.csv
figures/ringdown035_base_margins_by_target.png
figures/ringdown035_objective_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All three base production rows are truth-geometry rows:

| Target | Truth x/z/r mm | Base margin | Base confidence | Strongest truth-preserving diagnostic | Ratio |
| ---: | --- | ---: | --- | --- | ---: |
| 0 | 150 / 80 / 5.0 | 6.141948e-04 | moderate | veryhigh | 1.340 |
| 1 | 250 / 100 / 6.0 | 6.280926e-04 | moderate | late_high | 1.523 |
| 2 | 350 / 120 / 8.0 | 1.038879e-03 | strong | late_high | 1.619 |

Aggregate:

```text
target count: 3
base truth count: 3
base confidence labels: moderate=2, strong=1
best truth-preserving objectives: veryhigh=1, late_high=2
objective ratio rows: 15
objective confidence rows: 18
diagnostic geometry changes: 0
```

Ringdown025-to-ringdown035 seed89 comparison:

| Target | Ringdown025 base margin | Ringdown035 base margin | Ringdown035 / ringdown025 | Confidence change | Best diagnostic stayed same? |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 5.798369e-04 | 6.141948e-04 | 1.059 | moderate -> moderate | yes, veryhigh |
| 1 | 5.982895e-04 | 6.280926e-04 | 1.050 | moderate -> moderate | yes, late_high |
| 2 | 9.935884e-04 | 1.038879e-03 | 1.046 | moderate -> strong | yes, late_high |

Objective-ratio means:

| Objective | Mean ratio | Min ratio | Max ratio |
| --- | ---: | ---: | ---: |
| early_high | 0.776 | 0.712 | 0.853 |
| highband | 1.158 | 1.125 | 1.175 |
| late | 1.213 | 0.754 | 1.539 |
| late_high | 1.315 | 0.803 | 1.619 |
| veryhigh | 1.303 | 1.213 | 1.355 |

## Interpretation

The stronger ringdown035 source stress does not expose a new geometry failure
in the fitted-ringdown Tx/Rx=50 final-state branch. Base remains exact on all
three targets. Target 2 improves from moderate to strong confidence, and
targets 0 and 1 retain moderate confidence with slightly larger base margins
than the ringdown025 seed89 rows.

The diagnostic objective pattern remains target-specific and matches both
ringdown025 seeds:

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

The notable nuance is target 0. Late and late_high still weaken the shallow
target even under stronger ringdown, so the target-specific diagnostic split
is real evidence, not a plotting artifact.

## Validation

```text
JSON parse:
run_manifest.json pass
ringdown035_fitted_ringdown_summary.json pass

CSV row counts:
ringdown035_target_summary.csv: 3
ringdown035_objective_ratios.csv: 15
ringdown035_objective_confidence_rows.csv: 18

Figure validation:
ringdown035_base_margins_by_target.png: 1243x733, dynamic range 255
ringdown035_objective_ratios_by_target.png: 1515x835, dynamic range 255
visual inspection: both summary figures are readable

git diff --check: clean before tracker write; rerun after final validation
```

## Next Decision

The immediate next step should be a cross-condition fitted-ringdown robustness
summary comparing seed89 ringdown025 and seed89 ringdown035. That should be a
CPU summary artifact, not a new GPU sweep, because the per-target GPU branch
is already closed and the condition-to-condition comparison is the missing
decision table.
