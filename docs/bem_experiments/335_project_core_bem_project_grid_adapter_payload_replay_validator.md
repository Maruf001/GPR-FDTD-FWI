# BEM Experiment 335: Project-Grid Adapter Payload Replay Validator

Date: 2026-06-28

## Purpose

Validate the saved run `334` payload replay audit from artifacts.

This run confirms that the run `334` replay result is internally consistent:
payload shapes are stable, the best variant and metric are reproduced, replay
deltas are zero, source checks pass, figure validation is present, script
snapshots exist, and downstream claim guardrails remain blocked.

This is an artifact validator. It does not run FDTD, GPU/HPC work, field data,
field FWI, neural-network training, or synthetic 2D archive promotion.

## Output

```text
outputs/bem_experiments/335_project_core_bem_project_grid_adapter_payload_replay_validator
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_payload_replay_validator_checks.csv
data/project_core_bem_project_grid_adapter_payload_replay_validator_summary.json
figures/project_core_bem_project_grid_adapter_payload_replay_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
replay validation ready:            true
target cells:                       753
scan positions:                     7
selected frequency bins:            17
source best variant:                receiver_conjugate_div_source
replayed best variant:              receiver_conjugate_div_source
max frequency-bin delta:            0.0
max time-band delta:                0.0
field claim ready:                  false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

The saved run `334` replay audit is internally consistent: payload shapes are
stable, the best variant and metric are reproduced, replay deltas are zero, and
the guarded downstream states remain blocked.

## Decision

Use runs `334-335` as the guarded executable payload replay block. Future
adapter work can depend on the replayed eight-item payload, but broader field,
archive, 3D, GPU, and field-FWI claims remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_payload_replay_validator.py
3 passed
```

Figure validation:

```text
3329x902, dynamic range=255
```
