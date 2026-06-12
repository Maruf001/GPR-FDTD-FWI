# Experiment 399: Cross-Seed Ringdown050 Target-Specific Policy Synthesis

## Purpose

Run 865 synthesizes the target-specific policy evidence across seeds 13, 89,
21, and 34. It was refreshed after run 864 so seed21 target 2 now uses
`ringdown049453125`, matching the final practical seed21 target-0 threshold.

## 865: Cross-Seed Ringdown050 Target-Specific Policy Synthesis

Output:

```text
outputs/experiments/865_cross_seed_ringdown050_target_specific_policy_synthesis
```

Generation:

```text
CPU aggregation of promoted coordinate-confidence rows from runs 834, 835, 836,
838, 840, 842, 844, 854, 859, 860, 862, and 864, with rejected control rows
from runs 843, 846, 847, 858, and 861.
```

## Results

Per-seed policy summary:

| Seed | Policy | Condition | Summary run | Limiting target | Limiting run | Limiting margin |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 13 | 8/5/5 | full ringdown050 pass | 841 | 1 | 834 | 5.293926e-04 |
| 89 | 8/5/9 | full ringdown050 pass | 845 | 0 | 842 | 5.460353e-04 |
| 34 | 8/5/9 | full ringdown050 pass | 863 | 2 | 862 | 5.256874e-04 |
| 21 | 8/5/9 practical | target0 limited below ringdown050 | 857 | 0 | 854 | 5.000315e-04 |

Refreshed seed21 promoted rows:

| Target | Run | Tracker | Sources | Ringdown | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 854 | 388 | 8 | 0.49453125 | 5.000315e-04 | +3.148e-08 | accepted threshold |
| 1 | 836 | 370 | 5 | 0.50000000 | 5.799191e-04 | +7.992e-05 | accepted |
| 2 | 864 | 398 | 9 | 0.49453125 | 5.148618e-04 | +1.486e-05 | accepted practical |

Rejected controls:

| Seed | Target | Run | Sources | Margin | Reason |
| ---: | ---: | ---: | ---: | ---: | --- |
| 21 | 0 | 846 | 8 | 4.975041e-04 | ringdown050 near-miss |
| 21 | 0 | 847 | 9 | 4.718459e-04 | 9-source rescue weakened target0 |
| 21 | 0 | 858 | 7 | 4.425949e-04 | 7-source rescue weakened target0 |
| 89 | 2 | 843 | 5 | 4.414917e-04 | 5-source target2 weak before rescue |
| 34 | 2 | 861 | 5 | 4.575126e-04 | 5-source target2 weak before rescue |

## Interpretation

Three seeds now pass all targets at full ringdown050: seed13 under `8/5/5`,
seed89 under `8/5/9`, and seed34 under `8/5/9`. Seed21 remains the exception:
target 0 fails at ringdown050 and only passes at the razor-edge
`ringdown049453125` threshold. Run 864 is important because it shows seed21
target 2 also passes at that same practical threshold, so the seed21 policy is
internally coherent.

The full-ringdown050 open question is source-count efficiency for target 2.
Seed89 and seed34 both failed target 2 at 5 sources and passed at 9 sources;
the next branch should test the intermediate 7-source acquisition.

## Validation

```text
JSON parse: cross_seed_ringdown050_policy_synthesis.json and run_manifest.json pass
CSV rows: policy rows=12, rejected controls=5, seed summary rows=4
source validation: policy truth rows=12/12 and policy rows above cutoff=12/12
refreshed source validation: seed21 target2 uses run864/tracker398 at ringdown049453125
figure validation: full_ringdown050_base_margin_heatmap.png is 1312x1008 RGB with nonwhite_fraction=0.695569 and full 0-255 dynamic range
figure validation: cross_seed_limiting_policy_margins.png is 1632x976 RGB with nonwhite_fraction=0.474819 and full 0-255 dynamic range
figure validation: rejected_ringdown050_control_margins.png is 1952x1008 RGB with nonwhite_fraction=0.448327 and full 0-255 dynamic range
visual inspection: all three figures are readable with no overlapping labels or blank panels
resources: CPU aggregation and plotting only; no GPU workload
```

## Next Decision

Run the target-2 source-count refinement at full ringdown050. Start with seed34
target2 at 7 sources because seed34's 9-source rescue has the lower reserve
among the two full-ringdown050 `8/5/9` seeds.
