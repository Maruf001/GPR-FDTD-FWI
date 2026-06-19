# Field Experiment 155: Controlled Collection Handoff

Date: 2026-06-19

## Purpose

Create an operational run sheet for the next controlled 2D GSSI field pass by
joining the recovered packet scaffold from run `151`, the type-aware validation
from run `152`, the action priorities from run `153`, and the field-QC bridge
from run `154`.

This is CPU-only synthesis of saved packet CSVs and summaries. It does not run
DZT preprocessing, FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/155_gssi51600s_controlled_collection_handoff
```

Key artifacts:

```text
data/field_controlled_collection_run_sheet.md
data/field_controlled_collection_handoff_rows.csv
data/field_controlled_collection_packet_fill_map.csv
data/field_controlled_collection_gate_handoff.csv
data/field_controlled_collection_handoff_summary.json
figures/field_controlled_collection_handoff.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                           gssi51600s_controlled_collection_handoff
handoff actions:                        7
critical new-data actions:              5
critical new-data groups:               target_truth_geometry; time_zero_reference; amplitude_reference; profile_target_geometry; acquisition_control_links
packet rows:                            12
packet rows needing entry:              12
missing required values:                44
blocking findings:                      44
acceptance gates:                       7
failed acceptance gates:                7
reference repeat gate:                  3
reference uncertainty gate:             0.02 ns
reference depth equivalent:             1.9986 mm
field geometry type:                    independent_2d_line_profiles
is 3D survey:                           false
ready for collection day:               true
ready for packet acceptance:            false
ready for current archive QC supplement: true
ready for current archive field FWI:    false
ready for heavy field work:             false
ready for field 3D/HPC:                 false
gpu priority:                           none
```

Collection-facing priorities:

```text
1. target_truth_geometry       T_CONTROL_001
2. time_zero_reference         T0_REF_001, T0_REF_002, T0_REF_003
3. amplitude_reference         AMP_REF_001, AMP_REF_002, AMP_REF_003
4. profile_target_geometry     P_CONTROL_001 crossed with T_CONTROL_001
5. acquisition_control_links   P_CONTROL_001 repeats 1-3
6. session_metadata            planned_controlled_2d_session_001
7. reference_registry          six reference rows
```

## Interpretation

Run `155` is the field-side next-step artifact. It is not another inversion
readiness claim; it is the collection handoff that says exactly what must be
measured before field inversion can be defensible.

The current archive remains useful for scoped 2D field-QC/manuscript supplement
work. It is not ready for field FWI, heavy local GPU field work, field 3D/HPC,
or neural-network training until a filled controlled packet passes validation
and all acceptance gates pass.

## Validation

Focused handoff test:

```text
tests/test_gssi_field_controlled_collection_handoff.py
3 passed
```

Figure validation:

```text
field_controlled_collection_handoff.png: 2705x1583,
nonwhite=0.1490, dynamic range=255
```
