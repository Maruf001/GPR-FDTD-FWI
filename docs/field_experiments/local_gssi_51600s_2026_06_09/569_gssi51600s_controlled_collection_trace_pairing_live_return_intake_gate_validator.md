# Field Experiment 569: Trace-Pairing Intake Gate Validator

Date: 2026-07-01

## Purpose

Validate run `568` from saved outputs.

This run checks that the trace-pairing live-return intake gate is internally
consistent: three rows are represented, eighteen linked row-level files and
fifteen shared global metadata records are required, no linked files are
present, no rows are ready, and field analysis states remain blocked.

This is CPU-only intake validation. It does not parse DZT files, promote
provenance, accept controlled field evidence, run field FWI, run field 3D/HPC,
or launch neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/569_gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validator
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validator_check_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validator_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source trace-pairing intake ready:    true
validation checks:                    7
passed validation checks:             7
failed validation checks:             0
trace-pairing rows:                   3
linked required files:                18
linked live files present:            0
shared global metadata required:      15
shared global metadata present:       0
trace-pairing rows ready:             0
field table intake accepted:          false
parser ready:                         false
field FWI ready:                      false
gpu priority:                         none
```

Saved-output validation checks:

| Order | Check | Result |
| ---: | --- | --- |
| 1 | source intake gate ready | pass |
| 2 | three trace-pairing rows are represented | pass |
| 3 | linked file and global metadata counts are preserved | pass |
| 4 | current live state remains absent | pass |
| 5 | no trace-pairing rows are ready | pass |
| 6 | field analysis states remain blocked | pass |
| 7 | figure and script snapshots are present | pass |

## Interpretation

The trace-pairing intake gate is reproducible from saved artifacts and remains
in the correct pre-return state.

No field analysis row is ready until the linked row-level files and shared
global metadata arrive.

## Decision

Use runs `568-569` as the guarded live-return intake block for controlled
field trace-pairing rows. Keep parser/provenance/archive promotion, controlled
field evidence, field FWI, and field 3D/HPC blocked until linked field files
and shared global metadata pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validator.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validator.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate_validator.py: pass
```

Figure check:

```text
1492x846, dynamic range=255
```
