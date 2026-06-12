# Experiment 416: Seed233 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 882 summarizes the completed seed233 full-ringdown050 policy branch.

## 882: Seed233 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/882_seed233_ringdown050_target_specific_8_5_5_summary
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 878 | 413 | 8 | 5.434236e-04 | +4.342e-05 | accepted |
| 1 | 881 | 415 | 5 | 5.608831e-04 | +6.088e-05 | accepted |
| 2 | 880 | 414 | 5 | 5.878754e-04 | +8.788e-05 | accepted |

## Results

Seed233 passes as a full-ringdown050 `8/5/5` seed. The limiting row is target
0 from run 878.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 16
sub-cutoff diagnostics: target0 late, target0 late_high
```

Target2 5-source cross-seed comparison:

| Seed | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 13 | 838 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 89 | 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 34 | 861 | 5 | 4.575126e-04 | -4.249e-05 | rejected |
| 55 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |
| 144 | 875 | 5 | 5.470037e-04 | +4.700e-05 | accepted |
| 233 | 880 | 5 | 5.878754e-04 | +8.788e-05 | accepted |

## Interpretation

Seed233 joins seed13, seed55, and seed144 as an `8/5/5`
full-ringdown050 seed. Its limiting target-0 reserve is materially larger than
seed55 and much stronger than the seed21 full-ringdown050 near-miss. For target
2, the 5-source split is now four accepted seeds versus two weak seeds.

## Validation

```text
JSON parse: seed233_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, target2 cross-seed rows=6
source validation: promoted truth rows=3/3, promoted rows above cutoff=3/3
diagnostic validation: 18/18 diagnostics preserve truth, 16/18 diagnostics clear cutoff
figure validation: base margins plot is 1376x864 RGBA with nonwhite_fraction=0.447423 and full 0-255 dynamic range
figure validation: objective heatmap is 1792x912 RGBA with nonwhite_fraction=0.628758 and full 0-255 dynamic range
figure validation: target2 comparison plot is 1568x880 RGBA with nonwhite_fraction=0.426705 and full 0-255 dynamic range
visual inspection: all three figures are readable; heatmap red outlines mark sub-cutoff cells
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 882 as the seed233 policy input to the next cross-seed synthesis and
continue target-0 lower-tail replication.
