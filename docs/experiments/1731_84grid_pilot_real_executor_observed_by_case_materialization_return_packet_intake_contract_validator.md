# Experiment 1731: 84-Grid Pilot Observed-By-Case Return Packet Intake Contract Validator

Date: 2026-06-30

## Purpose

Validate run `1730`, the non-executed 21-item return-packet intake contract for
future observed-by-case materialization.

This validator confirms that the contract preserves the one approval token, ten
cache arrays, and ten result JSON files; that only the approval token and result
JSON items have output-local templates; and that materialization, FDTD, GPU,
field, and 3D/HPC states remain blocked.

## Output

```text
outputs/experiments/1731_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator.png
scripts/
```

## Result

```text
validation checks:                    5
failed checks:                        0
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

All five validation checks pass:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source return-packet contract ready | pass |
| 2 | contract rows preserve 21-item shape | pass |
| 3 | templates link only approval and result items | pass |
| 4 | materialization and downstream remain blocked | pass |
| 5 | figure and scripts exist | pass |

## Interpretation

Run `1731` guards the run `1730` contract. The next real promotion still
requires the actual external approval token, ten cache arrays, and ten result
JSON files to exist and be accepted. Until then, observed-by-case
materialization and FDTD execution remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator.py

6 passed
```

Figure check:

```text
2285x832, dynamic range=255
```
