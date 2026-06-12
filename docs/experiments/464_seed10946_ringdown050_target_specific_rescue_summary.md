# Experiment 464: Seed10946 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 930 consolidates the seed10946 branch after target0 and target2 required
9-source rescue while target1 passed at the 5-source control.

## 930: Seed10946 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/930_seed10946_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
925-929. No new FDTD scene was launched for this summary.
```

## Results

Summary counts:

```text
row count: 5
diagnostic objective rows: 30
accepted runs: 926, 928, 929
rejected truth-preserving runs: 925, 927
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 926 | 9 | 5.206657e-04 | +2.067e-05 | accepted |
| target2 | 928 | 9 | 5.592681e-04 | +5.927e-05 | accepted |
| target1 | 929 | 5 | 5.980473e-04 | +9.805e-05 | accepted |

## Interpretation

Seed10946 is accepted but branch-dependent. All rows preserve the true
geometry, but target0 and target2 fail their first controls and need 9-source
rescues. Target0 remains low-reserve after rescue because late and late_high
diagnostic variants stay below cutoff. Target2 is healthier after rescue, and
target1 is the cleanest row with all six diagnostic margins above cutoff.

## Validation

```text
JSON parse: run_manifest.json and seed10946_branch_summary.json pass
CSV rows: seed10946_branch_summary.csv has 5 data rows
diagnostics CSV rows: seed10946_objective_diagnostics.csv has 30 data rows
base margins figure: 1840x960 RGB, nonwhite_fraction=0.456653
objective heatmap: 1840x960 RGB, nonwhite_fraction=0.348066
target0 rescue trend: 1520x960 RGB, nonwhite_fraction=0.033862
target2 rescue trend: 1520x960 RGB, nonwhite_fraction=0.039888
visual inspection: all four figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed17711 target0
```

## Next Decision

Continue full-ringdown replication with seed17711 target0, sources=8, Tx/Rx=60.
