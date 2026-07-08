# BEM Experiment 682: 114/116 Dense-Frequency Transfer Audit Validator

Date: 2026-06-30

## Purpose

Validate the run `681` dense-frequency transfer audit.

The validator checks source readiness, the exact four-case and twelve-solve
shape, the 49-frequency grid, the 114/116/128 panel set, the dense-grid
transfer boundary, and the analytic-only claim boundary.

## Output

```text
outputs/bem_experiments/682_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator.png
scripts/
```

## Result

```text
validator checks:                     5
failed checks:                        0
frequency samples:                    49
variant cases:                        4
solve rows:                           12
minimum dense-frequency passing panel: 114
guarded dense-frequency panel:         114
116-panel max high-band L2:            0.0007631424594234813
116-panel minimum margin:              0.0002368575405765187
116-panel guard survives:              true
project FDTD comparison ready:         false
real 3D validation ready:              false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
```

## Interpretation

Run `682` confirms that the dense-frequency result is internally consistent:
the solve table has the intended 114/116/128 panel set, the denser grid is
preserved, all four variants pass, and no FDTD, field, 3D, or GPU/HPC claim is
promoted.

## Decision

Use run `681` as dense-frequency support for the guarded 116-panel analytic
transfer policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_dense_frequency_transfer_audit_validator.py
3 passed
```

Figure check:

```text
2321x860, dynamic range=255
```
