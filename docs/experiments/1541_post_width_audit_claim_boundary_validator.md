# Experiment 1541: Post Width Audit Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1540` post-width-audit claim boundary from artifacts.

This run checks source identity, claim counts, the width-audit claim row, width
metrics, blocked claim rows, downstream blocked states, figure validation, and
script snapshots.

## Output

```text
outputs/experiments/1541_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                   7
passed checks:                       7
failed checks:                       0
validation ready:                    true
claims:                              21
guarded claims:                      18
blocked claims:                      3
lower failure-to-suppression gap:    0.007812 mm
suppression-to-upper-failure gap:    0.015625 mm
failure-to-failure bracket span:     0.023437 mm
narrow sampled window ready:         true
wide suppression-window claim ready: false
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved post-width-audit claim boundary is internally consistent and keeps
wide-window, monotonic, physical, GPU, field, and 3D claims blocked.

## Decision

Use run `1541` as the validator for the run `1540` post-width-audit claim
boundary. Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_width_audit_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3689x929, dynamic range=255
```
