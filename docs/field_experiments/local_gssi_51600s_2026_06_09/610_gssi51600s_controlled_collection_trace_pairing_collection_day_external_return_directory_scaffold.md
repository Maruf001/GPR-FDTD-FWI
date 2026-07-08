# Field Experiment 610: External Return Directory Scaffold

Date: 2026-07-01

## Purpose

Create the parent directories for the controlled collection-day external return
paths without creating any measured DZT files or metadata files.

Run `607` showed that all 18 collection-coupled live files are absent. This run
prepares the directory layout only, so real files can be placed consistently
after collection while field evidence remains blocked.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/610_gssi51600s_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold
```

## Result

```text
source refresh ready:                    true
source refresh validation ready:         true
source refresh sensitivity ready:        true
directories checked:                        5
directories present after scaffold:         5
total return slots:                        33
required collection-coupled live files:    18
expected live files after scaffold:          0
live collection-coupled files after:         0
files created by scaffold:                  0
accepted live-state groups:                 0
controlled field evidence ready:        false
field FWI ready:                        false
field 3D/HPC ready:                     false
gpu priority:                          none
```

## Interpretation

The external return directory layout now exists for the pending controlled
collection. This is a logistics improvement only. It does not create measured
radar data, metadata records, controlled field evidence, field FWI input, or
field 3D/HPC input.

## Decision

Use the directories for collection logistics only. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until real measured files and
paired metadata pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_external_return_directory_scaffold.py
9 passed with validator/sensitivity block
```

Figure check:

```text
2825x861, dynamic range=255
```
