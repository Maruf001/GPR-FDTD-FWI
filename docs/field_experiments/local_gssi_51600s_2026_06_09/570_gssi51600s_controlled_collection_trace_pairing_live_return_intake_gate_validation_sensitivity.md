# Field Experiment 570: Trace-Pairing Intake Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `569` trace-pairing intake validator.

The sensitivity set checks that the exact saved intake state passes and that
damaged states fail when the source flag, row count, linked-file count, global
metadata count, live-file state, ready-row state, field-table acceptance,
field FWI state, figure, or script snapshot is changed.

This is CPU-only intake validation. It does not parse DZT files, promote
provenance, accept controlled field evidence, run field FWI, run field 3D/HPC,
or launch neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/570_gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity_scenario_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity.png
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
| source_not_ready | fail | fail | source intake gate ready |
| row_count_damage | fail | fail | three trace-pairing rows are represented |
| linked_count_damage | fail | fail | linked file and global metadata counts are preserved |
| global_count_damage | fail | fail | linked file and global metadata counts are preserved |
| live_file_promotion | fail | fail | current live state remains absent |
| ready_row_promotion | fail | fail | no trace-pairing rows are ready |
| field_table_acceptance_promotion | fail | fail | field analysis states remain blocked |
| field_fwi_promotion | fail | fail | field analysis states remain blocked |
| figure_damage | fail | fail | figure and script snapshots are present |
| snapshot_damage | fail | fail | figure and script snapshots are present |

## Interpretation

The trace-pairing intake validator rejects the main failure modes that would
make incomplete field trace rows appear acceptable.

## Decision

Use runs `568-570` as the guarded field trace-pairing intake block. Keep
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC blocked until linked field files and shared global metadata pass
intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validation_sensitivity.py: pass
```

Figure check:

```text
2428x847, dynamic range=255
```
