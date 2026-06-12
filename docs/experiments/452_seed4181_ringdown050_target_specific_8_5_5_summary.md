# Experiment 452: Seed4181 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 918 consolidates the seed4181 branch after target0, target2, and target1
all passed without rescue.

## 918: Seed4181 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/918_seed4181_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
915-917. No new FDTD scene was launched for this summary.
```

Source runs:

```text
915 target0 sources=8 ringdown050
916 target2 sources=5 ringdown050
917 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 3
diagnostic objective rows: 18
accepted runs: 915, 916, 917
rejected runs: none
cutoff: 5.0e-4
```

Best row by target:

| Target | Run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 915 | 8 | 5.844588e-04 | +8.446e-05 | accepted |
| target2 | 916 | 5 | 5.898714e-04 | +8.987e-05 | accepted |
| target1 | 917 | 5 | 6.807359e-04 | +1.807e-04 | accepted |

## Interpretation

Seed4181 cleanly passes the target-specific 8/5/5 full-ringdown policy. All
three targets are exact, all base margins are above cutoff, and all 18
objective-diagnostic rows also clear cutoff. This is stronger than the
seed1597 and seed2584 branches, which required targeted rescue.

Use seed4181 as evidence that the rescue policy should remain conditional:
launch rescue only for a target-specific miss rather than preemptively
increasing source density for every target.

## Validation

```text
JSON parse: run_manifest.json and seed4181_branch_summary.json pass
CSV rows: seed4181_branch_summary.csv has 3 data rows
diagnostics CSV rows: seed4181_objective_diagnostics.csv has 18 data rows
base margins figure: 1600x960 RGBA, nonwhite_fraction=0.472575
objective heatmap: 1600x920 RGBA, nonwhite_fraction=0.239709
offset figure: 1600x960 RGBA, nonwhite_fraction=0.164063
visual inspection: all three figures are readable; heatmap text contrast was regenerated before documentation
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed6765 target0
```

## Next Decision

Continue full-ringdown replication with seed6765 target0, sources=8, Tx/Rx=60.
