# Field Experiment 580: Collection-Day Return Preflight Gate

Date: 2026-07-01

## Purpose

Define the preflight gate for controlled-collection field return files before
any measured DZT or filled metadata JSON file is staged into the live return
area.

This run does not create measured DZT files, does not fill metadata JSON files,
does not stage files into the live return area, does not execute copy commands,
does not accept field evidence, and does not promote parser, provenance, field
FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/580_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_preflight_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source staging plan ready:        true
source validation ready:          true
source sensitivity ready:         true
preflight items:                  33
stages:                           6
metadata JSON items:              24
measured DZT items:               9
candidate files present:          0
metadata JSON valid:              0
metadata nonblank values:         0
DZT nonzero-size files:           0
DZT readable-header files:        0
preflight-passed items:           0
ready-to-stage items:             0
executed commands:                0
trace pairing ready:              false
field table intake accepted:      false
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

Required file checks:

```text
metadata JSON: not template path, JSON exists, JSON valid, nonblank measured values
measured DZT: DZT exists, nonzero size, readable header
```

## Interpretation

The controlled-collection preflight gate is now explicit. It checks the
twenty-four filled metadata JSON files and nine measured DZT files before any
field return is stageable.

The current state remains pre-return. No producer field file is present, no
metadata JSON is valid, no DZT file is readable, no item passes preflight, and
no command is executed.

## Decision

Use run `580` as the preflight gate before staging controlled-collection field
returns. Keep parser execution, provenance promotion, controlled field evidence,
field FWI, and field 3D/HPC blocked until real files pass preflight and guarded
intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate.py
3 passed
```

Python compile check:

```text
run_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate.py: pass
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_gate.py: pass
```

Figure check:

```text
2212x846, dynamic range=255
```
