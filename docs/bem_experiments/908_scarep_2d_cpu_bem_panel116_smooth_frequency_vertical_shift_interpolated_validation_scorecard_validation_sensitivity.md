# BEM Experiment 908: Panel-116 Smooth Frequency Vertical-Shift Interpolated Validation Sensitivity

Date: 2026-07-01

## Purpose

Sensitivity-test the run `907` validator against damaged row shape, false
interpolated closure, false bracket-guard pass, surrogate demotion, figure or
script damage, and premature downstream-promotion flags.

## Output

```text
outputs/bem_experiments/908_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_interpolated_validation_scorecard_validation_sensitivity
```

## Result

```text
scenarios:                  16
expected pass:              1
expected fail:              15
observed pass:              1
observed fail:              15
unexpected outcomes:        0
damaged scenarios rejected: 15
sensitivity ready:          true
```

## Interpretation

Only the exact interpolated scorecard passes. The validator rejects false
closure, false bracket-guard promotion, surrogate-boundary damage, figure or
script snapshot damage, and any premature correction, field, project-FDTD,
GPU, or 3D promotion.

## Decision

Use runs `906-908` as guarded continuous-shift surrogate evidence only.

## Validation

Focused smooth-model chain:

```text
19 passed
```

Figure check:

```text
2825x847, dynamic range=255
```
