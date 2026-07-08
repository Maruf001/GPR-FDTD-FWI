# BEM Experiment 336: Project-Grid Adapter Payload Replay Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `335` payload replay validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `334` replay audit and
rejects damaged versions with count drift, payload-shape drift,
best-variant drift, nonzero replay deltas, failed source checks, false
downstream promotion, invalid figure metadata, and missing script snapshots.

This is an artifact sensitivity test. It does not run FDTD, GPU/HPC work,
field data, field FWI, neural-network training, or synthetic 2D archive
promotion.

## Output

```text
outputs/bem_experiments/336_project_core_bem_project_grid_adapter_payload_replay_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_payload_replay_validation_sensitivity_scenarios.csv
data/project_core_bem_project_grid_adapter_payload_replay_validation_sensitivity_summary.json
figures/project_core_bem_project_grid_adapter_payload_replay_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                    10
expected pass:                1
observed pass:                1
expected failures:            9
observed failures:            9
unexpected outcomes:          0
sensitivity ready:            true
accepts exact run 334:        true
rejects damaged variants:     true
field claim ready:            false
3D validation ready:          false
GPU work ready:               false
field FWI ready:              false
```

## Interpretation

The payload replay validator accepts the exact run `334` audit and rejects
damaged variants covering count drift, shape drift, best-variant drift,
nonzero replay deltas, source-check failure, downstream promotion, figure
validation, and script snapshots.

## Decision

Use runs `334-336` as the guarded executable payload replay block. Future
adapter work should continue from the replayable eight-item payload while
field, archive, 3D, GPU, and field-FWI claims remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_project_grid_adapter_payload_replay_validation_sensitivity.py
3 passed
```

Figure validation:

```text
3293x891, dynamic range=255
```
