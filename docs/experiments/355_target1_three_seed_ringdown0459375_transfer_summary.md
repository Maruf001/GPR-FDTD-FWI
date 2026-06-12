# Experiment 355: Target-1 Three-Seed Ringdown0459375 Transfer Summary

## Purpose

Run 821 aggregates the target-1 cross-seed transfer check at ringdown0459375.
It combines seed89 run 819, seed21 run 820, and seed13 run 814 to determine
whether the highest passing seed13 target-1 stress level transfers across
source/noise seeds.

## 821: Target-1 Three-Seed Ringdown0459375 Transfer Summary

Output:

```text
outputs/experiments/821_target1_three_seed_ringdown0459375_transfer_summary
```

Source runs:

| Seed | Run | Baseline run | Base margin | Offset from cutoff | Retention vs ringdown035 | Confidence |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 89 | 819 | 794 | 5.314442e-04 | +3.144e-05 | 0.980 | moderate |
| 21 | 820 | 803 | 5.560564e-04 | +5.606e-05 | 0.978 | moderate |
| 13 | 814 | 806 | 5.007215e-04 | +7.215e-07 | 0.980 | moderate |

## Result

Target 1 remains exact and production-moderate for seed89, seed21, and seed13
at ringdown0459375. Seed13 remains the limiting seed with a `5.007215e-04`
base margin, only `7.215e-07` above the cutoff. The margin range across seeds
is `5.533e-05`.

All base rows recover the exact geometry:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

All 18 diagnostic objective rows preserve the true target-1 geometry.

## Interpretation

The strongest seed13 target-1 pass point transfers across the two earlier
source/noise seeds. The absolute margin still depends on seed, but the relative
retention from each ringdown035 baseline is nearly identical: 0.978-0.980. This
supports treating ringdown0459375 as a reproducible target-1 stress level, not
just a lucky seed13 boundary point.

Seed13 remains the limiting target-1 seed. For the next branch, the question is
whether ringdown0459375 transfers across the other targets for seed89 and
seed21, not whether target 1 needs more slicing.

## Validation

```text
JSON parse: target1_three_seed_transfer_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: target1_base_margin_by_seed.png is 1944x1188 RGB with nonwhite_fraction=0.528 and full 0-255 dynamic range
figure validation: target1_objective_margin_heatmap_by_seed.png is 2088x1044 RGB with nonwhite_fraction=0.630 and full 0-255 dynamic range
visual inspection: both summary figures are readable and show seed13 as the limiting seed
figure notes: figures/FIGURE_NOTES.md present
source validation: all base rows exact/moderate; all objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Extend ringdown0459375 cross-seed transfer beyond target 1. Start with seed89
target 2 at 9 sources and Tx/Rx=60.

