# BEM Experiment 867: Panel-116 Frequency-Bin Amplitude/Phase Decomposition Validator

Date: 2026-07-01

## Purpose

Validate the saved run `866` amplitude/phase decomposition from artifacts.

This validator does not rerun BEM, FDTD, field processing, 3D/HPC work, or GPU
kernels.

## Output

```text
outputs/bem_experiments/867_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_validator
```

## Result

```text
validation checks:                       6
passed checks:                           6
failed checks:                           0
frequency decomposition rows:            74
high-band decomposition rows:            27
above-target high-band rows:             5
above-target amplitude-dominant rows:    0
above-target phase-dominant rows:        1
above-target mixed rows:                 4
dominant above-target mode:              mixed
worst frequency:                         2.3125 GHz
worst complex relative L2:               0.0020304660813910734
worst scalar-gain-corrected L2:          0.0019054837810734088
scalar-gain reduction fraction:          0.061553503140539645
scalar-gain correction promoted:         false
project FDTD comparison ready:           false
field transfer ready:                    false
3D validation ready:                     false
```

## Interpretation

The saved decomposition validates as mixed/phase residual evidence. It does
not support scalar-gain repair, hard per-frequency acceptance, project-FDTD
comparison, field transfer, or 3D promotion.

## Decision

Use run `866` as the current amplitude/phase diagnostic for the remaining
high-band bin exceedance.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_frequency_bin_amplitude_phase_decomposition_audit_validator.py
3 passed
```

Figure check:

```text
2430x830, dynamic range=255
```
