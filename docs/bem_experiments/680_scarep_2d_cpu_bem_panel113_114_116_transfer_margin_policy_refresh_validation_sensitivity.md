# BEM Experiment 680: 113/114/116 Transfer Margin Policy Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `679` validator for the margin-aware transfer policy.

The validator should accept only the exact policy state and reject damaged
states that move the no-go panel, minimum passing panel, guarded recommended
panel, guard margins, source readiness, downstream claims, figure output, or
script snapshots.

## Output

```text
outputs/bem_experiments/680_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validation_sensitivity_rows.csv
data/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   18
expected pass cases:                 1
expected fail cases:                 17
actual pass cases:                   1
actual fail cases:                   17
unexpected cases:                    0
policy damage rejected:              true
claim-promotion damage rejected:     true
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `678` policy passes. All damaged states fail, including false
113-panel promotion, incorrect minimum passing panel, incorrect guarded panel,
lost guard margin, source-readiness damage, downstream promotion, figure
damage, and missing script snapshots.

## Interpretation

Run `680` hardens the margin-aware transfer policy. The current policy is:
114 panels as the minimum validated pass and 116 panels as the guarded
recommended analytic transfer endpoint.

## Decision

Keep the margin policy. Keep project-FDTD, 3D, field, GPU/HPC, and field-FWI
claims blocked.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel113_114_116_transfer_margin_policy_refresh_validation_sensitivity.py

9 passed
```

Figure check:

```text
2644x887, dynamic range=255
```
