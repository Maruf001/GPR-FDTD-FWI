# Experiment 1730: 84-Grid Pilot Observed-By-Case Return Packet Intake Contract

Date: 2026-06-30

## Purpose

Join the latest approval-token, cache-array, and result-JSON requirements into
one non-executed return-packet intake contract for future observed-by-case
materialization.

This run does not execute FDTD. It does not materialize observed arrays. It only
defines the external files that must be returned before materialization can be
accepted.

## Output

```text
outputs/experiments/1730_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_contract_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_role_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract.png
scripts/
```

## Result

```text
contract items:                       21
item roles:                           3
external approval tokens:             1
planned cache arrays:                 10
planned result JSON files:            10
linked templates:                     11
approval templates linked:            1
result JSON templates linked:         10
cache arrays without templates:       10
output-local templates:               11
templates accepted as external items: 0
present external items:               0
accepted external items:              0
materialization input-ready items:    0
ready for materialization:            false
observed-by-case materialized:        false
result written:                       false
commands executed:                    false
new FDTD executed:                    false
GPU work ready:                       false
field transfer ready:                 false
field FWI ready:                      false
3D/HPC ready:                         false
```

Role-level contract:

| Item role | Required items | Linked templates | Present items | Accepted items | Materialization input ready |
| --- | ---: | ---: | ---: | ---: | ---: |
| external approval token | 1 | 1 | 0 | 0 | 0 |
| planned cache array | 10 | 0 | 0 | 0 | 0 |
| planned result JSON | 10 | 10 | 0 | 0 | 0 |

## Interpretation

The future observed-by-case materialization return packet is now one 21-item
contract:

```text
1 external approval token
10 cache NPZ arrays
10 result JSON files
```

The approval token and result JSON files have output-local templates. The cache
arrays do not have templates because they must be produced by the real
materialization step. No external item is present or accepted, so
materialization, FDTD execution, GPU work, field transfer, field FWI, and
3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract.py

3 passed
```

Figure check:

```text
2393x847, dynamic range=255
```
