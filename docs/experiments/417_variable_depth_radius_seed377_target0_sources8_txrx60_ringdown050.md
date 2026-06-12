# Experiment 417: Seed377 Target-0 Sources=8 Tx/Rx=60 Ringdown050

## Purpose

Run 883 extends the full-ringdown050 target-0 lower-tail replication to the
next Fibonacci noise seed after seed233.

## Results

Run 883 is exact and accepted:

```text
output: outputs/experiments/883_coordinate_optimizer_variable_depth_radius_seed377_target0_sources8_txrx60_ringdown050_objectives
target: 0
sources: 8
best: x=150 mm, z=80 mm, r=5.0 mm
next radius: 5.25 mm
absolute radius margin: 5.527795e-04
offset from cutoff: +5.278e-05
confidence label: moderate
fallback warning: none
elapsed: 558.91 s
```

Diagnostic objective rows all preserve the true target-0 geometry:

| Objective | Margin | Status |
| --- | ---: | --- |
| base | 5.527795e-04 | above cutoff |
| highband | 7.266302e-04 | above cutoff |
| late | 3.914056e-04 | below cutoff |
| late_high | 4.474819e-04 | below cutoff |
| veryhigh | 6.871787e-04 | above cutoff |
| early_high | 6.204456e-04 | above cutoff |

## Interpretation

Seed377 is another target-0 full-ringdown050 pass, sitting above seeds 89,
233, 34, and 55 in reserve. Seed21 remains the only observed target-0
full-ringdown050 failure in this Fibonacci seed sequence.

## Validation

```text
JSON parse: run_manifest.json and multi_rebar_coordinate_optimizer_summary.json pass
CSV rows: confidence=1, objective diagnostics=6, objective top candidates=72, state history=2, candidates=12
figure validation: coordinate_confidence_margins.png is 1549x903 RGBA with nonwhite_fraction=0.274871 and full 0-255 dynamic range
visual inspection: confidence figure is readable and correctly shows one moderate row above the 0.0005 cutoff
figure notes: figures/FIGURE_NOTES.md present and run-specific
source validation: all six diagnostic objectives preserve target0 truth geometry; 4/6 clear cutoff
```

## Next Decision

Run seed377 target 2 at 5 sources and full ringdown050.
