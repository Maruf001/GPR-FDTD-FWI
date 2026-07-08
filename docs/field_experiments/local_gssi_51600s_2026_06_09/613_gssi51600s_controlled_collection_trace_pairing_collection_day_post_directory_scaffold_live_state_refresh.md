# Field Experiment 613: Post-Directory-Scaffold Live-State Refresh

Date: 2026-07-01

## Purpose

Refresh the controlled field-return live state after the external directory
scaffold from run `610`.

This run checks that the five external return parent directories exist while
the measured DZT files and paired metadata files remain absent.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/613_gssi51600s_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh
```

## Result

```text
source scaffold ready:                 true
source scaffold validation ready:      true
source scaffold sensitivity ready:     true
directory parents expected:               5
directory parents present:                5
live-state rows:                          6
total return slots:                      33
preparable metadata slots:               15
measured DZT files required:              9
paired metadata files required:           9
collection-coupled live files required:  18
live measured DZT files:                  0
live paired metadata files:               0
live collection-coupled files:            0
missing collection-coupled files:        18
accepted live-state groups:               0
controlled field evidence ready:      false
field FWI ready:                      false
field 3D/HPC ready:                   false
gpu priority:                        none
```

## Interpretation

The directory scaffold changed the logistics state, not the evidence state. The
external return folders are present, but all required collection-coupled files
are still missing.

## Decision

Keep controlled field evidence, field FWI, and field 3D/HPC blocked until
measured DZT files and paired metadata pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh.py
8 passed with validator/sensitivity block
```

Figure check:

```text
2969x900, dynamic range=255
```
