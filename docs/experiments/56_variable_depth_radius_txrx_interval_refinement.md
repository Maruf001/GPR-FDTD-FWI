# Experiment 56: Variable-Depth/Radius Tx/Rx Interval Refinement

## Goal

Continue the acquisition-geometry branch from experiment 55 by changing Tx/Rx
offset instead of source count:

```text
Does a larger Tx/Rx offset tighten the seed55 final-state target-0 and target-2
z/r ambiguity intervals more effectively than adding sources at 20 mm offset?
```

Common setup:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise, seed 55
5 sources
Tx/Rx offset 35 mm
```

## 485: Target-0 Final-State z/r Check At 35 mm Tx/Rx

Output:

```text
outputs/experiments/485_coordinate_optimizer_variable_depth_radius_seed55_target0_final_zr_txrx35
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 35 mm, seed55 replication cases, target index 0 only, x fixed,
z offsets 0:1:1 from z=80 mm, and radius offsets 0:1.25:0.25 from r=5 mm.
```

Runtime:

```text
194.9 s
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
| noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 2.414e-04 | weak | z=80, r=5.0-5.25 |
| source_mismatch_noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 4.006e-04 | weak | z=80, r=5.0-5.25 |

Comparison:

```text
20 mm / 5-source target-0 update-case margin: 3.503e-04, interval z=80-81, r=5.0-6.0
20 mm / 7-source target-0 update-case margin: 6.572e-04, interval z=80-81, r=5.0-5.75
35 mm / 5-source target-0 update-case margin: 4.006e-04, interval z=80, r=5.0-5.25
```

Interpretation:

```text
The 35 mm Tx/Rx offset does not produce a large margin, but it removes the
z=81 competing branch from the ambiguity interval and leaves only a local
5.0-5.25 mm radius interval. For target 0, offset geometry tightens the
interval shape more than it improves the absolute best-vs-next gap.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 68.1163
```

## 486: Target-2 Final-State z/r Check At 35 mm Tx/Rx

Output:

```text
outputs/experiments/486_coordinate_optimizer_variable_depth_radius_seed55_target2_final_zr_txrx35
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 5 sources,
Tx/Rx offset 35 mm, seed55 replication cases, target index 2 only, x fixed,
z offsets -1:0:1 from z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
162.3 s
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
| noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 4.104e-04 | weak | z=119-120, r=7.25-8.0 |
| source_mismatch_noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 6.826e-04 | moderate | z=120, r=8.0 |

Comparison:

```text
20 mm / 5-source target-2 coupled update-case margin: 1.083e-03, interval z=119-120, r=7.25-8.0
20 mm / 7-source target-2 update-case margin: 7.067e-04, interval z=119-120, r=7.25-8.0
35 mm / 5-source target-2 update-case margin: 6.826e-04, interval z=120, r=8.0
```

Interpretation:

```text
The 35 mm Tx/Rx offset collapses the source-mismatch target-2 ambiguity
interval to the exact point, even though the clean-noise row remains weak and
keeps the z=119/r=7.25 branch. Like target 0, geometry offset changes the
ambiguity structure more than it increases absolute radius margin.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 72.8655
```

## 487: 35 mm Tx/Rx Final-Interval Aggregate

Output:

```text
outputs/experiments/487_variable_depth_radius_seed55_txrx35_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 485 and 486.
```

Aggregate metrics:

```text
rows: 4
truth-geometry rows: 4
confidence labels: weak=3, moderate=1
minimum radius margin: 2.414e-04
maximum x/z/r ambiguity widths: 0.0 / 1.0 / 0.75 mm
target-0 rows: 2, truth-geometry rows: 2, weakest radius margin: 2.414e-04
target-2 rows: 2, truth-geometry rows: 2, weakest radius margin: 4.104e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1718x971 px, dynamic range 255, grayscale std 57.9102

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 41.8799
```

Figure notes:

```text
outputs/experiments/487_variable_depth_radius_seed55_txrx35_final_interval_summary/figures/FIGURE_NOTES.md
```

## Interpretation

At 35 mm Tx/Rx offset, the final-state point estimates remain exact and the
ambiguity intervals improve in structure:

```text
target 0: z ambiguity collapses to z=80, radius interval narrows to 5.0-5.25.
target 2: source-mismatch ambiguity collapses to z=120/r=8.0, but clean row
          still keeps z=119-120 and r=7.25-8.0.
```

The absolute margins are still weak/moderate, so this is an interval-tightening
result rather than a high-confidence point-size result.

## Next Decision

Tx/Rx offset is a more promising lever than source count for this branch's
remaining intervals, but 35 mm is not enough to make every row strong. The next
bounded acquisition test should either:

```text
1. try 50 mm Tx/Rx at the same final-state target-0/target-2 grids; or
2. stop acquisition changes and test a final-state high-frequency or weighted
   objective variant.
```
