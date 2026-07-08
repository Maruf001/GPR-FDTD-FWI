# Experiment 1773: 84-Grid External Return Contract Ledger

Date: 2026-07-01

## Purpose

Close the staged 84-grid external-return contract into one complete ledger.

This run joins the approval-token contract, the first nominal payload contract,
the first time-shift payload contract, the middle-payload contract, the
late-payload contract, and the final materialization gate. It does not
materialize observed-by-case data, execute FDTD, launch GPU work, transfer to
field data, run field FWI, or run 3D/HPC.

## Output

```text
outputs/experiments/1773_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_stage_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_expected_file_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stage count:                         6
expected live files:                 21
expected live files present:         0
expected live parent dirs present:   1
approval tokens required:            1
artifact files required:             20
cache arrays required:               10
result JSON files required:          10
artifact jobs required:              10
payloads required:                   5
stage expected file counts:          1;2;2;8;8;0
stage artifact job counts:           0;1;1;4;4;0
cumulative external item counts:     1;3;5;13;21;21
final cumulative artifact jobs:      10
contract sequence closed:            true
materialization ready:               false
new FDTD executed:                   false
GPU work ready:                      false
field transfer ready:                false
field FWI ready:                     false
3D/HPC ready:                        false
```

The six-stage sequence is:

| Stage | Role | Expected live files | Artifact jobs |
| ---: | --- | ---: | ---: |
| 1 | Approval token | 1 | 0 |
| 2 | First nominal job | 2 | 1 |
| 3 | First time-shift job | 2 | 1 |
| 4 | Middle payload jobs | 8 | 4 |
| 5 | Late payload jobs | 8 | 4 |
| 6 | Final materialization gate | 0 | 0 |

## Interpretation

The 84-grid external-return checklist is now complete. It requires one real
approval token plus twenty live artifact files: ten cache arrays and ten result
JSON files across ten artifact jobs and five payloads.

Only the approval-token parent directory exists. The real approval token and
all twenty artifact files are absent, so observed-by-case materialization and
FDTD execution remain blocked.

## Decision

Use this ledger as the complete external-return checklist. Keep materialization,
FDTD execution, GPU work, field transfer, field FWI, and 3D/HPC blocked until
all twenty-one external items are present.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger.py
4 passed
```

Python compile check:

```text
run_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger.py: pass
tests/test_local_2d_state_consistent_objective_revision_84grid_external_return_contract_ledger.py: pass
```

Figure check:

```text
2140x846, dynamic range=255
```
