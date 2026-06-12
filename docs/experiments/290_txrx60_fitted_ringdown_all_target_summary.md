# Experiment 290: Tx/Rx=60 Fitted-Ringdown All-Target Summary

## Purpose

Run 757 summarizes the Tx/Rx=60 acquisition-geometry branch from runs 754-756.
Those runs widened the Tx/Rx offset from 50 mm to 60 mm while keeping the
seed89 ringdown025 source-mismatch stress, final truth state, source-fit grid,
and objective diagnostics fixed.

This run converts the three substantive GPU diagnostics into one compact
table, one JSON summary, and two figures.

## 757: Tx/Rx=60 Fitted-Ringdown All-Target Summary

Output:

```text
outputs/experiments/757_txrx60_fitted_ringdown_all_target_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_seed21_fitted_ringdown_summary.py \
  --label txrx60 \
  --run-name txrx60_fitted_ringdown_all_target_summary \
  outputs/experiments/756_coordinate_optimizer_variable_depth_radius_seed89_target0_txrx60_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/754_coordinate_optimizer_variable_depth_radius_seed89_target1_txrx60_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json \
  outputs/experiments/755_coordinate_optimizer_variable_depth_radius_seed89_target2_txrx60_ringdown025_objectives/data/multi_rebar_coordinate_optimizer_summary.json
```

Inputs:

```text
run 756 target 0 summary
run 754 target 1 summary
run 755 target 2 summary
```

Artifacts:

```text
README.md
data/txrx60_fitted_ringdown_summary.json
data/txrx60_objective_confidence_rows.csv
data/txrx60_objective_ratios.csv
data/txrx60_target_summary.csv
figures/txrx60_base_margins_by_target.png
figures/txrx60_objective_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All three base rows are exact, but target 2 is weak:

| Target | Truth x/z/r mm | Base margin | Base confidence | Strongest truth-preserving diagnostic | Ratio |
| ---: | --- | ---: | --- | --- | ---: |
| 0 | 150 / 80 / 5.0 | 5.193087e-04 | moderate | veryhigh | 1.242 |
| 1 | 250 / 100 / 6.0 | 5.319351e-04 | moderate | late_high | 1.463 |
| 2 | 350 / 120 / 8.0 | 4.318875e-04 | weak | late_high | 1.459 |

Aggregate:

```text
target count: 3
base truth count: 3
base confidence labels: moderate=2, weak=1
best truth-preserving objectives: veryhigh=1, late_high=2
objective ratio rows: 15
objective confidence rows: 18
diagnostic geometry changes: 0
```

Tx/Rx=50-to-Tx/Rx=60 seed89 comparison:

| Target | Tx/Rx=50 base margin | Tx/Rx=60 base margin | Tx/Rx60 / Tx/Rx50 | Confidence change | Best diagnostic stayed same? |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 5.798369e-04 | 5.193087e-04 | 0.896 | moderate -> moderate | yes, veryhigh |
| 1 | 5.982895e-04 | 5.319351e-04 | 0.889 | moderate -> moderate | yes, late_high |
| 2 | 9.935884e-04 | 4.318875e-04 | 0.435 | moderate -> weak | yes, late_high |

## Interpretation

The Tx/Rx=60 branch preserves exact geometry across all three targets, but it
is clearly margin-degraded relative to Tx/Rx=50. The effect is modest for
targets 0 and 1 and severe for target 2.

The diagnostic objective pattern is unchanged:

```text
target 0: veryhigh is strongest
targets 1 and 2: late_high is strongest
```

The result should be reported conservatively:

```text
Tx/Rx=60 is exact but lower confidence than Tx/Rx=50.
Target 2 is exact/weak and is the branch-limiting row.
Diagnostic variants remain reporting evidence, not production update rules.
```

## Validation

```text
JSON parse:
run_manifest.json pass
txrx60_fitted_ringdown_summary.json pass

CSV row counts:
txrx60_target_summary.csv: 3
txrx60_objective_ratios.csv: 15
txrx60_objective_confidence_rows.csv: 18

Figure validation:
txrx60_base_margins_by_target.png: 1243x733, dynamic range 255
txrx60_objective_ratios_by_target.png: 1515x835, dynamic range 255
visual inspection: both summary figures are readable

git diff --check: rerun after final documentation pass
```

## Next Decision

Create a cross-condition fitted-ringdown summary comparing the seed89 Tx/Rx=50
and Tx/Rx=60 packages. That CPU summary should be the decision table before
starting any new GPU branch.
