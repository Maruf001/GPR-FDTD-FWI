# Field Experiment 144: Current Archive Packet Prefill Validation

Date: 2026-06-18

## Purpose

Validate the partially prefilled current-archive packet from run `143`.

This is CPU-only field-readiness validation. It does not run FDTD, FWI, GPU
kernels, 3D/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/144_gssi51600s_current_archive_packet_prefill_validation
```

Key artifacts:

```text
data/controlled_2d_packet_validation_summary.json
data/controlled_2d_packet_table_status.csv
data/controlled_2d_packet_acceptance_status.csv
data/controlled_2d_packet_validation_findings.csv
```

## Result

```text
tables:                              5
total rows:                         11
filled rows:                         9
validation rules:                   51
required-field evaluations:        108
blocking findings:                  67
missing required values:            67
dtype failures:                      0
cross-table failures:                0
acceptance gates:                    7
packet acceptance ready:             false
current archive field FWI ready:     false
current archive heavy field ready:   false
field 3D/HPC ready:                  false
gpu priority:                        none
```

## Interpretation

Prefill improves provenance but does not make the current archive inversion
ready. The remaining blockers are explicit: operator/antenna serial/gain,
target truth, surveyed profile start/end and target crossings, acquisition
target links, Tx/Rx offset, timing/amplitude reference links, and external
time-zero/amplitude reference rows.

All seven packet acceptance gates remain false. Field FWI, heavy field GPU
work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_current_archive_packet_prefill.py
tests/test_gssi_field_controlled_2d_packet_validator.py
8 passed
```
