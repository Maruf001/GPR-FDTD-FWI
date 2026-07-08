# BEM Experiment 877: Panel-116 Worst-Bin Aperture Complex-Bias Model Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `876` validator with damaged complex-bias model states and
premature promotion states.

This run reads saved artifacts only. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/877_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 16
expected pass scenarios:               1
expected fail scenarios:               15
observed pass scenarios:               1
observed fail scenarios:               15
unexpected outcomes:                   0
damaged scenarios:                     15
smooth complex-bias repair ready:      false
holdout-stable correction ready:       false
hard per-frequency endpoint ready:     false
project FDTD comparison ready:         false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The validator accepts only the exact saved complex-bias scorecard. It rejects
source-readiness damage, model-row damage, false target repair, false
in-sample pass, false leave-one-out stability, smooth-bias repair promotion,
hard per-frequency promotion, project-FDTD promotion, field or 3D promotion,
GPU-priority promotion, figure damage, and script-snapshot damage.

## Decision

Use runs `875-877` as the guarded smooth aperture-bias no-repair block for the
remaining 116-panel worst high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_complex_bias_model_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2681x875, dynamic range=255
```
