# Field Experiment 154: Field QC To Controlled Collection Bridge

Date: 2026-06-19

## Purpose

Connect the current local GSSI field-QC evidence to the corrected
controlled-collection action plan from run `153`.

This is CPU-only synthesis of saved field summaries and packet CSVs. It does
not run DZT preprocessing, FDTD, FWI, GPU kernels, field FWI, 3D/HPC work, or
neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/154_gssi51600s_field_qc_to_controlled_collection_bridge
```

Key artifacts:

```text
data/field_qc_to_controlled_collection_bridge_summary.json
data/field_qc_to_controlled_collection_evidence_rows.csv
data/field_qc_to_controlled_collection_action_rows.csv
figures/field_qc_to_controlled_collection_bridge.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                              gssi51600s_field_qc_to_controlled_collection_bridge
evidence axes:                             9
current archive supported axes:            5
inversion blocker axes:                    4
unresolved inversion blocker axes:         4
action groups:                             7
critical new-data action groups:           5
packet blocking findings:                  44
failed acceptance gates:                   7
reference repeat gate:                     3
reference uncertainty gate:                0.02 ns
reference depth equivalent:                1.9986 mm
field geometry type:                       independent_2d_line_profiles
is 3D survey:                              false
ready for current archive QC supplement:   true
ready for absolute time-zero:              false
ready for calibrated depth/radius:         false
ready for current archive field FWI:       false
ready for current archive heavy work:      false
ready for field 3D/HPC:                    false
ready for new controlled 2D acquisition:   true
gpu priority:                              none
```

Current-archive support axes:

```text
field archive dimensionality:  independent 2D line-profile bundle
short relative timing QC:      supported
waveform morphology QC:        supported
content-only timing margin:    supported
broad signal-contrast QC:      supported
```

Unresolved inversion blockers:

```text
absolute time-zero reference
absolute amplitude calibration
target truth and profile geometry
controlled repeat packet acceptance
```

Critical new-data action groups:

```text
target_truth_geometry
time_zero_reference
amplitude_reference
profile_target_geometry
acquisition_control_links
```

## Interpretation

Run `154` makes the field boundary explicit. The current archive is useful for
a scoped 2D field-QC/manuscript supplement because the short-profile relative
timing, waveform morphology, content-only timing margin, and broad-window
contrast evidence are supported.

It is not an inversion launch gate. Absolute time-zero references, amplitude
references, target truth, surveyed profile geometry, and controlled acquisition
links remain unresolved. Field FWI, heavy local GPU work, field 3D/HPC, and
calibrated field radius/depth claims remain blocked until a filled controlled
2D packet passes validation.

## Validation

Focused bridge test:

```text
tests/test_gssi_field_qc_to_controlled_collection_bridge.py
3 passed
```

Figure validation:

```text
field_qc_to_controlled_collection_bridge.png: 2705x971,
nonwhite=0.2522, dynamic range=255
```
