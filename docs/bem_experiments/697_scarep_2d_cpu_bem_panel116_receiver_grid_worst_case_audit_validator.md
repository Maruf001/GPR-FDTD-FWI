# BEM Experiment 697: 116-Panel Receiver-Grid Worst-Case Audit Validator

Date: 2026-06-30

## Purpose

Validate run `696`, the receiver-grid robustness audit for the 116-panel
analytic BEM policy.

The validator checks source readiness, scan/solve shape, locked target case,
116-panel and 128-panel pass status, analytic-only claim boundary, figure
output, and frozen script snapshots.

This run does not rerun BEM solves or promote project-FDTD, 3D, GPU/HPC, or
field claims.

## Output

```text
outputs/bem_experiments/697_scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validator_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_worst_case_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
scan-count rows:                           3
solve rows:                                6
116-panel pass count:                      3
128-panel pass count:                      3
116-panel max high-band relative L2:       0.0009518291083452528
116-panel receiver-grid transfer ready:    true
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
```

## Interpretation

The receiver-grid audit validates as an analytic-only worst-case support result
for the guarded 116-panel policy.

## Decision

Use run `697` as the validator for run `696`.

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
2357x838, dynamic range=255
```
