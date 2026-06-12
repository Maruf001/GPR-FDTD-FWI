# Experiment 385: Seed21 Ringdown049375 Target-Specific 8/5/9 Summary

## Purpose

Run 851 summarizes seed21 after target 2 passed at the target-0 practical
stress boundary in run 850. It promotes runs 849, 836, and 850, and keeps
runs 846 and 847 as rejected target-0 ringdown050 evidence.

## 851: Seed21 Ringdown049375 Target-Specific 8/5/9 Summary

Output:

```text
outputs/experiments/851_seed21_ringdown049375_target_specific_8_5_9_summary
```

Promoted rows:

| Target | Run | Tracker | Sources | Nominal ringdown | Margin | Offset from cutoff | Reference run | Delta vs reference |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 849 | 383 | 8 | 0.49375 | 5.003891e-04 | +3.891e-07 | 826 | -1.476e-05 |
| 1 | 836 | 370 | 5 | 0.50000 | 5.799191e-04 | +7.992e-05 | 820 | +2.386e-05 |
| 2 | 850 | 384 | 9 | 0.49375 | 5.151258e-04 | +1.513e-05 | 825 | -1.009e-05 |

Rejected target-0 ringdown050 rows:

| Target | Run | Tracker | Sources | Margin | Confidence | Reason |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 0 | 846 | 380 | 8 | 4.975041e-04 | weak | ringdown050 8-source row missed cutoff |
| 0 | 847 | 381 | 9 | 4.718459e-04 | weak | 9-source rescue weakened the production row |

## Result

The seed21 target-specific policy passes the promoted production rows:

```text
target 0: run 849, 8 sources, ringdown049375, margin=5.003891e-04
target 1: run 836, 5 sources, ringdown050, margin=5.799191e-04
target 2: run 850, 9 sources, ringdown049375, margin=5.151258e-04
```

The limiting production row is target 0 from run 849, only `3.891e-07` above
cutoff. All promoted production rows are exact/moderate. All 18 promoted
diagnostic rows preserve truth; 16/18 diagnostics are above cutoff. The two
sub-cutoff diagnostics are target 0 late and target 0 late_high.

## Interpretation

Seed21 supports a target-specific `8/5/9` policy at the practical
ringdown049375 boundary, with target 1 represented by a harder ringdown050
pass. It does not support an all-target ringdown050 policy because target 0
falls below cutoff in both the 8-source and 9-source ringdown050 attempts.

The limiting physics remains the shallow target-0 row. Target 2 passes the
same ringdown049375 stress with more reserve than target 0, and target 1 has
already survived a stronger stress level.

## Validation

```text
JSON parse: seed21_ringdown049375_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, rejected rows=2
figure validation: base margin plot is 1575x930 RGB with nonwhite_fraction=0.483739 and full 0-255 dynamic range
figure validation: objective heatmap is 1470x945 RGB with nonwhite_fraction=0.291335 and full 0-255 dynamic range
figure validation: target-0 boundary plot is 1575x900 RGB with nonwhite_fraction=0.425743 and full 0-255 dynamic range
visual inspection: all three figures are readable; base plot exposes the limiting target 0 row, heatmap exposes the two target-0 sub-cutoff diagnostics, and boundary plot exposes the rejected ringdown050 rows
source validation: all promoted base rows exact/moderate/above cutoff; all 18 promoted diagnostics truth-preserving; 16/18 diagnostics above cutoff
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 851 as the seed21 input to the cross-seed stress synthesis. The next
GPU run should refine the seed21 target-0 threshold or test the next
cross-seed boundary; retesting target 1 at the easier ringdown049375 condition
is not justified because run 836 already passed target 1 at ringdown050.
