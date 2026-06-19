# Field Experiment 136: Inversion Blocker Map After Contrast Evidence

Date: 2026-06-18

## Purpose

Synthesize the current short-anchor field evidence after the signed morphology,
timing-margin, signal-contrast, and broad-window contrast-regime work. The
question is whether the local GSSI 51600S data have crossed from field
morphology/timing QC into field inversion readiness.

This is CPU-only synthesis of saved field summaries. It does not run FDTD,
FWI, GPU kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/136_gssi51600s_field_inversion_blocker_map_post_contrast
```

Key artifacts:

```text
data/field_inversion_blocker_map_summary.json
data/field_inversion_blocker_map_rows.csv
data/field_inversion_blocker_map_gates.csv
data/figure_validation.csv
figures/field_inversion_blocker_map.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_field_inversion_blocker_map_qc_only
positive evidence axes:                6
ready positive evidence axes:          6
blocker axes:                          9
unresolved blocker axes:               9
critical unresolved blockers:          6
field morphology supplement ready:     true
short relative timing QC ready:        true
profile spatial calibration ready:     false
absolute time-zero ready:              false
radius/geometry seed ready:            false
absolute amplitude calibration ready:  false
cover-depth recovery ready:            false
field FWI ready:                       false
3D/HPC ready:                          false
heavy field work ready:                false
field geometry type:                   independent_2d_line_profiles
gpu priority:                          none
```

Ready evidence axes:

```text
short relative timing QC
waveform morphology QC
signed morphology QC
content-only timing margin
broad signal-contrast QC
apparent-depth scale QC
```

Unresolved blockers:

```text
leave-one content redundancy
long-profile transfer
profile spatial calibration
absolute time-zero
radius seed or radius recovery
absolute amplitude calibration
cover-depth recovery
field FWI
3D/HPC
```

## Interpretation

Run `136` closes the immediate field decision after the latest contrast work:
the measured data are useful as a short-profile field morphology/timing
supplement, but they are still not an inversion workload. The positive evidence
is real, especially signed morphology and broad-window signal contrast, but it
does not remove the independent blockers: no absolute time-zero, no single
spatial translation, weak radius evidence, no absolute amplitude calibration,
no cover-depth validation, and no 3D survey geometry.

The next field step should not be field FWI/HPC on this archive. Either keep
this dataset as scoped 2D QC/supplement evidence, or design a new controlled
field acquisition with surveyed target geometry, absolute timing/depth
controls, dielectric calibration, and amplitude calibration.

## Validation

Focused test for the new blocker-map script:

```text
tests/test_gssi_field_inversion_blocker_map.py
2 passed
```

Focused detector/field regression:

```text
62 passed
```

Full suite:

```text
877 passed
```

Figure validation:

```text
field_inversion_blocker_map.png: 2484x1039,
nonwhite=0.2673, dynamic range=255
```
