# BEM Experiment 686: 114/116 Frequency-Grid Anatomy Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `685` validator for the frequency-grid anatomy audit.

The validator should accept only the exact run `684` anatomy state and reject
damaged grid shape, target-case identity, grid-sensitivity flags, worst-bin
errors, policy-lowering flags, downstream claims, figure validation, and frozen
script snapshots.

## Output

```text
outputs/bem_experiments/686_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validation_sensitivity_cases.csv
data/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:              true
sensitivity cases:                   23
expected pass cases:                 1
expected fail cases:                 22
actual pass cases:                   1
actual fail cases:                   22
unexpected cases:                    0
damaged cases rejected:              true
lower panel policy change ready:     false
project FDTD comparison ready:       false
real 3D validation ready:            false
GPU/HPC ready:                       false
field transfer ready:                false
field FWI ready:                     false
```

The exact run `684` source passes. All damaged states fail, including source
readiness damage, grid-row or frequency-row removal, target-case damage,
panel-count or frequency-grid-count damage, grid-sensitivity damage,
dense-lower flag damage, per-frequency maximum damage, tight-margin or
guard-margin damage, lower-panel policy promotion, FDTD comparison promotion,
real-3D promotion, GPU/HPC promotion, field-transfer promotion, field-FWI
promotion, figure damage, and missing script snapshots.

## Interpretation

Run `686` hardens the metric-anatomy finding. The policy cannot be lowered by a
damaged aggregate-grid interpretation, a damaged per-frequency maximum, or a
downstream claim promotion.

## Decision

Keep runs `684-686` as the explanation and guardrail for interpreting the
dense-frequency block.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit.py
tests/test_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel114_116_frequency_grid_anatomy_audit_validation_sensitivity.py

9 passed
```

Figure check:

```text
2572x873, dynamic range=255
```
