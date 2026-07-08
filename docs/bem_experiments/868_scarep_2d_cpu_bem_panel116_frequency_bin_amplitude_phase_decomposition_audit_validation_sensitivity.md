# BEM Experiment 868: Panel-116 Frequency-Bin Amplitude/Phase Decomposition Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `867` validator with damaged decomposition states and
premature promotion states.

This run reads saved artifacts only. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/868_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 19
expected pass scenarios:               1
expected fail scenarios:               18
observed pass scenarios:               1
observed fail scenarios:               18
unexpected outcomes:                   0
damaged scenarios:                     18
scalar-gain correction promoted:       false
project FDTD comparison ready:         false
field transfer ready:                  false
3D validation ready:                   false
```

## Interpretation

The validator accepts only the exact saved mixed/phase diagnostic state. It
rejects damaged row counts, altered high-band and above-target counts,
amplitude/phase/mixed-count damage, worst-frequency damage, false scalar-gain
repair, scalar-gain promotion, project-FDTD promotion, field or 3D promotion,
figure damage, and script-snapshot damage.

## Decision

Use runs `866-868` as the guarded amplitude/phase diagnostic block for the
remaining 116-panel high-band frequency-bin exceedance.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
2862x868, dynamic range=255
```
