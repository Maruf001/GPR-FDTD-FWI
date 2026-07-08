# BEM Experiment 685: 114/116 Frequency-Grid Anatomy Audit Validator

Date: 2026-06-30

## Purpose

Validate the run `684` frequency-grid anatomy audit.

The validator checks the exact larger-radius target case, four grid-panel rows,
148 per-frequency rows, preserved grid-sensitive aggregate behavior, unchanged
worst per-frequency maxima, no policy lowering, and no downstream claim
promotion.

## Output

```text
outputs/bem_experiments/685_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator.png
scripts/
```

## Result

```text
validator checks:                    5
failed checks:                       0
target case:                         radius_75mm_baseline_eps
grid rows:                           4
frequency-error rows:                148
aggregate metric grid-sensitive:     true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

## Interpretation

Run `685` validates the interpretation from run `684`: the aggregate high-band
metric changes with frequency sampling, while the worst per-frequency error
does not improve. The validator preserves the decision not to lower the panel
policy.

## Decision

Use run `684` as the metric-anatomy explanation for why dense-grid support
does not supersede the guarded 116-panel policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator.py
3 passed
```

Figure check:

```text
2321x860, dynamic range=255
```
