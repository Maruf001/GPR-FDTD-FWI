# Experiment 1776: 84-Grid External Return Live Intake Gate

Date: 2026-07-01

## Purpose

Convert the 84-grid external-return ledger from runs `1773-1775` into a live
intake gate that can inspect real returned files.

This run does not materialize observed-by-case data, execute FDTD, launch GPU
work, transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1776_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_stage_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_item_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_artifact_job_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source external ledger ready:       true
stages:                             6
expected external items:            21
live parents present:               1
live files present:                 0
missing live files:                 21
accepted external items:            0
approval tokens required/accepted:  1 / 0
cache arrays required/accepted:     10 / 0
result JSON required/accepted:      10 / 0
artifact jobs required/accepted:    10 / 0
materialization input accepted:     false
ready for materialization:          false
new FDTD executed:                  false
gpu priority:                       none
```

Current intake statuses:

| Status | Count |
| --- | ---: |
| missing approval token | 1 |
| missing cache array | 10 |
| missing result JSON | 10 |

## Interpretation

The ledger is no longer only a checklist. It now has a live consumer that will
inspect the approval token, each cache array, each result JSON, and each paired
artifact job.

The expected return still has no accepted file:

- the approval token is absent,
- all ten cache arrays are absent,
- all ten result JSON files are absent,
- all ten paired artifact jobs remain unaccepted.

The intake accepts only real materialization evidence. It rejects missing files,
synthetic or placeholder approval tokens, unreadable or non-finite cache arrays,
malformed result JSON, identity mismatches, incomplete shape/hash metadata,
non-completed solver status, and result JSON that does not prove new FDTD
execution plus validator acceptance.

## Decision

Use run `1776` as the active 2D external-return intake gate. Keep 84-grid
materialization and FDTD execution blocked until the approval token and all
twenty artifacts pass intake.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py
5 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_live_intake_gate.py: pass
```

Figure check:

```text
2356x846, dynamic range=255
```
