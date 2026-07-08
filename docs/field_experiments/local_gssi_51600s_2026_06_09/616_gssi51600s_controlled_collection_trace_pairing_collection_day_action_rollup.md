# Field Experiment 616: Collection-Day Action Rollup

Date: 2026-07-01

## Purpose

Roll up the post-directory-scaffold live-state refresh into an
operator-facing collection-day action checklist.

This run consumes the guarded runs `613-615` and the controlled collection
slot manifest. It verifies that the external return directories exist, while
keeping all measured-file and paired-metadata return requirements blocked until
real collection files are supplied.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/616_gssi51600s_controlled_collection_trace_pairing_collection_day_action_rollup
```

## Result

```text
action groups:                         6
accepted action groups now:            2
directory parents:                     5
directory parents present:             5
total file slots:                     33
preparable metadata slots:            15
measured DZT files required:           9
paired metadata files required:        9
collection-coupled live files needed: 18
live measured DZT files:               0
live paired metadata files:            0
missing collection-coupled files:     18
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The filesystem scaffold is ready for collection-day logistics, but no measured
DZT files or paired metadata have arrived. The two accepted action groups are
directory verification and holding downstream escalation blocked.

## Decision

Use this as an operator-facing action rollup only. Keep controlled field
evidence, field FWI, and field 3D/HPC blocked until the measured DZT files and
paired metadata pass live intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_directory_scaffold_live_state_refresh.py
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_action_rollup.py
4 passed
```

Figure check:

```text
3113x913, dynamic range=255
```
