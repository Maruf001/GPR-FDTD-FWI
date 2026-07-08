# BEM Experiment 879: Panel-116 Worst-Bin Receiver-Pair Symmetry Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `878` receiver-pair symmetry audit from artifacts.

This validator does not rerun BEM, FDTD, field processing, 3D/HPC work, or GPU
kernels.

## Output

```text
outputs/bem_experiments/879_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_validator
```

## Result

```text
validation checks:                      6
passed checks:                          6
failed checks:                          0
receiver rows:                          13
receiver pairs:                         6
frequency:                              2.3125 GHz
symmetric pair energy fraction:         0.2888732114593446
antisymmetric pair energy fraction:     0.7111267885406554
antisymmetric-dominant pair count:      5
symmetric-dominant pair count:          1
maximum pair magnitude delta fraction:  0.05160289316381502
center total energy fraction:           0.08141503241185702
balanced pair magnitudes:               true
antisymmetric residual dominant:        true
one-sided amplitude artifact:           false
project FDTD comparison ready:          false
field transfer ready:                   false
3D validation ready:                    false
```

## Interpretation

The saved receiver-pair symmetry audit validates as magnitude-balanced,
antisymmetric-dominant, and not one-sided.

## Decision

Use run `878` as the current receiver-pair symmetry diagnostic for the worst
remaining 116-panel high-band frequency bin.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_worst_bin_receiver_pair_symmetry_audit_validator.py
3 passed
```

Figure check:

```text
2429x858, dynamic range=255
```
