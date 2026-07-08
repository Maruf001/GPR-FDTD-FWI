# Field Experiment 619: External Return Hygiene Audit

Date: 2026-07-01

## Purpose

Audit the external field-return tree after the directory scaffold and action
rollup.

This run only inspects the pending external return folders. It does not create
measured DZT files, metadata files, field evidence, field FWI, field 3D/HPC
artifacts, or GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/619_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_directory_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit.png
scripts/
```

## Result

```text
external return root exists:             true
leaf directories:                        5
leaf directories present:                5
leaf directories clean:                  5
leaf directories writable:               5
expected directories:                    8
actual directories:                      8
unexpected directories:                  0
total slots:                             33
collection-coupled slots:                18
actual files:                            0
actual symlinks:                         0
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

## Interpretation

The external return tree is clean and empty. The expected dataset-local pending
root and five leaf drop directories are present. There are no unexpected
directories, files, or symlinks.

This is a no-data hygiene result. It confirms the drop area is clean before
real measured returns arrive, but it does not supply measured radar evidence.

## Decision

Use this as a field-return hygiene guard only. Keep controlled field evidence,
field FWI, and field 3D/HPC blocked until measured DZT files and paired
metadata arrive and pass live preflight.

## Validation

Figure check:

```text
2933x864, dynamic range=255
```

Script snapshots:

```text
2
```
