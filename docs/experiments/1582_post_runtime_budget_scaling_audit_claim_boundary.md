# Experiment 1582: Post Runtime-Budget Scaling Audit Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded runtime-budget scaling audit from runs `1579-1581` into the
current local 2D claim boundary.

## Output

```text
outputs/experiments/1582_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary.png
```

## Result

```text
claims:                             27
guarded claims:                     24
blocked claims:                     3
runtime budget audit ready:         true
runtime budget sensitivity ready:   true
forecast scenarios:                 5
seconds per grid model:             39.1283
largest forecast grid models:       200
longest forecast minutes:           130.42766666666668
new FDTD executed:                  false
bounded CPU planning ready:         true
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The new guarded claim records bounded CPU runtime planning from the measured
replay rate. It does not promote new FDTD execution or downstream readiness.

## Decision

Use this as the current 2D claim boundary after the runtime-budget scaling
audit.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_runtime_budget_scaling_audit_claim_boundary.py
4 passed
```

Figure check:

```text
3941x906, dynamic range=255
```
