# Experiment 1516: Post Midpoint Probe Claim Boundary

Date: 2026-06-29

## Purpose

Integrate the guarded midpoint-probe correction from runs `1513-1515` into the
local 2D near/far claim boundary.

The boundary keeps the `44.621 mm` crossing as a margin-only estimate and adds
a separate directly tested claim: the far-error suppression transition remains
at `45.0 mm` in the tested fractional-offset probe.

This uses saved artifacts only. It does not run new FDTD simulations, launch
GPU work, transfer to field evidence, run field FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1516_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_MIDPOINT_PROBE_CLAIM_BOUNDARY.md
scripts/
```

## Result

```text
claims:                           17
guarded claims:                   14
blocked claims:                   3
base claims:                      16
base guarded claims:              13
base blocked claims:              3
boundary ready:                   true
midpoint sensitivity ready:       true
far -0.8 first suppression:       45.0 mm
far -1.6 first suppression:       45.0 mm
linear crossing promoted:         false
discrete transition offset:       45.0 mm
physical claim ready:             false
GPU work ready:                   false
field transfer ready:             false
field FWI ready:                  false
3D/HPC ready:                     false
```

The corrected boundary has two separate guarded statements:

| Claim | Status | Interpretation |
| --- | --- | --- |
| `fine_transition_crossing_is_near_45mm` | `guarded_margin_only_crossing_estimate` | The `44.621 mm` value remains a margin-only estimate. |
| `midpoint_probe_confirms_discrete_45mm_transition` | `guarded_acquisition_midpoint_probe` | The directly tested far-error suppression transition remains `45.0 mm`. |

## Interpretation

The direct midpoint probe corrects the earlier crossing-estimate
interpretation. The `44.621 mm` value should not be promoted to a discrete
operating threshold. The directly tested far-error suppression transition
remains `45.0 mm`.

## Decision

Use run `1516` as the current local 2D near/far claim boundary after the
midpoint-probe correction. Keep broad physical, GPU, field-transfer,
field-FWI, and 3D/HPC claims blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary.py: pass
```

Figure validation:

```text
3761x970, dynamic range=255
```
