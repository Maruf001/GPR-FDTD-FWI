# Experiment 1640: 84-Grid Pilot Real-Execution Implementation Gap Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `1639` validator.

The exact run `1638` artifacts should pass. Damaged source readiness, executor
probe counts, executor refusal counts, execution enablement, FDTD execution,
output counts, premature real-output presence, schema acceptance, template
substitution, blocker damage, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/experiments/1640_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     16
expected pass scenarios:                   1
expected failure scenarios:                15
unexpected scenarios:                      0
implementation-gap sensitivity ready:      true
exact source artifacts pass:               true
executor damage rejected:                  true
output damage rejected:                    true
blocker damage rejected:                   true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
new FDTD executed:                         false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
executor_probe_count_drift
executor_refusal_count_drift
executor_enablement_promotion
fdtd_execution_promotion
output_count_drift
output_present_promotion
output_nonempty_promotion
output_acceptance_promotion
template_allowed_promotion
blocker_ready_promotion
blocker_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Runs `1638-1640` close the current 2D audit chain. The result is a clear no-go
for full 84-row execution from the current executor. The useful next step is to
build a bounded real five-row pilot executor and validator that writes the run
`1635` result schema.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_execution_implementation_gap_audit_validation_sensitivity.py
4 passed
```

Figure check:

```text
3077x841, dynamic range=255
```
