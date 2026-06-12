# Experiment 375: Seed13 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 841 summarizes the seed13 ringdown050 target-specific source-count policy
after run 840 strengthened target 0. It aggregates runs 840, 834, and 838 and
decides whether the `8/5/5` source-count policy should be transferred to
another seed.

## 841: Seed13 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/841_seed13_ringdown050_target_specific_8_5_5_summary
```

Source rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Reference ringdown0459375 run | Delta vs reference |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 840 | 374 | 8 | 5.625753e-04 | +6.258e-05 | 817 | -1.787e-05 |
| 1 | 834 | 368 | 5 | 5.293926e-04 | +2.939e-05 | 814 | +2.867e-05 |
| 2 | 838 | 372 | 5 | 5.882895e-04 | +8.829e-05 | 816 | +3.491e-05 |

## Result

The seed13 target-specific `8/5/5` policy passes all three targets at
ringdown050. Every production base row is exact/moderate:

```text
target 0: run 840, 8 sources, margin 5.625753e-04
target 1: run 834, 5 sources, margin 5.293926e-04
target 2: run 838, 5 sources, margin 5.882895e-04
```

The limiting production row is target 1 from run 834, `2.939e-05` above the
cutoff. Target 0 is stronger than target 1 after restoring 8 sources, so the
run 839 boundary-level result should not be used as the policy row.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 17
sub-cutoff diagnostic: target 0 late objective, 4.583314e-04
```

## Interpretation

Seed13 now supports a target-specific ringdown050 policy. The result is not a
fixed 5-source all-target policy: target 0 needs the 8-source acquisition to
avoid the boundary-level row seen in run 839. Targets 1 and 2 remain strong
under 5 sources.

Relative to the earlier seed13 ringdown0459375 target-specific 8/9/9 policy,
target 1 and target 2 improve, while target 0 remains slightly weaker but
comfortably above cutoff. The cross-seed risk should therefore be tested
starting with target 0, because it is the only seed13 target with a remaining
sub-cutoff diagnostic row.

## Validation

```text
JSON parse: seed13_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18
figure validation: seed13_ringdown050_target_specific_base_margins.png is 1515x903 RGB with full 0-255 dynamic range
figure validation: seed13_ringdown050_target_specific_objective_heatmap.png is 1513x988 RGB with full 0-255 dynamic range
visual inspection: base margin plot and diagnostic heatmap are readable; heatmap scale covers all observed values
source validation: all base rows exact/moderate; all 18 diagnostic rows truth-preserving; 17/18 diagnostics above cutoff
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Run seed89 target 0 at ringdown050 with 8 sources and Tx/Rx=60. If target 0
passes, continue seed89 target 2 with the 5-source policy, then summarize
seed89 all-target ringdown050 transfer.
