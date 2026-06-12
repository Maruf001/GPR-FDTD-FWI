# Experiment 482: Seed75025 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 948 consolidates the seed75025 branch after target2 required a 9-source
rescue while target0 and target1 passed their standard controls.

## 948: Seed75025 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/948_seed75025_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
944-947. No new FDTD scene was launched for this summary.
```

Source runs:

```text
944 target0 sources=8 ringdown050
945 target2 sources=5 ringdown050 weak control
946 target2 sources=9 ringdown050 rescue
947 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 4
diagnostic objective rows: 24
accepted runs: 944, 946, 947
rejected truth-preserving runs: 945
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 944 | 8 | 5.720010e-04 | +7.200e-05 | accepted |
| target2 | 946 | 9 | 5.008405e-04 | +8.405e-07 | accepted rescue |
| target1 | 947 | 5 | 5.109638e-04 | +1.096e-05 | accepted |

Target2 rescue:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 945 | 5 | 4.472641e-04 | -5.274e-05 | rejected |
| 946 | 9 | 5.008405e-04 | +8.405e-07 | accepted |

## Interpretation

Seed75025 is accepted after one source-density rescue. Every row preserves the
true geometry, but this is a fragile branch: target2 barely clears cutoff after
rescue, target1 clears base with low reserve and an early_high caveat, and
target0 has a late-window caveat. Continue replication to test whether the
target2 rescue fragility persists.

## Validation

```text
JSON parse: run_manifest.json and seed75025_branch_summary.json pass
CSV rows: seed75025_branch_summary.csv has 4 data rows
diagnostics CSV rows: seed75025_objective_diagnostics.csv has 24 data rows
base margins figure: 1839x960 RGBA, nonwhite_fraction=0.446530
objective heatmap: 1839x960 RGBA, nonwhite_fraction=0.683392
target2 rescue trend: 1520x960 RGBA, nonwhite_fraction=0.021952
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed121393 target0
```

## Next Decision

Continue full-ringdown replication with seed121393 target0, sources=8,
Tx/Rx=60.
