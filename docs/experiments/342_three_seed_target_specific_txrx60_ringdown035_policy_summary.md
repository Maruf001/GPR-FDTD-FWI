# Experiment 342: Three-Seed Target-Specific Tx/Rx=60 Ringdown035 Policy Summary

## Purpose

Run 808 summarizes the target-specific Tx/Rx=60 source-count policy after the
seed13 replication completed. The policy is 8 sources for target 0 and
9 sources for targets 1 and 2. This package compares seed89, seed21, and
seed13 under the ringdown035, 10% noise, source-mismatch condition.

## 808: Three-Seed Target-Specific Tx/Rx=60 Ringdown035 Policy Summary

Output:

```text
outputs/experiments/808_three_seed_target_specific_txrx60_ringdown035_policy_summary
```

Generation:

```text
CPU aggregation of nine coordinate-optimizer summary JSON files into a
policy-row CSV, target-summary CSV, summary JSON, and comparison figure.
```

Inputs:

```text
seed89 target 0: run 795, 8 sources
seed89 target 1: run 794, 9 sources
seed89 target 2: run 796, 9 sources
seed21 target 0: run 802, 8 sources
seed21 target 1: run 803, 9 sources
seed21 target 2: run 804, 9 sources
seed13 target 0: run 805, 8 sources
seed13 target 1: run 806, 9 sources
seed13 target 2: run 807, 9 sources
```

Artifacts:

```text
README.md
data/three_seed_target_specific_policy_rows.csv
data/three_seed_target_specific_policy_target_summary.csv
data/three_seed_target_specific_policy_summary.json
figures/three_seed_policy_base_margins_by_target.png
figures/FIGURE_NOTES.md
run_manifest.json
```

## Results

All nine base confidence rows are exact and moderate:

```text
row count: 9
base truth rows: 9/9
base moderate-or-stronger rows: 9/9
confidence labels: moderate=9
best truth-preserving objective counts: highband=3, late_high=6
base margin range: 5.109178e-04 to 6.074783e-04
```

Policy rows:

| Seed | Target | Sources | Run | Base margin | Confidence | Best truth diagnostic |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| seed89 | 0 | 8 | 795 | 5.954728e-04 | moderate | highband |
| seed21 | 0 | 8 | 802 | 5.444706e-04 | moderate | highband |
| seed13 | 0 | 8 | 805 | 6.074783e-04 | moderate | highband |
| seed89 | 1 | 9 | 794 | 5.424900e-04 | moderate | late_high |
| seed21 | 1 | 9 | 803 | 5.683415e-04 | moderate | late_high |
| seed13 | 1 | 9 | 806 | 5.109178e-04 | moderate | late_high |
| seed89 | 2 | 9 | 796 | 6.058657e-04 | moderate | late_high |
| seed21 | 2 | 9 | 804 | 5.337948e-04 | moderate | late_high |
| seed13 | 2 | 9 | 807 | 5.645862e-04 | moderate | late_high |

Per-target summary:

| Target | Sources | Minimum margin | Median margin | Maximum margin | Weakest row | Strongest row |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 0 | 8 | 5.444706e-04 | 5.954728e-04 | 6.074783e-04 | seed21 run 802 | seed13 run 805 |
| 1 | 9 | 5.109178e-04 | 5.424900e-04 | 5.683415e-04 | seed13 run 806 | seed21 run 803 |
| 2 | 9 | 5.337948e-04 | 5.645862e-04 | 6.058657e-04 | seed21 run 804 | seed89 run 796 |

## Interpretation

The three-seed package supports the target-specific Tx/Rx=60 8/9/9 policy
under ringdown035 source mismatch. The result is stronger than the failed
uniform all-target policy branches: target 0 does not tolerate the uniform
9-source aperture, target 1 does not tolerate the uniform 8-source aperture,
but the target-specific 8/9/9 policy is exact/moderate across seed89, seed21,
and seed13.

The narrowest replicated row is target 1 seed13 at 5.109178e-04, barely above
the moderate cutoff. That row should be the first stress-test target if the
next branch increases source-ringdown mismatch, noise, or acquisition
perturbation.

## Validation

```text
JSON parse: run_manifest.json and three_seed_target_specific_policy_summary.json pass
CSV rows: policy rows=9, target summary rows=3
figure validation: three_seed_policy_base_margins_by_target.png is 1583x903 RGB with nonwhite_fraction=0.410 and full 0-255 dynamic range
visual inspection: grouped bar figure is readable, shows all bars above the moderate cutoff, and uses explicit scientific-notation labels
figure notes: figures/FIGURE_NOTES.md present
git diff --check: clean after documentation and symlink update
```

## Next Decision

Move to a new stress branch rather than more same-policy seed replication. The
most targeted next GPU run is the weakest replicated row, seed13 target 1 at
9 sources, under a stronger source-condition stress.
