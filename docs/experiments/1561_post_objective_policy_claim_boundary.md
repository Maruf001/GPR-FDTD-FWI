# Experiment 1561: Post Objective-Policy Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded objective-policy recommendation from runs `1558-1560` into the
current local 2D claim boundary.

This run does not launch FDTD, GPU work, field transfer, field FWI, or 3D/HPC.

## Output

```text
outputs/experiments/1561_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary
```

## Result

```text
claims:                               24
guarded claims:                       21
blocked claims:                       3
base boundary claims:                 23
objective-policy sensitivity ready:   true
objectives:                           6
candidate objectives:                 4
excluded objectives:                  2
candidate objectives:                 highband;late;late_high;veryhigh
excluded objectives:                  base;early_high
candidate selection rows:             80
excluded selection rows:              40
policy scope:                         saved_followup_offset_probe_only
gpu work ready:                       false
field transfer ready:                 false
3D/HPC ready:                         false
```

## Interpretation

The 2D boundary now includes a guarded objective-policy claim: for the saved
follow-up offset probe, retain `highband`, `late`, `late_high`, and `veryhigh`
as candidate objectives, and exclude `base` and `early_high`.

This is a narrow local policy for the already-saved follow-up probe. It does
not promote wide-window suppression, physical acquisition, GPU, field-transfer,
or 3D/HPC claims.

## Validation

```text
tests/test_local_2d_state_consistent_objective_revision_post_objective_policy_claim_boundary.py
2 passed
```

Figure validation:

```text
3941x924, dynamic range=255
```
