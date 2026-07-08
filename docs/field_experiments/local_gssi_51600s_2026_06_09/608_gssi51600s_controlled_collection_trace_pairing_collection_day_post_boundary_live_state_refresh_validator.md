# Field Experiment 608: Collection-Day Post-Boundary Live-State Refresh Validator

Date: 2026-07-01

## Purpose

Validate the saved run `607` field live-state refresh from artifacts.

The validator checks source readiness, state-row shape, required slot counts,
live-file absence, blocked field evidence, blocked field FWI/3D, figure
validation, and script snapshots.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/608_gssi51600s_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh_validator
```

## Result

```text
validation checks:                         6
passed checks:                             6
failed checks:                             0
state rows:                                6
total return slots:                       33
measured DZT files required:               9
paired metadata files required:            9
collection-coupled live files required:   18
live collection-coupled files:             0
missing collection-coupled files:         18
accepted live-state groups:                0
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The post-boundary live-state refresh validates as live-file absent and
evidence-blocked.

## Decision

Keep field downstream work blocked until measured DZT files and paired metadata
files pass intake.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_post_boundary_live_state_refresh_validator.py
8 passed with refresh/sensitivity block
```

Figure check:

```text
2285x858, dynamic range=255
```
