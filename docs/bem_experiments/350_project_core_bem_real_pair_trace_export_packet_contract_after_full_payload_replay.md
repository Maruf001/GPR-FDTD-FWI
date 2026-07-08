# BEM Experiment 350: Real-Pair Trace Export Packet Contract After Full-Payload Replay

Date: 2026-06-29

## Purpose

Turn the post-replay real-pair blocker from runs `347-349` into a concrete
FDTD export packet contract.

The BEM replay branch is no longer blocked by missing formula payloads. It is
blocked by missing real FDTD-side files and metadata. This run defines exactly
what the future FDTD export packet must contain before a real BEM/FDTD
comparison can be executed.

This run does not stage real FDTD traces, execute a real BEM/FDTD comparison,
calibrate thresholds, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/350_project_core_bem_real_pair_trace_export_packet_contract_after_full_payload_replay
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_contract_after_full_payload_replay_packet_rows.csv
data/project_core_bem_real_pair_trace_export_packet_contract_after_full_payload_replay_acceptance_rows.csv
data/project_core_bem_real_pair_trace_export_packet_contract_after_full_payload_replay_summary.json
figures/project_core_bem_real_pair_trace_export_packet_contract_after_full_payload_replay.png
scripts/script_snapshot_manifest.json
```

## Result

```text
packet contract ready:              true
packet items:                       34
projected trace files:              26
metadata/control items:             8
acceptance checks:                  217
background trace files:             13
target trace files:                 13
receiver keys:                      13
frequency keys:                     9
expected FDTD frequency-bin rows:   234
expected paired residual rows:      117
real packet files present:          false
real pair execution ready:          false
GPU work ready:                     false
field FWI ready:                    false
figure size:                        3491x929
figure dynamic range:               255
```

The eight metadata/control items are:

```text
trace_set_metadata.json
scalar_projection_convention.json
time_zero_reference.json
amplitude_reference.json
fdtd_projected_frequency_bins.csv
fdtd_frequency_extraction_metadata.json
bem_fdtd_paired_residuals.csv
threshold_calibration.json
```

## Interpretation

The BEM side now has a precise handoff target for the real FDTD export:
26 projected scalar traces, eight metadata/control files, 217 acceptance
checks, 234 expected FDTD frequency-bin rows, and 117 expected paired residual
rows.

This does not make the real comparison executable yet. It converts the blocker
from a general statement into a file-level packet contract.

## Decision

Use run `350` as the next FDTD export target. Keep real BEM/FDTD execution,
threshold calibration, broad BEM replacement, 3D validation, GPU/HPC work,
field transfer, and field FWI blocked until the packet is staged and validated.
