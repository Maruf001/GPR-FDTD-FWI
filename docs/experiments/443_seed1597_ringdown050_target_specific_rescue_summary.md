# Experiment 443: Seed1597 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 909 consolidates the seed1597 branch after target0 passed by a razor
margin, target2 passed at 5 sources, target1 failed at 5 sources, and target1
was rescued at 9 sources.

## 909: Seed1597 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/909_seed1597_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
905-908. No new FDTD scene was launched for this summary.
```

Source runs:

```text
905 target0 sources=8 ringdown050
906 target2 sources=5 ringdown050
907 target1 sources=5 ringdown050
908 target1 sources=9 ringdown050
```

## Results

Summary counts:

```text
row count: 4
diagnostic objective rows: 24
accepted runs: 905, 906, 908
rejected truth-preserving runs: 907
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 905 | 8 | 5.003598e-04 | +3.598e-07 | accepted |
| target2 | 906 | 5 | 5.227926e-04 | +2.279e-05 | accepted |
| target1 | 908 | 9 | 5.127098e-04 | +1.271e-05 | accepted |

Target1 rescue:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 907 | 5 | 4.919485e-04 | -8.052e-06 | rejected |
| 908 | 9 | 5.127098e-04 | +1.271e-05 | accepted |

## Interpretation

Seed1597 is an accepted but low-reserve seed. Every row preserves the true
geometry, but target0 passes by only 3.598e-07 and target1 needs the 9-source
rescue. It is therefore closer to seed610 than seed987 in margin reserve, but
unlike seed610 it has a source-density rescue that brings every target above
cutoff.

Use seed1597 as evidence that the 8/5/5 policy is not sufficient for every
seed, but that the target1 9-source rescue can be enough when the 5-source miss
is shallow.

## Validation

```text
JSON parse: run_manifest.json and seed1597_branch_summary.json pass
CSV rows: seed1597_branch_summary.csv has 4 data rows
diagnostics CSV rows: seed1597_objective_diagnostics.csv has 24 data rows
base margins figure: 1839x960 RGBA, nonwhite_fraction=0.440328
objective heatmap: 1839x960 RGBA, nonwhite_fraction=0.630825
target1 rescue trend: 1520x960 RGBA, nonwhite_fraction=0.036398
visual inspection: all three figures are readable and support the conclusion
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed2584 target0
```

## Next Decision

Continue full-ringdown replication with seed2584 target0, sources=8, Tx/Rx=60.
