# BEM Experiment 339: Fresh-Case Replay Boundary Validation Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `338` fresh-case replay boundary validator with controlled
damaged variants.

Run `338` validated that run `337` correctly separates the older run `094`
fresh-case numerical pass from the stricter independent formula-replay
standard. This run verifies that the validator is sensitive to the mistakes
that would change that boundary.

This is a CPU-only validator sensitivity run. It does not run FDTD, launch GPU
or HPC work, use field data, use the synthetic 2D archive, run field FWI, or
make a field-transfer claim.

## Output

```text
outputs/bem_experiments/339_project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validation_sensitivity_scenarios.csv
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validation_sensitivity_summary.json
figures/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validation_sensitivity.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FRESH_CASE_REPLAY_BOUNDARY_VALIDATION_SENSITIVITY.md
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

The validator accepts the exact run `337` boundary and rejects controlled damage
to case counts, fresh-case pass counts, the worst error metric, replay item
counts, missing-input identity, comparator-output state, downstream promotion,
figure validation, and script snapshots.

## Decision

Use runs `337-339` as the guarded fresh-case replay-boundary block. The next
BEM improvement should create a new fresh-case stress branch that saves full
formula replay payloads per case.
