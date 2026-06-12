# Experiment 518: Seed2178309 Target1 Sources=11 Tx/Rx=60 Ringdown050

## Purpose

Run 984 tests the final seed2178309 target1 source-density escalation after
both the 5-source control and 9-source rescue stayed exact but weak.

## 984: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=11 Tx/Rx=60 Ringdown050

Output:

```text
outputs/experiments/984_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources11_txrx60_ringdown050_objectives
```

## Results

The final recovered coordinate state remains exact, but the confidence margin
is weak and worsens:

```text
x = [150, 250, 350] mm
z = [80, 100, 120] mm
r = [5, 6, 8] mm
```

Base confidence row:

```text
target: 1
sources: 11
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 3.915066e-04
offset from cutoff: -1.084934e-04
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: about 831.8 s
```

Diagnostic objective rows preserve the true target1 geometry, but four of six
margins are below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 3.915066e-04 | below cutoff |
| highband | 5.173575e-04 | above cutoff |
| late | 4.929374e-04 | below cutoff |
| late_high | 5.621870e-04 | above cutoff |
| veryhigh | 4.421479e-04 | below cutoff |
| early_high | 3.913754e-04 | below cutoff |

## Interpretation

Run 984 rejects source-density escalation as the seed2178309 target1 remedy.
The result is a confidence failure, not a geometry failure, and the 5/9/11
source trend is nonmonotonic-worsening. Summarize the branch and move to a
receiver/acquisition mechanism test.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.193031 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]; target1 truth_radius_mm is 6.0 mm
resources: 11-source GPU checks were about 93% utilization; Python process RSS was about 461 MB during the sweep
```

## Next Decision

Create the seed2178309 branch summary and run a targeted receiver/acquisition
mechanism test.
