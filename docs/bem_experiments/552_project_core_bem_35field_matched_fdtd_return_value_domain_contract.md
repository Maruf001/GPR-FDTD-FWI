# BEM Experiment 552: Matched-FDTD Return Value-Domain Contract

Date: 2026-06-30

## Purpose

Define value-domain checks for future matched-FDTD return rows after the
row-identity contract has passed.

Runs `549-551` lock the row identities. This run adds the value rules: the
source-hash return file must contain lowercase SHA-256 strings, and the
scattered-norm return file must contain positive finite floating point values.

This run does not create real FDTD return values and does not promote BEM/FDTD
comparison evidence, 3D validation, GPU/HPC work, field transfer, or field FWI.

## Output

```text
outputs/bem_experiments/552_project_core_bem_35field_matched_fdtd_return_value_domain_contract
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_value_domain_rows.csv
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_value_domain_contract_summary.json
figures/project_core_bem_35field_matched_fdtd_return_value_domain_contract.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source row-identity ready:                 true
source row-identity validation ready:      true
source row-identity sensitivity ready:     true
source acceptance gate ready:              true
required value contracts:                  558
source-hash value contracts:               279
positive-float value contracts:            279
real values present:                       0
accepted value domains:                    0
file sequence contracts:                   2
value actions:                             3
value-domain contract ready:               true
GPU priority:                              none
```

## Decision

Future matched-FDTD return values must pass both row identity and value-domain
checks before BEM/FDTD comparison evidence can be written.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_value_domain_contract.py
4 passed
```

Figure check:

```text
2465x846, dynamic range=255
```
