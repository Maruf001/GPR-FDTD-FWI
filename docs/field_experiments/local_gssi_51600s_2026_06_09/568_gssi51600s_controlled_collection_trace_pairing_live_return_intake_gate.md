# Field Experiment 568: Trace-Pairing Live-Return Intake Gate

Date: 2026-07-01

## Purpose

Define the live-return intake gate for the controlled field trace-pairing
table.

Runs `565-567` define and guard the table shape. This run checks whether each
profile repeat has its six linked row-level files and the shared global
metadata needed before a trace-pairing row can enter analysis.

This is CPU-only intake validation. It does not parse DZT files, promote
provenance, accept controlled field evidence, run field FWI, run field 3D/HPC,
or launch neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/568_gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_row_status.csv
data/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_live_return_intake_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source ledger ready:                    true
source trace-pairing schema ready:      true
trace-pairing rows:                     3
linked required files:                  18
linked live files present:              0
linked live files missing:              18
shared global metadata required:        15
shared global metadata present:         0
trace-pairing rows ready:               0
field table intake accepted:            false
parser ready:                           false
provenance ready:                       false
archive ready:                          false
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
```

Row status:

| Repeat | Linked files required | Linked files present | Shared global metadata present | Row ready |
| ---: | ---: | ---: | ---: | --- |
| 1 | 6 | 0 | 0 | false |
| 2 | 6 | 0 | 0 | false |
| 3 | 6 | 0 | 0 | false |

## Interpretation

The field trace-pairing intake gate is now explicit. A profile repeat cannot
enter analysis until its controlled profile file, profile metadata, time-zero
reference file, time-zero metadata, amplitude reference file, amplitude
metadata, and shared global metadata are present and accepted.

The current state remains pre-return: no trace-pairing row is ready.

## Decision

Use run `568` as the live-return intake gate for future field trace-pairing
rows. Keep parser/provenance/archive promotion, controlled field evidence,
field FWI, and field 3D/HPC blocked until trace-pairing rows pass this gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate.py
4 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_live_return_intake_gate.py: pass
```

Figure check:

```text
1564x846, dynamic range=255
```
