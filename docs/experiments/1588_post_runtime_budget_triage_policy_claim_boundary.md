# Experiment 1588: Post Runtime-Budget Triage Policy Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded runtime-budget triage policy from runs `1585-1587` into the
current 2D claim boundary.

## Output

```text
outputs/experiments/1588_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary.png
```

## Result

```text
claims:                                 28
guarded claims:                         25
blocked claims:                         3
runtime-budget triage policy ready:     true
runtime-budget triage sensitivity ready:true
forecast scenarios:                     5
budget tiers:                           5
default budget:                         60 min
default recommended grid models:        90
two-hour recommended grid models:       90
two-hour includes 200-grid screen:      false
first budget allowing 200-grid screen:  150 min
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
```

The new guarded claim records the measured-runtime planning policy: 90 grid
models are the default one-hour CPU-screen ceiling, and the 200-grid screen is
not a two-hour screen under the current measured rate.

## Decision

Use this as the current 2D claim boundary after the runtime-budget triage
policy. No new FDTD, physical, GPU, field-transfer, field-FWI, or 3D/HPC claim
is promoted.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_triage_policy_claim_boundary.py
4 passed
```

Figure check:

```text
3941x906, dynamic range=255
```
