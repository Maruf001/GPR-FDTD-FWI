# BEM Experiment 689: Frequency Metric Policy Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `688` BEM metric policy validator.

The validator should accept only the exact run `687` policy and reject damaged
policy rows, panel roles, grid-sensitivity state, per-frequency diagnostic
state, policy-lowering flags, downstream claims, figure validation, and frozen
script snapshots.

## Output

```text
outputs/bem_experiments/689_scarep_2d_cpu_bem_frequency_metric_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validation_sensitivity_cases.csv
data/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_frequency_metric_policy_refresh_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   16
expected pass cases:                 1
expected fail cases:                 15
actual pass cases:                   1
actual fail cases:                   15
unexpected cases:                    0
damaged cases rejected:              true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `687` policy passes. All damaged states fail, including source
readiness damage, policy-row removal, policy-item damage, minimum-panel damage,
guarded-panel damage, grid-sensitivity loss, per-frequency diagnostic removal,
lower-panel policy promotion, FDTD comparison promotion, real-3D promotion,
GPU/HPC promotion, field-transfer promotion, field-FWI promotion, figure
damage, and missing script snapshots.

## Interpretation

Run `689` hardens the refreshed metric policy. A damaged metric interpretation
or premature downstream promotion cannot validate.

## Decision

Keep runs `687-689` as the current BEM transfer metric policy block.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_frequency_metric_policy_refresh.py
tests/test_scarep_2d_cpu_bem_frequency_metric_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_frequency_metric_policy_refresh_validation_sensitivity.py

9 passed
```

Figure check:

```text
2536x850, dynamic range=255
```
