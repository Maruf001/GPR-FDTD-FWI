# Experiment 520: Seed2178309 Target1 Sources=5 Tx/Rx=60 Linear Receiver Ringdown050

## Purpose

Run 986 tests whether receiver interpolation rescues the seed2178309 target1
confidence weakness.

## 986: Coordinate Optimizer Variable-Depth/Radius Seed2178309 Target1 Sources=5 Tx/Rx=60 Linear Receiver Ringdown050

Output:

```text
outputs/experiments/986_coordinate_optimizer_variable_depth_radius_seed2178309_target1_sources5_txrx60_linear_receiver_ringdown050_objectives
```

## Results

Run 986 is exact but weak, and it matches the nearest-receiver 5-source control:

```text
receiver sampling: linear
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
absolute radius margin: 4.821346e-04
offset from cutoff: -1.786535e-05
confidence label: weak
fallback warning: radius_weak_confidence
elapsed: about 361.6 s
```

Diagnostic objective rows preserve the true target1 geometry; base and
early_high remain below cutoff:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 4.821346e-04 | below cutoff |
| highband | 6.104248e-04 | above cutoff |
| late | 7.771451e-04 | above cutoff |
| late_high | 8.359646e-04 | above cutoff |
| veryhigh | 5.628775e-04 | above cutoff |
| early_high | 4.647245e-04 | below cutoff |

## Interpretation

Linear receiver sampling does not change the target1 margin. The next mechanism
test should vary acquisition offset rather than receiver interpolation.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
top candidates: exact target1 geometry is rank 1 for all six objective variants
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.230895 and nonzero dynamic range
visual inspection: confidence figure is readable and shows one weak row below the 5.0e-4 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
metadata validation: receiver_sampling is linear; summary truth_radius_values_mm is target-specific at [5.0, 6.0, 8.0]
resources: 5-source GPU checks were about 88% utilization
```

## Next Decision

Run a seed2178309 target1 Tx/Rx=50 acquisition-offset probe at 5 sources. That
run is underway as experiment 987.
