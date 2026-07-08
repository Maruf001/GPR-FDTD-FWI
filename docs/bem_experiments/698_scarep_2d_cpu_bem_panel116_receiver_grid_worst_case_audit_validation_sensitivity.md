# BEM Experiment 698: 116-Panel Receiver-Grid Worst-Case Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `697` validator.

The sensitivity set keeps one exact source case and applies controlled damage
to source readiness, scan shape, solve shape, scan-count identity, target-case
identity, 116-panel failure, 128-panel failure, high-band error threshold,
project-FDTD promotion, 3D promotion, field promotion, figure validation, and
script snapshots.

This run does not rerun BEM solves.

## Output

```text
outputs/bem_experiments/698_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validation_sensitivity_case_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:                    true
sensitivity cases:                         14
expected pass cases:                       1
expected fail cases:                       13
actual pass cases:                         1
actual fail cases:                         13
unexpected cases:                          0
damaged cases:                             13
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

## Interpretation

The validator accepts only the exact receiver-grid audit and rejects shape,
target, transfer, promotion, figure, and snapshot damage.

## Decision

Treat runs `696-698` as analytic-only support for the guarded 116-panel policy.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validator.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validation_sensitivity.py

10 passed
```

Figure check:

```text
2537x850, dynamic range=255
```
