# BEM Experiment 703: 116-Panel Receiver-Grid Policy Refresh Validator

Date: 2026-06-30

## Purpose

Validate run `702`, the guarded 116-panel analytic BEM receiver-grid policy
refresh.

This is a CPU-only validation wrapper around saved run `702` artifacts. It
does not run new BEM solves, compare against project FDTD outputs, run 3D
Maxwell BEM, launch GPU/HPC work, or promote field transfer.

## Output

```text
outputs/bem_experiments/703_scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator
```

Key artifacts:

```text
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator_check_rows.csv
data/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator_summary.json
figures/scarep_2d_cpu_bem_panel116_receiver_grid_policy_refresh_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
metric rows:                               2
policy rows:                               5
guarded receiver-grid panel:               116
frequency grids:                           2
scan-count variants:                       3
worst 116-panel high-band relative L2:     0.0009518291083452528
minimum margin to target:                  0.000048170891654747265
per-frequency diagnostic required:         true
lower-panel policy change ready:           false
field transfer ready:                      false
field FWI ready:                           false
validation ready:                          true
```

The checks cover source readiness, metric/policy shape, 116-panel guarded
endpoint status, diagnostic policy preservation, analytic-only claim boundary,
figure output, and frozen script snapshots.

## Interpretation

Run `702` validates as an analytic-only 116-panel receiver-grid endpoint
policy.

## Decision

Keep 116 panels as the guarded receiver-grid analytic BEM endpoint.

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
2357x841, dynamic range=255
```

