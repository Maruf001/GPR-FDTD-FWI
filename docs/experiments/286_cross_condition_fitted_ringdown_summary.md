# Experiment 286: Cross-Condition Fitted-Ringdown Summary

## Purpose

Run 753 compares the seed89 ringdown025 and ringdown035 all-target summary
packages. Runs 747 and 752 already packaged each condition independently. This
run combines them into one decision table and two figures so the effect of the
stronger fitted-ringdown tail is visible before starting another GPU branch.

## 753: Cross-Condition Fitted-Ringdown Summary

Output:

```text
outputs/experiments/753_cross_condition_fitted_ringdown_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_cross_condition_fitted_ringdown_summary.py \
  --run-name cross_condition_fitted_ringdown_summary \
  ringdown025=outputs/experiments/747_seed89_fitted_ringdown_all_target_summary/data/seed89_fitted_ringdown_summary.json \
  ringdown035=outputs/experiments/752_ringdown035_fitted_ringdown_all_target_summary/data/ringdown035_fitted_ringdown_summary.json
```

Inputs:

```text
run 747 seed89 ringdown025 all-target summary
run 752 seed89 ringdown035 all-target summary
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
base confidence labels: moderate=5, strong=1
best truth-preserving objectives: veryhigh=2, late_high=4
ringdown035 vs ringdown025 directions: stronger=3
best objective unchanged across conditions: 3/3 targets
```

Target comparison:

| Target | Ringdown025 base margin | Ringdown035 base margin | Ringdown035 / ringdown025 | Direction | Confidence change | Diagnostic |
| ---: | ---: | ---: | ---: | --- | --- | --- |
| 0 | 5.798369e-04 | 6.141948e-04 | 1.059 | stronger | moderate -> moderate | veryhigh |
| 1 | 5.982895e-04 | 6.280926e-04 | 1.050 | stronger | moderate -> moderate | late_high |
| 2 | 9.935884e-04 | 1.038879e-03 | 1.046 | stronger | moderate -> strong | late_high |

## Interpretation

The ringdown035 condition slightly strengthens all three seed89 target margins
without changing recovered geometry. Target 2 is the only confidence-label
upgrade, moving from moderate to strong. Targets 0 and 1 remain moderate with
larger margins.

The diagnostic objective pattern is unchanged across conditions:

```text
target 0: veryhigh
target 1: late_high
target 2: late_high
```

This closes the stronger-ringdown branch as a robustness confirmation. It does
not justify promoting a diagnostic objective for production updates. Base
remains the coordinate-update objective; veryhigh and late_high remain
target-specific reporting evidence.

## Validation

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_cross_condition_fitted_ringdown_summary.py
3 passed

JSON parse:
run_manifest.json pass
cross_condition_fitted_ringdown_summary.json pass

CSV row counts:
cross_condition_target_rows.csv: 6
cross_condition_target_comparison.csv: 3

Figure validation:
cross_condition_base_margins_by_target.png: 1447x835, dynamic range 255
cross_condition_margin_ratios_by_target.png: 1345x767, dynamic range 255
visual inspection: both figures are readable and show ringdown035 above 1.0

git diff --check: rerun after final documentation pass
```

## Next Decision

Move to a different bounded GPU stress rather than extending the ringdown035
condition again. A useful next branch is an acquisition-geometry robustness
stress, preserving the same exact final-state target table and diagnostic
objective matrix so the results remain directly comparable to runs 740-753.
