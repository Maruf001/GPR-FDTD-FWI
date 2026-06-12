# Experiment 358: Seed89 All-Targets Ringdown0459375 Transfer Summary

## Purpose

Run 824 aggregates the seed89 target-specific 8/9/9 policy at
ringdown0459375. It combines target 0 run 823, target 1 run 819, and target 2
run 822 to close the seed89 all-target transfer branch.

## 824: Seed89 All-Targets Ringdown0459375 Transfer Summary

Output:

```text
outputs/experiments/824_seed89_alltargets_ringdown0459375_transfer_summary
```

Source runs:

| Run | Tracker | Target | Sources | Baseline run | Base margin | Retention vs ringdown035 | Offset from cutoff | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 823 | 357 | 0 | 8 | 795 | 5.648510e-04 | 0.949 | +6.485e-05 | moderate |
| 819 | 353 | 1 | 9 | 794 | 5.314442e-04 | 0.980 | +3.144e-05 | moderate |
| 822 | 356 | 2 | 9 | 796 | 5.960116e-04 | 0.984 | +9.601e-05 | moderate |

## Result

Seed89 passes the all-target ringdown0459375 transfer check. All three base
rows are exact and production-moderate under the target-specific 8/9/9
source-count policy. Target 1 remains the limiting production row with a
`5.314442e-04` margin, while target 0 is `5.648510e-04` and target 2 is
`5.960116e-04`.

All base rows recover the exact geometry:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

All 18 diagnostic objective rows preserve the true target geometry. Two target
0 diagnostic rows fall below `5e-04`: `late` at `4.524691e-04` and
`late_high` at `4.830870e-04`. These are weak-margin diagnostic windows, not
geometry failures.

## Interpretation

The seed89 all-target result matches the seed13 policy-level conclusion: the
8/9/9 policy transfers at ringdown0459375, and target 1 remains the limiting
production target. The main seed89 difference is diagnostic: target 0 has two
late-window below-cutoff objective rows, whereas seed13 target 0 only had the
late row below cutoff and seed13 target 2 had an early_high weak diagnostic.

Retention relative to ringdown035 ranges from 0.949 to 0.984. Target 0 loses
the most margin relative to its own ringdown035 baseline, but it still clears
the production cutoff by `6.485e-05`.

## Validation

```text
JSON parse: seed89_alltargets_ringdown0459375_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: seed89_alltargets_base_margins.png is 1944x1116 RGBA with nonwhite_fraction=0.433 and full 0-255 RGB-converted dynamic range
figure validation: seed89_alltargets_objective_margin_heatmap.png is 2088x1044 RGBA with nonwhite_fraction=0.662 and full 0-255 RGB-converted dynamic range
visual inspection: both summary figures are readable and show target 1 as the limiting seed89 production row
source validation: all base rows exact/moderate; all objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Extend ringdown0459375 all-target transfer to seed21. Seed21 target 1 already
passes from run 820, so run seed21 target 2 at 9 sources next, followed by
seed21 target 0 at 8 sources.
