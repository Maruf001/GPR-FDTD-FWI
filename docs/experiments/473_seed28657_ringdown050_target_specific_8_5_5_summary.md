# Experiment 473: Seed28657 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 939 consolidates the seed28657 branch after target0, target2, and target1
all passed without rescue.

## 939: Seed28657 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/939_seed28657_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
936-938. No new FDTD scene was launched for this summary.
```

Source runs:

```text
936 target0 sources=8 ringdown050
937 target2 sources=5 ringdown050
938 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 3
diagnostic objective rows: 18
accepted runs: 936, 937, 938
rejected runs: none
cutoff: 5.0e-4
```

Best row by target:

| Target | Run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 936 | 8 | 5.720267e-04 | +7.203e-05 | accepted |
| target2 | 937 | 5 | 5.256723e-04 | +2.567e-05 | accepted |
| target1 | 938 | 5 | 5.076047e-04 | +7.605e-06 | accepted |

## Interpretation

Seed28657 passes the target-specific 8/5/5 full-ringdown policy without
source-density rescue. It is not a high-reserve branch: target1 barely clears
the base cutoff, target0 has a late-window diagnostic caveat, and target2 plus
target1 both have early_high caveats.

## Validation

```text
JSON parse: run_manifest.json and seed28657_branch_summary.json pass
CSV rows: seed28657_branch_summary.csv has 3 data rows
diagnostics CSV rows: seed28657_objective_diagnostics.csv has 18 data rows
base margins figure: 1600x960 RGB, nonwhite_fraction=0.450572
objective heatmap: 1600x920 RGB, nonwhite_fraction=0.637889
offset figure: 1600x960 RGB, nonwhite_fraction=0.129497
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed46368 target0
```

## Next Decision

Continue full-ringdown replication with seed46368 target0, sources=8, Tx/Rx=60.
