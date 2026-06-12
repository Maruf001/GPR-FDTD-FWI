# Experiment 379: Seed89 Ringdown050 Target-Specific 8/5/9 Summary

## Purpose

Run 845 summarizes seed89 all-target ringdown050 transfer after the 9-source
target-2 rescue in run 844. It promotes runs 842, 835, and 844 and keeps run
843 as the rejected 5-source target-2 branch.

## 845: Seed89 Ringdown050 Target-Specific 8/5/9 Summary

Output:

```text
outputs/experiments/845_seed89_ringdown050_target_specific_8_5_9_summary
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Reference ringdown0459375 run | Delta vs reference |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 842 | 376 | 8 | 5.460353e-04 | +4.604e-05 | 823 | -1.882e-05 |
| 1 | 835 | 369 | 5 | 5.590847e-04 | +5.908e-05 | 819 | +2.764e-05 |
| 2 | 844 | 378 | 9 | 5.821195e-04 | +8.212e-05 | 822 | -1.389e-05 |

Rejected row:

```text
run 843: target 2, 5 sources, margin 4.414917e-04, weak, radius_weak_confidence
```

## Result

The seed89 target-specific `8/5/9` policy passes all three targets at
ringdown050:

```text
target 0: run 842, 8 sources, margin 5.460353e-04
target 1: run 835, 5 sources, margin 5.590847e-04
target 2: run 844, 9 sources, margin 5.821195e-04
```

The limiting production row is target 0, `4.604e-05` above cutoff. All
promoted production rows are exact/moderate. All 18 promoted diagnostic rows
preserve truth; 16 are above cutoff. The two sub-cutoff diagnostic rows are
target 0 late and target 0 late_high, matching the shallow-target pattern
already seen in lower-stress transfer.

## Interpretation

Seed89 confirms that ringdown050 transfer needs target-specific source counts,
but the target-specific policy can differ by seed. Seed13 passed as `8/5/5`;
seed89 needs `8/5/9` because the 5-source target-2 row was exact but weak.
The 9-source target-2 rescue restores both production confidence and
diagnostic margin robustness.

This means the next seed should not assume fixed 5-source target 2. Seed21
should be tested target by target, starting with target 0 at 8 sources because
target 1 already passed in run 836.

## Validation

```text
JSON parse: seed89_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, rejected rows=1
figure validation: seed89_ringdown050_target_specific_base_margins.png is 1515x903 RGB with full 0-255 dynamic range
figure validation: seed89_ringdown050_target_specific_objective_heatmap.png is 1513x988 RGB with full 0-255 dynamic range
figure validation: seed89_target2_sources5_vs_sources9_rescue.png is 1243x869 RGB with full 0-255 dynamic range
visual inspection: base margin plot, diagnostic heatmap, and rescue comparison are readable
source validation: all promoted base rows exact/moderate; all 18 promoted diagnostic rows truth-preserving; 16/18 diagnostics above cutoff
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Run seed21 target 0 at ringdown050 with 8 sources and Tx/Rx=60. Seed21 target
1 already passed in run 836; target 0 is the next required all-target transfer
input before resolving target 2 source count.
