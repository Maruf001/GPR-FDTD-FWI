# Experiment 1438: Local 2D Post Objective-Revision Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `1437` local 2D objective-revision claim boundary from
artifacts.

This run checks that the boundary table, summary counts, `veryhigh` failure
pattern, local-policy support, and blocked downstream claims agree.

This run does not execute new FDTD simulations, launch GPU work, transfer to
field data, run field FWI, or promote 3D/HPC work.

## Output

```text
outputs/experiments/1438_local_2d_state_consistent_post_objective_revision_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_post_objective_revision_claim_boundary_validation_checks.csv
data/local_2d_state_consistent_post_objective_revision_claim_boundary_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_post_objective_revision_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_POST_OBJECTIVE_REVISION_CLAIM_BOUNDARY_VALIDATOR.md
scripts/run_local_2d_state_consistent_post_objective_revision_claim_boundary_validator.py
scripts/test_local_2d_state_consistent_post_objective_revision_claim_boundary_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                 6
passed checks:                     6
blocking failures:                 0
claim-boundary validation ready:   true
objective revision local ready:    true
veryhigh failure count:            3
non-veryhigh failure count:        0
drop-veryhigh supported:           true
majority-vote supported:           true
promote revised objective now:     false
broad radius tolerance promoted:   false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

## Interpretation

The saved claim boundary is internally consistent. The drop-`veryhigh` and
majority-vote policy support is recorded, the `veryhigh` failure pattern
remains bounded to the three saved prospective cases, and
broad/physical/GPU/field/FWI/3D claims remain blocked.

## Decision

Use run `1438` as the validator for the local 2D objective-revision claim
boundary. Sensitivity remains required before treating the validator as
guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_post_objective_revision_claim_boundary_validator.py
3 passed
```

Figure validation:

```text
2825x850, dynamic range=255
```
