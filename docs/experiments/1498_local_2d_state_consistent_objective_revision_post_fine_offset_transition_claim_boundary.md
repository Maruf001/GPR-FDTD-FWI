# Experiment 1498: Post Fine Offset-Transition Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the local 2D near/far claim boundary after adding the fine
40-45 mm acquisition-layout transition block from runs `1495-1497`.

This run uses saved artifacts only. It does not run new FDTD simulations,
launch GPU work, transfer to field evidence, run field FWI, or start 3D/HPC
work.

## Output

```text
outputs/experiments/1498_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                              14
guarded claims:                      11
blocked claims:                      3
base claims:                         13
design axes ready:                   5 / 5
boundary ready:                      true
fine validation ready:               true
fine sensitivity ready:              true
fine Tx/Rx offsets mm:               [40, 41, 42, 43, 44, 45]
fine grid models:                    90
fine objective selection rows:       540
fine candidate rows:                 2160
fine truth/any/all failure:          58 / 32 / 12
40-44 mm far-error any persists:     true
45 mm far-error any suppressed:      true
40-45 mm far-error all suppressed:   true
first any far -0.8 suppression mm:   45.0
first any far -1.6 suppression mm:   45.0
broad radius promoted:               false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
figure size:                         3725x964
figure dynamic range:                255
```

## Interpretation

The refined 2D near/far claim boundary now includes the fine
acquisition-layout transition. In the tested 40-45 mm sweep, far-error
any-objective failures persist through 44 mm and first clear at 45 mm, while
all-objective far-error failures remain absent throughout the fine sweep.

This adds one guarded acquisition-layout claim to the previous boundary. The
broader decision does not change: the mechanism remains a local synthetic
result, not a broad radius-tolerance policy or a field-transfer claim.

## Decision

Use run `1498` as the current fine-refined local 2D near/far claim boundary.
Keep broad invariant radius-tolerance, physical-transfer, GPU, field-FWI, and
3D/HPC claims blocked until measured-field evidence or a new validated compute
objective changes the decision boundary.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_fine_offset_transition_claim_boundary.py
4 passed
```
