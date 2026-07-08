# Experiment 1550: Post Follow-Up Offset Probe Claim Boundary Validator

Date: 2026-06-29

## Purpose

Validate the saved run `1549` local 2D post-follow-up offset-probe claim
boundary from artifacts.

## Output

```text
outputs/experiments/1550_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary_validator
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
validation ready:                   true
claim count:                        22
guarded claim count:                19
blocked claim count:                3
planned case count:                 20
any-failure model count:            20
all-objective-failure model count:  0
narrow sampled window ready:        true
wide suppression-window ready:      false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator checks claim counts, the follow-up claim row, follow-up probe
metrics, blocked claim rows, downstream blocked states, figure validation, and
script snapshots.

## Decision

Use run `1550` as the validator for run `1549`. Sensitivity hardening remains
required before closing the block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary_validator.py
3 passed
```

Figure check:

```text
3797x929, dynamic range=255
```
