# Field Experiment 146: Controlled Packet Blocker Prioritization

Date: 2026-06-18

## Purpose

Collapse the run `144` packet-validation blockers and run `145` external
time-zero requirement into a small, prioritized controlled-acquisition action
set.

This is CPU-only synthesis of saved field packet outputs. It does not run FDTD,
FWI, GPU kernels, field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/146_gssi51600s_controlled_packet_blocker_prioritization
```

Key artifacts:

```text
data/field_controlled_packet_blocker_prioritization_summary.json
data/field_controlled_packet_action_groups.csv
data/field_controlled_packet_gate_actions.csv
data/field_controlled_packet_blocker_rows.csv
figures/field_controlled_packet_blocker_prioritization.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                       gssi51600s_controlled_packet_blocker_prioritization
blocking findings:                  67
action groups:                       7
new controlled-data action groups:   6
archive/notes-resolvable groups:     1
failed acceptance gates:             7
reference repeat gate:               3
reference uncertainty gate:          0.02 ns
reference depth equivalent:          1.9986 mm
ready for new controlled 2D pass:    true
ready for current archive field FWI: false
ready for heavy field work:          false
ready for field 3D/HPC:              false
gpu priority:                        none
```

Critical new-data blocker groups:

```text
target_truth_geometry
time_zero_reference
amplitude_reference
profile_target_geometry
acquisition_control_links
```

The seven action groups are:

```text
priority 1: target_truth_geometry       10 missing fields, at least 1 target row
priority 2: time_zero_reference          2 missing fields, at least 3 references
priority 3: amplitude_reference          2 missing fields, at least 3 references
priority 4: profile_target_geometry     24 missing fields, surveyed profile frame
priority 5: acquisition_control_links   20 missing fields, at least 3 repeats
priority 6: session_metadata             3 missing fields, recover/recollect metadata
priority 7: reference_registry           6 missing fields, reference IDs and links
```

## Interpretation

The current field archive is not inversion-ready, but the reason is now
operational rather than vague. The 67 validation blockers collapse into a
controlled-acquisition collection plan. Only session metadata may be recoverable
from notes; the other blocker groups require new controlled field data.

No field FWI, heavy field GPU work, or field 3D/HPC is justified until these
actions are completed in the packet and the validator reports all seven
acceptance gates ready.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_packet_blocker_prioritization.py
3 passed
```

Figure validation:

```text
field_controlled_packet_blocker_prioritization.png: 2569x937,
nonwhite=0.2717, dynamic range=255
```
