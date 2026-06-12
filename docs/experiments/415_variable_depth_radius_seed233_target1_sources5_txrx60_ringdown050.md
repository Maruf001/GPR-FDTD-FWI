# Experiment 415: Seed233 Target-1 Sources=5 Tx/Rx=60 Ringdown050

## Purpose

Run 881 completes the seed233 full-ringdown050 target-specific branch by
testing target 1 at 5 sources.

## Results

Run 881 is exact and accepted:

```text
output: outputs/experiments/881_coordinate_optimizer_variable_depth_radius_seed233_target1_sources5_txrx60_ringdown050_objectives
target: 1
sources: 5
best: x=250 mm, z=100 mm, r=6.0 mm
next radius: 6.25 mm
absolute radius margin: 5.608831e-04
offset from cutoff: +6.088e-05
confidence label: moderate
fallback warning: none
elapsed: 362.25 s
```

Diagnostic objective rows all preserve the true target-1 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.608831e-04 | above cutoff |
| highband | 7.586555e-04 | above cutoff |
| late | 8.291244e-04 | above cutoff |
| late_high | 9.892309e-04 | above cutoff |
| veryhigh | 7.180034e-04 | above cutoff |
| early_high | 5.581712e-04 | above cutoff |

## Interpretation

Seed233 completes as an `8/5/5` full-ringdown050 seed:

| Target | Run | Sources | Margin | Offset from cutoff | Status |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 878 | 8 | 5.434236e-04 | +4.342e-05 | accepted |
| 1 | 881 | 5 | 5.608831e-04 | +6.088e-05 | accepted |
| 2 | 880 | 5 | 5.878754e-04 | +8.788e-05 | accepted |

Target 0 is the limiting seed233 row.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.278486 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
source validation: all six diagnostic objectives preserve target1 truth geometry; 6/6 clear cutoff
```

## Next Decision

Generate the seed233 `8/5/5` policy summary.
