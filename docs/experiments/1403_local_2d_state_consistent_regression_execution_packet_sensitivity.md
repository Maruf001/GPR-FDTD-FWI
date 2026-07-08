# Local 2D Experiment 1403: State-Consistent Regression Execution Packet Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `1402` regression execution packet validator with damaged
packet variants.

Run `1402` showed that the exact run `1401` packet is consumer-ready. This run
checks the negative-control side: damaged packets should fail.

This run does not run new FDTD/FWI inversions, launch GPU/HPC work, compare
against field data, or promote field transfer.

## Output

```text
outputs/experiments/1403_local_2d_state_consistent_regression_execution_packet_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_regression_execution_packet_sensitivity_scenarios.csv
data/local_2d_state_consistent_regression_execution_packet_sensitivity_summary.json
figures/local_2d_state_consistent_regression_execution_packet_sensitivity.png
docs/LOCAL_2D_STATE_CONSISTENT_REGRESSION_EXECUTION_PACKET_SENSITIVITY.md
scripts/run_local_2d_state_consistent_regression_execution_packet_sensitivity.py
scripts/test_local_2d_state_consistent_regression_execution_packet_sensitivity.py
```

## Result

```text
scenarios:                         10
expected pass scenarios:           1
observed pass scenarios:           1
expected failure scenarios:        9
observed failure scenarios:        9
unexpected outcomes:               0
sensitivity ready:                 true
full pack authoritative:           true
sentinel replaces full pack:       false
GPU work ready:                    false
field transfer ready:              false
field FWI ready:                   false
3D/HPC ready:                      false
```

| Scenario | Expected pass | Observed pass | Failed checks |
| --- | --- | --- | --- |
| exact_execution_packet | true | true | none |
| missing_route | false | false | route_count_matches_summary; full_pack_route_count_matches_summary |
| boundary_route_uses_sentinel | false | false | fast_smoke_route_count_matches_summary; full_pack_route_count_matches_summary |
| sentinel_marked_boundary_authoritative | false | false | reduced_sentinel_table_is_fast_smoke_only |
| full_pack_not_authoritative | false | false | full_core_pack_table_is_authoritative |
| wrong_sentinel_row_count | false | false | reduced_sentinel_table_is_fast_smoke_only |
| packet_not_ready | false | false | execution_packet_marked_ready |
| sentinel_replaces_full_pack | false | false | sentinel_does_not_replace_full_pack |
| gpu_marked_ready | false | false | gpu_field_3d_remain_blocked |
| field_transfer_marked_ready | false | false | gpu_field_3d_remain_blocked |

## Interpretation

The execution packet validator accepts the exact packet and rejects all damaged
variants: missing route, boundary route using the sentinel, sentinel marked
boundary-authoritative, full pack not authoritative, wrong sentinel row count,
packet not ready, sentinel replacing the full pack, GPU marked ready, and field
transfer marked ready.

This gives the 2D regression execution-packet package both positive and
negative-control coverage.

## Decision

Use runs `1401`-`1403` as the current local 2D regression execution-packet guard
package.

Keep the full core pack authoritative and keep GPU, field transfer, field FWI,
and 3D/HPC blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_regression_execution_packet_validator.py
tests/test_local_2d_state_consistent_regression_execution_packet_sensitivity.py
8 passed
```

Python compile check:

```text
run_local_2d_state_consistent_regression_execution_packet_sensitivity.py: pass
tests/test_local_2d_state_consistent_regression_execution_packet_sensitivity.py: pass
```

Figure check:

```text
2717x843, dynamic range=255
```
