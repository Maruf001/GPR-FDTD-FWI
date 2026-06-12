# Experiment 371: Three-Seed Target-1 5-Source Ringdown050 Transfer Summary

## Purpose

Run 837 summarizes the target-1 cross-seed transfer of the 5-source
ringdown050 policy from seed13 run 834, seed89 run 835, and seed21 run 836.
This closes the target-1 transfer branch before extending the policy to other
targets.

## 837: Three-Seed Target-1 5-Source Ringdown050 Transfer Summary

Output:

```text
outputs/experiments/837_three_seed_target1_5source_ringdown050_transfer_summary
```

Source rows:

| Seed | Run | Tracker | Margin | Offset from cutoff | Prior 9-source transfer row | Gain vs prior |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 834 | 368 | 5.293926e-04 | +2.939e-05 | 814 | +2.867e-05 |
| 89 | 835 | 369 | 5.590847e-04 | +5.908e-05 | 819 | +2.764e-05 |
| 21 | 836 | 370 | 5.799191e-04 | +7.992e-05 | 820 | +2.386e-05 |

## Result

The 5-source Tx/Rx=60 ringdown050 policy transfers across all three tested
target-1 seeds. Every production base row is exact/moderate:

```text
seed13 target 1: run 834, margin 5.293926e-04
seed89 target 1: run 835, margin 5.590847e-04
seed21 target 1: run 836, margin 5.799191e-04
```

The global limiting row is seed13 run 834, which remains `2.939e-05` above
the production cutoff. All 18 diagnostic objective rows preserve truth and all
18 are above cutoff.

## Interpretation

The target-1 result is now stronger than the previous ringdown0459375
cross-seed transfer. At each seed, the higher-stress 5-source ringdown050 row
has a larger margin than the earlier 9-source ringdown0459375 transfer row.
That supports treating the acquisition change as a real policy improvement,
not only a seed13-specific correction.

The remaining risk is target transfer. Target 1 is centered under the 5-source
scan aperture; target 2 should be checked next because it previously required
the 9-source policy and will test whether the 5-source acquisition can still
support the right-side rebar.

## Validation

```text
JSON parse: three_seed_target1_ringdown050_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: three_seed_target1_ringdown050_base_margins.png is 1710x1007 RGBA with nonwhite_fraction=0.375809 and full 0-255 RGB-converted dynamic range
figure validation: ringdown050_vs_ringdown0459375_margin_gain.png is 1710x1007 RGBA with nonwhite_fraction=0.465549 and full 0-255 RGB-converted dynamic range
visual inspection: both summary figures are readable after legend placement cleanup
source validation: all base rows exact/moderate; all 18 objective rows truth-preserving and above cutoff
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Run seed13 target 2 at ringdown050 with the same 5-source Tx/Rx=60 acquisition
and diagnostic objective suite. If target 2 passes, continue target extension;
if it fails, bracket whether the 5-source policy is target-1-specific.
