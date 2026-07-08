# Field Experiment 528: Metadata Completion Route Validator

Date: 2026-06-30

## Purpose

Validate run `527`, the controlled-collection metadata completion route.

This is an output-local validation wrapper around saved run `527` artifacts. It
does not create live field receipt files, parse DZT files, promote controlled
field evidence, run field FWI, launch GPU/HPC work, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/528_gssi51600s_controlled_collection_metadata_completion_route_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_metadata_completion_route_validator_check_rows.csv
data/gssi51600s_controlled_collection_metadata_completion_route_validator_summary.json
figures/gssi51600s_controlled_collection_metadata_completion_route_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
route rows:                                5
metadata files:                            24
metadata values/fields:                    51
paired measured-DZT dependencies:          9
current metadata values ready:             0
current metadata live files present:       0
field FWI ready:                           false
field 3D/HPC ready:                        false
validation ready:                          true
```

The checks cover source readiness, route shape, metadata count accounting,
empty current metadata state, downstream boundary preservation, figure output,
and frozen script snapshots.

## Interpretation

Run `527` validates as an output-local preparation artifact.

## Decision

Use run `527` as the controlled-collection metadata completion order.

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
2357x838, dynamic range=255
```

