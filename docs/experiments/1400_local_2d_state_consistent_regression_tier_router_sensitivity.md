# Local 2D Experiment 1400: State-Consistent Regression Tier Router Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1399` router validator with damaged router scenarios.

Run `1398` defined the routing contract and run `1399` validated it from a
consumer perspective. This run checks that important routing drift is rejected:
missing fast-smoke route, boundary changes incorrectly using the sentinel, GPU
being marked ready, the sentinel replacing the full pack, and route-count drift.

This run does not rerun FDTD/FWI, launch GPU work, use field data, run field
FWI, or run 3D/HPC validation.

## Output

```text
outputs/experiments/1400_local_2d_state_consistent_regression_tier_router_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_tier_router_sensitivity_rows.csv
data/local_2d_state_consistent_regression_tier_router_sensitivity_summary.json
figures/local_2d_state_consistent_regression_tier_router_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_TIER_ROUTER_SENSITIVITY.md
scripts/run_local_2d_state_consistent_regression_tier_router_sensitivity.py
scripts/test_local_2d_state_consistent_regression_tier_router_sensitivity.py
```

## Result

```text
scenarios:                          6
expected passes:                    1
observed passes:                    1
expected failures:                  5
observed failures:                  5
unexpected outcomes:                0
router sensitivity ready:           true
full pack authoritative:            true
sentinel replaces full pack:        false
GPU ready:                          false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Scenario | Expected pass | Observed pass | Unexpected |
| --- | --- | --- | --- |
| exact_router | true | true | false |
| missing_consumer_fast_smoke_route | false | false | false |
| boundary_route_uses_sentinel | false | false | false |
| gpu_marked_ready | false | false | false |
| sentinel_replaces_full_pack | false | false | false |
| route_count_mismatch | false | false | false |

## Interpretation

The router guard is sensitive to the important failure modes. It accepts the
exact router and rejects damaged routers that would weaken the reduced-sentinel
boundary.

## Decision

Use runs `1398`-`1400` as the local 2D regression routing guard.

The reduced sentinel remains optional fast smoke only; the full 88-row pack
remains authoritative.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_tier_router_contract.py
tests/test_local_2d_state_consistent_regression_tier_router_validator.py
tests/test_local_2d_state_consistent_regression_tier_router_sensitivity.py
9 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_tier_router_sensitivity.py: pass
tests/test_local_2d_state_consistent_regression_tier_router_sensitivity.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```
