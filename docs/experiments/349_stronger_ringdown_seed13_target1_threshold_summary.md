# Experiment 349: Stronger Ringdown Seed13 Target-1 Threshold Summary

## Purpose

Run 815 aggregates the seed13 target-1 stronger-ringdown threshold branch from
runs 809-814. It is a CPU summary of six completed GPU coordinate-optimizer
runs, intended to close the target-1 branch before moving the stronger
ringdown stress to another target.

## 815: Stronger Ringdown Seed13 Target-1 Threshold Summary

Output:

```text
outputs/experiments/815_stronger_ringdown_seed13_target1_threshold_summary
```

Source runs:

| Run | Tracker | Ringdown scale | Base margin | Offset from cutoff | Confidence |
| ---: | ---: | ---: | ---: | ---: | --- |
| 809 | 343 | 0.450000 | 5.030490e-04 | +3.049e-06 | moderate |
| 813 | 347 | 0.456250 | 5.015250e-04 | +1.525e-06 | moderate |
| 814 | 348 | 0.459375 | 5.007215e-04 | +7.215e-07 | moderate |
| 812 | 346 | 0.462500 | 4.998907e-04 | -1.093e-07 | weak |
| 811 | 345 | 0.475000 | 4.963021e-04 | -3.698e-06 | weak |
| 810 | 344 | 0.500000 | 4.879320e-04 | -1.207e-05 | weak |

## Result

The final target-1 production base-confidence threshold bracket is:

```text
lower pass: run 814, ringdown scale 0.459375, margin 5.007215e-04
upper weak: run 812, ringdown scale 0.462500, margin 4.998907e-04
bracket width: 0.003125
midpoint estimate: 0.4609375
```

All six base rows preserve exact final geometry, and all 36 diagnostic
objective rows preserve the true target-1 geometry. The base margins strictly
decrease as ringdown scale increases.

## Interpretation

The target-1 stronger-ringdown branch is now precise enough to close. The
limiting effect is confidence margin, not geometry selection: every run still
selects x=250 mm, z=100 mm, r=6.0 mm for target 1, but the production base
margin crosses the `5e-04` cutoff between 0.459375 and 0.4625.

The diagnostic objective curves support the same interpretation. The base row
is the limiting objective. Early-high is close to the cutoff but remains above
it, while highband, late, late-high, and very-high keep larger
truth-preserving margins.

## Validation

```text
JSON parse: ringdown_threshold_summary.json and run_manifest.json pass
CSV rows: threshold rows=6, objective rows=36
figure validation: base_margin_threshold_curve.png is 1980x1116 RGB with nonwhite_fraction=0.085 and full 0-255 dynamic range
figure validation: objective_variant_margin_curves.png is 2052x1170 RGB with nonwhite_fraction=0.101 and full 0-255 dynamic range
visual inspection: both summary figures are readable and show the threshold bracket clearly
figure notes: figures/FIGURE_NOTES.md present
source validation: all base rows exact; all diagnostic objective rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Move the stronger-ringdown stress to another target instead of continuing to
slice target 1. Use ringdown0459375 because it is the highest passing target-1
stress level. Start with seed13 target 2 at 9 sources and Tx/Rx=60 because it
was the weaker remaining seed13 policy target at ringdown035.

