# Field Experiment 607: Collection-Day Post-Boundary Live-State Refresh

Date: 2026-07-01

## Purpose

Refresh the live field-return state after the collection-day claim boundary in
run `604`.

This run rescans the expected field return slots. It does not create measured
DZT files, create paired measured metadata, accept field evidence, run field
FWI, or run field 3D/HPC.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/607_gssi51600s_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh
```

## Result

```text
source boundary ready:                    true
source boundary validation ready:         true
source boundary sensitivity ready:        true
state rows:                                  6
total return slots:                         33
preparable metadata slots:                  15
measured DZT files required:                 9
paired metadata files required:              9
collection-coupled live files required:     18
live measured DZT files:                     0
live paired metadata files:                  0
live collection-coupled files:               0
missing collection-coupled files:           18
accepted live-state groups:                  0
controlled field evidence ready:         false
field FWI ready:                         false
field 3D/HPC ready:                      false
gpu priority:                            none
```

## Interpretation

The live field-return state is unchanged after the claim boundary. The packet
still needs nine measured DZT files and nine paired measured metadata files
before it can become measured field evidence.

## Decision

Keep controlled field evidence, field FWI, and field 3D/HPC blocked until the
measured DZT files and paired metadata pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2933x900, dynamic range=255
```
