# Experiment 1523: Post High-Side Stability Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1522` claim boundary from artifacts.

This run checks the high-side claim row, the updated midpoint claim row, the
`45.125 mm` reappearance metrics, blocked downstream states, figure validation,
and script snapshots.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1523_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_HIGH_SIDE_STABILITY_CLAIM_BOUNDARY_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:                   8
passed checks:                       8
failed checks:                       0
validation ready:                    true
claims:                              18
guarded claims:                      15
blocked claims:                      3
far -0.8 first suppression:          45.0 mm
far -1.6 first suppression:          45.0 mm
far -0.8 first reappearance:         45.125 mm
far -1.6 first reappearance:         45.125 mm
larger-offset safety claim ready:    false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Interpretation

The saved post-high-side claim boundary is internally consistent: it preserves
the sampled `45.0 mm` suppression point, records the `45.125 mm` failure
reappearance, and keeps downstream claims blocked.

## Decision

Use run `1523` as the validator for the run `1522` claim boundary. Sensitivity
hardening remains required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_high_side_stability_claim_boundary_validator.py: pass
```

Figure validation:

```text
3581x924, dynamic range=255
```
