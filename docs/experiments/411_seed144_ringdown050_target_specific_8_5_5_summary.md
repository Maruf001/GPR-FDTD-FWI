# Experiment 411: Seed144 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 877 summarizes the completed seed144 full-ringdown050 policy branch.

## 877: Seed144 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/877_seed144_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU aggregation of promoted rows from runs 873, 876, and 875, plus target2
5-source comparison rows from runs 838, 843, 861, 871, and 875.
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 873 | 407 | 8 | 6.144391e-04 | +1.144e-04 | accepted |
| 1 | 876 | 410 | 5 | 5.183405e-04 | +1.834e-05 | accepted |
| 2 | 875 | 409 | 5 | 5.470037e-04 | +4.700e-05 | accepted |

## Results

Seed144 passes as a full-ringdown050 `8/5/5` seed. The limiting row is target
1 from run 876, `1.834e-05` above cutoff.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 15
sub-cutoff diagnostics: target0 late, target1 early_high, target2 early_high
```

Target2 5-source cross-seed comparison:

| Seed | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 13 | 838 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 89 | 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 34 | 861 | 5 | 4.575126e-04 | -4.249e-05 | rejected |
| 55 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |
| 144 | 875 | 5 | 5.470037e-04 | +4.700e-05 | accepted |

## Interpretation

Seed144 joins seed13 and seed55 as an `8/5/5` full-ringdown050 seed. Seed89
and seed34 remain `8/5/9`, and seed21 remains target-0 limited below full
ringdown050. The target2 5-source split now has three accepted seeds and two
weak seeds, reinforcing that the target2 source-count policy is seed-dependent
rather than a universal 5-source or 9-source rule.

## Validation

```text
JSON parse: seed144_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, target2 cross-seed rows=5
source validation: promoted truth rows=3/3, promoted rows above cutoff=3/3
diagnostic validation: 18/18 diagnostics preserve truth, 15/18 diagnostics clear cutoff
figure validation: base margins plot is 1376x864 RGBA with nonwhite_fraction=0.425864 and full 0-255 dynamic range
figure validation: objective heatmap is 1792x912 RGBA with nonwhite_fraction=0.629932 and full 0-255 dynamic range
figure validation: target2 comparison plot is 1472x880 RGBA with nonwhite_fraction=0.417421 and full 0-255 dynamic range
visual inspection: all three figures are readable; heatmap red outlines mark sub-cutoff cells
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Refresh the cross-seed policy synthesis with seed55 and seed144, and continue
full-ringdown050 lower-tail replication on the next Fibonacci seed.
