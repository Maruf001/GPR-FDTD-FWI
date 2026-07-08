# Field Experiment 137: Controlled Field Acquisition Design From Blockers

Date: 2026-06-18

## Purpose

Translate the run `136` field inversion blocker map into a concrete controlled
2D acquisition design. This keeps the current local GSSI archive scoped as
field morphology/timing QC while defining what must be measured in a future
controlled field pass before field inversion could be defensible.

This is CPU-only synthesis of saved blocker rows. It does not run FDTD, FWI,
GPU kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/137_gssi51600s_field_controlled_acquisition_design
```

Key artifacts:

```text
data/field_controlled_acquisition_design_summary.json
data/field_controlled_acquisition_design_rows.csv
data/field_controlled_acquisition_design_phases.csv
data/field_controlled_acquisition_design_gates.csv
data/figure_validation.csv
figures/field_controlled_acquisition_design.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         gssi51600s_controlled_field_acquisition_design_from_blockers
design requirements:                  9
must-have requirements:               5
unresolved must-have requirements:    5
source critical blockers:             6
current archive is 3D survey:          false
current field geometry type:           independent_2d_line_profiles
current archive field FWI ready:       false
current archive heavy field ready:     false
new controlled 2D design ready:        true
field 3D/HPC ready:                   false
gpu priority:                          none
```

Must-have controls:

```text
absolute time-zero reference
surveyed profile/target spatial geometry
known target radius or diameter
known cover depth plus dielectric/velocity calibration
absolute or reference amplitude calibration
```

## Interpretation

Run `137` makes the field path operational rather than simply saying "not
ready." The current archive remains a scoped 2D field morphology/timing
supplement. A future controlled 2D validation pass should collect surveyed
profile starts, trace spacing, scan direction, target x locations, absolute
timing reference, measured target radius/diameter, cover depth, dielectric or
velocity calibration, gain/coupling metadata, and a reference amplitude target.

The current field archive is not a 3D survey and should not be submitted as a
field FWI/HPC workload.

## Validation

Focused test:

```text
tests/test_gssi_field_controlled_acquisition_design.py
2 passed
```

Figure validation:

```text
field_controlled_acquisition_design.png: 2399x937,
nonwhite=0.2911, dynamic range=255
```
