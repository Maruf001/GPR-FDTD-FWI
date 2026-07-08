# BEM Experiment 049: Field-Table Replacement Gap Audit

Date: 2026-06-25

## Purpose

Compare raw `scarep` analytic Green fields against the project-domain
target-cell field table used by the current adapter.

This is a CPU-only field-table replacement audit. It records project-core
background target-cell fields and compares them to analytic Green fields at the
same cells. It does not use field data, GPU work, FWI, 3D/HPC, neural networks,
or the historical `outputs/experiments` archive.

## Output

```text
outputs/bem_experiments/049_project_core_bem_field_table_replacement_gap_audit
```

Key artifacts:

```text
data/project_core_bem_field_table_replacement_gap_audit.csv
data/project_core_bem_field_table_replacement_gap_audit_summary.json
data/project_core_bem_field_table_replacement_gap_audit_arrays.npz
figures/project_core_bem_field_table_replacement_gap_audit.png
docs/PROJECT_CORE_BEM_FIELD_TABLE_REPLACEMENT_GAP_AUDIT.md
```

## Result

```text
surface samples:                    10
target cells:                       533
global scaled field L2:             1.0419444002374967
per-source scaled field L2:         0.817994101096804
leave-one-source scaled field L2:   1.0723419515425194
BEM field replacement ready:        false
gpu required:                       false
```

## Interpretation

Raw analytic Green fields do not reproduce the project-domain target-cell field
surface under leave-one-source scaling. This explains why direct analytic/BEM
fields failed the adapter gates in runs `039` and `040`.

## Decision

Do not replace the project-domain field table with raw analytic Green fields.
The next replacement attempt needs a calibrated finite-domain field map or a BEM
model that includes the project source, boundary, and material conventions.

## Validation

```text
python -m py_compile run_project_core_bem_field_table_replacement_gap_audit.py
python run_project_core_bem_field_table_replacement_gap_audit.py
```

Figure check:

```text
project_core_bem_field_table_replacement_gap_audit.png: 1817x770, dynamic range=255
```
