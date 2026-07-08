# Field Experiment 566: Trace-Pairing Table Schema Validator

Date: 2026-07-01

## Purpose

Validate run `565` from saved outputs.

This run checks that the controlled field trace-pairing table schema is
internally consistent: three profile rows, eighteen columns, nine linked
measured DZT files, nine per-file metadata records, fifteen shared global
metadata records, zero ready rows, and blocked parser/field evidence states.

This is CPU-only schema validation. It does not parse DZT files, promote
provenance, accept controlled field evidence, run field FWI, run field 3D/HPC,
or launch neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/566_gssi51600s_controlled_collection_trace_pairing_table_schema_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_table_schema_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_table_schema_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_table_schema_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source trace-pairing schema ready:    true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
trace-pairing rows:                   3
schema columns:                       18
linked measured DZT files:            9
linked per-file metadata records:     9
shared global metadata records:       15
trace-pairing rows ready:             0
field table filled:                   false
parser ready:                         false
field FWI ready:                      false
gpu priority:                         none
```

Saved-output validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source trace-pairing schema ready | pass |
| 2 | table shape is preserved | pass |
| 3 | required links are preserved | pass |
| 4 | live files remain absent | pass |
| 5 | field receipt boundary is preserved | pass |
| 6 | parser and field evidence remain blocked | pass |
| 7 | figure and script snapshots are present | pass |

## Interpretation

The trace-pairing table schema is reproducible from saved artifacts and
preserves the intended field analysis shape.

The table remains unfilled because the measured DZT files and per-file
metadata are absent.

## Decision

Use runs `565-566` as the controlled field trace-pairing schema block. Keep
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC blocked until the live files arrive and pairing rows can be
filled.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema_validator.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_table_schema_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
