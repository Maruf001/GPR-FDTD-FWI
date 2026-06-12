# Experiment 469: Seed17711 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 935 consolidates the seed17711 branch after target0 required 9-source
rescue while target2 and target1 passed at the 5-source control.

## 935: Seed17711 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/935_seed17711_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
931-934. No new FDTD scene was launched for this summary.
```

Source runs:

```text
931 target0 sources=8 ringdown050
932 target0 sources=9 ringdown050
933 target2 sources=5 ringdown050
934 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 4
diagnostic objective rows: 24
accepted runs: 932, 933, 934
rejected truth-preserving runs: 931
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 932 | 9 | 5.524814e-04 | +5.248e-05 | accepted |
| target2 | 933 | 5 | 5.362844e-04 | +3.628e-05 | accepted |
| target1 | 934 | 5 | 5.806372e-04 | +8.064e-05 | accepted |

Target0 rescue:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 931 | 8 | 4.845798e-04 | -1.542e-05 | rejected |
| 932 | 9 | 5.524814e-04 | +5.248e-05 | accepted |

## Interpretation

Seed17711 is accepted after one source-density rescue. Every row preserves the
true geometry. Target0 is the only row requiring rescue and remains
late-window low-reserve; target2 passes with an early_high caveat; target1 is
clean across all diagnostic objective variants.

## Validation

```text
JSON parse: run_manifest.json and seed17711_branch_summary.json pass
CSV rows: seed17711_branch_summary.csv has 4 data rows
diagnostics CSV rows: seed17711_objective_diagnostics.csv has 24 data rows
base margins figure: 1840x960 RGB, nonwhite_fraction=0.446837
objective heatmap: 1840x960 RGB, nonwhite_fraction=0.647362
target0 rescue trend: 1520x960 RGB, nonwhite_fraction=0.037674
visual inspection: all three figures are readable and support the summary
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed28657 target0
```

## Next Decision

Continue full-ringdown replication with seed28657 target0, sources=8, Tx/Rx=60.
