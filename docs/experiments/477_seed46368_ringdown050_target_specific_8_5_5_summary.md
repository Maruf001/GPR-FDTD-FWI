# Experiment 477: Seed46368 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 943 consolidates the seed46368 branch after target0, target2, and target1
all passed without rescue.

## 943: Seed46368 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/943_seed46368_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
940-942. No new FDTD scene was launched for this summary.
```

Source runs:

```text
940 target0 sources=8 ringdown050
941 target2 sources=5 ringdown050
942 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 3
diagnostic objective rows: 18
accepted runs: 940, 941, 942
rejected runs: none
cutoff: 5.0e-4
```

Best row by target:

| Target | Run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 940 | 8 | 5.065156e-04 | +6.516e-06 | accepted |
| target2 | 941 | 5 | 5.164762e-04 | +1.648e-05 | accepted |
| target1 | 942 | 5 | 5.072307e-04 | +7.231e-06 | accepted |

Diagnostic caveats:

| Target | Caveat |
| --- | --- |
| target0 | late and late_high margins remain below cutoff |
| target2 | early_high margin remains below cutoff |
| target1 | all diagnostic objective margins clear cutoff |

## Interpretation

Seed46368 passes the target-specific 8/5/5 full-ringdown policy without
source-density rescue, but it is one of the lowest-reserve accepted branches in
this replication series. Target0 and target1 clear the base cutoff by less
than 1.0e-05, target2 has only 1.648e-05 reserve, and the branch still carries
late-window and early_high diagnostic caveats. Treat the seed as accepted but
fragile; continue the Fibonacci replication sequence to see whether this
low-reserve pattern persists.

## Validation

```text
JSON parse: run_manifest.json and seed46368_branch_summary.json pass
CSV rows: seed46368_branch_summary.csv has 3 data rows
diagnostics CSV rows: seed46368_objective_diagnostics.csv has 18 data rows
base margins figure: 1600x960 RGB, nonwhite_fraction=0.465796
objective heatmap: 1600x920 RGB, nonwhite_fraction=0.635810
offset figure: 1600x960 RGB, nonwhite_fraction=0.140478
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed75025 target0
```

## Next Decision

Continue full-ringdown replication with seed75025 target0, sources=8,
Tx/Rx=60.
