# BEM Experiment 880: Panel-116 Worst-Bin Receiver-Pair Symmetry Audit Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `879` validator with damaged receiver-pair symmetry states
and premature promotion states.

This run reads saved artifacts only. It does not rerun BEM, FDTD, field
processing, 3D/HPC work, or GPU kernels.

## Output

```text
outputs/bem_experiments/880_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_validation_sensitivity
```

## Result

```text
sensitivity scenarios:                 18
expected pass scenarios:               1
expected fail scenarios:               17
observed pass scenarios:               1
observed fail scenarios:               17
unexpected outcomes:                   0
damaged scenarios:                     17
receiver-pair correction promoted:     false
hard per-frequency endpoint ready:     false
project FDTD comparison ready:         false
field transfer ready:                  false
3D validation ready:                   false
gpu priority:                          none
```

## Interpretation

The validator accepts only the exact saved receiver-pair symmetry state. It
rejects row damage, symmetry-fraction damage, false one-sided-artifact
promotion, false correction promotion, hard per-frequency promotion,
project-FDTD promotion, field or 3D promotion, GPU-priority promotion, figure
damage, and script-snapshot damage.

## Decision

Use runs `878-880` as the guarded receiver-pair symmetry diagnostic block for
the remaining 116-panel worst high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
2717x867, dynamic range=255
```
