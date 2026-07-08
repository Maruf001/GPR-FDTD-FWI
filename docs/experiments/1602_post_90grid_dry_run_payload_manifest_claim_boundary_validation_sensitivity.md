# Experiment 1602: Post 90-Grid Dry-Run Payload Manifest Claim-Boundary Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `1601` validator against controlled damage to the
post-manifest claim boundary.

## Output

```text
outputs/experiments/1602_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                       30
expected pass scenarios:                     1
observed pass scenarios:                     1
expected failure scenarios:                  29
observed failure scenarios:                  29
unexpected outcomes:                         0
validation sensitivity ready:                true
validator accepts exact run 1600:            true
validator rejects damaged variants:          true
commands executed:                           false
new FDTD executed:                           false
physical claim ready:                        false
GPU work ready:                              false
field transfer ready:                        false
field FWI ready:                             false
3D/HPC ready:                                false
```

The validator accepts the exact run `1600` boundary and rejects damage to claim
counts, manifest-claim support, manifest metrics, hidden execution, downstream
promotion, figure validation, and script snapshots.

## Decision

Use runs `1600-1602` as the current guarded 2D post-90-grid-manifest
claim-boundary block.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_post_90grid_dry_run_payload_manifest_claim_boundary_validation_sensitivity.py
3 passed
```

Figure check:

```text
3581x887, dynamic range=255
```
