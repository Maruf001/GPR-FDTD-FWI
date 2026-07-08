# Experiment 1446: Objective-Revision Execution Materialization

Date: 2026-06-28

## Purpose

Materialize the guarded local 2D objective-revision execution manifest from
runs `1443-1445` against the saved prospective sweep evidence from run `1436`.

This run does not run new FDTD simulations. It turns the guarded execution
routes into explicit saved route outcomes:

```text
drop-veryhigh primary selection
majority-vote cross-check
veryhigh diagnostic trace
blocked broad-radius, physical, GPU, field, FWI, and 3D/HPC routes
```

## Output

```text
outputs/experiments/1446_local_2d_state_consistent_objective_revision_execution_materialization
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_execution_materialized_routes.csv
data/local_2d_state_consistent_objective_revision_execution_materialized_cases.csv
data/local_2d_state_consistent_objective_revision_execution_veryhigh_diagnostics.csv
data/local_2d_state_consistent_objective_revision_execution_materialization_summary.json
figures/local_2d_state_consistent_objective_revision_execution_materialization.png
docs/LOCAL_2D_STATE_CONSISTENT_OBJECTIVE_REVISION_EXECUTION_MATERIALIZATION.md
scripts/run_local_2d_state_consistent_objective_revision_execution_materialization.py
scripts/test_local_2d_state_consistent_objective_revision_execution_materialization.py
scripts/script_snapshot_manifest.json
```

## Result

```text
manifest routes:                       6
materialized routes:                   3
materialized case rows:                15
drop-veryhigh cases:                   5
drop-veryhigh truth recovered:         5
drop-veryhigh failures:                0
majority-vote cases:                   5
majority-vote truth recovered:         5
majority-vote failures:                0
veryhigh diagnostic cases:             5
veryhigh diagnostic truth recovered:   2
veryhigh diagnostic failures:          3
materialization ready:                 true
promote revised objective now:         false
broad radius promoted:                 false
physical claim ready:                  false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

## Interpretation

The materialized route table gives explicit saved outcomes for the guarded
objective-revision manifest. The drop-`veryhigh` primary route recovers the
truth in all five saved prospective cases, and the majority-vote cross-check
also recovers the truth in all five cases.

The `veryhigh` objective remains diagnostic only. It recovers the truth in two
of five cases and fails in three cases. This supports using the revised local
objective policy for the current saved local setup, not promoting a broad
radius-tolerance, physical-transfer, field-transfer, field-FWI, GPU, or 3D/HPC
claim.

## Decision

Use run `1446` as the materialized local 2D objective-revision execution
result. Validate and stress-test this materialization before treating it as a
guarded downstream artifact.

## Validation

Focused test:

```text
tests/test_local_2d_state_consistent_objective_revision_execution_materialization.py
3 passed
```

Figure validation:

```text
3077x889, dynamic range=255
```
