# Experiment 291: Cross-Tx/Rx Condition Fitted-Ringdown Summary

## Purpose

Run 758 compares the seed89 Tx/Rx=50 and Tx/Rx=60 all-target packages. Runs
747 and 757 already packaged each condition independently. This run combines
them into one decision table and two figures so the acquisition-geometry
sensitivity is visible before starting another GPU branch.

## 758: Cross-Tx/Rx Condition Fitted-Ringdown Summary

Output:

```text
outputs/experiments/758_cross_txrx_condition_fitted_ringdown_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_cross_condition_fitted_ringdown_summary.py \
  --run-name cross_txrx_condition_fitted_ringdown_summary \
  --baseline-label txrx50 \
  --comparison-label txrx60 \
  txrx50=outputs/experiments/747_seed89_fitted_ringdown_all_target_summary/data/seed89_fitted_ringdown_summary.json \
  txrx60=outputs/experiments/757_txrx60_fitted_ringdown_all_target_summary/data/txrx60_fitted_ringdown_summary.json
```

Inputs:

```text
run 747 seed89 Tx/Rx=50 all-target summary
run 757 seed89 Tx/Rx=60 all-target summary
```

Artifacts:

```text
README.md
data/cross_condition_fitted_ringdown_summary.json
data/cross_condition_target_comparison.csv
data/cross_condition_target_rows.csv
figures/cross_condition_base_margins_by_target.png
figures/cross_condition_margin_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All six condition-target base rows are truth-geometry rows:

```text
condition count: 2
target count: 3
base truth rows: 6/6
base confidence labels: moderate=5, weak=1
best truth-preserving objectives: veryhigh=2, late_high=4
txrx60 vs txrx50 directions: weaker=3
confidence transitions: moderate->moderate=2, moderate->weak=1
best objective unchanged across conditions: 3/3 targets
```

Target comparison:

| Target | Tx/Rx=50 base margin | Tx/Rx=60 base margin | Tx/Rx60 / Tx/Rx50 | Direction | Confidence change | Diagnostic |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 0 | 5.798369e-04 | 5.193087e-04 | 0.896 | weaker | moderate -> moderate | veryhigh |
| 1 | 5.982895e-04 | 5.319351e-04 | 0.889 | weaker | moderate -> moderate | late_high |
| 2 | 9.935884e-04 | 4.318875e-04 | 0.435 | weaker | moderate -> weak | late_high |

## Interpretation

The Tx/Rx=60 result is exact but weaker on every target. The shallow and
center targets remain moderate with roughly 10-11% lower base margins. The deep
target is the limiting row: it remains exact but loses more than half its
Tx/Rx=50 base margin and drops to weak confidence.

The target-specific diagnostic pattern is unchanged:

```text
target 0: veryhigh
target 1: late_high
target 2: late_high
```

This closes the Tx/Rx=60 acquisition branch. It supports a nuanced claim:

```text
Tx/Rx=60 preserves geometry but reduces radius confidence.
Target 2 is exact/weak and should be reported as the branch limit.
Do not widen Tx/Rx further before integrating this degradation.
```

## Validation

```text
JSON parse:
run_manifest.json pass
cross_condition_fitted_ringdown_summary.json pass

CSV row counts:
cross_condition_target_rows.csv: 6
cross_condition_target_comparison.csv: 3

Figure validation:
cross_condition_base_margins_by_target.png: 1447x835, dynamic range 255
cross_condition_margin_ratios_by_target.png: 1345x767, dynamic range 255
visual inspection: both figures are readable and show Tx/Rx=60 below Tx/Rx=50
figure notes: figures/FIGURE_NOTES.md present and condition-generic wording checked

git diff --check: rerun after final documentation pass
```

## Next Decision

Move to a new bounded physics branch rather than widening Tx/Rx further. A
reasonable next GPU branch is to test a different source-mismatch dimension or
a revisit/finer-radius stress for the exact/weak target-2 condition, but not to
hide the Tx/Rx=60 degradation inside an aggregate claim.
