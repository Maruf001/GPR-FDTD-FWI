# BEM Experiment 545: Matched FDTD Return Real-File Acceptance Gate Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `544` validator.

The exact run `543` artifacts should pass. Damaged source readiness, file
counts, file presence, nonempty file promotion, file acceptance, entry counts,
entry acceptance, row evidence promotion, column counts, column acceptance,
action readiness, action counts, downstream promotion, figure damage, and
script-snapshot damage should fail.

## Output

```text
outputs/bem_experiments/545_project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_validation_sensitivity_summary.json
figures/project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                     16
expected pass scenarios:                   1
expected failure scenarios:                15
unexpected scenarios:                      0
acceptance-gate sensitivity ready:         true
exact source artifacts pass:               true
file damage rejected:                      true
entry or column damage rejected:           true
action damage rejected:                    true
downstream promotion rejected:             true
figure damage rejected:                    true
script-snapshot damage rejected:           true
real return packet accepted:               false
real BEM/FDTD comparison ready:            false
GPU priority:                              none
```

The rejected scenarios are:

```text
source_chain_not_ready
file_count_drift
file_present_promotion
file_nonempty_promotion
file_acceptance_promotion
entry_count_drift
entry_acceptance_promotion
entry_evidence_promotion
column_count_drift
column_acceptance_promotion
action_ready_promotion
action_count_drift
downstream_promotion
figure_damage
script_snapshot_damage
```

## Decision

Use runs `543-545` as the real matched-FDTD return-file acceptance gate before
any BEM/FDTD comparison evidence. The branch remains blocked on real FDTD
return-value export.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_real_file_acceptance_gate_validation_sensitivity.py
4 passed
```

Figure check:

```text
3077x840, dynamic range=255
```
