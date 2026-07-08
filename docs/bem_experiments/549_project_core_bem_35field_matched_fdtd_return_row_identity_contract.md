# BEM Experiment 549: Matched-FDTD Return Row-Identity Contract

Date: 2026-06-30

## Purpose

Lock the row identities for the two future matched-FDTD return CSV files before
any returned values can be accepted.

Runs `543-548` defined the required files and created the empty staging
directory. This run adds a stricter contract: every future returned row must
match the expected file key, pair hash, worksheet row, receiver index,
frequency, and required value field.

This is a contract and validation run. It does not create real FDTD return
values and does not promote BEM/FDTD comparison evidence, 3D validation,
GPU/HPC work, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/549_project_core_bem_35field_matched_fdtd_return_row_identity_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_file_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_row_identity_rows.csv
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_row_identity_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_return_row_identity_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source gate ready:                         true
source scaffold ready:                     true
source scaffold validation ready:          true
source scaffold sensitivity ready:         true
required files:                            2
file sequence contracts:                   2
required row identities:                   558
unique row identities:                     558
required columns:                          22
staged files present:                      0
accepted file identities:                  0
accepted row identities:                   0
contract actions:                          4
ready contract actions:                    0
row-identity contract ready:               true
GPU priority:                              none
```

## Decision

The future matched-FDTD return files now have a locked row-identity contract.
Returned files must match these row identities before numeric values or
BEM/FDTD comparison evidence can be accepted.

The branch remains blocked on real FDTD return CSV files.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_row_identity_contract.py
4 passed
```

Figure check:

```text
2465x844, dynamic range=255
```
