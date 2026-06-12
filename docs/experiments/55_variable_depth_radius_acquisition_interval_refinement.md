# Experiment 55: Variable-Depth/Radius Acquisition Interval Refinement

## Goal

Follow experiment 54's three-seed staged recovery with a bounded acquisition
check:

```text
Can increasing from 5 to 7 source positions collapse the remaining weak
target-0 and target-2 z/r ambiguity intervals in the seed55 final state?
```

This is not a new global search. It starts from the exact final seed55 state:

```text
x=[150,250,350] mm
z=[80,100,120] mm
r=[5,6,8] mm
source mismatch + 10% noise, seed 55
7 sources, Tx/Rx offset 20 mm
```

## 482: Target-0 Final-State z/r Check With 7 Sources

Output:

```text
outputs/experiments/482_coordinate_optimizer_variable_depth_radius_seed55_target0_final_zr_sources7
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 7 sources,
seed55 replication cases, target index 0 only, x fixed, z offsets 0:1:1 from
z=80 mm, and radius offsets 0:1.25:0.25 from r=5 mm.
```

Runtime:

```text
265.8 s
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
| noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 3.893e-04 | weak | z=80-81, r=5.0-6.0 |
| source_mismatch_noise10_seed55 | 150 / 80 / 5.0 | 5.25 | 6.572e-04 | moderate | z=80-81, r=5.0-5.75 |

Comparison to run 479:

```text
5-source final target-0 update-case margin: 3.503e-04
7-source final target-0 update-case margin: 6.572e-04
margin ratio: about 1.88x
```

Interpretation:

```text
Seven sources improve the target-0 source-mismatch row enough to promote it
from weak to moderate and shrink the update-case radius interval upper bound
from 6.0 to 5.75 mm. The clean-noise row remains weak and keeps a 5.0-6.0 mm
interval, so source count alone does not fully collapse target-0 uncertainty.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 71.9029
```

## 483: Target-2 Final-State z/r Check With 7 Sources

Output:

```text
outputs/experiments/483_coordinate_optimizer_variable_depth_radius_seed55_target2_final_zr_sources7
```

Command pattern:

```text
run_multi_rebar_coordinate_optimizer.py with gpu-cpml, 1 mm grid, 7 sources,
seed55 replication cases, target index 2 only, x fixed, z offsets -1:0:1 from
z=120 mm, and radius offsets -1:0:0.25 from r=8 mm.
```

Runtime:

```text
224.7 s
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
| noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 3.660e-04 | weak | z=119-120, r=7.25-8.0 |
| source_mismatch_noise10_seed55 | 350 / 120 / 8.0 | 7.25 | 7.067e-04 | moderate | z=119-120, r=7.25-8.0 |

Comparison to run 478:

```text
5-source target-2 coupled update-case margin: 1.083e-03
7-source final target-2 update-case margin: 7.067e-04
```

Interpretation:

```text
Seven sources do not improve the target-2 interval. The point best remains
truth, but the near-best z=119/r=7.25 branch stays inside the ambiguity rule.
For target 2, source-count escalation is not a reliable interval-collapse
strategy.
```

Plot validation:

```text
coordinate_confidence_margins.png:
1549x903 px, dynamic range 255, grayscale std 71.9482
```

## 484: Seven-Source Final-Interval Aggregate

Output:

```text
outputs/experiments/484_variable_depth_radius_seed55_sources7_final_interval_summary
```

Command:

```text
run_coordinate_confidence_aggregate.py over coordinate summaries 482 and 483.
```

Aggregate metrics:

```text
rows: 4
truth-geometry rows: 4
confidence labels: weak=2, moderate=2
minimum radius margin: 3.660e-04
maximum x/z/r ambiguity widths: 0.0 / 1.0 / 1.0 mm
target-0 rows: 2, truth-geometry rows: 2, weakest radius margin: 3.893e-04
target-2 rows: 2, truth-geometry rows: 2, weakest radius margin: 3.660e-04
```

Plot validation:

```text
coordinate_confidence_aggregate.png:
1719x971 px, dynamic range 255, grayscale std 58.5068

coordinate_ambiguity_widths.png:
1719x971 px, dynamic range 255, grayscale std 57.6320
```

Figure notes:

```text
outputs/experiments/484_variable_depth_radius_seed55_sources7_final_interval_summary/figures/FIGURE_NOTES.md
```

## Interpretation

Seven-source acquisition at the same 20 mm Tx/Rx offset is a partial
confidence refinement, not a general fix:

```text
target 0: update-case margin improves and interval narrows, but clean row is
          still weak.
target 2: point truth remains first, but the 7.25 mm / z=119 branch remains
          near-best and the update-case margin is lower than in the 5-source
          coupled run.
```

## Next Decision

Do not promote 7 sources as the default answer for the remaining
variable-depth/variable-radius radius intervals. Keep interval reporting as
the default. The next useful bounded GPU variation should change acquisition
geometry or objective structure, for example:

```text
1. a larger Tx/Rx offset final-state interval check for target 0 and target 2;
2. a high-frequency or weighted-objective final-state interval check;
3. a compact source-shape/basis check only if a new source mismatch branch is
   introduced.
```
