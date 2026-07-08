# BEM Experiment 345: Full-Payload Replay Claim Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `344` full-payload replay claim boundary.

This validator checks the claim counts, replay counts, zero replay deltas,
blocked broader claims, downstream guardrails, figure validation, and script
snapshots.

This uses saved artifacts only. It does not run FDTD, launch GPU or HPC work,
use field data, use the synthetic 2D archive, run field FWI, or make a field
transfer claim.

## Output

```text
outputs/bem_experiments/345_project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validator_checks.csv
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validator_summary.json
figures/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_validator.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FULL_PAYLOAD_REPLAY_CLAIM_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:                  6
passed checks:                      6
failed checks:                      0
validation ready:                   true
claims:                             7
guarded claims:                     4
blocked claims:                     3
fresh cases:                        3
full-payload ready cases:           3
replay-ready cases:                 3
homogeneous replay scope ready:     true
broad BEM replacement ready:        false
field transfer ready:               false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

Run `344` validates as the BEM full-payload replay claim boundary: the
homogeneous fresh-case branch is replayable from saved payloads, while broader
BEM, field, 3D, GPU, and FWI claims remain blocked.

## Decision

Use run `345` as the validator for the BEM full-payload replay claim boundary.
Sensitivity hardening remains the next guard step.
