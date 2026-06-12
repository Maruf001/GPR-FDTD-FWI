# Experiment 367: Seed13 Target-1 5-Source Acquisition Boundary Summary

## Purpose

Run 833 summarizes the controlled 5-source target-1 acquisition branch from
runs 829-832 and compares it with the earlier 9-source threshold branch from
runs 809-814. The goal is to decide whether to transfer ringdown0475 across
seeds or first probe a higher seed13 stress point.

## 833: Seed13 Target-1 5-Source Acquisition Boundary Summary

Output:

```text
outputs/experiments/833_seed13_target1_5source_acquisition_boundary_summary
```

Source runs:

| Source count | Runs | Ringdown scales |
| ---: | --- | --- |
| 9 | 809, 813, 814, 812, 811, 810 | 0.450000, 0.456250, 0.459375, 0.462500, 0.475000, 0.500000 |
| 5 | 829, 830, 831, 832 | 0.459375, 0.462500, 0.468750, 0.475000 |

## Result

The prior 9-source branch crosses the production cutoff between
ringdown0459375 and ringdown04625:

| Boundary | Run | Ringdown | Margin | Offset from cutoff | Confidence |
| --- | ---: | ---: | ---: | ---: | --- |
| 9-source lower pass | 814 | 0.459375 | 5.007215e-04 | +7.215e-07 | moderate |
| 9-source upper weak | 812 | 0.462500 | 4.998907e-04 | -1.093e-07 | weak |

The 5-source branch remains exact/moderate through ringdown0475:

| Run | Ringdown | Margin | Offset from cutoff | Confidence |
| ---: | ---: | ---: | ---: | --- |
| 829 | 0.459375 | 5.427631e-04 | +4.276e-05 | moderate |
| 830 | 0.462500 | 5.419127e-04 | +4.191e-05 | moderate |
| 831 | 0.468750 | 5.401188e-04 | +4.012e-05 | moderate |
| 832 | 0.475000 | 5.382033e-04 | +3.820e-05 | moderate |

Matched-stress acquisition gain:

| Ringdown scale | 5-source run | 9-source run | Delta margin | Ratio |
| ---: | ---: | ---: | ---: | ---: |
| 0.459375 | 829 | 814 | +4.204160e-05 | 1.084 |
| 0.462500 | 830 | 812 | +4.202201e-05 | 1.084 |
| 0.475000 | 832 | 811 | +4.190116e-05 | 1.084 |

All 60 objective diagnostic rows across the compared runs preserve the true
target-1 geometry.

## Interpretation

Run 833 shows that the 5-source aperture is not merely rescuing one borderline
case. Across all matched stress points, it adds about `4.2e-05` margin over
the 9-source acquisition. That is enough to move the old ringdown04625 weak
row to moderate and to keep ringdown0475 comfortably moderate.

The trend also suggests that ringdown050 is worth testing before transfer. The
old 9-source ringdown050 row was weak, but applying the observed matched-stress
gain would plausibly move it back above cutoff. This should be tested directly
rather than assumed.

## Validation

```text
JSON parse: seed13_target1_acquisition_boundary_summary.json and run_manifest.json pass
CSV rows: boundary rows=10, objective rows=60
figure validation: base_margin_acquisition_comparison.png is 1980x1170 RGBA with nonwhite_fraction=0.039141 and full 0-255 RGB-converted dynamic range
figure validation: shared_ringdown_margin_advantage.png is 1620x990 RGBA with nonwhite_fraction=0.534134 and full 0-255 RGB-converted dynamic range
visual inspection: both figures are readable after label-placement cleanup
source validation: all 5-source base rows exact/moderate; all 60 diagnostic rows truth-preserving
resources: CPU aggregation only; no GPU workload
```

## Next Decision

Run seed13 target 1 with the 5-source Tx/Rx=60 acquisition at ringdown050. If
it passes, summarize the 5-source upper stress shift and then start cross-seed
transfer; if it fails, bracket the 5-source upper boundary between
ringdown0475 and ringdown050.
