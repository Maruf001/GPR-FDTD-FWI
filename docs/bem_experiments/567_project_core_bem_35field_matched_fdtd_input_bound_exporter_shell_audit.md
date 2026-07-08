# BEM Experiment 567: Matched-FDTD Input-Bound Exporter Shell Audit

Date: 2026-06-30

## Purpose

Audit the new input-bound matched-FDTD return exporter shell.

Run `566` showed that the BEM-side return files are accepted, but the
matched-FDTD export side still lacks real input rows and accepted output CSV
files. This run records the next implementation step: a guarded exporter that
can validate and write matched-FDTD return CSV files only when real FDTD input
rows are supplied.

This run does not supply real FDTD rows, write accepted FDTD return evidence,
run a BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation readiness.

## Output

```text
outputs/bem_experiments/567_project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit_binding_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source binding-gap ready:              true
input-bound exporter available:        true
FDTD file keys checked:                2
required return rows:                  558
contract checks passed:                2
missing-input refusals:                2
real input CSVs supplied:              0
accepted return files written:         0
evidence-ready files:                  0
bindings audited:                      5
ready bindings:                        3
blocking bindings:                     2
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
| input-bound exporter script | 1 | 1 | true |
| FDTD source-hash manifest contract check | 1 | 1 | true |
| FDTD scattered-norm values contract check | 1 | 1 | true |
| real FDTD input CSV files | 0 | 2 | false |
| accepted matched-FDTD output CSV files | 0 | 2 | false |

## Interpretation

The matched-FDTD exporter has moved from an always-refusing historical shell to
an input-bound shell. It can check both required FDTD file keys and refuses real
mode when no input and output CSV paths are supplied. Focused unit tests verify
that valid temporary rows can be written and malformed rows are rejected, but no
real FDTD rows have been supplied to the experiment stream.

## Decision

Use run `567` as the current exporter implementation checkpoint. The next
comparison-enabling work is to define and produce the two real matched-FDTD
input CSVs for this exporter, then rerun row-identity, value-domain, and
comparison acceptance after accepted output files exist.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_input_bound_return_exporter.py
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_shell_audit.py
9 passed
```

Figure check:

```text
2429x847, dynamic range=255
```
