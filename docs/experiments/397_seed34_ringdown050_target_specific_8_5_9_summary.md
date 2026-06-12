# Experiment 397: Seed34 Ringdown050 Target-Specific 8/5/9 Summary

## Purpose

Run 863 summarizes seed34 ringdown050 transfer after target 0 and target 1
passed, target 2 failed at 5 sources, and target 2 was rescued at 9 sources.

## 863: Seed34 Ringdown050 Target-Specific 8/5/9 Summary

Output:

```text
outputs/experiments/863_seed34_ringdown050_target_specific_8_5_9_summary
```

Generation:

```text
CPU aggregation of runs 859, 860, 862, and rejected control run 861 into
policy-row CSVs, summary JSON, and three decision figures.
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 859 | 393 | 8 | 5.310935e-04 | +3.109e-05 | accepted |
| 1 | 860 | 394 | 5 | 5.326011e-04 | +3.260e-05 | accepted |
| 2 | 862 | 396 | 9 | 5.256874e-04 | +2.569e-05 | accepted |

Rejected row:

| Target | Run | Tracker | Sources | Margin | Confidence | Reason |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 2 | 861 | 395 | 5 | 4.575126e-04 | weak | 5-source target-2 row failed production confidence |

## Results

Seed34 passes all three promoted production rows under the `8/5/9`
target-specific policy:

```text
target 0: run 859, 8 sources, margin=5.310935e-04
target 1: run 860, 5 sources, margin=5.326011e-04
target 2: run 862, 9 sources, margin=5.256874e-04
```

The limiting production row is target 2 from run 862, only `2.569e-05` above
cutoff. The rejected 5-source target-2 row from run 861 is exact but weak,
and the 9-source rescue improves it by `6.817e-05`.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 16
sub-cutoff diagnostics: target 0 late and target 1 early_high
```

## Interpretation

Seed34 confirms a second `8/5/9` ringdown050 transfer after seed89. It differs
from seed13, which passed as `8/5/5`, and from seed21, which is limited by
target 0 below ringdown050.

The target-2 result is the main seed34 decision: 5 sources is exact but weak,
while 9 sources is exact/moderate and all diagnostic objectives clear cutoff.

## Validation

```text
JSON parse: seed34_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, rejected rows=1
figure validation: base margin plot is 1804x1073 RGB with nonwhite_fraction=0.479624 and full 0-255 dynamic range
figure validation: objective heatmap is 1970x1005 RGB with nonwhite_fraction=0.695773 and full 0-255 dynamic range
figure validation: target-2 rescue plot is 1413x937 RGB with nonwhite_fraction=0.451218 and full 0-255 dynamic range
visual inspection: all three figures are readable; heatmap uses red outlines for the two sub-cutoff truth-preserving diagnostics
source validation: all promoted base rows exact/moderate/above cutoff; all 18 promoted diagnostics truth-preserving; 16/18 diagnostics above cutoff
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 863 as the seed34 input to the next cross-seed ringdown050 synthesis.
The synthesis should compare seed13 `8/5/5`, seed89 `8/5/9`, seed21
ringdown049453125/049375 limited by target 0, and seed34 `8/5/9`.
