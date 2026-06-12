# Experiment 408: Seed55 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 874 summarizes the completed seed55 full-ringdown050 policy branch.

## 874: Seed55 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/874_seed55_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU aggregation of promoted rows from runs 870, 872, and 871, plus target2
5-source comparison rows from runs 838, 843, 861, and 871.
```

Promoted rows:

| Target | Run | Tracker | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 870 | 404 | 8 | 5.079048e-04 | +7.905e-06 | accepted |
| 1 | 872 | 406 | 5 | 5.506251e-04 | +5.063e-05 | accepted |
| 2 | 871 | 405 | 5 | 5.677153e-04 | +6.772e-05 | accepted |

## Results

Seed55 passes as a full-ringdown050 `8/5/5` seed. The limiting row is target 0
from run 870, only `7.905e-06` above cutoff.

Objective diagnostics:

```text
diagnostic rows: 18
truth-preserving diagnostic rows: 18
diagnostic rows above cutoff: 15
sub-cutoff diagnostics: target0 late, target0 late_high, target2 early_high
```

Target2 5-source cross-seed comparison:

| Seed | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 13 | 838 | 5 | 5.882895e-04 | +8.829e-05 | accepted |
| 89 | 843 | 5 | 4.414917e-04 | -5.851e-05 | rejected |
| 34 | 861 | 5 | 4.575126e-04 | -4.249e-05 | rejected |
| 55 | 871 | 5 | 5.677153e-04 | +6.772e-05 | accepted |

## Interpretation

Seed55 joins seed13 as an `8/5/5` full-ringdown050 seed. Seed89 and seed34
remain `8/5/9`, and seed21 remains target-0 limited below full ringdown050.
The target2 split is now balanced in the tested full-ringdown050 seeds:
seed13/seed55 pass with 5 sources, while seed89/seed34 require 9.

## Validation

```text
JSON parse: seed55_ringdown050_target_specific_summary.json and run_manifest.json pass
CSV rows: base rows=3, objective rows=18, target2 cross-seed rows=4
source validation: promoted truth rows=3/3, promoted rows above cutoff=3/3
diagnostic validation: 18/18 diagnostics preserve truth, 15/18 diagnostics clear cutoff
figure validation: base margins plot is 1376x864 RGB with nonwhite_fraction=0.494790 and full 0-255 dynamic range
figure validation: objective heatmap is 1792x912 RGB with nonwhite_fraction=0.665367 and full 0-255 dynamic range
figure validation: target2 comparison plot is 1472x880 RGB with nonwhite_fraction=0.503137 and full 0-255 dynamic range
visual inspection: all three figures are readable; heatmap red outlines mark sub-cutoff cells
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 874 as the seed55 input to the next cross-seed synthesis, and continue
seed144 target-specific tests.
