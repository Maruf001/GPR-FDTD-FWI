# BEM Experiment 338: Fresh-Case Replay Boundary Validator

Date: 2026-06-28

## Purpose

Validate the saved run `337` fresh-case replay boundary from artifacts.

Run `337` showed that the three run `094` fresh cases passed their numerical
adapter comparison but cannot be independently replayed from formula inputs
because the saved arrays omit Tx background fields, Rx background fields, and
the source spectrum. This run verifies that boundary using only the saved run
`337` rows, summary, figure validation, and script snapshots.

This is a CPU-only validator. It does not run FDTD, launch GPU or HPC work,
use field data, use the synthetic 2D archive, run field FWI, or make a field
transfer claim.

## Output

```text
outputs/bem_experiments/338_project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validator
```

Key artifacts:

```text
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validator_checks.csv
data/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validator_summary.json
figures/project_core_bem_project_grid_adapter_fresh_case_replay_boundary_validator.png
scripts/script_snapshot_manifest.json
docs/PROJECT_CORE_BEM_PROJECT_GRID_ADAPTER_FRESH_CASE_REPLAY_BOUNDARY_VALIDATOR.md
```

## Result

```text
validation checks:                  7
passed checks:                      7
failed checks:                      0
boundary validation ready:          true
fresh cases:                        3
fresh case passes:                  3
single-payload replay ready:        true
required replay items per case:     12
minimum saved replay items:         9
maximum missing replay items:       3
formula-replay ready cases:         0
formula-replay blocked cases:       3
field claim ready:                  false
3D validation ready:                false
GPU work ready:                     false
field FWI ready:                    false
```

## Interpretation

The saved run `337` replay boundary is internally consistent. The older fresh
cases passed their numerical comparisons, but their saved arrays are not enough
for the stricter executable replay standard established by run `334`.

## Decision

Use run `338` as the saved-artifact validator for the fresh-case replay
boundary. Future fresh-case stress work should save the full replay payload per
case before claiming independent replayability across fresh cases.
