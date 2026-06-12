# Experiment 412: Cross-Seed Ringdown050 Target-Specific Policy Synthesis V2

## Purpose

Run 879 refreshes the cross-seed target-specific acquisition policy synthesis
after adding the completed seed55 and seed144 policy summaries.

## 879: Cross-Seed Ringdown050 Target-Specific Policy Synthesis V2

Output:

```text
outputs/experiments/879_cross_seed_ringdown050_target_specific_policy_synthesis_v2
```

Generation:

```text
CPU aggregation of promoted policy rows from seeds 13, 89, 34, 21, 55, and
144, plus rejected full-ringdown050 controls from seed21 target0 and the
seed89/seed34 target2 source-count refinement branch.
```

Per-seed limiting rows:

| Seed | Policy | Condition | Summary run | Limiting target | Limiting run | Limiting margin |
| ---: | --- | --- | ---: | ---: | ---: | ---: |
| 13 | 8/5/5 | full ringdown050 pass | 841 | 1 | 834 | 5.293926e-04 |
| 89 | 8/5/9 | full ringdown050 pass | 845 | 0 | 842 | 5.460353e-04 |
| 34 | 8/5/9 | full ringdown050 pass | 863 | 2 | 862 | 5.256874e-04 |
| 21 | 8/5/9 practical | target0 limited below ringdown050 | 857 | 0 | 854 | 5.000315e-04 |
| 55 | 8/5/5 | full ringdown050 pass | 874 | 0 | 870 | 5.079048e-04 |
| 144 | 8/5/5 | full ringdown050 pass | 877 | 1 | 876 | 5.183405e-04 |

## Results

The refreshed synthesis has 18 promoted policy rows:

```text
policy rows: 18
policy truth rows: 18
policy rows above cutoff: 18
rejected controls: 9
rejected truth rows: 9
rejected rows below cutoff: 9
seed summary rows: 6
```

Rejected controls:

| Seed | Target | Run | Sources | Margin | Reason |
| ---: | ---: | ---: | ---: | ---: | --- |
| 21 | 0 | 846 | 8 | 4.975041e-04 | seed21 target0 8-source ringdown050 near-miss |
| 21 | 0 | 847 | 9 | 4.718459e-04 | seed21 target0 9-source rescue weakened production row |
| 21 | 0 | 858 | 7 | 4.425949e-04 | seed21 target0 7-source rescue weakened production row |
| 89 | 2 | 843 | 5 | 4.414917e-04 | seed89 target2 5-source row weak before 9-source rescue |
| 89 | 2 | 868 | 7 | 4.616187e-04 | seed89 target2 7-source row weak before 9-source rescue |
| 89 | 2 | 869 | 8 | 4.604986e-04 | seed89 target2 8-source row weak before 9-source rescue |
| 34 | 2 | 861 | 5 | 4.575126e-04 | seed34 target2 5-source row weak before 9-source rescue |
| 34 | 2 | 866 | 7 | 4.168378e-04 | seed34 target2 7-source row weak before 9-source rescue |
| 34 | 2 | 867 | 8 | 4.722037e-04 | seed34 target2 8-source row weak before 9-source rescue |

## Interpretation

The current evidence supports a target-specific source-count policy, not a
single universal source count. Seed13, seed55, and seed144 pass at `8/5/5`.
Seed89 and seed34 pass full ringdown050 only at `8/5/9` because target 2 stays
weak at 5, 7, and 8 sources. Seed21 is a separate practical-threshold case:
target 0 and target 2 pass only at ringdown049453125, while target 1 passes at
full ringdown050.

The target-0 lower tail remains the most important open robustness question:
seed21 fails at full ringdown050, seed55 passes with a small reserve, and
seed144 passes strongly. The active seed233 target-0 run directly tests that
gap.

## Validation

```text
JSON parse: cross_seed_ringdown050_policy_synthesis.json and run_manifest.json pass
CSV rows: policy rows=18, rejected controls=9, seed summary rows=6
source validation: policy truth rows=18/18 and policy rows above cutoff=18/18
rejected validation: rejected truth rows=9/9 and rejected rows below cutoff=9/9
figure validation: full_ringdown050_base_margin_heatmap.png is 1312x1008 RGBA with nonwhite_fraction=0.657351 and full 0-255 dynamic range
figure validation: cross_seed_limiting_policy_margins.png is 1632x976 RGBA with nonwhite_fraction=0.439418 and full 0-255 dynamic range
figure validation: rejected_ringdown050_control_margins.png is 1952x1008 RGBA with nonwhite_fraction=0.417169 and full 0-255 dynamic range
visual inspection: all three figures are readable; practical-threshold and rejected-control markings are clear
resources: CPU aggregation and plotting only; no GPU workload
```

## Next Decision

Use run 879 as the current cross-seed policy synthesis and continue the active
seed233 target-0 lower-tail replication.
