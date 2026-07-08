# Experiment 816: Target2 Close14 Three-Seed Probe

Date: 2026-06-18

## Purpose

Complete the fixed target2 close14 source5 / Tx/Rx=45 mm probe defined in
experiment 815. Existing seed34 was reused. Missing seeds 13 and 21 were run
one at a time under the local utilization policy, then all three seeds were
aggregated and synthesized against the stricter 0.5x ambiguity gate.

## Output

```text
outputs/experiments/1294_coordinate_optimizer_close14_seed13_sources5_txrx45_noise15p361328125_objectives
outputs/experiments/1295_coordinate_optimizer_close14_seed21_sources5_txrx45_noise15p361328125_objectives
outputs/experiments/1296_coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate
outputs/experiments/1297_synthetic_target2_close14_three_seed_probe_synthesis
```

Key artifacts:

```text
1294/data/multi_rebar_coordinate_optimizer_summary.json
1295/data/multi_rebar_coordinate_optimizer_summary.json
1296/data/coordinate_confidence_aggregate.json
1297/data/target2_close14_three_seed_probe_summary.json
1297/data/target2_close14_three_seed_probe_rows.csv
1297/figures/target2_close14_three_seed_probe_synthesis.png
```

## Result

Policy label:

```text
target2_close14_source5_txrx45_three_seed_persistent_x_near_tie
```

Summary:

```text
seeds:                         13,21,34
rows:                          6
truth geometry selected:       6 / 6
strong radius confidence:      6 / 6
x-ambiguity rows:              6 / 6
near ties at 0.5x gate:        6 / 6
near ties at 1.0x gate:        6 / 6
competing x geometry:          265.0 mm
radius margin min/max:         0.001500 / 0.002458
```

## Interpretation

This closes the target2 close14 source5 / Tx/Rx=45 mm probe. The optimizer
selects the true geometry in every seed/case and radius confidence is strong,
but the +1 mm lateral competitor remains inside even the 0.5x ambiguity gate
in every row. This should be reported as a robust objective-uniqueness limit,
not as a clean x-resolution result.

No further GPU work is justified for this exact probe unless the research
question changes.

## Validation

Focused tests:

```text
tests/test_synthetic_target2_close14_probe_synthesis.py: 4 passed
```

Figure validation:

```text
target2_close14_three_seed_probe_synthesis.png: 2229x835,
nonwhite=0.3022, dynamic range=255
```
