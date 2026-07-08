# BEM Experiment 564: Matched-FDTD Return Interface Boundary Audit

Date: 2026-06-30

## Purpose

Make the current BEM/FDTD comparison boundary explicit after the matched-FDTD
template-pack block.

Runs `557`-`559` accepted and validated the BEM-side return files. Runs
`561`-`563` created, validated, and sensitivity-tested blank matched-FDTD
return templates. This run audits both sides together and records the exact
remaining blocker before any real BEM/FDTD comparison.

This run does not create FDTD return files, execute commands, run a BEM/FDTD
comparison, launch GPU/HPC work, transfer to field evidence, or promote 3D
validation readiness.

## Output

```text
outputs/bem_experiments/564_project_core_bem_35field_matched_fdtd_return_interface_boundary_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_interface_rows.csv
data/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_interface_boundary_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source chain ready:                         true
BEM side ready:                             true
matched-FDTD template side ready:           true
matched-FDTD real side ready:               false
accepted BEM return files:                  2
accepted BEM return rows:                   558
required matched-FDTD return files:         2
accepted matched-FDTD return files:         0
accepted matched-FDTD return rows:          0
blank matched-FDTD template values:         558
matched-FDTD command checks:                2
matched-FDTD commands executed:             0
missing matched-FDTD return files:          2
real BEM/FDTD comparison ready:             false
downstream promotion in sources:            false
3D validation ready:                        false
GPU/HPC ready:                              false
field transfer ready:                       false
field FWI ready:                            false
boundary audit ready:                       true
```

Interface state:

| Side | State | Accepted files | Accepted rows | Remaining blocker |
| --- | --- | ---: | ---: | --- |
| BEM candidate | accepted real BEM return files | 2 | 558 | matched FDTD return files absent |
| matched FDTD | validated blank return templates | 0 | 0 | two real matched-FDTD CSV return files with 558 accepted values |

## Interpretation

The BEM side is no longer the comparison blocker for the current 35-field
packet. The accepted BEM return files are present and validated.

The FDTD side remains the blocker. The project has a checklist, a command plan,
and blank templates for the two required matched-FDTD return CSV files, but no
real FDTD return values have been produced or accepted.

## Decision

Do not run a BEM/FDTD comparison from templates or proxy values. The next
comparison-enabling task is to produce the two real matched-FDTD return CSV
files, fill 558 accepted values, run the two command checks from run `556`, and
rerun the row-identity and value-domain validators.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_interface_boundary_audit.py
5 passed
```

Figure check:

```text
2357x847, dynamic range=255
```
