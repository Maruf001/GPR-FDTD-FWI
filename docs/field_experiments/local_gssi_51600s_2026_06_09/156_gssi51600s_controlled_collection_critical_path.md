# Field Experiment 156: Controlled Collection Critical Path

Date: 2026-06-19

## Purpose

Audit the critical path from the run `155` controlled-collection handoff to a
packet that could pass acceptance. This is CPU-only synthesis of the existing
handoff rows, gate handoff table, packet fill map, and summary.

This does not run DZT preprocessing, FDTD, FWI, GPU kernels, field FWI,
3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/156_gssi51600s_controlled_collection_critical_path
```

Key artifacts:

```text
data/field_controlled_collection_critical_actions.csv
data/field_controlled_collection_gate_critical_path.csv
data/field_controlled_collection_phase_plan.csv
data/field_controlled_collection_critical_path_summary.json
figures/field_controlled_collection_critical_path.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_controlled_collection_critical_path
source handoff:                       gssi51600s_controlled_collection_handoff
actions:                              7
new controlled-data actions:          6
critical new-data actions:            5
field-inversion prerequisite actions: 3
acceptance gates:                     7
ready gates:                          0
current-archive unblockable gates:    0
packet rows needing entry:            12
missing required values:              44
reference repeat gate:                3
reference uncertainty gate:           0.02 ns
field geometry type:                  independent_2d_line_profiles
is 3D survey:                         false
ready for collection execution:       true
ready for packet acceptance:          false
ready for current archive field FWI:  false
ready for heavy field work:           false
ready for field 3D/HPC:               false
gpu priority:                         none
```

Critical gate paths:

```text
field_fwi_or_heavy_work:
  target_truth_geometry -> time_zero_reference -> amplitude_reference

absolute_time_zero_references:
  time_zero_reference -> reference_registry

amplitude_references:
  amplitude_reference -> reference_registry

required_metadata_fields:
  profile_target_geometry -> acquisition_control_links -> session_metadata -> reference_registry

cross_table_links:
  profile_target_geometry -> acquisition_control_links -> reference_registry

short_repeat_redundancy:
  profile_target_geometry -> acquisition_control_links
```

Collection phases:

```text
1. target_truth        target_truth_geometry
2. references          time_zero_reference, amplitude_reference, reference_registry
3. survey_geometry     profile_target_geometry
4. controlled_repeats  acquisition_control_links
5. session_metadata    session_metadata
```

## Interpretation

Run `156` makes the stop rule explicit: the current archive cannot unblock any
acceptance gate by itself. The next useful field action is still a controlled
2D collection with real target truth, time-zero references, amplitude
references, surveyed profile geometry, controlled repeats, and verified
session/reference metadata.

The field archive remains useful for scoped measured-field 2D QC and manuscript
supplement context. It is not a 3D survey and it is not ready for field FWI,
heavy local GPU field work, field 3D/HPC, or neural-network training.

## Validation

Focused critical-path test:

```text
tests/test_gssi_field_controlled_collection_critical_path.py
2 passed
```

Figure validation:

```text
field_controlled_collection_critical_path.png: 2144x835,
nonwhite=0.3715, dynamic range=255
```
