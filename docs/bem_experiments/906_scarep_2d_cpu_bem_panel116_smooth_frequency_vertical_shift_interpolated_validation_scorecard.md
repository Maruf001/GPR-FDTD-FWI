# BEM Experiment 906: Panel-116 Smooth Frequency Vertical-Shift Interpolated Validation Scorecard

Date: 2026-07-01

## Purpose

Check whether the smooth run `900` vertical-shift models survive interpolation
between the saved run `897` shifted-grid samples, instead of only passing after
snapping to the nearest `0.05 mm` grid point.

This run does not rerun the BEM solver. It interpolates the saved candidate
grid and records a conservative neighboring-grid bracket guard. It does not
promote a correction, project-FDTD comparison, field transfer, GPU work, or
3D/HPC claim.

## Output

```text
outputs/bem_experiments/906_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_interpolated_validation_scorecard
```

## Result

```text
model count:                              5
continuous frequency rows:                125
interpolated all-frequency pass models:   1
bracket-guard all-frequency pass models:  0
best interpolated model:                  best_gaussian_bump
best interpolated max relative L2:        0.0008751841676054046
best interpolated worst frequency:        2.65625 GHz
best bracket-guard max relative L2:       0.001367588871846657
best bracket-guard worst frequency:       2.3125 GHz
continuous surrogate passes:              true
bracket guard passes:                     false
```

## Interpretation

The best gaussian-bump model remains below the `0.001` target under linear
interpolation between saved shift-grid samples. The conservative bracket guard
does not pass because one neighboring grid endpoint remains above target at
`2.3125 GHz`, so this is still surrogate evidence rather than a promoted
correction.

## Decision

Use this as continuous-shift surrogate evidence only. Keep project-FDTD
comparison, field transfer, correction promotion, GPU priority, and 3D/HPC
work blocked.

## Validation

Focused smooth-model chain:

```text
19 passed
```

Figure check:

```text
2284x840, dynamic range=255
```
