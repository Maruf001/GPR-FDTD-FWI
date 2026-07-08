# Experiment 1774: 84-Grid External Return Contract Ledger Validator

Date: 2026-07-01

## Purpose

Validate the saved run `1773` external-return contract ledger from its output
artifacts.

This run does not materialize observed-by-case data, execute FDTD, launch GPU
work, transfer to field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1774_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator_check_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source external ledger ready:     true
validation checks:                7
passed validation checks:         7
failed validation checks:         0
expected external items:          21
external items present:           0
approval tokens required:         1
artifact files required:          20
artifact jobs required:           10
payloads required:                5
materialization ready:            false
new FDTD executed:                false
GPU work ready:                   false
field transfer ready:             false
field FWI ready:                  false
3D/HPC ready:                     false
```

Validation checks:

| Check | Result |
| --- | --- |
| Source external ledger ready | pass |
| Twenty-one external items represented | pass |
| Current external state remains absent | pass |
| Stage shape preserved | pass |
| Materialization remains blocked | pass |
| Downstream states remain blocked | pass |
| Figure and script snapshots present | pass |

## Interpretation

The saved 84-grid external-return ledger is internally consistent. It sees one
approval item and twenty pilot-result artifacts, confirms that none is present,
preserves the six-stage shape, and keeps materialization plus downstream work
blocked.

## Decision

Use run `1773` as the 2D external-return ledger and run `1774` as its
saved-artifact validator. Sensitivity hardening remains the next useful step
before relying on the ledger for damaged future return states.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator.py
3 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
