# BEM Experiment 907: Panel-116 Smooth Frequency Vertical-Shift Interpolated Validation Scorecard Validator

Date: 2026-07-01

## Purpose

Validate run `906` as surrogate-only continuous-shift evidence: exact row
shape, interpolated closure, unresolved bracket guard, figure/script
integrity, and blocked downstream-promotion flags.

## Output

```text
outputs/bem_experiments/907_scarep_2d_cpu_bem_panel116_smooth_frequency_vertical_shift_interpolated_validation_scorecard_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
interpolated all-frequency pass models:    1
bracket-guard all-frequency pass models:   0
best interpolated max relative L2:         0.0008751841676054046
best bracket-guard max relative L2:        0.001367588871846657
validation ready:                          true
```

## Interpretation

The validator confirms the interpolated smooth-model scorecard exactly as
surrogate evidence. It also preserves the unresolved bracket guard and keeps
all correction, project-comparison, field, GPU, and 3D claims blocked.

## Decision

Use run `906` as guarded continuous-shift surrogate evidence only.

## Validation

Focused smooth-model chain:

```text
19 passed
```

Figure check:

```text
2465x858, dynamic range=255
```
