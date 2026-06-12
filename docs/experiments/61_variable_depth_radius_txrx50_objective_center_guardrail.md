# Experiment 61: Variable-Depth/Radius Tx/Rx 50 mm Objective Center Guardrail

## Goal

Guard the veryhigh objective from experiment 60 on the center target before
considering it as a global final-state reporting diagnostic:

```text
Does the veryhigh objective preserve the center target and improve confidence
when z/r are varied around x=250 mm, z=100 mm, r=6 mm?
```

Common setup:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise
seeds 13, 34, and 55
5 sources
Tx/Rx offset 50 mm
```

Objective variants are the same as experiment 60:

```text
base, highband, late, late_high, veryhigh, early_high
```

## 504: Target-1 Three-Seed Objective Variant Guardrail

Output:

```text
outputs/experiments/504_coordinate_optimizer_variable_depth_radius_target1_txrx50_three_seed_objective_variants
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, target index 1 only, six seed/case rows, x fixed,
z offsets -1:1:1 from z=100 mm, radius offsets -1:1:0.25 from r=6 mm, and
the six diagnostic objective variants from experiment 60.
```

Runtime:

```text
439.2 s
```

Base final state:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
```

Base margins:

```text
rows: 6
truth rows: 6
minimum / mean / maximum radius margin: 1.777e-04 / 3.404e-04 / 4.836e-04
moderate-or-better rows: 0/6
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
```

Veryhigh diagnostic margins:

```text
truth rows: 6/6
geometry changes relative to base: 0
minimum / mean / maximum radius margin: 2.689e-04 / 5.734e-04 / 7.299e-04
moderate-or-better rows: 5/6
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 62.5567
```

## 505: All-Target Objective Confidence Report

Output:

```text
outputs/experiments/505_variable_depth_radius_all_targets_txrx50_objective_confidence_report
```

Command:

```text
run_coordinate_objective_diagnostic_report.py over coordinate summaries 499, 504, and 501.
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Mean margin ratio |
| --- | ---: | ---: | ---: | ---: |
| early_high | 18 | 18 | 0 | 0.603 |
| highband | 18 | 18 | 0 | 0.963 |
| late | 18 | 18 | 0 | 1.380 |
| late_high | 18 | 18 | 0 | 1.364 |
| veryhigh | 18 | 18 | 0 | 1.803 |

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 18 | 18 | weak=15, moderate=3 | 0 / 0 / 0.25 |
| early_high | 18 | 18 | weak=18 | 0 / 0 / 0 |
| highband | 18 | 18 | weak=15, moderate=3 | 0 / 0 / 0 |
| late | 18 | 18 | weak=9, moderate=7, strong=2 | 0 / 0 / 0.25 |
| late_high | 18 | 18 | weak=9, moderate=7, strong=2 | 0 / 0 / 0 |
| veryhigh | 18 | 18 | weak=5, moderate=11, strong=2 | 0 / 0 / 0 |

Veryhigh confidence metrics:

```text
minimum / mean / maximum radius margin: 2.689e-04 / 6.513e-04 / 1.132e-03
confidence labels: weak=5, moderate=11, strong=2
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
9505x1005 px, dynamic range 255, grayscale std 69.0722
```

Figure notes:

```text
outputs/experiments/505_variable_depth_radius_all_targets_txrx50_objective_confidence_report/figures/FIGURE_NOTES.md
```

## Interpretation

The center-target guardrail passes:

```text
target 1: veryhigh keeps all six rows exact and removes the base 6.0-6.25 mm
          clean-row radius ambiguity.
all targets: veryhigh keeps all 18 rows exact, has no geometry changes, and
             collapses x/z/r ambiguity widths to zero.
```

The result supports using veryhigh as a final-state reporting diagnostic for
the full variable-depth/variable-radius branch at Tx/Rx=50 mm. It still should
not silently replace the base update rule without explicit reporting, because
5/18 rows remain weak by the existing absolute confidence threshold.

## Next Decision

Do not run more scalar source-count or Tx/Rx geometry escalation for this
branch. The next bounded step should be either:

```text
1. add a compact all-target final-state summary that reports both base and
   veryhigh confidence rows side by side; or
2. move to a new physics stress, keeping run 498 as the base acquisition
   package and run 505 as the objective-confidence package.
```
