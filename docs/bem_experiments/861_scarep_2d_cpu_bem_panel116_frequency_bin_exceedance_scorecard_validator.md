# BEM Experiment 861: 116-Panel Frequency-Bin Exceedance Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `860` exceedance scorecard.

## Output

```text
outputs/bem_experiments/861_scarep_2d_cpu_bem_panel116_frequency_bin_exceedance_scorecard_validator
```

## Result

```text
validation checks:                      6
passed checks:                          6
failed checks:                          0
total high-band bins:                   27
total bins above target:                5
worst frequency:                        2.3125 GHz
worst per-frequency relative L2:        0.0020304660813911003
per-frequency diagnostic required:      true
lower-panel policy change ready:        false
field transfer ready:                   false
field FWI ready:                        false
```

## Decision

Run `860` validates as aggregate-endpoint evidence with a required
per-frequency diagnostic guard.

## Validation

Figure check:

```text
2429x838, dynamic range=255
```
