# BEM Experiment 917: Panel-116 Continuous-Shift Project-FDTD Launch/Return Packet Validation Sensitivity

Date: 2026-07-01

## Purpose

Stress-test the run `916` launch/return packet validator by damaging the saved
run `915` packet in controlled ways.

The sensitivity set mutates packet readiness, source readiness, frequency-slot
counts, high-band counts, packet identity, return presence, comparison
acceptance, schema shape, packet-file hashes, gate state, execution flags,
downstream promotion, figure metadata, and script snapshots.

## Output

```text
outputs/bem_experiments/917_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_launch_return_packet_validation_sensitivity
```

## Result

```text
source validator ready:               true
scenarios:                            22
expected passes:                       1
expected failures:                    21
observed passes:                       1
observed failures:                    21
unexpected outcomes:                   0
damaged scenarios:                    21
damaged scenarios rejected:           21
project FDTD launch packet written: true
project FDTD execution authorized:  false
project FDTD return rows present:   false
project FDTD comparison completed:  false
field transfer ready:                false
real 3D validation ready:            false
gpu priority:                        none
```

## Interpretation

The run `916` validator accepts only the exact non-executed launch/return
packet. It rejects damaged schemas, packet files, gates, false return rows, and
downstream promotions.

## Decision

Use runs `915-917` as the guarded launch/return packet block.

## Validation

Focused test:

```text
tests/test_scarep_2d_cpu_bem_panel116_continuous_shift_project_fdtd_launch_return_packet_validation_sensitivity.py
3 passed
```

Figure check:

```text
3311x884, dynamic range=255
```
