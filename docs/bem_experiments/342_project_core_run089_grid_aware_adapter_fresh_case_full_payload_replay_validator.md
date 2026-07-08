# BEM Experiment 342: Fresh-Case Full-Payload Replay Validator

Date: 2026-06-28

## Purpose

Validate the saved run `341` full-payload replay audit from artifacts.

Run `341` showed that all three run `340` full-payload fresh cases replay from
saved formula inputs and reproduce the saved adapter outputs exactly to
numerical precision. This run validates that result from the saved tables,
summary, figure validation, and script snapshots.

This is a CPU-only validator. It does not run FDTD, launch GPU or HPC work, use
field data, use the synthetic 2D archive, run field FWI, or make a
field-transfer claim.

## Output

```text
outputs/bem_experiments/342_project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validator
```

Key artifacts:

```text
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validator_checks.csv
data/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validator_summary.json
figures/project_core_run089_grid_aware_adapter_fresh_case_full_payload_replay_validator.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_RUN089_GRID_AWARE_ADAPTER_FRESH_CASE_FULL_PAYLOAD_REPLAY_VALIDATOR.md
```

## Result

```text
validation checks:                  6
passed checks:                      6
failed checks:                      0
replay validation ready:            true
case count:                         3
replay-ready cases:                 3
replay-blocked cases:               0
max frequency-bin delta:            0.0
max time-band delta:                0.0
field claim ready:                  false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

The saved run `341` replay audit is internally consistent: all three full-
payload fresh cases recover their best variants and reproduce saved outputs
with zero recorded replay delta.

## Decision

Use run `342` as the saved-artifact validator for the full-payload replay
checkpoint before sensitivity hardening.
