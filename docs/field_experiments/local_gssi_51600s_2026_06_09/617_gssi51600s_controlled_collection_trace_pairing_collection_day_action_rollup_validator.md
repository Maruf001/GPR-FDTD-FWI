# Field Experiment 617: Collection-Day Action Rollup Validator

Date: 2026-07-01

## Purpose

Validate the saved run `616` collection-day action rollup from artifacts.

The validator checks the summary readiness flag, action-row shape, directory
and slot counts, absence of live collection-coupled files, blocked downstream
field-analysis states, figure metadata, and frozen script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/617_gssi51600s_controlled_collection_trace_pairing_collection_day_action_rollup_validator
```

## Result

```text
validation checks:                    7
checks passed:                        7
checks failed:                        0
action groups:                        6
accepted action groups now:           2
directory parents:                    5
directory parents present:            5
total file slots:                    33
preparable metadata slots:           15
measured DZT files required:          9
paired metadata files required:       9
collection-coupled live files needed:18
live collection-coupled files:        0
missing collection-coupled files:    18
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

## Interpretation

The saved collection-day action rollup validates as a logistics checklist, not
as field evidence.

## Decision

Use run `616` as the current field collection-day action rollup. Keep field
analysis blocked until the measured DZT files and paired metadata arrive and
pass live intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup_validator.py
4 passed
```

Figure check:

```text
2933x879, dynamic range=255
```
