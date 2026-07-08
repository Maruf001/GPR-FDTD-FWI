# Field Experiment 620: External Return Hygiene Audit Validator

Date: 2026-07-01

## Purpose

Validate the saved run `619` external-return hygiene audit.

The validator checks summary readiness, expected leaf directories, clean
directory tree state, absence of live files and symlinks, slot-count
preservation, downstream field-analysis blockers, figure output, and script
snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/620_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validator_validation_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validator_summary.json
data/figure_validation.csv
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_hygiene_audit_validator.png
scripts/
```

## Result

```text
validation checks:                       7
passed checks:                           7
failed checks:                           0
leaf directories:                        5
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
```

## Decision

Run `619` validates as a clean, empty external-return tree. Field analysis
remains blocked until measured returns and paired metadata arrive.

## Validation

Figure check:

```text
2645x861, dynamic range=255
```

Script snapshots:

```text
2
```
