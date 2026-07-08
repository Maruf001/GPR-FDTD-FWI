# Field Experiment 567: Trace-Pairing Table Schema Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `566` trace-pairing table validator.

The sensitivity set checks that the exact saved trace-pairing schema passes
and that damaged states fail when the source flag, column count, row count,
required links, live-file state, ready-row state, filled state, parser state,
figure, or script snapshot is changed.

This is CPU-only schema validation. It does not parse DZT files, promote
provenance, accept controlled field evidence, run field FWI, run field 3D/HPC,
or launch neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/567_gssi51600s_controlled_collection_trace_pairing_table_schema_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_table_schema_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_table_schema_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_table_schema_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source validator ready:              true
scenarios:                           11
expected pass count:                 1
expected fail count:                 10
observed pass count:                 1
observed fail count:                 10
unexpected outcomes:                 0
damaged scenarios rejected:          10
gpu priority:                        none
```

Sensitivity scenarios:

| Scenario | Expected | Observed | First failed check |
| --- | --- | --- | --- |
| exact | pass | pass |  |
| source_not_ready | fail | fail | source trace-pairing schema ready |
| column_count_damage | fail | fail | table shape is preserved |
| pair_row_count_damage | fail | fail | table shape is preserved |
| required_link_damage | fail | fail | required links are preserved |
| live_file_promotion | fail | fail | live files remain absent |
| ready_row_promotion | fail | fail | live files remain absent |
| field_table_filled_promotion | fail | fail | parser and field evidence remain blocked |
| parser_promotion | fail | fail | parser and field evidence remain blocked |
| figure_damage | fail | fail | figure and script snapshots are present |
| snapshot_damage | fail | fail | figure and script snapshots are present |

## Interpretation

The trace-pairing schema validator rejects the main failure modes that would
make an incomplete or damaged field analysis table appear acceptable.

## Decision

Use runs `565-567` as the guarded controlled field trace-pairing schema block.
Keep parser/provenance/archive promotion, controlled field evidence, field FWI,
and field 3D/HPC blocked until the live files arrive and pairing rows can be
filled.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_table_schema_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_table_schema_validation_sensitivity.py: pass
```

Figure check:

```text
2428x847, dynamic range=255
```
