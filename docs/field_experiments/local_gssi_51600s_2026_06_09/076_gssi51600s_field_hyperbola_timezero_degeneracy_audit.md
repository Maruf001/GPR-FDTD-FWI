# Field Experiment 076: Hyperbola Time-Zero Degeneracy Audit

Date: 2026-06-18

## Purpose

Quantify how much non-identifiability remains in the local GSSI hyperbola and
common-offset score surfaces. This is a CPU-only reduction of existing field
QC outputs; it does not launch FDTD, FWI, GPU kernels, 3D inversion, radius
recovery, or cover-depth recovery.

## Output

```text
086_gssi51600s_field_hyperbola_timezero_degeneracy_audit
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/086_gssi51600s_field_hyperbola_timezero_degeneracy_audit/data/field_hyperbola_timezero_degeneracy_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/086_gssi51600s_field_hyperbola_timezero_degeneracy_audit/data/field_common_offset_ambiguity_rows.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/086_gssi51600s_field_hyperbola_timezero_degeneracy_audit/data/field_hyperbola_timezero_degeneracy_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/086_gssi51600s_field_hyperbola_timezero_degeneracy_audit/figures/field_hyperbola_timezero_degeneracy.png
```

## Result

Policy label:

```text
field_hyperbola_timezero_degeneracy_not_calibrated_inversion
```

Summary:

```text
surface summary rows:               4
offset summary rows:                2
boundary best-fit surfaces:         3 / 4
max near-top epsr span:             4.085
max near-top time-zero span:        0.300 ns
max near-top offset count, 5% gate: 5
cover-depth claim ready:            false
radius claim ready:                 false
field FWI ready:                    false
gpu priority:                       none
```

## Interpretation

The existing hyperbola and common-offset score surfaces are useful measured
field QC overlays, but they are not calibrated inversion evidence. Near-top
score regions span multiple dielectric and time-zero choices, the common-offset
sweep keeps several Tx/Rx offsets plausible, and most best fits sit on grid
boundaries.

This strengthens the field claim boundary: the dataset can support measured
2D line-profile timing/repeatability and overlay QC, but not calibrated
cover-depth, radius, 3D, or field-FWI recovery.

## Validation

Focused tests:

```text
tests/test_gssi_field_hyperbola_timezero_degeneracy_audit.py
3 passed
```

Figure validation:

```text
086 field_hyperbola_timezero_degeneracy.png: 2739x1515, dynamic range=255
```
