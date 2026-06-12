# Experiment 448: Seed2584 Ringdown050 Target-Specific Rescue Summary

## Purpose

Run 914 consolidates the seed2584 branch after target0 failed at the 8-source
control, target0 passed a 9-source rescue, and target2 and target1 passed at
the 5-source controls.

## 914: Seed2584 Ringdown050 Target-Specific Rescue Summary

Output:

```text
outputs/experiments/914_seed2584_ringdown050_target_specific_rescue_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
910-913. No new FDTD scene was launched for this summary.
```

Source runs:

```text
910 target0 sources=8 ringdown050
911 target0 sources=9 ringdown050
912 target2 sources=5 ringdown050
913 target1 sources=5 ringdown050
```

## Results

Summary counts:

```text
row count: 4
diagnostic objective rows: 24
accepted runs: 911, 912, 913
rejected truth-preserving runs: 910
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| target0 | 911 | 9 | 5.468829e-04 | +4.688295e-05 | accepted |
| target2 | 912 | 5 | 5.528720e-04 | +5.287201e-05 | accepted |
| target1 | 913 | 5 | 5.254512e-04 | +2.545123e-05 | accepted |

Target0 rescue:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 910 | 8 | 4.822702e-04 | -1.772975e-05 | rejected |
| 911 | 9 | 5.468829e-04 | +4.688295e-05 | accepted |

## Interpretation

Seed2584 is accepted after one source-density rescue. Every row preserves the
true geometry, but the 8-source target0 row falls below cutoff. The 9-source
target0 rescue clears cutoff with a healthier reserve than the seed1597 target1
rescue, while target2 and target1 need no rescue at the 5-source control.

Use seed2584 as evidence that the target-specific policy should keep the
rescue branch targeted: increase source density only for the failing target
before changing ringdown or objective windows.

## Validation

```text
JSON parse: run_manifest.json and seed2584_branch_summary.json pass
CSV rows: seed2584_branch_summary.csv has 4 data rows
diagnostics CSV rows: seed2584_objective_diagnostics.csv has 24 data rows
base margins figure: 1839x960 RGBA, nonwhite_fraction=0.433435
objective heatmap: 1839x960 RGBA, nonwhite_fraction=0.630360
target0 rescue trend: 1520x960 RGBA, nonwhite_fraction=0.045302
visual inspection: all three figures are readable; target0 rescue trend labels are clear after regeneration
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU was moved to seed4181 target0
```

## Next Decision

Continue full-ringdown replication with seed4181 target0, sources=8, Tx/Rx=60.
