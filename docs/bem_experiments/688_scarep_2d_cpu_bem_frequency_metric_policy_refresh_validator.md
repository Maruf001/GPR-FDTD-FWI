# BEM Experiment 688: Frequency Metric Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate the run `687` BEM transfer metric policy.

The validator checks the five policy rows, the 113/114/116 panel roles, the
guard-margin boundary, the grid-sensitive aggregate metric flag, the
per-frequency diagnostic requirement, and the analytic-only claim boundary.

## Output

```text
outputs/bem_experiments/688_scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator.png
scripts/
```

## Result

```text
validator checks:                    5
failed checks:                       0
policy rows:                         5
nearest no-go panel:                 113
minimum passing panel:               114
guarded recommended panel:           116
aggregate metric grid-sensitive:     true
per-frequency diagnostic required:   true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

## Interpretation

Run `688` validates the refreshed policy: 116 remains the guarded endpoint,
per-frequency anatomy remains a diagnostic guard, and no downstream claim is
promoted.

## Decision

Use run `687` as the current BEM transfer metric policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator.py
3 passed
```

Figure check:

```text
2321x857, dynamic range=255
```
