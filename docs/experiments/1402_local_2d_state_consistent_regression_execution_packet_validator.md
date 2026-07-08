# Local 2D Experiment 1402: State-Consistent Regression Execution Packet Validator

Date: 2026-06-28

## Purpose

Validate the run `1401` regression execution packet from a consumer
perspective.

Run `1401` joined the regression router to the concrete 11-row reduced sentinel
and 88-row full core-pack tables. This run checks that a downstream consumer can
read that packet and preserve the route counts, table inventory,
sentinel/full-pack roles, and blocked downstream states.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1402_local_2d_state_consistent_regression_execution_packet_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_execution_packet_validation_checks.csv
data/local_2d_state_consistent_regression_execution_packet_validator_summary.json
figures/local_2d_state_consistent_regression_execution_packet_validator.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_EXECUTION_PACKET_VALIDATOR.md
scripts/run_local_2d_state_consistent_regression_execution_packet_validator.py
scripts/test_local_2d_state_consistent_regression_execution_packet_validator.py
```

## Result

```text
validation checks:                  9
validation passes:                  9
blocking failures:                  0
source routes:                      6
source fast-smoke routes:           2
source full-pack routes:            4
packet validation ready:            true
full pack authoritative:            true
sentinel replaces full pack:        false
GPU work ready:                     false
field transfer ready:               false
field FWI ready:                    false
3D/HPC ready:                       false
```

| Check | Expected | Observed | Passes |
| --- | --- | --- | --- |
| route_count_matches_summary | 6 | 6 | true |
| table_inventory_count_matches_summary | 2 | 2 | true |
| fast_smoke_route_count_matches_summary | 2 | 2 | true |
| full_pack_route_count_matches_summary | 4 | 4 | true |
| reduced_sentinel_table_is_fast_smoke_only | 11 rows, fast smoke yes, boundary no | 11 rows, fast smoke true, boundary false | true |
| full_core_pack_table_is_authoritative | 88 rows, boundary yes | 88 rows, boundary true | true |
| execution_packet_marked_ready | true | true | true |
| sentinel_does_not_replace_full_pack | false | false | true |
| gpu_field_3d_remain_blocked | false | false | true |

## Interpretation

The regression execution packet is internally consistent and consumer-ready:
route counts, table inventory, sentinel/full-pack roles, and blocked
GPU/field/3D states are preserved.

## Decision

Use run `1401` as the local 2D regression execution packet and run `1402` as
its consumer validator.

Keep the full core pack authoritative and do not promote GPU, field transfer,
field FWI, or 3D/HPC work.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_execution_packet.py
tests/test_local_2d_state_consistent_regression_execution_packet_validator.py
8 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_execution_packet_validator.py: pass
tests/test_local_2d_state_consistent_regression_execution_packet_validator.py: pass
```

Figure check:

```text
2645x841, dynamic range=255
```
