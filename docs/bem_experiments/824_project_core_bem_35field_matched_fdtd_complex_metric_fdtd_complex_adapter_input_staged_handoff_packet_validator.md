# BEM Experiment 824: Complex FDTD Adapter Input Staged Handoff Packet Validator

Date: 2026-07-01

## Purpose

Validate the saved staged complex FDTD handoff packet from run `823`.

The validator checks the stage shape, cumulative shape, ten output-local packet
files, final 279-row cumulative packet, blank real FDTD value/provenance fields,
blocked external input, blocked comparison, figure validation, and script
snapshots.

## Output

```text
outputs/bem_experiments/824_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_validator
```

## Result

```text
validation checks:                         8
passed checks:                             8
failed checks:                             0
stage count:                               5
stage row shape:                           1;8;30;120;120
cumulative row shape:                      1;9;39;159;279
packet files:                              10
packet files present:                      10
final cumulative rows:                     279
final cumulative FDTD value blank cells:   558
final cumulative provenance blank cells:   1395
external input file present:               false
accepted as real external input:           false
real BEM/FDTD comparison ready:            false
3D/HPC ready:                              false
```

## Interpretation

The saved staged packet is internally stable and remains output-local. It is a
producer handoff packet only, not real BEM/FDTD evidence.

## Decision

Use this validator before accepting any changes to the staged complex FDTD
handoff packet.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_staged_handoff_packet_validator.py
```

Figure check:

```text
2825x936, dynamic range=255
```
