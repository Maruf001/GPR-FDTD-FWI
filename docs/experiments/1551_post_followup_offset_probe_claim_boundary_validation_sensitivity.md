# Experiment 1551: Post Follow-Up Offset Probe Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1550` validator for the run `1549` local 2D
post-follow-up offset-probe claim boundary.

## Output

```text
outputs/experiments/1551_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary_validation_sensitivity
```

## Result

```text
scenario count:                     14
expected pass count:                1
observed pass count:                1
expected failure count:             13
observed failure count:             13
unexpected outcomes:                0
validation sensitivity ready:       true
validator accepts exact run 1549:   true
validator rejects damaged variants: true
claim count:                        22
guarded claim count:                19
blocked claim count:                3
planned case count:                 20
any-failure model count:            20
all-objective-failure model count:  0
wide suppression-window ready:      false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
3D/HPC ready:                       false
```

The exact run `1549` artifacts pass. Thirteen damaged variants fail as expected
for claim drift, follow-up row drift, follow-up count drift, false wide-window
promotion, downstream promotion, figure drift, and script-snapshot drift.

## Decision

Use runs `1549-1551` as the guarded 2D post-follow-up offset-probe
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x895, dynamic range=255
```
