# Experiment 438: Seed987 Ringdown050 Target-Specific 8/5/5 Summary

## Purpose

Run 904 consolidates the accepted seed987 target-specific branch after target0,
target2, and target1 all passed under full ringdown050.

## 904: Seed987 Ringdown050 Target-Specific 8/5/5 Summary

Output:

```text
outputs/experiments/904_seed987_ringdown050_target_specific_8_5_5_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
900, 902, and 903. No new FDTD scene was launched for this summary.
```

Source runs:

```text
900 target0 sources=8 ringdown050
902 target2 sources=5 ringdown050
903 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 3
diagnostic objective rows: 18
accepted runs: 900, 902, 903
rejected runs: none
cutoff: 5.0e-4
```

Target-specific branch:

| Target | Run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 900 | 8 | 5.111568e-04 | +1.116e-05 | accepted |
| target2 | 902 | 5 | 5.518990e-04 | +5.190e-05 | accepted |
| target1 | 903 | 5 | 5.664717e-04 | +6.647e-05 | accepted |

Objective reserve:

| Run | Target | Below-cutoff variants |
| ---: | --- | --- |
| 900 | target0 | late, late_high |
| 902 | target2 | early_high |
| 903 | target1 | none |

## Interpretation

Seed987 is a clean accepted seed under the current target-specific policy. The
target0 margin is the lowest reserve, but it still clears cutoff and preserves
the true geometry across all objective variants. Target2 and target1 both pass
with more base reserve than target0.

This makes seed987 a useful positive contrast to seed610. Seed610 stayed
truth-preserving but weak on target1 and target2; seed987 stays
truth-preserving and clears the production cutoff on all three targets without
rescue runs.

## Validation

```text
JSON parse: run_manifest.json and seed987_branch_summary.json pass
CSV rows: seed987_branch_summary.csv has 3 data rows
diagnostics CSV rows: seed987_objective_diagnostics.csv has 18 data rows
base margins figure: 1600x960 RGBA, nonwhite_fraction=0.466273
objective heatmap: 1600x919 RGBA, nonwhite_fraction=0.615909
offset figure: 1600x960 RGBA, nonwhite_fraction=0.391625
visual inspection: all three figures are readable and support the conclusion
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed1597 target0
```

## Next Decision

Continue full-ringdown replication with seed1597 target0, sources=8, Tx/Rx=60.
