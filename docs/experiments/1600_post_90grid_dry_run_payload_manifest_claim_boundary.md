# Experiment 1600: Post 90-Grid Dry-Run Payload Manifest Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded 90-grid dry-run payload-manifest block from runs `1597-1599`
into the current 2D claim boundary.

## Output

```text
outputs/experiments/1600_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_claim_rows.csv
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_summary.json
figures/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claims:                                      30
guarded claims:                              27
blocked claims:                              3
dry-run payload manifest ready:              true
manifest validation sensitivity ready:       true
payload rows:                                90
objective profiles:                          5
transition bins:                             18
budget:                                      60 min
estimated total runtime:                     58.69245 min
budget headroom:                             1.30755 min
executable commands:                         0
run-specific execution script available:     false
commands executed:                           false
new FDTD executed:                           false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The new guarded claim records that the default one-hour 90-grid screen has been
materialized as a review-only payload manifest. It is still not an executable
FDTD run.

## Decision

Use this as the current 2D claim boundary after the dry-run payload-manifest
block. New FDTD, physical, GPU, field-transfer, field-FWI, and 3D/HPC claims
remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary.py
5 passed
```

Figure check:

```text
3941x894, dynamic range=255
```
