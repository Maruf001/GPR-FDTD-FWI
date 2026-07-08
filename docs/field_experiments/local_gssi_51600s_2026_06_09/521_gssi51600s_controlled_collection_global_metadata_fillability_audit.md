# Field Experiment 521: Global Metadata Fillability Audit

Date: 2026-06-30

## Purpose

Turn the 15 global metadata placeholders from the controlled collection return
packet into a practical fillability table.

This run answers a field-preparation question:

```text
Which global metadata entries can be prepared from existing records, and which
entries must be verified or logged on collection day?
```

This is an output-local preparation audit. It does not create live field
receipt files, parse DZT files, promote controlled field evidence, run field
FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/521_gssi51600s_controlled_collection_global_metadata_fillability_audit
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_metadata_rows.csv
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_stage_rows.csv
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_summary.json
figures/gssi51600s_controlled_collection_global_metadata_fillability_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
global metadata rows:                      15
fill stages:                               3
prepare from existing records:             7
verify before measurement:                 4
log during or after collection:            4
must verify on collection day:             8
current value-ready files:                 0
current live files present:                0
current live receipt-ready files:          0
templates accepted as live receipt:        0
required receipt checks:                   75
template value placeholders:               30
fillability audit ready:                   true
field FWI ready:                           false
field 3D/HPC ready:                        false
```

Fillability stages:

| Stage | Metadata files | Required receipt checks | Current value-ready | Current live files |
| --- | ---: | ---: | ---: | ---: |
| before collection from existing records | 7 | 35 | 0 | 0 |
| setup before measurement | 4 | 20 | 0 | 0 |
| during or after collection log | 4 | 20 | 0 | 0 |

The seven record-based entries are:

```text
antenna_model_serial_and_nominal_frequency
antenna_serial
material
software_version
survey_method
system
truth_source
```

The eight collection-day entries are setup geometry, coupling/lift condition,
antenna positioning/polarization, gain setting, date, notes, operator, and
weather.

## Interpretation

The field packet now has a clearer split. Seven global metadata JSON files can
be prepared from instrument inventory, survey-plan, material, and target-truth
records before collection. Eight global metadata JSON files still require
setup verification or collection-day logging.

No metadata value is currently accepted as ready, and no live receipt file is
present. This is a preparation artifact only.

## Decision

Use this audit to prepare the record-based global metadata before collection.
Keep live receipt, parser/provenance/archive readiness, field FWI, and field
3D/HPC blocked until real field files are returned and validated.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_global_metadata_fillability_audit.py
tests/test_gssi_field_controlled_collection_global_metadata_fillability_audit_validator.py
tests/test_gssi_field_controlled_collection_global_metadata_fillability_audit_validation_sensitivity.py
9 passed
```

Figure check:

```text
2572x841, dynamic range=255
```

