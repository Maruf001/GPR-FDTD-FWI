# Field Experiment 153: Recovered Scaffold Type-Aware Blocker Prioritization

Date: 2026-06-18

## Purpose

Regenerate the controlled-field collection action plan from the corrected
run `152` type-aware scaffold validation.

This is CPU-only synthesis of saved packet-validation outputs. It does not run
DZT preprocessing, FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/153_gssi51600s_recovered_scaffold_type_aware_blocker_prioritization
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
policy label:                         gssi51600s_controlled_packet_blocker_prioritization
source validation run:                 152_gssi51600s_recovered_scaffold_type_aware_validation
source reference run:                  145_gssi51600s_field_time_zero_reference_requirement
blocking findings:                     44
missing required values:               44
action groups:                         7
new controlled-data action groups:     6
archive/notes-resolvable groups:       1
failed acceptance gates:               7
reference repeat gate:                 3
reference uncertainty gate:            0.02 ns
reference depth equivalent:            1.9986 mm
ready for new controlled 2D pass:      true
ready for current archive field FWI:   false
ready for heavy field work:            false
ready for field 3D/HPC:                false
gpu priority:                          none
```

Updated action groups:

```text
priority 1: target_truth_geometry       9 missing fields, at least 1 target row
priority 2: time_zero_reference         6 missing fields, at least 3 references
priority 3: amplitude_reference         6 missing fields, at least 3 references
priority 4: profile_target_geometry     6 missing fields, surveyed profile frame
priority 5: acquisition_control_links   9 missing fields, at least 3 repeats
priority 6: session_metadata            2 missing fields, recover/recollect date/operator
priority 7: reference_registry          6 missing fields, reference file names
```

Critical new-data blocker groups remain:

```text
target_truth_geometry
time_zero_reference
amplitude_reference
profile_target_geometry
acquisition_control_links
```

## Interpretation

Run `153` is the corrected field-collection action plan. The current archive
and scaffold remain blocked for inversion, but the required next measurements
are now more precise and less inflated than run `146`:

```text
1. Measure target material, center coordinates, cover depth, diameter/radius,
   dielectric/velocity, and uncertainty.
2. Collect three time-zero references with uncertainty <= 0.02 ns or explicitly
   propagated uncertainty.
3. Collect three amplitude references with repeatability metrics.
4. Survey profile start/end coordinates, scan direction, trace spacing, and
   survey method in one coordinate frame.
5. Record three controlled profile repeats with file names, Tx/Rx offset, and
   coupling condition.
6. Fill collection date and operator.
7. Record reference file names for all six reference rows.
```

This supports a future controlled 2D field collection. It does not justify
current-archive field FWI, heavy local GPU work, field 3D/HPC, or calibrated
field radius/depth claims.

## Validation

Focused blocker-prioritization test:

```text
tests/test_gssi_field_controlled_packet_blocker_prioritization.py
3 passed
```

Figure validation:

```text
field_controlled_packet_blocker_prioritization.png: 2569x937,
nonwhite=0.3284, dynamic range=255
```
