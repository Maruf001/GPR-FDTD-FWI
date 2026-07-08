# BEM Experiment 859: 116-Panel Controlling Receiver Frequency Anatomy Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `858` validator with damaged or prematurely promoted
states.

The sensitivity set checks source readiness, row shape, scan identity, panel
identity, aggregate error, guard margin, frequency-bin diagnostic state,
frequency-grid sensitivity, controlling-source identity, lower-panel
promotion, project-FDTD promotion, 3D/GPU/field promotion, figure output, and
script snapshots.

## Output

```text
outputs/bem_experiments/859_scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validation_sensitivity_case_rows.csv
data/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validation_sensitivity_summary.json
data/figure_validation.csv
figures/scarep_2d_cpu_bem_panel116_controlling_receiver_frequency_anatomy_audit_validation_sensitivity.png
scripts/
```

## Result

```text
sensitivity cases:                       19
expected pass cases:                     1
expected fail cases:                     18
actual pass cases:                       1
actual fail cases:                       18
unexpected cases:                        0
damaged cases:                           18
sensitivity ready:                       true
field transfer ready:                    false
field FWI ready:                         false
```

## Decision

The validator accepts only the exact saved anatomy state and rejects damaged or
prematurely promoted states. Use runs `857-859` as the guarded per-frequency
diagnostic block for the controlling 116-panel analytic BEM receiver layout.

## Validation

Figure check:

```text
2897x854, dynamic range=255
```

Script snapshots:

```text
2
```
