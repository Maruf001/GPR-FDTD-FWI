# Experiment 62: Source-Shape Center Veryhigh Objective Transfer

## Goal

Test whether the veryhigh objective from the variable-depth/radius branch
transfers to the older coupled source-shape center-radius interval:

```text
Can the 1.8-4.2 GHz veryhigh objective collapse the remaining source-shape
center r=6.0 vs r=6.2 mm interval under ringdown/source mismatch?
```

This repeats the run 447 setup with additional objective variants.

Common setup:

```text
x=[150,250,350] mm
z=[90,90,90] mm
r=[6,6,6] mm
source mismatch + ringdown025 + 10% noise, seed 55
fit ringdown coefficient
target index 1 only
x/z fixed at truth
radius offsets -0.4:0.4:0.2 from r=6 mm
5 sources
```

Objective variants:

```text
base, highband, late, late_high, veryhigh, early_high
```

## 506: Source-Shape Center Objective Variant Sweep

Output:

```text
outputs/experiments/506_multi_rebar_coupled_source_shape_true_state_radius_veryhigh_objectives
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
fit-ringdown-coefficient, the run 447 source_mismatch_ringdown025_noise10_seed55
case, target index 1, x/z fixed, radius offsets -0.4:0.4:0.2, top-k 5, and
the six objective variants from experiment 60.
```

Runtime:

```text
161.9 s
```

Base final state:

```text
x=[150,250,350] mm
z=[90,90,90] mm
r=[6,6,6] mm
```

Objective rows:

| Objective | Best x/z/r [mm] | Next radius [mm] | Margin | Ratio to base | Label | Radius ambiguity |
| --- | --- | ---: | ---: | ---: | --- | --- |
| base | 250 / 90 / 6.0 | 6.2 | 1.006e-04 | 1.000 | weak | 6.0-6.2 |
| highband | 250 / 90 / 6.0 | 6.2 | 1.146e-04 | 1.139 | weak | 6.0 |
| late | 250 / 90 / 6.0 | 6.2 | 1.417e-04 | 1.408 | weak | 6.0-6.4 |
| late_high | 250 / 90 / 6.0 | 6.2 | 1.632e-04 | 1.622 | weak | 6.0 |
| veryhigh | 250 / 90 / 6.0 | 6.2 | 6.388e-05 | 0.635 | weak | 6.0 |
| early_high | 250 / 90 / 6.0 | 6.2 | 7.017e-05 | 0.697 | weak | 6.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 42.1151
```

## 507: Source-Shape Center Objective Confidence Report

Output:

```text
outputs/experiments/507_source_shape_center_true_state_veryhigh_objective_confidence_report
```

Command:

```text
run_coordinate_objective_diagnostic_report.py over coordinate summary 506.
```

Report result:

```text
rows: 5 diagnostic ratios
all variants preserve truth geometry
best absolute-margin variant: late_high at 1.632e-04, ratio 1.622x
veryhigh margin ratio: 0.635x
all objective-specific confidence labels: weak
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
2059x1005 px, dynamic range 255, grayscale std 72.3885
```

Figure notes:

```text
outputs/experiments/507_source_shape_center_true_state_veryhigh_objective_confidence_report/figures/FIGURE_NOTES.md
```

## Interpretation

The veryhigh objective does not transfer to the source-shape/ringdown center
interval:

```text
veryhigh preserves the correct geometry but reduces the absolute margin below
the base row.
late_high is the best tested transfer variant, but it is still weak and does
not reach the moderate absolute-margin threshold.
```

This keeps the source-shape branch interval-supported. The variable-depth /
variable-radius veryhigh diagnostic should be treated as branch-specific, not
as a universal high-frequency objective.

## Next Decision

Do not promote veryhigh globally. For the source-shape branch, keep reporting
the center target as a weak 6.0-6.2 mm interval unless a different physics
lever appears.
