# BEM Experiment 704: 116-Panel Receiver-Grid Policy Refresh Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `703` validator by confirming that it accepts the exact run
`702` receiver-grid policy refresh and rejects damaged or prematurely promoted
states.

This is a CPU-only validation-sensitivity wrapper around saved artifacts. It
does not run new BEM solves, compare against project FDTD outputs, run 3D
Maxwell BEM, launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/704_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity_case_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                         16
expected pass cases:                       1
expected fail cases:                       15
actual pass cases:                         1
actual fail cases:                         15
unexpected cases:                          0
damaged cases:                             15
3D validation ready:                       false
field transfer ready:                      false
field FWI ready:                           false
validation sensitivity ready:              true
```

The damaged cases cover source readiness, metric/policy row shape, panel drift,
frequency-grid count drift, error/margin damage, diagnostic removal,
lower-panel promotion, project-FDTD promotion, 3D/GPU/field promotion, figure
damage, and missing script snapshots.

## Interpretation

The validator accepts only the exact run `702` policy refresh and rejects all
damaged states tested here. This keeps the policy narrow: 116 panels are
accepted as an analytic BEM receiver-grid endpoint, not as project-FDTD, 3D, or
field evidence.

## Decision

Keep the 116-panel receiver-grid policy as analytic-only evidence.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator.py
tests/test_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validation_sensitivity.py
9 passed
```

Figure check:

```text
2645x850, dynamic range=255
```

