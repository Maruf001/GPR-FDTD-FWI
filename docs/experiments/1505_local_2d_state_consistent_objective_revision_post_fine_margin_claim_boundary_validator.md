# Experiment 1505: Post Fine Margin Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1504` post-margin local 2D claim boundary from
artifacts.

Run `1504` added the guarded positive-margin observation to the claim boundary.
This run checks that the saved boundary preserves the expected claim counts,
margin claim, margin metrics, blocked downstream states, figure validation, and
script snapshots.

This run does not run new FDTD simulations, launch GPU work, transfer claims to
field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1505_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:           7
passed checks:               7
failed checks:               0
validation ready:            true
claims:                      15
guarded claims:              12
blocked claims:              3
margin sensitivity ready:    true
margin sign flip:            true
max min-margin before 45:    -0.000374885
min margin at 45:            0.00022905
GPU work ready:              false
field transfer ready:        false
3D/HPC ready:                false
figure size:                 3761x928
figure dynamic range:        255
```

## Interpretation

The post-margin claim boundary validates from artifacts. It preserves 15
claims, 12 guarded claims, the positive 45 mm margin observation, and blocked
downstream states.

## Decision

Use run `1505` as the validator for the post-margin local 2D claim boundary.
Sensitivity hardening remains required before treating this boundary as
guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_margin_claim_boundary_validator.py
3 passed
```
