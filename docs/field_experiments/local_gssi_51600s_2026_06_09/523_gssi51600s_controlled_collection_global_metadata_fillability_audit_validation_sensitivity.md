# Field Experiment 523: Global Metadata Fillability Audit Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `522` validator by confirming that it accepts the exact run
`521` fillability audit and rejects damaged or prematurely promoted states.

This is an output-local validation-sensitivity wrapper around saved artifacts.
It does not create live field receipt files, parse DZT files, promote
controlled field evidence, run field FWI, launch GPU/HPC work, or run field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/523_gssi51600s_controlled_collection_global_metadata_fillability_audit_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_global_metadata_fillability_audit_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_global_metadata_fillability_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                         16
expected pass cases:                       1
expected fail cases:                       15
actual pass cases:                         1
actual fail cases:                         15
unexpected cases:                          0
damaged cases:                             15
validation sensitivity ready:              true
field FWI ready:                           false
field 3D/HPC ready:                        false
```

The damaged cases cover source readiness, metadata/stage row shape,
fill-stage counts, value-ready promotion, live-file promotion, template receipt
promotion, parser/downstream promotion, field-FWI/3D promotion, figure damage,
and missing script snapshots.

## Interpretation

The validator accepts only the exact run `521` fillability audit and rejects
all damaged states tested here. This keeps the run `521` claim boundary narrow:
it is a collection-preparation aid, not measured field evidence.

## Decision

Keep run `521` as an output-local collection-preparation artifact, not live
field evidence.

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
2645x854, dynamic range=255
```

