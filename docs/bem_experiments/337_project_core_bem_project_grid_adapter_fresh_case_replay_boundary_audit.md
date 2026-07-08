# BEM Experiment 337: Fresh-Case Replay Boundary Audit

Date: 2026-06-28

## Purpose

Audit whether the saved run `094` fresh-case grid-aware adapter stress arrays
are sufficient for independent formula replay.

Run `094` established that three fresh homogeneous cases pass the numerical
adapter comparison. Run `334` later showed that a single saved run `093` payload
can be replayed exactly from the adapter formula. This run asks whether the
same independent replay standard can be applied retroactively to all run `094`
fresh cases.

This is a CPU-only artifact audit. It does not run FDTD, launch GPU or HPC
work, use field data, use the synthetic 2D archive, run field FWI, or make a
field-transfer claim.

## Output

```text
outputs/bem_experiments/337_project_core_bem_project_grid_adapter_fresh_case_replay_boundary_audit
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_audit_rows.csv
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_audit_summary.json
figures/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_audit.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FRESH_CASE_REPLAY_BOUNDARY_AUDIT.md
```

## Result

```text
fresh cases:                         3
fresh case passes:                   3
single-payload replay ready:         true
required replay items per case:      12
minimum saved replay items:          9
maximum missing replay items:        3
formula-replay ready cases:          0
formula-replay blocked cases:        3
fresh-case independent replay ready: false
future full payload required:        true
field claim ready:                   false
3D validation ready:                 false
GPU work ready:                      false
field FWI ready:                     false
```

Each run `094` fresh case saves comparator-ready outputs but omits three inputs
needed for independent formula replay:

```text
tx_background_field_at_cells
rx_background_field_at_cells
source_spectrum
```

## Interpretation

The fresh-case stress result remains useful as a numerical acceptance result:
all three fresh homogeneous cases passed. It is not, however, sufficient for
the stricter executable replay standard introduced by run `334`, because the
saved artifacts do not contain the full formula inputs.

This is an artifact-completeness boundary, not a numerical failure.

## Decision

Use run `337` as the fresh-case replay boundary. Future fresh-case stress
scripts should save the full replay payload per case before claiming
independent replayability across fresh geometries.

No field transfer, 3D validation, GPU escalation, or field FWI is justified by
this audit.
