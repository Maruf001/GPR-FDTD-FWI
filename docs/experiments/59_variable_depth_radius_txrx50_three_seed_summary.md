# Experiment 59: Variable-Depth/Radius Tx/Rx 50 mm Three-Seed Summary

## Goal

Complete the seed13 replication requested by experiment 58 and package the
three-seed Tx/Rx=50 mm acquisition result:

```text
Does Tx/Rx=50 mm preserve exact final-state target-0 and target-2 point
estimates and keep z/r ambiguity narrow across seeds 13, 34, and 55?
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

## 495: Seed13 Target-0 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/495_coordinate_optimizer_variable_depth_radius_seed13_target0_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed13 replication cases, target index 0 only, x fixed,
z offsets 0:1:1 from z=80 mm, and radius offsets 0:1.25:0.25 from r=5 mm.
```

Runtime:

```text
195.8 s
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
| noise10_seed13 | 150 / 80 / 5.0 | 5.25 | 1.884e-04 | weak | z=80, r=5.0-5.25 |
| source_mismatch_noise10_seed13 | 150 / 80 / 5.0 | 5.25 | 3.198e-04 | weak | z=80, r=5.0-5.25 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 57.0722
```

## 496: Seed13 Target-2 Final-State z/r Check At 50 mm Tx/Rx

Output:

```text
outputs/experiments/496_coordinate_optimizer_variable_depth_radius_seed13_target2_final_zr_txrx50
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 50 mm, seed13 replication cases, target index 2 only, x fixed,
z offsets -1:0:1 from z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
162.2 s
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
| noise10_seed13 | 350 / 120 / 8.0 | 7.25 | 3.099e-04 | weak | z=120, r=8.0 |
| source_mismatch_noise10_seed13 | 350 / 120 / 8.0 | 7.25 | 5.634e-04 | moderate | z=120, r=8.0 |

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 64.9628
```

## 497: Seed13 50 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/497_variable_depth_radius_seed13_txrx50_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 495 and 496.
```

Aggregate metrics:

```text
rows: 4
truth-geometry rows: 4
confidence labels: weak=3, moderate=1
minimum radius margin: 1.884e-04
mean radius margin: 3.454e-04
maximum radius margin: 5.634e-04
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
target-0 rows: 2, truth-geometry rows: 2, weakest radius margin: 1.884e-04
target-2 rows: 2, truth-geometry rows: 2, weakest radius margin: 3.099e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1718x971 px, dynamic range 255, grayscale std 51.8201

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 37.7941
```

Figure notes:

```text
outputs/experiments/497_variable_depth_radius_seed13_txrx50_final_interval_summary/figures/FIGURE_NOTES.md
```

## 498: Three-Seed 50 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/498_variable_depth_radius_seed13_seed34_seed55_txrx50_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 488, 489, 491, 492, 495, and 496.
```

Aggregate metrics:

```text
rows: 12
truth-geometry rows: 12
confidence labels: weak=9, moderate=3
minimum radius margin: 1.884e-04
mean radius margin: 3.931e-04
maximum radius margin: 7.536e-04
maximum x/z/r ambiguity widths: 0.0 / 0.0 / 0.25 mm
target-0 rows: 6, truth-geometry rows: 6, weakest radius margin: 1.884e-04
target-2 rows: 6, truth-geometry rows: 6, weakest radius margin: 3.099e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1720x971 px, dynamic range 255, grayscale std 57.6840

coordinate_ambiguity_widths.png:
1720x971 px, dynamic range 255, grayscale std 44.4266
```

Figure notes:

```text
outputs/experiments/498_variable_depth_radius_seed13_seed34_seed55_txrx50_final_interval_summary/figures/FIGURE_NOTES.md
```

## Interpretation

Tx/Rx=50 mm is now replicated across the three staged-coordinate seeds:

```text
target 0: all six rows are exact at x=150/z=80/r=5.0, but every row remains
          weak; five of six rows retain the 5.0-5.25 mm ambiguity interval.
target 2: all six rows are exact at x=350/z=120/r=8.0; clean rows are weak,
          source-mismatch rows are moderate, and all ambiguity intervals are
          exact at z=120/r=8.0.
aggregate: 12/12 truth-geometry rows, zero x/z ambiguity, maximum radius
           ambiguity width 0.25 mm.
```

The acquisition conclusion is now stronger than experiment 58: 50 mm Tx/Rx is
the best tested final-state geometry for removing x/z interval ambiguity in
this branch. The radius-confidence conclusion is unchanged: target 0 remains a
weak 5.0-5.25 mm interval claim, and target 2 is point-supported but still only
weak/moderate by the current best-vs-next objective gaps.

## Next Decision

Do not spend more GPU time on source-count or Tx/Rx scalar escalation for this
branch until a new objective lever is tested. The next bounded research step is
a target-0 focused objective diagnostic at Tx/Rx=50 mm, using the same
final-state seed set and comparing base/highband or weighted high-frequency
variants against the 5.0-5.25 mm residual interval.
