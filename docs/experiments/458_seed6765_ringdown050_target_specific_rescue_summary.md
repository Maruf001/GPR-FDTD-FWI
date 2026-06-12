# Experiment 458: Seed6765 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 924 consolidates the seed6765 branch after target0 and target2 required
9-source rescue while target1 passed at the 5-source control.

## 924: Seed6765 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/924_seed6765_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
919-923. No new FDTD scene was launched for this summary.
```

## Results

Summary counts:

```text
row count: 5
diagnostic objective rows: 30
accepted runs: 920, 922, 923
rejected truth-preserving runs: 919, 921
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 920 | 9 | 5.485377e-04 | +4.854e-05 | accepted |
| target2 | 922 | 9 | 5.066980e-04 | +6.698e-06 | accepted |
| target1 | 923 | 5 | 6.067870e-04 | +1.068e-04 | accepted |

## Interpretation

Seed6765 is accepted but low-reserve. All rows preserve the true geometry, but
both target0 and target2 fail their first controls and need 9-source rescue.
The target2 rescue barely clears cutoff, so seed6765 should be used as evidence
that the targeted rescue policy works but does not always create large reserve.

## Validation

```text
JSON parse: run_manifest.json and seed6765_branch_summary.json pass
CSV rows: seed6765_branch_summary.csv has 5 data rows
diagnostics CSV rows: seed6765_objective_diagnostics.csv has 30 data rows
base margins figure: 1840x960 RGBA, nonwhite_fraction=0.448404
objective heatmap: 1840x960 RGBA, nonwhite_fraction=0.347938
target0 rescue trend: 1520x960 RGBA, nonwhite_fraction=0.034151
target2 rescue trend: 1520x960 RGBA, nonwhite_fraction=0.033207
visual inspection: all four figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed10946 target0
```

## Next Decision

Continue full-ringdown replication with seed10946 target0, sources=8, Tx/Rx=60.
