# Field Experiment 264: Controlled Collection Real-Return Empty Intake Layout Validator

Date: 2026-06-28

## Purpose

Validate the saved run `263` empty intake layout from artifacts.

This run checks that required directories and template files exist, no DZT
placeholders are present, metadata and checksum templates are empty, downstream
acceptance states remain blocked, figure validation passes, and script
snapshots are present.

It does not create DZT files, fabricate metadata, accept an archive, promote
controlled field evidence, run field FWI, launch field 3D/HPC, or use GPU work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/264_gssi51600s_controlled_collection_real_return_empty_intake_layout_validator
```

Key artifacts:

```text
data/field_controlled_collection_real_return_empty_intake_layout_validator_checks.csv
data/field_controlled_collection_real_return_empty_intake_layout_validator_summary.json
data/figure_validation.csv
figures/field_controlled_collection_real_return_empty_intake_layout_validator.png
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_EMPTY_INTAKE_LAYOUT_VALIDATOR.md
scripts/run_gssi_field_controlled_collection_real_return_empty_intake_layout_validator.py
scripts/test_gssi_field_controlled_collection_real_return_empty_intake_layout_validator.py
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                              9
passed checks:                       9
failed checks:                       0
validation ready:                 true
source layout ready:              true
required file slots:                 9
global metadata template rows:      11
file metadata template rows:        21
checksum template rows:              9
placeholder DZT files:               0
real files present:              false
provenance acceptance ready:     false
field FWI ready:                 false
field 3D/HPC ready:              false
gpu priority:                    none
```

## Interpretation

The saved empty intake layout is internally consistent: required directories
and template files exist, no DZT placeholders are present, metadata and
checksum templates are empty, and all archive/evidence/downstream gates remain
closed.

## Decision

Use runs `263-264` as the validated empty real-return intake layout.
Sensitivity testing remains required before treating the layout validator as
guarded. Real files, measured metadata, and checksums remain required.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_collection_real_return_empty_intake_layout_validator.py
3 passed
```

Figure validation:

```text
3077x880, dynamic range=255
```
