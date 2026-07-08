# Experiment 1437: Local 2D Post Objective-Revision Claim Boundary

Date: 2026-06-28

## Purpose

Refresh the local 2D claim boundary after the run `1436` prospective
objective-revision sweep.

This run uses saved run `1436` artifacts only. It does not execute new FDTD
simulations, launch GPU work, transfer to field data, run field FWI, or promote
3D/HPC work.

## Output

```text
outputs/experiments/1437_local_2d_state_consistent_post_objective_revision_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_post_objective_revision_claim_boundary_rows.csv
data/local_2d_state_consistent_post_objective_revision_claim_boundary_summary.json
figures/local_2d_state_consistent_post_objective_revision_claim_boundary.png
docs/LOCAL_2D_STATE_CONSISTENT_POST_OBJECTIVE_REVISION_CLAIM_BOUNDARY.md
scripts/run_local_2d_state_consistent_post_objective_revision_claim_boundary.py
scripts/test_local_2d_state_consistent_post_objective_revision_claim_boundary.py
scripts/script_snapshot_manifest.json
```

## Result

```text
boundary rows:                         5
local-ready rows:                      1
bounded observations:                  1
blocked claims:                        3
objective revision local validation:   true
veryhigh failure count:                3
veryhigh failure labels:               far_neighbor_radius_minus_1p10mm; far_neighbor_radius_minus_1p40mm; near_neighbor_radius_plus_2p00mm
non-veryhigh failure count:            0
drop-veryhigh prospective supported:   true
majority-vote prospective supported:   true
promote revised objective now:         false
broad radius tolerance promoted:       false
physical claim ready:                  false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

The revised local objective policy is validated for the current prospective
local 2D sweep, while `veryhigh` is identified as unstable for the tested
radius-neighbor branch.

## Decision

Use run `1437` as the current local 2D objective-revision claim boundary. Keep
broad-radius, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_post_objective_revision_claim_boundary.py
4 passed
```

Figure validation:

```text
2771x840, dynamic range=255
```
