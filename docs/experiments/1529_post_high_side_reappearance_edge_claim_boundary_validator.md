# Experiment 1529: Post High-Side Reappearance Edge Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1528` local 2D claim boundary from artifacts.

This run checks that the high-side reappearance-edge decision is internally
consistent before the block is sensitivity-hardened. It does not run new FDTD
simulations, launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/experiments/1529_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validator.png
scripts/
```

## Result

```text
validation checks:                   8
passed checks:                       8
failed checks:                       0
validation ready:                    true
claims:                              19
guarded claims:                      16
blocked claims:                      3
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance:         45.015625 mm
far -1.6 first reappearance:         45.015625 mm
larger-offset safety claim ready:    false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved claim boundary is internally consistent. It preserves the sampled
45.0 mm suppression point, records failure reappearance at 45.015625 mm, and
keeps downstream physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Decision

Use run `1529` as the validator for the run `1528` claim boundary. Sensitivity
hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_reappearance_edge_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
3581x923, dynamic range=255
```
