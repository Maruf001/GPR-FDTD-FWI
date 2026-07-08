# Local 2D Experiment 1398: State-Consistent Regression Tier Router Contract

Date: 2026-06-28

## Purpose

Turn the reduced sentinel adoption, provenance lock, and sensitivity results
into an operational routing contract.

Runs `1395`-`1397` established that the 11-row reduced sentinel is valid as an
optional fast-smoke layer, locked to the 88-row full core pack, stable to row
ordering, and sensitive to real row drift. This run states when that reduced
sentinel is enough and when the full core pack is required.

This run does not rerun FDTD/FWI, launch GPU work, use field data, run field
FWI, or run 3D/HPC validation.

## Output

```text
outputs/experiments/1398_local_2d_state_consistent_regression_tier_router_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_tier_router_rows.csv
data/local_2d_state_consistent_regression_tier_router_contract_summary.json
figures/local_2d_state_consistent_regression_tier_router_contract.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_TIER_ROUTER_CONTRACT.md
scripts/run_local_2d_state_consistent_regression_tier_router_contract.py
scripts/test_local_2d_state_consistent_regression_tier_router_contract.py
```

## Result

```text
routes:                              6
fast-smoke routes:                   2
full-pack-required routes:           4
reduced sentinel rows:               11
full core pack rows:                 88
reduced/full row fraction:           0.125
required token count:                32
lock sensitivity scenarios:          6
unexpected lock outcomes:            0
router contract ready:               true
full pack authoritative:             true
sentinel replaces full pack:         false
broad radius tolerance promoted:     false
GPU ready:                           false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

| Change type | Recommended tier | Minimum rows | Requires full pack |
| --- | --- | ---: | --- |
| consumer_wiring_schema_parsing_plotting | reduced_sentinel_fast_smoke | 11 | false |
| harmless_row_order_change | reduced_sentinel_lock_check | 11 | false |
| row_key_or_digest_drift | full_core_pack_required | 88 | true |
| boundary_objective_margin_or_token_change | full_core_pack_required | 88 | true |
| physical_claim_or_broad_radius_tolerance | full_core_pack_plus_new_design | 88 | true |
| gpu_field_transfer_field_fwi_or_3d_hpc | blocked_by_current_2d_evidence | 88 | true |

## Interpretation

The reduced 11-row sentinel is now operationally routed. It is useful for fast
CPU smoke checks on consumer wiring, schema, parsing, plotting, and harmless
row-order changes.

The full 88-row pack remains authoritative for any boundary, objective, margin,
token-definition, physical-claim, GPU, field-transfer, field-FWI, or 3D/HPC
decision.

## Decision

Use this router contract for local 2D regression selection.

Do not use the reduced sentinel to replace the full core pack or promote GPU,
field, field FWI, or 3D/HPC work.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_reduced_sentinel_provenance_lock.py
tests/test_local_2d_state_consistent_reduced_sentinel_provenance_lock_sensitivity.py
tests/test_local_2d_state_consistent_regression_tier_router_contract.py
11 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_tier_router_contract.py: pass
tests/test_local_2d_state_consistent_regression_tier_router_contract.py: pass
```

Figure check:

```text
3040x838, dynamic range=255
```
