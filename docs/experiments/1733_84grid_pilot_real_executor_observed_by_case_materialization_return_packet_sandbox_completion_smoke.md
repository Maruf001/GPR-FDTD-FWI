# Experiment 1733: 84-Grid Observed-by-Case Materialization Return-Packet Sandbox Completion Smoke

Date: 2026-06-30

## Purpose

Test the positive intake path for the run `1730` 21-item materialization
return-packet contract without touching the locked external-return paths and
without running FDTD.

Run `1730` defined the real return packet: one external approval token, ten
cache arrays, and ten result JSON files. This run fills that same packet shape
inside an output-local sandbox and verifies file, parse, and load mechanics.

## Output

```text
outputs/experiments/1733_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_sandbox_item_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_sandbox_role_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke.png
scripts/
```

## Result

```text
source contract ready:                 true
source contract items:                 21
sandbox items written:                 21
sandbox approval tokens:               1
sandbox cache arrays:                  10
sandbox result JSON files:             10
sandbox nonempty items:                21
sandbox suffix-valid items:            21
sandbox parse/load-valid items:        21
sandbox accepted items:                21
sandbox complete roles:                3
templates linked:                      11
templates accepted as external items:  0
external items present:                0
synthetic-only items:                  21
observed data materialized:            0
new FDTD executions:                   0
ready for materialization:             false
GPU work ready:                        false
field transfer ready:                  false
field FWI ready:                       false
3D/HPC ready:                          false
```

Role completion:

| Item role | Required items | Sandbox accepted | External present |
| --- | ---: | ---: | ---: |
| external approval token | 1 | 1 | 0 |
| planned cache array | 10 | 10 | 0 |
| planned result JSON | 10 | 10 | 0 |

## Interpretation

The 21-item materialization return-packet contract has a working positive
file/parse/load path in an output-local sandbox. This does not authorize or
perform materialization. The synthetic cache arrays and JSON files are not
external approval, not observed data, and not FDTD results.

## Decision

Use run `1733` as the positive-path intake smoke for the run `1730` return
packet. Keep real materialization, FDTD execution, GPU work, field transfer,
field FWI, and 3D/HPC blocked until real external items are present and
accepted through the locked contract.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_sandbox_completion_smoke.py

3 passed
```

Figure check:

```text
2501x858, dynamic range=255
```
