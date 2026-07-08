# BEM Experiment 656: 64/82/84/88/96/128 Frequency-Cost Policy Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test run `655`, the validator for the refreshed scarep 2D CPU BEM
panel policy.

The validator should accept only the exact run `655` source state and reject
damaged states that change the 64/82/84/88/96/128 policy roles, the 82-to-84
high-frequency threshold, the 84-panel cost/margin condition, or the
analytic-only claim boundary.

## Output

```text
outputs/bem_experiments/656_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:         true
sensitivity cases:              35
expected pass cases:            1
expected fail cases:            34
actual pass cases:              1
actual fail cases:              34
unexpected cases:               0
policy-role damage rejected:       true
high-frequency damage rejected:    true
claim-promotion damage rejected:   true
project FDTD comparison ready:     false
real 3D validation ready:          false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
```

The exact source passes. All damaged states fail, including source readiness
loss, row-shape damage, 82-panel no-go promotion, 84-panel role damage,
88/96/128 role drift, high-frequency threshold drift, 84-panel margin loss,
84-panel cost drift, project-FDTD promotion, 3D promotion, GPU/HPC promotion,
field-transfer promotion, field-FWI promotion, figure damage, and missing
script snapshots.

## Interpretation

The current analytic-cylinder BEM panel policy is now sensitivity-hardened:

```text
64 panels: default for receiver-line and broad/low/mid-band sweeps
82 panels: nearest tested high-frequency no-go
84 panels: minimum guarded high-frequency candidate
88 panels: comfortable low-cost reference
96 panels: validated superseded reference
128 panels: strict endpoint
```

The result still does not justify project-FDTD comparison claims, field
transfer, 3D validation, GPU/HPC escalation, or field FWI.

## Decision

Use runs `654-656` as the current scarep analytic-cylinder BEM panel-policy
checkpoint. The next BEM work should move away from further panel-threshold
tuning unless a new geometry, observable, or matched FDTD comparison objective
is defined.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel64_82_84_88_96_128_frequency_cost_policy_refresh_validation_sensitivity.py

9 passed
```

Figure check:

```text
3148x902, dynamic range=255
```
