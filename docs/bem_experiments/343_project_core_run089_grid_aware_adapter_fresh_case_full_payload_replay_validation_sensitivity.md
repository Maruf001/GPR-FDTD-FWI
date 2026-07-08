# BEM Experiment 343: Fresh-Case Full-Payload Replay Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `342` full-payload replay validator with controlled damaged
variants.

Run `342` validates that run `341` can replay the saved run `340` fresh-case
payloads exactly. This run checks that the validator rejects the kinds of drift
that would change that conclusion.

This is a CPU-only validator sensitivity run. It does not run FDTD, launch GPU
or HPC work, use field data, use the synthetic 2D archive, run field FWI, or
make a field-transfer claim.

## Output

```text
outputs/bem_experiments/343_project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validation_sensitivity
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validation_sensitivity_scenarios.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validation_sensitivity_summary.json
figures/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validation_sensitivity.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_FRESH_CASE_FULL_PAYLOAD_REPLAY_VALIDATION_SENSITIVITY.md
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
field claim ready:            false
3D validation ready:          false
GPU work ready:               false
field FWI ready:              false
```

## Interpretation

The validator accepts the exact run `341` replay audit and rejects controlled
damage to case counts, replay-ready counts, best variants, error metrics,
replay deltas, downstream states, figure validation, and script snapshots.

## Decision

Use runs `340-343` as the guarded full-payload fresh-case replay block. Broader
BEM promotion still requires a new scientific objective beyond this homogeneous
replayability repair.
