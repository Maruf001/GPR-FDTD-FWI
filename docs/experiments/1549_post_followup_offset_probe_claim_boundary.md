# Experiment 1549: Post Follow-Up Offset Probe Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the local 2D claim boundary after the executed follow-up offset probe
from runs `1546-1548`.

## Output

```text
outputs/experiments/1549_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary
```

## Result

```text
claim count:                         22
guarded claim count:                 19
blocked claim count:                 3
base claim count:                    21
base guarded claim count:            18
base blocked claim count:            3
follow-up sensitivity ready:         true
validator accepts exact run 1546:    true
validator rejects damaged variants:  true
planned case count:                  20
any-failure model count:             20
all-objective-failure model count:   0
narrow sampled window ready:         true
wide suppression-window claim ready: false
monotonic acquisition claim ready:   false
physical claim ready:                false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The new guarded claim records that the bounded 20-case follow-up probe executed
all planned offsets. All 20 models still had at least one objective failure,
and zero models had all-objective failure.

## Interpretation

The extra offsets around 45.0 mm do not turn the sampled suppression point into
a wider operating rule. The result remains a narrow local 2D objective-boundary
finding.

## Decision

Use run `1549` as the current local 2D claim boundary after the executed
follow-up offset probe. Keep wide-window, monotonic acquisition, physical, GPU,
field, field FWI, and 3D/HPC claims blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_followup_offset_probe_claim_boundary.py
3 passed
```

Figure check:

```text
3977x952, dynamic range=255
```
