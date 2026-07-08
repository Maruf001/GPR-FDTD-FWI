# Field Experiment 625: Controlled Collection First-Return Pair Acceptance Gate

Date: 2026-07-01

## Purpose

Turn the nine-pair first-return watchlist from run `622` into an explicit
acceptance gate for measured DZT files and paired metadata files.

This run reads saved field artifacts and the current live filesystem state. It
does not create measured files, run field preprocessing, run field FWI, launch
3D/HPC work, or use GPU kernels.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/625_gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_acceptance_rows.csv
data/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate_summary.json
figures/gssi51600s_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source watchlist ready:                 true
source validation ready:                true
source sensitivity ready:               true
acceptance pairs:                       9
accepted pairs:                         0
blocked pairs:                          9
DZT files present:                      0
metadata files present:                 0
missing DZT files:                      9
missing metadata files:                 9
parent directories present:             true
required acceptance checks:             108
passed acceptance checks:               0
controlled-profile pairs:               3
time-zero pairs:                        3
amplitude-reference pairs:              3
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                           none
```

## Interpretation

The field acceptance gate is structurally ready, but no measured pair can pass
yet. Each of the nine required DZT/metadata pairs has 12 acceptance checks,
giving 108 checks total. All nine pairs are blocked because the live measured
DZT files and paired metadata JSON files are absent.

## Decision

Use this as the current first-return acceptance gate. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until all nine measured pairs
exist and pass acceptance.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_first_return_pair_acceptance_gate.py
3 passed
```

Figure check:

```text
2861x876, dynamic range=255
```
