# Field Experiment 581: Collection-Day Return Preflight Gate Validator

Date: 2026-07-01

## Purpose

Validate the saved controlled-collection return preflight gate from run `580`.

This validator checks that the preflight gate preserves the current pre-return
state: thirty-three controlled return items are represented, real field files
are still absent, no item passes preflight, no item is ready to stage, no command
is executed, and field analysis remains blocked.

This is a CPU-only validation run. It does not create measured DZT files, does
not fill metadata JSON files, does not stage files into the live return area,
does not execute copy commands, and does not promote parser, provenance, field
FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/581_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source preflight gate ready:      true
validation checks:                7
passed validation checks:         7
failed validation checks:         0
preflight items:                  33
metadata JSON items:              24
measured DZT items:               9
candidate files present:          0
preflight-passed items:           0
ready-to-stage items:             0
executed commands:                0
field table intake accepted:      false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

The seven checks cover:

```text
1. source preflight gate readiness
2. thirty-three items and six stages
3. twenty-four metadata JSON items and nine measured DZT items
4. absent and unreadable producer field files
5. zero preflight-passed, stageable, or executed items
6. blocked field-analysis states
7. nonblank figure and script snapshots
```

## Interpretation

The saved preflight gate is internally consistent. It represents the complete
controlled-collection return list but does not treat any placeholder, blank
metadata file, missing DZT file, or unexecuted command as field evidence.

## Decision

Use run `581` as the validator for the run `580` preflight gate. Parser
execution, provenance promotion, controlled field evidence, field FWI, and
field 3D/HPC remain blocked until real field files pass this gate and the
guarded intake checks.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validation_sensitivity.py

9 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
