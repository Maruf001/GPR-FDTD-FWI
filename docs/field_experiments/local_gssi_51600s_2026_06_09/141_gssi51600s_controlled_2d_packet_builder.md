# Field Experiment 141: Controlled 2D Packet Builder

Date: 2026-06-18

## Purpose

Generate reusable CSV packet templates and validation rules from the run `140`
controlled 2D acquisition protocol.

This is CPU-only field-operations tooling. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/141_gssi51600s_controlled_2d_packet_builder
```

Key artifacts:

```text
templates/session_log.csv
templates/target_truth.csv
templates/profile_geometry.csv
templates/acquisition_run.csv
templates/reference_measurement.csv
data/controlled_2d_packet_validation_rules.csv
data/controlled_2d_packet_current_archive_prefill_limits.csv
data/controlled_2d_packet_summary.json
```

## Result

```text
template tables:                         5
template files:                          5
validation rules:                       51
required metadata fields:               51
acceptance gates:                        7
current archive partial prefill tables:  3
current archive blocked prefill tables:  2
current archive must-have controls:      0 / 5
new controlled 2D acquisition ready:     true
packet validation ready:                 true
current archive field FWI ready:         false
current archive heavy field ready:       false
field 3D/HPC ready:                      false
gpu priority:                            none
```

## Interpretation

The current GSSI archive can partially prefill session, profile-geometry, and
acquisition-run provenance. It cannot supply target-truth or external
reference-measurement controls, so field FWI, heavy field GPU work, and field
3D/HPC remain blocked.

The useful next field action is to fill these packet templates during a future
controlled 2D acquisition, then validate the packet before any inversion
proposal.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_2d_packet_builder.py
3 passed
```
