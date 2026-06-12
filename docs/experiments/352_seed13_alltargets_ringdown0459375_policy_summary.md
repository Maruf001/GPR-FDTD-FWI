# Experiment 352: Seed13 All-Targets Ringdown0459375 Policy Summary

## Purpose

Run 818 aggregates the seed13 target-specific 8/9/9 source-count policy at
ringdown0459375. It combines runs 817, 814, and 816 to close the same-seed
all-target stress check at the highest passing target-1 ringdown scale.

## 818: Seed13 All-Targets Ringdown0459375 Policy Summary

Output:

```text
outputs/experiments/818_seed13_alltargets_ringdown0459375_policy_summary
```

Source runs:

| Run | Tracker | Target | Sources | Base margin | Offset from cutoff | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 817 | 351 | 0 | 8 | 5.804441e-04 | +8.044e-05 | moderate |
| 814 | 348 | 1 | 9 | 5.007215e-04 | +7.215e-07 | moderate |
| 816 | 350 | 2 | 9 | 5.533762e-04 | +5.338e-05 | moderate |

## Result

The seed13 target-specific 8/9/9 policy remains exact and production-moderate
for all targets at ringdown0459375. Target 1 remains the limiting production
row with a base margin of `5.007215e-04`, just above the confidence cutoff.

All base rows recover the exact geometry:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

All 18 objective diagnostic rows preserve the true target geometry. Two
diagnostic rows fall below `5e-04`: target 0 under `late`, and target 2 under
`early_high`. They are diagnostic weak-margin cases, not geometry failures.

## Interpretation

The target-specific source policy is now supported at a stronger, quantified
stress level for seed13. The limiting row is still target 1, matching the
target-1 threshold summary from run 815. Target 0 and target 2 retain
substantially larger production margins at the same ringdown scale.

This means ringdown0459375 is a seed13 all-target pass point for the 8/9/9
policy. The next question is not further same-seed target slicing, but whether
this stress level transfers to other source/noise seeds.

## Validation

```text
JSON parse: alltargets_ringdown0459375_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: alltargets_base_margins.png is 1944x1116 RGB with nonwhite_fraction=0.577 and full 0-255 dynamic range
figure validation: alltargets_objective_margin_heatmap.png is 2088x1044 RGB with nonwhite_fraction=0.629 and full 0-255 dynamic range
visual inspection: both summary figures are readable and show the all-target result clearly
figure notes: figures/FIGURE_NOTES.md present
source validation: all base rows exact/moderate; all objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Move to cross-seed transfer at ringdown0459375. Start with seed89 target 1 at
9 sources and Tx/Rx=60 because target 1 is the limiting production row.

