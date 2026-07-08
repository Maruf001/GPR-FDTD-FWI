# Local 2D Experiment 1401: State-Consistent Regression Execution Packet

Date: 2026-06-28

## Purpose

Turn the regression-tier router into an execution packet with explicit reduced
sentinel and full core-pack table paths.

Runs `1398`-`1400` validated the router policy. This run makes the policy
executable by joining each route to the concrete table that should be used.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1401_local_2d_state_consistent_regression_execution_packet
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_execution_packet_routes.csv
data/local_2d_state_consistent_regression_execution_packet_tables.csv
data/local_2d_state_consistent_regression_execution_packet_summary.json
figures/local_2d_state_consistent_regression_execution_packet.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_EXECUTION_PACKET.md
scripts/run_local_2d_state_consistent_regression_execution_packet.py
scripts/test_local_2d_state_consistent_regression_execution_packet.py
```

## Result

```text
routes:                              6
fast-smoke routes:                   2
full-pack routes:                    4
reduced sentinel rows:               11
full core pack rows:                 88
reduced/full row fraction:           0.125
inventory matches router:            true
execution packet ready:              true
full pack remains authoritative:     true
sentinel replaces full pack:         false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

## Regression Tables

| Table | Rows | Boundary authoritative | Fast smoke allowed |
| --- | ---: | --- | --- |
| reduced_sentinel_fast_smoke | 11 | false | true |
| full_core_regression_pack | 88 | true | false |

## Routes

| Change type | Selected table | Rows | Action |
| --- | --- | ---: | --- |
| consumer_wiring_schema_parsing_plotting | reduced_sentinel_fast_smoke | 11 | run reduced sentinel smoke and keep full pack authoritative |
| harmless_row_order_change | reduced_sentinel_fast_smoke | 11 | run reduced sentinel smoke and keep full pack authoritative |
| row_key_or_digest_drift | full_core_regression_pack | 88 | run full core pack before changing boundary-sensitive behavior |
| boundary_objective_margin_or_token_change | full_core_regression_pack | 88 | run full core pack before changing boundary-sensitive behavior |
| physical_claim_or_broad_radius_tolerance | full_core_regression_pack | 88 | run full core pack before changing boundary-sensitive behavior |
| gpu_field_transfer_field_fwi_or_3d_hpc | full_core_regression_pack | 88 | do not promote; full pack can only support local 2D evidence |

## Interpretation

The router is now executable as a packet. Two fast-smoke routes use the 11-row
reduced sentinel, while four boundary-sensitive or blocked routes use the
88-row full core pack or remain blocked. The sentinel does not replace the full
pack.

## Decision

Use this packet for local 2D regression-table selection.

Keep the full core pack authoritative for boundary, objective, margin, token,
physical claim, GPU, field-transfer, field-FWI, and 3D/HPC decisions.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_execution_packet.py
tests/test_local_2d_state_consistent_regression_tier_router_sensitivity.py
7 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_execution_packet.py: pass
tests/test_local_2d_state_consistent_regression_execution_packet.py: pass
```

Figure check:

```text
3040x874, dynamic range=255
```
