# Experiment 486: Seed121393 Ringdown050 Target0 Unresolved Source-Density Summary

## Purpose

Run 952 consolidates the seed121393 target0 source-density rescue sequence
after 8, 9, and 11 sources all failed the base confidence cutoff.

## 952: Seed121393 Ringdown050 Target0 Unresolved Source-Density Summary

Output:

```text
outputs/experiments/952_seed121393_ringdown050_target0_unresolved_source_density_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
949-951. No new FDTD scene was launched for this summary.
```

Source runs:

```text
949 target0 sources=8 ringdown050 weak control
950 target0 sources=9 ringdown050 weak rescue
951 target0 sources=11 ringdown050 weak escalation
```

## Results

Summary counts:

```text
row count: 3
diagnostic objective rows: 18
accepted runs: none
rejected truth-preserving runs: 949, 950, 951
cutoff: 5.0e-4
```

Source-density trend:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 949 | 8 | 4.651123e-04 | -3.489e-05 | rejected |
| 950 | 9 | 4.911751e-04 | -8.825e-06 | rejected |
| 951 | 11 | 4.384714e-04 | -6.153e-05 | rejected |

## Interpretation

Seed121393 target0 is unresolved under source-density rescue. The row is
truth-preserving for all three source counts, but every base margin stays below
cutoff. The 9-source row is the best attempt and still misses by 8.825e-06;
the 11-source escalation worsens the base margin. Stop this branch and
continue replication with the next seed.

## Validation

```text
JSON parse: run_manifest.json and seed121393_target0_unresolved_summary.json pass
CSV rows: seed121393_target0_source_density_summary.csv has 3 data rows
diagnostics CSV rows: seed121393_target0_objective_diagnostics.csv has 18 data rows
source-density trend figure: 1520x960 RGBA, nonwhite_fraction=0.022791
objective heatmap: 1839x960 RGBA, nonwhite_fraction=0.701479
visual inspection: both figures are readable and support the unresolved decision
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed196418 target0
```

## Next Decision

Continue full-ringdown replication with seed196418 target0, sources=8,
Tx/Rx=60.
