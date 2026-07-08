# Experiment 1535: Post Two-Sided Edge Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1534` two-sided edge claim boundary from artifacts.

This run checks source identity, claim counts, high-side and low-side edge
claim rows, two-sided edge metrics, blocked downstream states, figure
validation, and script snapshots.

## Output

```text
outputs/experiments/1535_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validator_validation_checks.csv
data/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                   8
passed checks:                       8
failed checks:                       0
validation ready:                    true
claims:                              20
guarded claims:                      17
blocked claims:                      3
far -0.8 last failed below 45:       44.992188 mm
far -1.6 last failed below 45:       44.992188 mm
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance above 45:45.015625 mm
far -1.6 first reappearance above 45:45.015625 mm
broad acquisition safety ready:      false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved two-sided claim boundary is internally consistent. The artifact
records failure persistence immediately below 45.0 mm, suppression at 45.0 mm,
and reappearance immediately above 45.0 mm.

## Decision

Use run `1535` as the validator for the run `1534` two-sided claim boundary.
Sensitivity hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_two_sided_edge_claim_boundary_validator.py
4 passed
```

Figure validation:

```text
3797x943, dynamic range=255
```
