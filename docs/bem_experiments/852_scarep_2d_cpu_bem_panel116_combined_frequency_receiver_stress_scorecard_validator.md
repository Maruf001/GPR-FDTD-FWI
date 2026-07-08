# BEM Experiment 852: 116-Panel Combined Stress Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `851` combined frequency/receiver scorecard.

This validator checks the source readiness, row shape, pass counts,
guard-margin state, controlling-case identity, frequency-grid policy, analytic
claim boundary, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/852_scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_combined_frequency_receiver_stress_scorecard_validator.png
scripts/
```

## Result

```text
validation checks:                        7
passed checks:                            7
failed checks:                            0
stress rows:                              6
frequency grids:                          2
scan-count variants:                      3
maximum high-band relative L2:            0.0009518291083452528
minimum margin to target:                 4.8170891654747265e-05
controlling frequency grid:               25
controlling scan positions:               13
validation ready:                         true
field transfer ready:                     false
field FWI ready:                          false
```

## Decision

Run `851` validates as an analytic-only 116-panel BEM endpoint check.

## Validation

Figure check:

```text
2537x836, dynamic range=255
```

Script snapshots:

```text
2
```
