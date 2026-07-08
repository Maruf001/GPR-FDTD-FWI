# BEM Experiment 858: 116-Panel Controlling Receiver Frequency Anatomy Validator

Date: 2026-07-01

## Purpose

Validate the saved run `857` per-frequency anatomy audit.

This validator checks source readiness, grid/frequency row shape, aggregate
pass and guard-margin state, per-frequency diagnostic need, controlling
receiver identity, analytic-only boundary, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/858_scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validator.png
scripts/
```

## Result

```text
validation checks:                       7
passed checks:                           7
failed checks:                           0
grid rows:                               2
frequency-error rows:                    74
high-band frequency-error rows:          27
25-frequency high-band relative L2:      0.0009518291083452528
49-frequency high-band relative L2:      0.0007643703508458867
25-frequency margin to target:           4.8170891654747265e-05
49-frequency margin to target:           0.00023562964915411328
worst per-frequency relative L2:         0.0020304660813911003
validation ready:                        true
field transfer ready:                    false
field FWI ready:                         false
```

## Decision

Run `857` validates as an aggregate-pass, per-frequency-diagnostic-required
analytic BEM state.

## Validation

Figure check:

```text
2501x836, dynamic range=255
```

Script snapshots:

```text
2
```
