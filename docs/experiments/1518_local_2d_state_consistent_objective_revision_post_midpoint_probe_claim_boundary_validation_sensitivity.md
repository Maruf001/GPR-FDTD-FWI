# Experiment 1518: Post Midpoint Probe Claim Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1517` post-midpoint claim-boundary validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `1516` corrected
claim boundary and rejects damaged variants covering claim-count drift,
margin-only wording loss, midpoint-claim drift, suppression-offset drift,
linear-threshold promotion, blocked-row drift, downstream promotion, figure
validation drift, and script-snapshot drift.

It does not run FDTD, launch GPU work, transfer to field evidence, run field
FWI, or start 3D/HPC work.

## Output

```text
outputs/experiments/1518_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_POST_MIDPOINT_PROBE_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                          15
expected pass:                      1
observed pass:                      1
expected failures:                  14
observed failures:                  14
unexpected outcomes:                0
sensitivity ready:                  true
accepts exact run 1516:             true
rejects damaged variants:           true
linear crossing promoted:           false
discrete transition offset:         45.0 mm
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The run `1517` validator accepts the exact run `1516` boundary and rejects the
damaged variants. This protects the corrected claim-boundary language:
`44.621 mm` remains a margin-only estimate, while the directly tested discrete
far-error suppression transition remains `45.0 mm`.

## Decision

Use runs `1516-1518` as the guarded post-midpoint local 2D claim-boundary
block. Keep broad physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_post_midpoint_probe_claim_boundary_validation_sensitivity.py: pass
```

Figure validation:

```text
3437x922, dynamic range=255
```
