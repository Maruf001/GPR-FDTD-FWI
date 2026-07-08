# Experiment 1493: Post Offset-Transition Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1492` refined near/far claim-boundary artifact from
saved tables.

This run checks claim counts, five-axis readiness, spacing/source/acquisition
counts, the acquisition-layout transition thresholds, blocked claims, blocked
downstream states, figure validation, and script snapshots.

This is CPU-only artifact validation. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1493_local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_validator_checks.csv
data/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_validator_summary.json
figures/local_2d_state_consistent_objective_revision_post_offset_transition_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:             9
passed checks:                 9
failed checks:                 0
validation ready:              true
claims:                        13
guarded claims:                10
blocked claims:                3
design axes ready:             5 / 5
source threshold stable:       true
45 mm acquisition suppression: true
35 mm all-failure suppression: true
any failure through 40 mm:     true
broad radius promoted:         false
physical claim ready:          false
GPU work ready:                false
field transfer ready:          false
field FWI ready:               false
3D/HPC ready:                  false
figure size:                   3545x928
figure dynamic range:          255
```

## Interpretation

Run `1492` validates as the refined local 2D near/far claim boundary. The
mechanism remains guarded local evidence, and the acquisition-layout branch now
has a two-threshold transition map.

## Decision

Use run `1493` as the validator for the refined offset-transition claim
boundary. Keep broad-radius, physical, GPU, field-transfer, field-FWI, and
3D/HPC claims blocked.
