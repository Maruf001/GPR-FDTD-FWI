# Experiment 1448: Objective-Revision Execution Materialization Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1447` validator for the run `1446` local 2D
objective-revision execution materialization.

This run checks whether the validator accepts the exact saved run `1446`
artifact set and rejects controlled damage to route rows, case rows,
`veryhigh` diagnostic rows, summary gates, downstream readiness flags, figure
validation, and script snapshots.

It does not run new FDTD simulations, launch GPU work, transfer to field data,
run field FWI, or launch 3D/HPC work.

## Output

```text
outputs/experiments/1448_local_2d_state_consistent_objective_revision_execution_materialization_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_materialization_sensitivity_scenarios.csv
data/local_2d_state_consistent_objective_revision_execution_materialization_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_execution_materialization_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MATERIALIZATION_SENSITIVITY.md
scripts/run_local_2d_state_consistent_objective_revision_execution_materialization_sensitivity.py
scripts/test_local_2d_state_consistent_objective_revision_execution_materialization_sensitivity.py
scripts/script_snapshot_manifest.json
```

## Result

```text
scenarios:                          48
expected pass scenarios:            1
observed pass scenarios:            1
expected failure scenarios:         47
observed failure scenarios:         47
unexpected outcomes:                0
sensitivity ready:                  true
exact run 1446 accepted:            true
damaged variants rejected:          true
promote revised objective now:      false
broad radius promoted:              false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

## Interpretation

The materialization validator accepts the exact run `1446` artifact set and
rejects every damaged variant. The rejected variants cover primary-route
drift, majority-vote drift, `veryhigh` diagnostic drift, blocked-route
promotion, case-table drift, summary drift, downstream promotion, figure
validation drift, and script-snapshot drift.

This closes the local 2D objective-revision materialization block as a guarded
saved artifact: drop-`veryhigh` is supported as the local primary policy for
the saved prospective cases, majority vote is supported as the cross-check, and
`veryhigh` remains diagnostic only.

## Decision

Use runs `1446-1448` as the guarded local 2D objective-revision execution
materialization. The local policy result is ready as a saved artifact, while
broad-radius, physical-transfer, GPU, field-FWI, and 3D/HPC claims remain
blocked.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_materialization_sensitivity.py
3 passed
```

Figure validation:

```text
4301x917, dynamic range=255
```
