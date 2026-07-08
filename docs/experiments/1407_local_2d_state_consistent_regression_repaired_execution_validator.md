# Local 2D Experiment 1407: State-Consistent Repaired Regression Execution Validator

Date: 2026-06-28

## Purpose

Validate the run `1405` packet repair and the run `1406` repaired execution dry
run from a consumer perspective.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1407_local_2d_state_consistent_regression_repaired_execution_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_repaired_execution_validation_checks.csv
data/local_2d_state_consistent_regression_repaired_execution_validator_summary.json
figures/local_2d_state_consistent_regression_repaired_execution_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_REPAIRED_EXECUTION_VALIDATOR.md
scripts/run_local_2d_state_consistent_regression_repaired_execution_validator.py
scripts/test_local_2d_state_consistent_regression_repaired_execution_validator.py
```

## Result

```text
validation checks:                  10
validation passes:                  10
blocking failures:                  0
validation ready:                   true
full pack authoritative:            true
sentinel replaces full pack:        false
physical claim ready:               false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

The validator confirms the 88-row materialized core table, the 28-row exclusion
of expanded observations, the two unchanged reduced-sentinel routes, the four
repaired full-pack routes, the clean repaired dry run, and the blocked
downstream states.

## Interpretation

The repaired packet is now validated positively. It is ready for
negative-control sensitivity testing.

This does not change the scientific boundary: the full core pack remains
authoritative, the reduced sentinel remains fast-smoke-only, and the repaired
packet still does not justify physical-claim promotion, GPU work, field
transfer, field FWI, or 3D/HPC.

## Decision

Use runs `1405`-`1407` as the positive side of the repaired local 2D regression
execution-packet guard, pending sensitivity testing.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_repaired_execution_validator.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_repaired_execution_validator.py: pass
tests/test_local_2d_state_consistent_regression_repaired_execution_validator.py: pass
```

Figure check:

```text
2717x840, dynamic range=255
```
