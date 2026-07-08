# BEM Experiment 874: Panel-116 Worst-Bin Aperture Trim Scorecard Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `873` validator with damaged aperture-trim states and
premature promotion states.

This run reads saved artifacts only. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/874_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 17
expected pass scenarios:               1
expected fail scenarios:               16
observed pass scenarios:               1
observed fail scenarios:               16
unexpected outcomes:                   0
damaged scenarios:                     16
aperture-trim correction promoted:     false
hard per-frequency endpoint ready:     false
project FDTD comparison ready:         false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The validator accepts only the exact saved aperture-trim scorecard. It rejects
source-readiness damage, row-shape damage, false target repair, false subset
pass, aperture-trim promotion, hard per-frequency promotion, project-FDTD
promotion, field or 3D promotion, GPU-priority promotion, figure damage, and
script-snapshot damage.

## Decision

Use runs `872-874` as the guarded aperture-trim no-repair block for the
remaining 116-panel worst high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_aperture_trim_scorecard_validation_sensitivity.py
3 passed
```

Figure check:

```text
2681x875, dynamic range=255
```
