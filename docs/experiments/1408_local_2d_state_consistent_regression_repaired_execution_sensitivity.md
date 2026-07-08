# Local 2D Experiment 1408: State-Consistent Repaired Regression Execution Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1407` repaired execution validator with damaged repaired
packet summaries.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1408_local_2d_state_consistent_regression_repaired_execution_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_repaired_execution_sensitivity_scenarios.csv
data/local_2d_state_consistent_regression_repaired_execution_sensitivity_summary.json
figures/local_2d_state_consistent_regression_repaired_execution_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_REPAIRED_EXECUTION_SENSITIVITY.md
scripts/run_local_2d_state_consistent_regression_repaired_execution_sensitivity.py
scripts/test_local_2d_state_consistent_regression_repaired_execution_sensitivity.py
```

## Result

```text
scenarios:                         13
expected pass scenarios:           1
expected failure scenarios:        12
observed pass scenarios:           1
observed failure scenarios:        12
unexpected outcomes:               0
sensitivity ready:                 true
full pack authoritative:           true
sentinel replaces full pack:       false
physical claim ready:              false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

The exact repaired packet passes. Damaged cases fail for the intended reasons:
wrong materialized row count, wrong excluded-row count, wrong repaired route
count, repair not ready, dry-run failure, row-count mismatch, schema failure,
route-mode drift, dry-run ready flag false, sentinel replacing the full pack,
GPU readiness, and field-transfer readiness.

## Interpretation

The repaired local 2D regression execution-packet guard now has both positive
validation and negative-control coverage. The 88-row materialized full-pack
table is the correct execution table for full-pack routes.

This closes the table-materialization issue found in run `1404`. It does not
change the physics boundary: broad physical claims, GPU work, field transfer,
field FWI, and 3D/HPC remain blocked.

## Decision

Use runs `1405`-`1408` as the guarded repaired local 2D regression execution
packet.

Keep the full pack authoritative, keep the reduced sentinel fast-smoke-only, and
keep physical-claim promotion, GPU work, field transfer, field FWI, and 3D/HPC
blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_repaired_execution_sensitivity.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_repaired_execution_sensitivity.py: pass
tests/test_local_2d_state_consistent_regression_repaired_execution_sensitivity.py: pass
```

Figure check:

```text
2969x861, dynamic range=255
```
