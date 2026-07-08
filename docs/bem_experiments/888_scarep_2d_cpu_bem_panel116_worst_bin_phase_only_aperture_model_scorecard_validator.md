# BEM Experiment 888: Panel-116 Worst-Bin Phase-Only Aperture Model Scorecard Validator

Date: 2026-07-01

## Purpose

Validate the saved run `887` phase-only aperture model scorecard.

The validator checks source readiness, model row stability, absence of a
target-passing phase-only repair, the in-sample versus leave-one-out split,
blocked downstream claim flags, figure output, and script snapshots.

## Output

```text
outputs/bem_experiments/888_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard_validator
```

## Result

```text
validation checks:                       6
checks passed:                           6
checks failed:                           0
receiver rows:                           13
model rows:                               6
frequency:                               2.3125 GHz
target relative L2:                      0.001
uncorrected relative L2:                 0.002030466081391074
best in-sample model:                    constant_odd_even_phase
best in-sample relative L2:              0.0018234403083841053
best in-sample reduction fraction:       0.10195972979028295
best leave-one-out model:                constant_phase
best leave-one-out relative L2:          0.0019827840138898723
best leave-one-out reduction fraction:   0.023483311510692412
phase-only model repair ready:           false
source/receiver phase refinement needed: true
project FDTD comparison ready:           false
field transfer ready:                    false
real 3D validation ready:                false
gpu priority:                            none
```

## Interpretation

The saved scorecard validates as a no-repair result. The most flexible
phase-only candidate gives the best in-sample score, but the stable holdout
candidate is only a constant phase correction and still remains above target.

## Decision

Use run `887` as a validated no-repair result for unit-amplitude aperture
phase correction.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_phase_only_aperture_model_scorecard_validator.py
3 passed
```

Figure check:

```text
2465x864, dynamic range=255
```

