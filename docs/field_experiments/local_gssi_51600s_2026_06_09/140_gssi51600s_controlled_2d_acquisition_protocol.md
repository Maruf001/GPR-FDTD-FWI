# Field Experiment 140: Controlled 2D Acquisition Protocol

Date: 2026-06-18

## Purpose

Convert the current field blockers and time-zero gap into a practical
controlled 2D acquisition protocol for a future measured validation pass.

This is CPU-only synthesis from runs `137-139`. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/140_gssi51600s_controlled_2d_acquisition_protocol
```

Key artifacts:

```text
data/controlled_2d_acquisition_protocol_summary.json
data/controlled_2d_acquisition_protocol_steps.csv
data/controlled_2d_acquisition_metadata_schema.csv
data/controlled_2d_acquisition_acceptance_gates.csv
data/controlled_2d_acquisition_field_sheet_template.csv
```

## Result

```text
protocol steps:                         8
must-have protocol steps:               6
metadata tables:                        5
required metadata fields:               51
acceptance gates:                       7
minimum short repeats per target:       3
new controlled 2D acquisition ready:    true
current archive field FWI ready:        false
current archive heavy field ready:      false
field 3D/HPC ready:                     false
gpu priority:                           none
```

## Interpretation

A future controlled 2D field pass should collect session metadata, target
radius/diameter truth, cover depth, dielectric/velocity calibration, absolute
time-zero references, surveyed profile/target geometry, amplitude references,
and at least three short-profile repeats per controlled target.

The current local GSSI archive remains QC/context only. Field FWI, heavy field
GPU work, and field 3D/HPC remain blocked until a new controlled acquisition
satisfies the protocol gates.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_2d_acquisition_protocol.py
tests/test_gssi_field_time_zero_control_gap_manifest.py
4 passed
```
