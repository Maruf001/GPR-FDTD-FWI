# Experiment 60: Variable-Depth/Radius Tx/Rx 50 mm Objective Variant Diagnostic

## Goal

Hold the best acquisition geometry from experiment 59 fixed and test whether a
targeted objective variant improves the remaining final-state radius
confidence:

```text
At Tx/Rx=50 mm, can a time-window/bandpass objective widen the target-0
5.0 vs 5.25 mm gap without changing the correct x/z/r branch?
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

Objective variants:

| Label | Time window [ns] | Bandpass [GHz] | Purpose |
| --- | --- | --- | --- |
| base | 1.0-7.0 | none | Current reporting objective |
| highband | 1.0-7.0 | 1.1-3.4 | Existing highband diagnostic |
| late | 1.5-5.5 | none | Late scattered-field emphasis |
| late_high | 1.5-5.5 | 1.1-3.4 | Late highband emphasis |
| veryhigh | 1.0-7.0 | 1.8-4.2 | More aggressive high-frequency emphasis |
| early_high | 0.8-3.5 | 1.1-3.4 | Early highband guard |

## 499: Target-0 Three-Seed Objective Variant Sweep

Output:

```text
outputs/experiments/499_coordinate_optimizer_variable_depth_radius_target0_txrx50_three_seed_objective_variants
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, target index 0 only, six seed/case rows, x fixed,
z offsets 0:1:1 from z=80 mm, radius offsets 0:1.25:0.25 from r=5 mm, and
the six diagnostic objective variants listed above.
```

Runtime:

```text
197.4 s
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
minimum / mean / maximum radius margin: 1.884e-04 / 2.896e-04 / 4.215e-04
moderate-or-better rows: 0/6
```

Veryhigh diagnostic margins:

```text
truth rows: 6/6
geometry changes relative to base: 0
minimum / mean / maximum radius margin: 3.400e-04 / 4.856e-04 / 6.373e-04
moderate-or-better rows: 2/6
margin ratio to base: min=1.512, mean=1.742, max=2.303
veryhigh ambiguity intervals: all exact at z=80 mm, r=5.0 mm
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 59.4530
```

## 500: Target-0 Objective Diagnostic Report

Output:

```text
outputs/experiments/500_variable_depth_radius_target0_txrx50_three_seed_objective_variant_report
```

Command:

```text
run_coordinate_objective_diagnostic_report.py over coordinate summary 499.
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Mean margin ratio |
| --- | ---: | ---: | ---: | ---: |
| early_high | 6 | 6 | 0 | 0.656 |
| highband | 6 | 6 | 0 | 0.907 |
| late | 6 | 6 | 0 | 0.797 |
| late_high | 6 | 6 | 0 | 0.736 |
| veryhigh | 6 | 6 | 0 | 1.742 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
3181x1005 px, dynamic range 255, grayscale std 66.6519
```

Figure notes:

```text
outputs/experiments/500_variable_depth_radius_target0_txrx50_three_seed_objective_variant_report/figures/FIGURE_NOTES.md
```

## 501: Target-2 Three-Seed Objective Variant Guardrail Sweep

Output:

```text
outputs/experiments/501_coordinate_optimizer_variable_depth_radius_target2_txrx50_three_seed_objective_variants
```

Command pattern:

```text
same as run 499, but target index 2 only, x fixed, z offsets -1:0:1 from
z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
163.4 s
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
minimum / mean / maximum radius margin: 3.099e-04 / 4.966e-04 / 7.536e-04
moderate-or-better rows: 3/6
```

Veryhigh diagnostic margins:

```text
truth rows: 6/6
geometry changes relative to base: 0
minimum / mean / maximum radius margin: 6.661e-04 / 8.950e-04 / 1.132e-03
moderate-or-better rows: 6/6
strong rows: 2/6
veryhigh ambiguity intervals: all exact at z=120 mm, r=8.0 mm
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 66.9820
```

## 502: Target-0/Target-2 Objective Diagnostic Report

Output:

```text
outputs/experiments/502_variable_depth_radius_target0_target2_txrx50_three_seed_objective_variant_report
```

Command:

```text
run_coordinate_objective_diagnostic_report.py over coordinate summaries 499 and 501.
```

Objective ratio summary:

| Objective | Rows | Truth rows | Geometry changes | Mean margin ratio |
| --- | ---: | ---: | ---: | ---: |
| early_high | 12 | 12 | 0 | 0.617 |
| highband | 12 | 12 | 0 | 0.954 |
| late | 12 | 12 | 0 | 1.316 |
| late_high | 12 | 12 | 0 | 1.273 |
| veryhigh | 12 | 12 | 0 | 1.831 |

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
6343x1005 px, dynamic range 255, grayscale std 68.6975
```

