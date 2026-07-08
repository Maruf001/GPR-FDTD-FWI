# Experiment 1585: Runtime Budget Triage Policy

Date: 2026-06-29

## Purpose

Convert the measured runtime forecast from run `1579` into concrete CPU-screen
budget tiers.

## Output

```text
outputs/experiments/1585_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_triage_rows.csv
data/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy_summary.json
figures/local_2d_state_consistent_objective_revision_runtime_budget_triage_policy.png
```

## Result

```text
source budget ready:                     true
runtime-budget triage policy ready:      true
forecast scenarios:                      5
budget tiers:                            5
default budget:                          60 min
default recommended grid models:         90
default recommended scenario:            fine_transition_90
two-hour recommended grid models:        90
two-hour includes 200-grid screen:       false
first budget allowing 200-grid screen:   150 min
longest forecast:                        130.4277 min
seconds per grid model:                  39.1283
new FDTD executed:                       false
physical claim ready:                    false
GPU work ready:                          false
field transfer ready:                    false
field FWI ready:                         false
3D/HPC ready:                            false
```

The measured runtime forecast supports a 90-grid CPU screen within a one-hour
default budget. The 200-grid screen does not fit inside two hours; it first
fits the defined budget tiers at 150 minutes.

## Decision

Use 90 grid models as the default bounded CPU-screen ceiling from the current
measured replay rate. This is a planning policy only; it does not execute new
FDTD or promote physical, GPU, field, FWI, or 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_runtime_budget_triage_policy.py
4 passed
```

Figure check:

```text
3401x881, dynamic range=255
```
