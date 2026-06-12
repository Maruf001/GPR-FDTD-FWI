# Experiment 57: Variable-Depth/Radius Tx/Rx 50 mm Interval Refinement

## Goal

Extend experiment 56's 35 mm Tx/Rx offset result to a larger 50 mm offset:

```text
Does Tx/Rx=50 mm collapse the seed55 final-state target-0 and target-2 z/r
ambiguity intervals while preserving the exact point estimates?
```

Common setup:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise, seed 55
5 sources
Tx/Rx offset 50 mm
```

## 488: Target-0 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/488_coordinate_optimizer_variable_depth_radius_seed55_target0_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed55 replication cases, target index 0 only, x fixed,
z offsets 0:1:1 from z=80 mm, and radius offsets 0:1.25:0.25 from r=5 mm.
```

Runtime:

```text
196.0 s
```

Final state:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
```

Confidence rows:

| Case | Best x/z/r [mm] | Next radius [mm] | Margin | Label | Ambiguity interval |
| --- | --- | ---: | ---: | --- | --- |
| noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 1.922e-04 | weak | z=80, r=5.0-5.25 |
| source_mismatch_noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 4.215e-04 | weak | z=80, r=5.0 |

Comparison:

```text
20 mm / 5-source target-0 update interval: z=80-81, r=5.0-6.0
35 mm / 5-source target-0 update interval: z=80, r=5.0-5.25
50 mm / 5-source target-0 update interval: z=80, r=5.0
```

Interpretation:

```text
For target 0, the 50 mm offset collapses the source-mismatch ambiguity interval
to the exact point but still leaves a weak clean-noise row with a 5.0-5.25 mm
local radius interval. This is interval collapse for the injected mismatch
case, not a strong-margin radius claim.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 67.0204
```

## 489: Target-2 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/489_coordinate_optimizer_variable_depth_radius_seed55_target2_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed55 replication cases, target index 2 only, x fixed,
z offsets -1:0:1 from z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
161.8 s
```

Final state:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
```

Confidence rows:

| Case | Best x/z/r [mm] | Next radius [mm] | Margin | Label | Ambiguity interval |
| --- | --- | ---: | ---: | --- | --- |
| noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 3.375e-04 | weak | z=120, r=8.0 |
| source_mismatch_noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 6.847e-04 | moderate | z=120, r=8.0 |

Comparison:

```text
20 mm / 5-source target-2 update interval: z=119-120, r=7.25-8.0
35 mm / 5-source target-2 update interval: update case z=120, r=8.0, clean row still z=119-120, r=7.25-8.0
50 mm / 5-source target-2 interval: z=120, r=8.0 in both rows
```

Interpretation:

```text
For target 2, Tx/Rx=50 mm collapses both clean and source-mismatch ambiguity
intervals to the exact point. The margins remain weak/moderate, but the
near-best z=119/r=7.25 branch is outside the configured ambiguity threshold.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 70.7119
```

## 490: 50 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/490_variable_depth_radius_seed55_txrx50_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 488 and 489.
```

Aggregate metrics:

```text
rows: 4
truth-geometry rows: 4
confidence labels: weak=3, moderate=1
minimum radius margin: 1.922e-04
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
target-0 rows: 2, truth-geometry rows: 2, weakest radius margin: 1.922e-04
target-2 rows: 2, truth-geometry rows: 2, weakest radius margin: 3.375e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1718x971 px, dynamic range 255, grayscale std 56.6733

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 36.3521
```

Figure notes:

```text
outputs/experiments/490_variable_depth_radius_seed55_txrx50_final_interval_summary/figures/FIGURE_NOTES.md
```

## Interpretation

Tx/Rx=50 mm is the best acquisition geometry tested for the seed55 final-state
intervals:

```text
target 0: source-mismatch row collapses to z=80/r=5.0; clean row remains a
          weak 5.0-5.25 mm radius interval.
target 2: both clean and source-mismatch rows collapse to z=120/r=8.0.
aggregate: z ambiguity is zero and maximum radius ambiguity is 0.25 mm.
```

The caveat is still important: confidence labels remain weak/moderate because
the best-vs-next gaps are small in absolute terms. Use this as acquisition
interval-shaping evidence, not as a strong point-size margin.

## Next Decision

For variable-depth/variable-radius final-state interval refinement, Tx/Rx=50 mm
is more effective than adding sources or using Tx/Rx=35 mm. The next bounded
step should be one of:

```text
1. replicate Tx/Rx=50 mm final-state checks on seed34 before promoting it as
   branch guidance; or
2. hold acquisition fixed and test a weighted/high-frequency objective on the
   seed55 final-state intervals.
```
