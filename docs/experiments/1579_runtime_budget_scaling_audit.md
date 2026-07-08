# Experiment 1579: Runtime Budget Scaling Audit

Date: 2026-06-29

## Purpose

Estimate bounded CPU runtime budgets from the measured aggregate replay cost in
run `1573`.

## Output

```text
outputs/experiments/1579_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_forecast_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit.png
```

## Result

```text
source runtime ready:               true
runtime budget audit ready:         true
forecast scenarios:                 5
source elapsed seconds:             782.566
source grid models:                 20
seconds per grid model:             39.1283
seconds per objective row:          6.5213833333333335
seconds per candidate row:          1.6303458333333334
largest forecast grid models:       200
longest forecast minutes:           130.42766666666668
longest forecast hours:             2.173794444444445
new FDTD executed:                  false
bounded CPU planning ready:         true
per-objective CLI available:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The forecast rows use the measured 39.1283 seconds per grid model from run
`1573`. The largest included planning case has 200 grid models and estimates to
about 130.43 CPU minutes.

## Decision

Use this as planning context for bounded CPU probes. This run does not execute
new FDTD and does not promote physical, GPU, field, FWI, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_scaling_audit.py
4 passed
```

Figure check:

```text
3401x895, dynamic range=255
```
