# BEM Experiment 862: 116-Panel Frequency-Bin Exceedance Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `861` validator with damaged or prematurely promoted
states.

## Output

```text
outputs/bem_experiments/862_scarep_2d_cpu_bem_panel116_frequency_bin_exceedance_scorecard_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                  13
expected pass scenarios:                1
expected fail scenarios:                12
observed pass scenarios:                1
observed fail scenarios:                12
unexpected outcomes:                    0
damaged scenarios:                      12
field transfer ready:                   false
field FWI ready:                        false
```

## Decision

The validator accepts only the exact exceedance scorecard and rejects damaged
or prematurely promoted states. Use runs `860-862` as the guarded
per-frequency exceedance concentration block.

## Validation

Figure check:

```text
2645x853, dynamic range=255
```
