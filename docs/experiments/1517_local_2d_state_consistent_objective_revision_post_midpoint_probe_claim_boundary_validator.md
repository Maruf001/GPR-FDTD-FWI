# Experiment 1517: Post Midpoint Probe Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1516` post-midpoint claim boundary from artifacts.

This run checks that the corrected boundary preserves the separation between
the margin-only crossing estimate and the directly tested `45.0 mm` transition
claim. It also validates claim counts, blocked downstream rows, figure output,
and script snapshots.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1517_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_MIDPOINT_PROBE_CLAIM_BOUNDARY_VALIDATOR.md
scripts/
```

## Result

```text
validation checks:                  8
passed checks:                      8
failed checks:                      0
validation ready:                   true
claims:                             17
guarded claims:                     14
blocked claims:                     3
far -0.8 first suppression:         45.0 mm
far -1.6 first suppression:         45.0 mm
linear crossing promoted:           false
discrete transition offset:         45.0 mm
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The saved post-midpoint claim boundary is internally consistent. The crossing
estimate remains margin-only, the direct midpoint probe carries the discrete
`45.0 mm` transition claim, and downstream physical, GPU, field, and 3D claims
remain blocked.

## Decision

Use run `1517` as the validator for the run `1516` corrected claim boundary.
Sensitivity hardening remains required before treating the block as fully
guarded.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validator.py: pass
```

Figure validation:

```text
3545x930, dynamic range=255
```
