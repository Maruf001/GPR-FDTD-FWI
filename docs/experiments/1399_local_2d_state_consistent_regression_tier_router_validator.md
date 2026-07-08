# Local 2D Experiment 1399: State-Consistent Regression Tier Router Validator

Date: 2026-06-28

## Purpose

Validate the run `1398` regression tier router from a consumer perspective.

Run `1398` states when the 11-row reduced sentinel is sufficient and when the
full 88-row core pack is required. This run checks that those routing rules are
present and internally consistent.

This run does not rerun FDTD/FWI, launch GPU work, use field data, run field
FWI, or run 3D/HPC validation.

## Output

```text
outputs/experiments/1399_local_2d_state_consistent_regression_tier_router_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_tier_router_validation_checks.csv
data/local_2d_state_consistent_regression_tier_router_validator_summary.json
figures/local_2d_state_consistent_regression_tier_router_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_TIER_ROUTER_VALIDATOR.md
scripts/run_local_2d_state_consistent_regression_tier_router_validator.py
scripts/test_local_2d_state_consistent_regression_tier_router_validator.py
```

## Result

```text
validation checks:                  8
validation passes:                  8
blocking failures:                  0
source routes:                      6
source fast-smoke routes:           2
source full-pack-required routes:   4
router validation ready:            true
full pack authoritative:            true
sentinel replaces full pack:        false
GPU ready:                          false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Check | Expected | Observed | Passes |
| --- | --- | --- | --- |
| route_count_matches_summary | 6 | 6 | true |
| fast_smoke_route_count_matches_summary | 2 | 2 | true |
| full_pack_route_count_matches_summary | 4 | 4 | true |
| consumer_route_allows_reduced_sentinel | true | true | true |
| boundary_route_requires_full_pack | true | true | true |
| gpu_field_route_remains_blocked | true | true | true |
| sentinel_does_not_replace_full_pack | false | false | true |
| full_pack_remains_authoritative | true | true | true |

## Interpretation

The router contract is consumer-valid. Fast smoke is allowed only for consumer
wiring and harmless row-order checks. Boundary-sensitive and GPU/field/3D
changes remain full-pack-required or blocked.

## Decision

Use run `1398` as the local 2D regression tier router and run `1399` as its
consumer validator.

Do not let the reduced sentinel replace the full core pack.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_tier_router_contract.py
tests/test_local_2d_state_consistent_regression_tier_router_validator.py
6 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_tier_router_validator.py: pass
tests/test_local_2d_state_consistent_regression_tier_router_validator.py: pass
```

Figure check:

```text
2645x805, dynamic range=255
```
