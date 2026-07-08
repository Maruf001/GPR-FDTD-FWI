# Field Experiment 223: Controlled Archive Operator Manifest Sensitivity

Date: 2026-06-28

## Purpose

Stress-test the run `222` operator manifest validator.

This run checks whether the validator accepts the exact run `221` manifest and
rejects controlled damage to file slots, role counts, archive directories,
planned checks, DZT guard values, operator-readiness flags, command-execution
state, real archive acceptance, and downstream field states.

It does not ingest real field files, execute command templates, accept a real
archive, run field FWI, launch GPU/HPC work, or run field 3D validation.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/223_gssi51600s_controlled_archive_operator_manifest_sensitivity
```

Key artifacts:

```text
data/field_controlled_archive_operator_manifest_sensitivity_scenarios.csv
data/field_controlled_archive_operator_manifest_sensitivity_summary.json
figures/field_controlled_archive_operator_manifest_sensitivity.png
docs/FIELD_CONTROLLED_ARCHIVE_OPERATOR_MANIFEST_SENSITIVITY.md
```

## Result

```text
scenarios:                         25
expected pass scenarios:           1
expected failure scenarios:        24
observed pass scenarios:           1
observed failure scenarios:        24
unexpected outcomes:               0
sensitivity ready:                 true
operator collection ready:         true
real archive acceptance ready:     false
checksum intake ready:             false
controlled evidence ready:         false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

The exact manifest passes. All damaged variants fail as expected:

| Damage family | Example failure modes |
| --- | --- |
| file manifest shape | file-slot count drift, missing file slot, role-count drift |
| archive placement | directory-count drift, directory assignment drift, directory not ready |
| intake checks | check-count drift, missing check row, unexpected check group, checks-per-file drift |
| DZT guard values | minimum-size drift, header drift, checksum requirement removed, ledger requirement removed |
| readiness flags | manifest not ready, operator collection not ready |
| execution boundary | real files present, commands executed, check row executed |
| downstream promotion | real archive acceptance, checksum intake, evidence, field FWI, or field 3D/HPC marked ready |

## Interpretation

The operator manifest validator is guarded against the main ways the manifest
could silently drift. It accepts the exact manifest and rejects changes that
would alter file requirements, archive placement, check requirements, or
downstream readiness.

## Decision

Use runs `221-223` as the guarded field operator-manifest package. The package
is ready for field collection and archive staging, but real archive acceptance,
checksum intake, controlled evidence, field FWI, GPU work, and field 3D/HPC
remain blocked until real measured files pass the manifest checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_archive_operator_manifest_sensitivity.py
6 passed
```

Compile check:

```text
run_gssi_field_controlled_archive_operator_manifest_sensitivity.py: pass
tests/test_gssi_field_controlled_archive_operator_manifest_sensitivity.py: pass
```

Figure check:

```text
field_controlled_archive_operator_manifest_sensitivity.png
3257x894, dynamic range=255
```
