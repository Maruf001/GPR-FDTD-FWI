# Experiment 281: Cross-Seed Fitted-Ringdown Summary

## Purpose

Run 748 compares the seed21 and seed89 all-target fitted-ringdown summaries.
Runs 743 and 747 already packaged each seed independently. This run combines
them into one decision table and two figures so the seed sensitivity is visible
before launching another GPU branch.

## 748: Cross-Seed Fitted-Ringdown Summary

Output:

```text
outputs/experiments/748_cross_seed_fitted_ringdown_summary
```

Command:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -u run_cross_seed_fitted_ringdown_summary.py \
  --run-name cross_seed_fitted_ringdown_summary \
  seed21=outputs/experiments/743_seed21_fitted_ringdown_all_target_summary/data/seed21_fitted_ringdown_summary.json \
  seed89=outputs/experiments/747_seed89_fitted_ringdown_all_target_summary/data/seed89_fitted_ringdown_summary.json
```

Inputs:

```text
run 743 seed21 all-target summary
run 747 seed89 all-target summary
```

Artifacts:

```text
README.md
data/cross_seed_fitted_ringdown_summary.json
data/cross_seed_target_comparison.csv
data/cross_seed_target_rows.csv
figures/cross_seed_base_margins_by_target.png
figures/cross_seed_margin_ratios_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All six seed-target base rows are truth-geometry rows:

```text
seed count: 2
target count: 3
base truth rows: 6/6
base confidence labels: moderate=6
best truth-preserving objectives: veryhigh=2, late_high=4
seed89 vs seed21 directions: stronger=2, weaker=1
best objective unchanged across seeds: 3/3 targets
```

Target comparison:

| Target | Seed21 base margin | Seed89 base margin | Seed89 / seed21 | Direction | Diagnostic |
| ---: | ---: | ---: | ---: | --- | --- |
| 0 | 5.385658e-04 | 5.798369e-04 | 1.077 | stronger | veryhigh |
| 1 | 7.175881e-04 | 5.982895e-04 | 0.834 | weaker | late_high |
| 2 | 8.000475e-04 | 9.935884e-04 | 1.242 | stronger | late_high |

## Interpretation

The cross-seed result strengthens the fitted-ringdown branch:

```text
all targets stay exact/moderate under both added seeds
target-specific diagnostic pattern is unchanged across seeds
target 1 is the only seed89 margin regression
```

This supports the production rule but preserves uncertainty:

```text
Base remains the coordinate-update objective.
Veryhigh is target-0 reporting evidence.
Late_high is target-1/2 reporting evidence.
Target 1 should be discussed as seed-sensitive because seed89 reduces its base margin.
```

## Validation

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest -q tests/test_cross_seed_fitted_ringdown_summary.py
3 passed

JSON parse:
run_manifest.json pass
cross_seed_fitted_ringdown_summary.json pass

CSV row counts:
cross_seed_target_rows.csv: 6
cross_seed_target_comparison.csv: 3

Figure validation:
cross_seed_base_margins_by_target.png: 1447x835, dynamic range 255
cross_seed_margin_ratios_by_target.png: 1345x767, dynamic range 255
visual inspection: both figures are readable and show target1 below 1.0

git diff --check: rerun after final documentation pass
```

## Next Decision

Move to a different bounded physics stress rather than extending the same
seed-replication branch immediately. A useful next branch would perturb the
ringdown condition or acquisition geometry while preserving the same
truth-state comparison structure.
