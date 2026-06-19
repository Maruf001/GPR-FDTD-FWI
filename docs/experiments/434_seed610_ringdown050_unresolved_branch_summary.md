# Experiment 434: Seed610 Ringdown050 Unresolved Branch Summary

## Purpose

Run 901 consolidates the seed610 branch after target0 barely passed and
target1/target2 remained exact but weak through source-density and ringdown-only
controls.

## 901: Seed610 Ringdown050 Unresolved Branch Summary

Output:

```text
outputs/experiments/901_seed610_ringdown050_unresolved_branch_summary
```

Generation:

```text
CPU-side structured aggregation of completed coordinate-optimizer outputs
887-899. No new FDTD scene was launched for this summary.
```

Source runs:

```text
887 target0 sources=8 ringdown050
888 target2 sources=5 ringdown050
889 target2 sources=9 ringdown050
890 target2 sources=11 ringdown050
891 target2 sources=9 ringdown049453125
892 target2 sources=9 ringdown0475
893 target2 sources=9 ringdown0459375
894 target2 sources=9 ringdown040
895 target2 sources=9 ringdown035
896 target2 sources=9 ringdown025
897 target1 sources=5 ringdown050
898 target1 sources=9 ringdown050
899 target1 sources=8 ringdown050
```

## Results

Summary counts:

```text
row count: 13
diagnostic objective rows: 78
accepted runs: 887
rejected truth-preserving runs: 888-899
cutoff: 5.0e-4
```

Best row by target:

| Target | Best run | Sources | Ringdown | Base margin | Offset from cutoff | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| target0 | 887 | 8 | 0.50 | 5.005897e-04 | +5.897e-07 | accepted |
| target1 | 897 | 5 | 0.50 | 4.677410e-04 | -3.226e-05 | rejected |
| target2 | 894 | 9 | 0.40 | 4.969192e-04 | -3.081e-06 | rejected |

Target1 simple aperture branch:

| Run | Sources | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 897 | 5 | 4.677410e-04 | -3.226e-05 | rejected |
| 899 | 8 | 4.205166e-04 | -7.948e-05 | rejected |
| 898 | 9 | 4.197879e-04 | -8.021e-05 | rejected |

Target2 ringdown branch:

| Run | Ringdown | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | --- |
| 889 | 0.50 | 4.802438e-04 | -1.976e-05 | rejected |
| 891 | 0.49453125 | 4.818309e-04 | -1.817e-05 | rejected |
| 892 | 0.475 | 4.869258e-04 | -1.307e-05 | rejected |
| 893 | 0.459375 | 4.903121e-04 | -9.688e-06 | rejected |
| 894 | 0.40 | 4.969192e-04 | -3.081e-06 | rejected |
| 895 | 0.35 | 4.942263e-04 | -5.774e-06 | rejected |
| 896 | 0.25 | 4.677785e-04 | -3.222e-05 | rejected |

## Interpretation

Seed610 is a broad low-margin seed, not a single bad target row. Target0 clears
the cutoff by only 5.897e-07. Target1 is best at the 5-source control and gets
worse at 8 and 9 sources. Target2 is closest at ringdown040 but still misses
the cutoff and becomes non-monotone at lower ringdown.

The important positive evidence is that every rejected row is truth-preserving:
the optimizer keeps the correct x/z/r geometry as rank 1. The unresolved issue
is radius-margin reserve. That means another simple source-count or ringdown
test is unlikely to add useful information; a seed610 revisit should use a
specialized aperture/objective design rather than extending the exhausted
branches.

## Validation

```text
JSON parse: run_manifest.json and seed610_branch_summary.json pass
CSV rows: seed610_branch_summary.csv has 13 data rows
diagnostics CSV rows: seed610_objective_diagnostics.csv has 78 data rows
base margins figure: 2400x960 RGBA, nonwhite_fraction=0.259229
objective heatmap: 2400x768 RGBA, nonwhite_fraction=0.623955
branch trends figure: 2080x768 RGBA, nonwhite_fraction=0.061759
visual inspection: all three figures are readable and support the conclusion
figure notes: figures/FIGURE_NOTES.md present and run-specific
resources: no new FDTD scene; GPU stayed occupied by the next production run
```

## Next Decision

Move GPU replication to seed987 target0 while keeping seed610 reserved for a
specialized objective/aperture follow-up if later cross-seed evidence justifies
it.

## 2026-06-17 Addendum

The specialized target1 acquisition-offset follow-up has now been run:

```text
run:      1224_coordinate_optimizer_variable_depth_radius_seed610_target1_sources5_txrx52p5_ringdown050_objectives
target:   target1
sources:  5
Tx/Rx:    52.5 mm
```

Run 1224 preserved exact x/z/r geometry and substantially improved the target1
base margin relative to the old Tx/Rx=60 source-count branch, but it remained
strictly weak:

| Run | Sources | Tx/Rx mm | Base margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 897 | 5 | 60.0 | 4.677410e-4 | -3.226e-5 | weak |
| 899 | 8 | 60.0 | 4.205166e-4 | -7.948e-5 | weak |
| 898 | 9 | 60.0 | 4.197879e-4 | -8.021e-5 | weak |
| 1224 | 5 | 52.5 | 4.962451e-4 | -3.755e-6 | weak near-miss |

The seed610 target1 policy remains exact-but-unresolved. The 52.5 mm aperture
is the best tested target1 setting for this seed, but it does not justify
relabelling the branch as accepted under the strict base-margin rule.
