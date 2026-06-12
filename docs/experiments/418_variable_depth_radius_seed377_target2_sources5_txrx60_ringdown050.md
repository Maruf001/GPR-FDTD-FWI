# Experiment 418: Seed377 Target-2 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 884 tests seed377 target 2 at full ringdown050 with 5 sources.

## Results

Run 884 is exact and accepted, but low-reserve:

```text
output: outputs/experiments/884_coordinate_optimizer_variable_depth_radius_seed377_target2_sources5_txrx60_ringdown050_objectives
target: 2
sources: 5
best: x=350 mm, z=120 mm, r=8.0 mm
next radius: 8.75 mm
absolute radius margin: 5.096084e-04
offset from cutoff: +9.608e-06
confidence label: moderate
fallback warning: none
elapsed: 363.99 s
```

Diagnostic objective rows all preserve the true target-2 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.096084e-04 | above cutoff |
| highband | 6.306553e-04 | above cutoff |
| late | 8.124983e-04 | above cutoff |
| late_high | 8.090769e-04 | above cutoff |
| veryhigh | 6.267420e-04 | above cutoff |
| early_high | 4.615672e-04 | below cutoff |

## Interpretation

Seed377 target 2 passes at 5 sources, but it is the weakest accepted target-2
5-source row so far. Keep it as accepted, but preserve the low-reserve warning
in the seed377 summary.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.255027 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row just above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
source validation: all six diagnostic objectives preserve target2 truth geometry; 5/6 clear cutoff
```

## Next Decision

Run seed377 target 1 at 5 sources and full ringdown050.