Figure notes:

```text
outputs/experiments/502_variable_depth_radius_target0_target2_txrx50_three_seed_objective_variant_report/figures/FIGURE_NOTES.md
```

## 503: Target-0/Target-2 Objective Confidence Report

Output:

```text
outputs/experiments/503_variable_depth_radius_target0_target2_txrx50_objective_confidence_report
```

Code update:

```text
run_coordinate_objective_diagnostic_report.py now also writes
coordinate_objective_confidence_rows.csv by rebuilding confidence and
ambiguity rows from the saved per-step objective_results.
```

Focused test:

```text
/home/lam001/miniforge3/envs/FNO/bin/python -m pytest tests/test_coordinate_objective_diagnostic_report.py -q
8 passed in 0.18 s
```

Command:

```text
run_coordinate_objective_diagnostic_report.py over coordinate summaries 499 and 501.
```

Objective-confidence summary:

| Objective | Rows | Truth rows | Labels | Max x/z/r ambiguity [mm] |
| --- | ---: | ---: | --- | --- |
| base | 12 | 12 | weak=9, moderate=3 | 0 / 0 / 0.25 |
| early_high | 12 | 12 | weak=12 | 0 / 0 / 0 |
| highband | 12 | 12 | weak=9, moderate=3 | 0 / 0 / 0 |
| late | 12 | 12 | weak=6, moderate=4, strong=2 | 0 / 0 / 0.25 |
| late_high | 12 | 12 | weak=6, moderate=4, strong=2 | 0 / 0 / 0 |
| veryhigh | 12 | 12 | weak=4, moderate=6, strong=2 | 0 / 0 / 0 |

Veryhigh confidence metrics:

```text
minimum / mean / maximum radius margin: 3.400e-04 / 6.903e-04 / 1.132e-03
confidence labels: weak=4, moderate=6, strong=2
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.0 mm
```

Plot validation:

```text
coordinate_objective_diagnostic_ratios.png:
6343x1005 px, dynamic range 255, grayscale std 68.6975
```

Figure notes:

```text
outputs/experiments/503_variable_depth_radius_target0_target2_txrx50_objective_confidence_report/figures/FIGURE_NOTES.md
```

## Interpretation

The veryhigh objective is the only tested variant that consistently improves
the target-0 residual radius gap while preserving the true branch:

```text
target 0: veryhigh keeps all six rows exact and collapses the diagnostic
          ambiguity interval to r=5.0 mm, but only 2/6 rows cross the
          moderate absolute-margin threshold.
target 2: veryhigh keeps all six rows exact, all rows become moderate or
          better, and two source-mismatch rows become strong.
combined: 12/12 truth rows, zero geometry changes, mean margin ratio 1.831;
          run 503 records veryhigh labels weak=4, moderate=6, strong=2 and
          zero x/z/r ambiguity width.
```

This is the first objective-level lever that improves the final-state interval
evidence after the Tx/Rx=50 acquisition package. It should be treated as a
diagnostic/reporting objective until the update rule and confidence reporting
are deliberately extended to produce objective-specific confidence rows.

## Next Decision

The objective-specific confidence reporting is now packaged in run 503. Use
the veryhigh objective as a final-state reporting diagnostic for target 0 and
target 2 at Tx/Rx=50 mm. The center-target guardrail is handled next in
experiment 61.
