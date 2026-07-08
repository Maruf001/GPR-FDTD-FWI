# Experiment 1775: 84-Grid External Return Contract Ledger Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `1774` validator for the 84-grid external-return contract
ledger.

This run does not materialize observed-by-case data, execute FDTD, launch GPU
work, transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1775_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity_scenario_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:             true
sensitivity scenarios:              9
expected pass scenarios:            1
expected fail scenarios:            8
observed pass scenarios:            1
observed fail scenarios:            8
unexpected outcomes:                0
damaged scenarios:                  8
damaged scenarios rejected:         8
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source not ready | fail | fail | source external ledger ready |
| file count drift | fail | fail | twenty-one external items are represented |
| file status damage | fail | fail | current external state remains absent |
| stage shape damage | fail | fail | stage shape is preserved |
| false materialization | fail | fail | materialization remains blocked |
| downstream promotion | fail | fail | downstream states remain blocked |
| figure damage | fail | fail | figure and script snapshots are present |
| snapshot damage | fail | fail | figure and script snapshots are present |

## Interpretation

The validator accepts only the exact saved 84-grid external-return ledger
state. It rejects damaged source readiness, external-item counts, file status,
stage shape, false materialization, downstream promotion, damaged figure
validation, and missing script snapshots.

## Decision

Use runs `1773-1775` as the guarded 2D external-return ledger block. The
current 2D path remains blocked on the approval item and pilot-result files,
but the ledger side is now ready to reject damaged future return states.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validation_sensitivity.py: pass
```

Figure check:

```text
2212x847, dynamic range=255
```
