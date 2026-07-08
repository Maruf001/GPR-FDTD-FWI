# BEM Experiment 836: Stage-1 Producer Command Packet

Date: 2026-07-01

## Purpose

Convert the stage-1 live-return contract into a concrete non-executed producer
packet for the first real FDTD complex-field row.

This run does not execute FDTD, create an external return file, merge a partial
file into the full 279-row input, run comparison, transfer to field data, or
start 3D/HPC work.

## Output

```text
outputs/bem_experiments/836_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_producer_command_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_acceptance_rows.csv
data/project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet_summary.json
figures/project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet.png
```

## Result

```text
producer command rows:             1
acceptance checks:                 6
passed acceptance checks:          6
failed acceptance checks:          0
stage:                             1
pair id:                           stage01_pair000
receiver index:                   15
frequency:                         1.0 GHz
required rows:                     1
required columns:                 12
stage-1 partial file present:      false
full external input present:       false
FDTD executed now:                 false
executed command count:            0
real BEM/FDTD comparison ready:    false
field transfer ready:              false
3D/HPC ready:                      false
```

The target partial return remains:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_stage1_partial.csv
```

The required schema is:

```text
stage
pair_id
receiver_index
frequency_hz
fdtd_real
fdtd_imag
returned_fdtd_source_hash
solver_run_id
solver_status
solver_log_sha256
real_fdtd_exported
input_contract_sha256
```

## Interpretation

The next real FDTD producer task is now exactly one complex electric-field row:
receiver `15` at `1.0 GHz`. This is the smallest real return that can test the
stage-1 live intake path.

## Decision

Use this packet to request the first real stage-1 partial return. Do not promote
comparison until that file exists and passes the live intake gate.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_stage1_producer_command_packet.py
2 passed
```

Figure check:

```text
3221x897, dynamic range=255
```
