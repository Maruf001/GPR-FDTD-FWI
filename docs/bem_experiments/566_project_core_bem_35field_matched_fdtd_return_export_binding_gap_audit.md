# BEM Experiment 566: Matched-FDTD Return Export-Binding Gap Audit

Date: 2026-06-30

## Purpose

Audit the current binding gap between the accepted BEM-side return files and
the missing matched-FDTD return export path.

Runs `557`-`565` established that the BEM-side return files are accepted and
that the matched-FDTD side has validated blank templates only. This run combines
that state with the earlier real-export implementation gap to answer one
practical question:

```text
Which exact bindings still block the real BEM/FDTD return comparison?
```

This run does not create FDTD return files, execute matched-FDTD commands, run a
BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or promote
3D validation readiness.

## Output

```text
outputs/bem_experiments/566_project_core_bem_35field_matched_fdtd_return_export_binding_gap_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_export_binding_gap_audit_binding_rows.csv
data/project_core_bem_35field_matched_fdtd_return_export_binding_gap_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_export_binding_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source chain ready:                    true
bindings audited:                      6
ready bindings:                        1
blocking bindings:                     5
FDTD exporter refusals:                2
writer refusals:                       4
accepted BEM return files:             2
accepted matched-FDTD return files:    0
accepted matched-FDTD return rows:     0
matched-FDTD commands executed:        0
BEM/FDTD comparison ready:             false
3D validation ready:                   false
GPU/HPC ready:                         false
field transfer ready:                  false
field FWI ready:                       false
audit ready:                           true
```

Binding status:

| Binding | Current | Required | Ready |
| --- | ---: | ---: | --- |
| BEM-side accepted return files | 2 | 2 | true |
| matched-FDTD exporter real mode | 0 | 2 | false |
| matched-FDTD accepted-file writer real mode | 0 | 4 | false |
| matched-FDTD return CSV files | 0 | 2 | false |
| matched-FDTD return values | 0 | 558 | false |
| matched-FDTD command checks | 0 | 2 | false |

## Interpretation

The comparison is not blocked by the BEM-side return packet anymore. It is
blocked by the real matched-FDTD export path: exporter real mode is still
refused, writer real mode is still refused, and no accepted matched-FDTD return
CSV files or return rows exist.

## Decision

Use run `566` as the current BEM/FDTD comparison blocker map. The next
comparison-enabling task is not another template, proxy value, or comparison
audit. It is implementing a controlled real matched-FDTD return exporter and
writer that can produce the two accepted return CSV files required by runs
`555`-`556`.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_export_binding_gap_audit.py
3 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
