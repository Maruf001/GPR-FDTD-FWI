# Experiment 1732: 84-Grid Pilot Observed-By-Case Return Packet Intake Contract Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1731` validator for the run `1730` observed-by-case
return-packet intake contract.

This run checks that the validator accepts only the exact 21-item contract and
rejects damaged states that change contract shape, damage template linkage,
promote external items, or prematurely enable materialization, FDTD, GPU, field,
or 3D/HPC states.

## Output

```text
outputs/experiments/1732_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validation_sensitivity_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validation_sensitivity_summary.json
data/figure_validation.csv
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validation_sensitivity.png
scripts/
```

## Result

```text
source validator ready:                 true
sensitivity cases:                      26
expected pass cases:                    1
expected fail cases:                    25
actual pass cases:                      1
actual fail cases:                      25
unexpected outcomes:                    0
exact source passes:                    true
damaged cases rejected:                 true
external-promotion cases rejected:      true
execution-promotion cases rejected:     true
new FDTD executed:                      false
GPU work ready:                         false
field transfer ready:                   false
field FWI ready:                        false
3D/HPC ready:                           false
```

The rejected damage cases cover:

| Group | Examples |
| --- | --- |
| Source and shape | source readiness, row removal, role removal, approval/cache/result count damage |
| Template boundary | template link damage, approval/result template damage, cache incorrectly templated, template accepted as external item |
| External item promotion | item present, item accepted, materialization input ready |
| Execution promotion | materialization ready, observed materialized, result written, commands executed, FDTD executed |
| Downstream promotion | GPU work, field transfer, field FWI, 3D/HPC |
| Artifact integrity | figure damage and missing script snapshots |

## Interpretation

Runs `1730`-`1732` now form a guarded 2D observed-by-case return-packet block.
The next real promotion still requires all external items to exist and be
accepted:

```text
1 external approval token
10 cache NPZ arrays
10 result JSON files
```

Until that happens, observed-by-case materialization, FDTD execution, GPU work,
field transfer, field FWI, and 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validator.py
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_observed_by_case_materialization_return_packet_intake_contract_validation_sensitivity.py

9 passed
```

Figure check:

```text
2860x922, dynamic range=255
```
