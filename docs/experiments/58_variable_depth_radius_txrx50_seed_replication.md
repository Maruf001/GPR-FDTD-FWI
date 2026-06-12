# Experiment 58: Variable-Depth/Radius Tx/Rx 50 mm Seed Replication

## Goal

Replicate experiment 57's Tx/Rx=50 mm final-state interval check on seed34 and
package a two-seed acquisition summary:

```text
Does the 50 mm Tx/Rx geometry keep the exact final-state point estimates and
the narrowed z/r intervals when the noise seed changes from 55 to 34?
```

Common setup:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise
5 sources
Tx/Rx offset 50 mm
```

## 491: Seed34 Target-0 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/491_coordinate_optimizer_variable_depth_radius_seed34_target0_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed34 replication cases, target index 0 only, x fixed,
z offsets 0:1:1 from z=80 mm, and radius offsets 0:1.25:0.25 from r=5 mm.
```

Runtime:

```text
196.7 s
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
| noise10_seed34 | 150 / 80 / 5.0 | 5.25 | 2.541e-04 | weak | z=80, r=5.0-5.25 |
| source_mismatch_noise10_seed34 | 150 / 80 / 5.0 | 5.25 | 3.618e-04 | weak | z=80, r=5.0-5.25 |

Interpretation:

```text
Target 0 remains point-correct and loses the previous z=80-81 ambiguity, but
unlike seed55 the source-mismatch row does not collapse to a single radius
point. The replicated 50 mm geometry therefore supports z-interval collapse
and radius narrowing, not strong target-0 point-radius confidence.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 60.8077
```

## 492: Seed34 Target-2 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/492_coordinate_optimizer_variable_depth_radius_seed34_target2_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed34 replication cases, target index 2 only, x fixed,
z offsets -1:0:1 from z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
163.5 s
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
| noise10_seed34 | 350 / 120 / 8.0 | 7.25 | 3.306e-04 | weak | z=120, r=8.0 |
| source_mismatch_noise10_seed34 | 350 / 120 / 8.0 | 7.25 | 7.536e-04 | moderate | z=120, r=8.0 |

Interpretation:

```text
Target 2 reproduces the seed55 result: both clean-noise and source-mismatch
rows are exact point intervals for z/r, with the mismatch row reaching the
moderate confidence label.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.8503
```

## 493: Seed34 50 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/493_variable_depth_radius_seed34_txrx50_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 491 and 492.
```

Aggregate metrics:

```text
rows: 4
truth-geometry rows: 4
confidence labels: weak=3, moderate=1
minimum radius margin: 2.541e-04
mean radius margin: 4.250e-04
maximum radius margin: 7.536e-04
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
target-0 rows: 2, truth-geometry rows: 2, weakest radius margin: 2.541e-04
target-2 rows: 2, truth-geometry rows: 2, weakest radius margin: 3.306e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1718x971 px, dynamic range 255, grayscale std 54.7703

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 37.8173
```

Figure notes:

```text
outputs/experiments/493_variable_depth_radius_seed34_txrx50_final_interval_summary/figures/FIGURE_NOTES.md
```

## 494: Seed34+Seed55 50 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/494_variable_depth_radius_seed34_seed55_txrx50_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 488, 489, 491, and 492.
```

Aggregate metrics:

```text
rows: 8
truth-geometry rows: 8
confidence labels: weak=6, moderate=2
minimum radius margin: 1.922e-04
mean radius margin: 4.170e-04
maximum radius margin: 7.536e-04
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
target-0 rows: 4, truth-geometry rows: 4, weakest radius margin: 1.922e-04
target-2 rows: 4, truth-geometry rows: 4, weakest radius margin: 3.306e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1720x971 px, dynamic range 255, grayscale std 56.0951

coordinate_ambiguity_widths.png:
1720x971 px, dynamic range 255, grayscale std 40.2068
```

Figure notes:

```text
outputs/experiments/494_variable_depth_radius_seed34_seed55_txrx50_final_interval_summary/figures/FIGURE_NOTES.md
```

## Interpretation

Tx/Rx=50 mm is now replicated on seed34 and seed55 for final-state target-0
and target-2 z/r interval checks:

```text
target 0: exact point estimate in all four rows; z ambiguity is zero, but the
          radius interval remains 5.0-5.25 mm in three of four rows.
target 2: exact z=120/r=8.0 interval in all four rows; source-mismatch rows
          are moderate and clean rows remain weak.
aggregate: 8/8 rows are truth geometry, x/z ambiguity is zero, and maximum
           radius ambiguity width is 0.25 mm.
```

This promotes Tx/Rx=50 mm from a seed55-only observation to the leading tested
acquisition geometry for narrowing final-state intervals. It does not promote
the radius estimates to strong point-size confidence; the best-vs-next
objective gaps remain weak or moderate.

## Next Decision

The next bounded step should complete one of:

```text
1. replicate the same Tx/Rx=50 mm final-state check on seed13 for a three-seed
   acquisition summary; or
2. hold Tx/Rx=50 mm fixed and test a weighted/high-frequency objective that
   specifically targets the target-0 5.0-5.25 mm residual interval.
```
