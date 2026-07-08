# Field Experiment 143: Current Archive Packet Prefill

Date: 2026-06-18

## Purpose

Create a controlled-acquisition packet copy prefilled only with provenance
supported by the existing local GSSI archive.

This is CPU-only field-readiness tooling. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/143_gssi51600s_current_archive_packet_prefill
```

Key artifacts:

```text
packet/session_log.csv
packet/profile_geometry.csv
packet/acquisition_run.csv
packet/target_truth.csv
packet/reference_measurement.csv
data/current_archive_packet_prefill_status.csv
data/current_archive_packet_prefill_summary.json
```

## Result

```text
packet tables:                         5
total packet rows:                    11
filled packet rows:                    9
session rows prefilled:                1
profile rows prefilled:                4
acquisition rows prefilled:            4
target-truth rows prefilled:           0
reference rows prefilled:              0
packet validation ready:               true
current archive field FWI ready:       false
current archive heavy field ready:     false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The current archive can prefill session, profile, and acquisition provenance:
dataset id/date, antenna/system/software, dielectric setting, scan spacing,
time range, raw file names, profile ids, and trace spacing.

It cannot defensibly prefill target truth, target crossings, Tx/Rx offset,
external time-zero references, or amplitude references. Those controls remain
empty and must be collected in a future controlled 2D acquisition.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_archive_packet_prefill.py
4 passed
```
