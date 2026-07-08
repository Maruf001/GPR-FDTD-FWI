# BEM Experiment 346: Full-Payload Replay Claim Boundary Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `345` full-payload replay claim-boundary validator with
controlled damaged variants.

This run checks that the validator accepts the exact run `344` claim boundary
and rejects damaged variants that alter claim counts, replay counts, replay
deltas, blocked-claim readiness, downstream guardrails, figure validation, or
script snapshots.

This uses saved artifacts only. It does not run FDTD, launch GPU or HPC work,
use field data, use the synthetic 2D archive, run field FWI, or make a field
transfer claim.

## Output

```text
outputs/bem_experiments/346_project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validation_sensitivity_rows.csv
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validation_sensitivity_summary.json
figures/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FULL_PAYLOAD_REPLAY_CLAIM_BOUNDARY_VALIDATION_SENSITIVITY.md
```

## Result

```text
scenarios:                    12
expected pass:                1
observed pass:                1
expected failures:            11
observed failures:            11
unexpected outcomes:          0
sensitivity ready:            true
exact run accepted:           true
damaged variants rejected:    true
broad BEM replacement ready:  false
field transfer ready:         false
3D validation ready:          false
GPU work ready:               false
field FWI ready:              false
```

## Interpretation

The run `345` validator accepts the exact run `344` claim boundary and rejects
controlled damaged variants that alter claim counts, replay counts, replay
deltas, blocked-claim state, downstream guardrails, figure validation, or script
snapshots.

## Decision

Use runs `344-346` as the guarded BEM full-payload replay claim-boundary block.
This hardens the homogeneous replayability claim but still does not promote
broad BEM replacement, field transfer, 3D validation, GPU work, or field FWI.
