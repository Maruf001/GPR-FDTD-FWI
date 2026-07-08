# BEM Experiment 915: Panel-116 Continuous-Shift Project-FDTD Launch/Return Packet

Date: 2026-07-01

## Purpose

Build a non-executed project-FDTD launch/return packet scaffold for the smooth
continuous-shift BEM candidate guarded by runs `912-914`.

This run writes packet files, frequency slots, return-schema requirements, and
fail-closed gates. It does not authorize or execute FDTD, stage return rows, or
complete a BEM/FDTD comparison.

## Output

```text
outputs/bem_experiments/915_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_launch_return_packet
```

## Result

```text
packet id:                              panel116_continuous_shift_project_fdtd_packet_v1
source contract ready:                  true
source contract validation ready:       true
source contract sensitivity ready:      true
source continuous validation ready:     true
BEM model:                              best_gaussian_bump
BEM continuous worst relative L2:       0.0008519458802336965
frequency slots:                        25
high-band frequency slots:               9
return schema columns:                  15
acceptance gates:                        6
passed acceptance gates:                 6
packet files:                            4
packet file hashes:                      4
project FDTD launch packet written:    true
project FDTD execution authorized:     false
project FDTD executed:                 false
project FDTD return rows present:      false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

Packet files:

| File key | Written |
| --- | --- |
| launch_request | true |
| frequency_slot_manifest | true |
| return_schema | true |
| non_execution_notice | true |

The return schema requires 15 columns:

```text
packet_id, solver_run_id, solver_status, frequency_index, frequency_hz,
frequency_ghz, receiver_id, receiver_index, receiver_x_m, receiver_z_m,
fdtd_real, fdtd_imag, fdtd_source_hash, solver_log_sha256,
provenance_json_sha256
```

## Interpretation

The smooth panel-116 BEM candidate now has a concrete project-FDTD handoff
packet. The packet preserves the 25 launch frequency slots and requires a
complex real/imaginary FDTD return schema with receiver-frequency identity and
provenance.

The packet is not evidence. It writes launch/return requirements only.

## Decision

Use this as the non-executed launch/return handoff packet. Comparison, field
transfer, GPU priority, and 3D validation remain blocked until real FDTD rows
pass a separate intake gate.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_launch_return_packet.py
5 passed
```

Figure check:

```text
3581x895, dynamic range=255
```
