# Field Experiment 529: Metadata Completion Route Validation Sensitivity

Date: 2026-06-30

## Purpose

Stress-test the run `528` validator by confirming that it accepts the exact run
`527` metadata completion route and rejects damaged or prematurely promoted
states.

This is an output-local validation-sensitivity wrapper around saved artifacts.
It does not create live field receipt files, parse DZT files, promote
controlled field evidence, run field FWI, launch GPU/HPC work, or run field
3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/529_gssi51600s_controlled_collection_metadata_completion_route_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_completion_route_validation_sensitivity_case_rows.csv
data/gssi51600s_controlled_collection_metadata_completion_route_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_metadata_completion_route_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity cases:                         15
expected pass cases:                       1
expected fail cases:                       14
actual pass cases:                         1
actual fail cases:                         14
unexpected cases:                          0
damaged cases:                             14
field FWI ready:                           false
field 3D/HPC ready:                        false
validation sensitivity ready:              true
```

The damaged cases cover source readiness, route shape, metadata file count,
metadata value count, DZT dependency count, false metadata value readiness,
false live-file readiness, receipt/parser promotion, field-FWI/3D promotion,
figure damage, and missing script snapshots.

## Interpretation

The validator accepts only the exact run `527` metadata completion route and
rejects all damaged states tested here. The route remains output-local
preparation, not live field evidence.

## Decision

Keep run `527` as output-local preparation, not live field evidence.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_metadata_completion_route.py
tests/test_gssi_field_controlled_collection_metadata_completion_route_validator.py
tests/test_gssi_field_controlled_collection_metadata_completion_route_validation_sensitivity.py
9 passed
```

Figure check:

```text
2573x855, dynamic range=255
```

