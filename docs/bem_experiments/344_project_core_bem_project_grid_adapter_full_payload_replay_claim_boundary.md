# BEM Experiment 344: Full-Payload Replay Claim Boundary

Date: 2026-06-28

## Purpose

Synthesize the BEM claim boundary after repairing the fresh-case replay payload
gap.

Runs `337-339` identified and guarded the artifact gap in the older run `094`
fresh-case stress output. Runs `340-343` repaired that gap by saving full
formula replay payloads for all three fresh homogeneous cases and proving that
the saved outputs replay exactly.

This uses saved artifacts only. It does not run FDTD, launch GPU or HPC work,
use field data, use the synthetic 2D archive, run field FWI, or make a field
transfer claim.

## Output

```text
outputs/bem_experiments/344_project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_claim_rows.csv
data/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary_summary.json
figures/project_core_bem_project_grid_adapter_full_payload_replay_claim_boundary.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FULL_PAYLOAD_REPLAY_CLAIM_BOUNDARY.md
```

## Result

```text
claims:                         7
guarded claims:                 4
blocked claims:                 3
fresh cases:                    3
full-payload ready cases:       3
replay-ready cases:             3
max replay frequency delta:     0.0
max replay band delta:          0.0
full-payload replay guarded:    true
homogeneous replay scope ready: true
broad BEM replacement ready:    false
field transfer ready:           false
3D validation ready:            false
GPU work ready:                 false
field FWI ready:                false
```

## Interpretation

The BEM fresh-case replayability gap has been repaired for the tested
homogeneous branch: all three cases save full formula payloads and replay
exactly. This does not promote broader BEM replacement, field transfer, 3D
validation, GPU work, or field FWI.

## Decision

Use run `344` as the BEM full-payload replay claim boundary. The next BEM
scientific step must define a broader material, half-space, layered, 3D, or
measured-comparison objective.
