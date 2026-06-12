# Experiment 391: Seed21 Target-0 Ringdown Threshold Summary

## Purpose

Run 857 summarizes the seed21 target-0 8-source Tx/Rx=60 ringdown threshold
branch after runs 852-856 refined the cutoff-scale boundary.

## 857: Seed21 Target-0 Ringdown Threshold Summary

Output:

```text
outputs/experiments/857_seed21_target0_ringdown_threshold_summary
```

Source rows:

| Run | Tracker | Sources | Nominal ringdown | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 848 | 382 | 8 | 0.4750000000 | 5.086877e-04 | +8.688e-06 | accepted |
| 849 | 383 | 8 | 0.4937500000 | 5.003891e-04 | +3.891e-07 | accepted |
| 854 | 388 | 8 | 0.4945312500 | 5.000315e-04 | +3.148e-08 | accepted |
| 856 | 390 | 8 | 0.4947265625 | 4.999420e-04 | -5.805e-08 | rejected |
| 855 | 389 | 8 | 0.4949218750 | 4.998524e-04 | -1.476e-07 | rejected |
| 853 | 387 | 8 | 0.4953125000 | 4.996730e-04 | -3.270e-07 | rejected |
| 852 | 386 | 8 | 0.4968750000 | 4.989535e-04 | -1.046e-06 | rejected |
| 846 | 380 | 8 | 0.5000000000 | 4.975041e-04 | -2.496e-06 | rejected |
| 847 | 381 | 9 | 0.5000000000 | 4.718459e-04 | -2.816e-05 | rejected rescue |

## Result

The highest accepted 8-source row is run 854:

```text
nominal ringdown: 0.49453125
margin: 5.000314833767e-04
offset from cutoff: +3.148e-08
```

The nearest rejected 8-source row is run 856:

```text
nominal ringdown: 0.4947265625
margin: 4.999419531073e-04
offset from cutoff: -5.805e-08
```

Final accepted/failed interval:

```text
[0.49453125, 0.4947265625)
interval width: 0.0001953125
```

## Interpretation

The practical seed21 target-0 threshold is run 854, but it is a razor-edge
threshold rather than a robust reserve. Ringdown050 remains rejected, and the
9-source rescue from run 847 is weaker than the 8-source ringdown050 row.

All production rows recover the true target-0 geometry. The failure mode is
radius confidence margin, not geometry selection. Late and late_high
diagnostic objectives remain below cutoff across the branch while preserving
truth.

## Validation

```text
JSON parse: seed21_target0_ringdown_threshold_summary.json and run_manifest.json pass
CSV rows: threshold rows=9, objective rows=54
figure validation: threshold curve is 1725x1020 RGB with nonwhite_fraction=0.047040 and full 0-255 dynamic range
figure validation: threshold zoom is 1575x930 RGB with nonwhite_fraction=0.140397 and full 0-255 dynamic range
figure validation: objective heatmap is 1725x960 RGB with nonwhite_fraction=0.583213 and full 0-255 dynamic range
visual inspection: curve, zoom, and heatmap are readable; labels fit; final bracket and 9-source rescue are visible
source validation: all production rows recover true target-0 geometry; accepted interval is bracketed by run 854 and run 856
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Use run 854 as the practical seed21 target-0 threshold point and run 856 as
the nearest rejected point. Continue with cross-seed stress synthesis or a new
non-redundant physical branch; do not continue target-0 midpoint bracketing
unless a stricter numerical threshold is explicitly needed.
