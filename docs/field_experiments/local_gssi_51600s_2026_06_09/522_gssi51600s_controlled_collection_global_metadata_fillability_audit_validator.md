# Field Experiment 522: Global Metadata Fillability Audit Validator

Date: 2026-06-30

## Purpose

Validate run `521`, the global metadata fillability audit for the controlled
collection return packet.

This is an output-local validation wrapper around saved run `521` artifacts. It
does not create live field receipt files, parse DZT files, promote controlled
field evidence, run field FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/522_gssi51600s_controlled_collection_global_metadata_fillability_audit_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_validator_check_rows.csv
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_validator_summary.json
figures/gssi51600s_controlled_collection_global_metadata_fillability_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
global metadata rows:                      15
fill stages:                               3
prepare from existing records:             7
verify before measurement:                 4
log during or after collection:            4
must verify on collection day:             8
current value-ready files:                 0
current live files present:                0
current live receipt-ready files:          0
validation ready:                          true
field FWI ready:                           false
field 3D/HPC ready:                        false
```

The checks cover source readiness, metadata/stage shape, fill-stage accounting,
placeholder/live state, downstream boundary preservation, figure output, and
frozen script snapshots.

## Interpretation

Run `521` validates as an output-local collection-preparation artifact. It does
not make any metadata file live or receipt-ready.

## Decision

Use run `521` for global metadata preparation while keeping live receipt and
field FWI blocked.

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
2357x838, dynamic range=255
```

