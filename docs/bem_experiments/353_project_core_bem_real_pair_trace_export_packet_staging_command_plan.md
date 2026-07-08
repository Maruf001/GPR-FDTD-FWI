# BEM Experiment 353: Real-Pair Trace Export Packet Staging Command Plan

Date: 2026-06-29

## Purpose

Convert the guarded file-level BEM/FDTD packet contract from run `350` into an
ordered, non-executed staging command plan.

Runs `350-352` define and guard the packet contents. This run answers the next
practical question:

```text
What exact staging phases must happen before a real paired BEM/FDTD comparison
can be executed?
```

This run does not stage real FDTD traces, execute shell commands, run a real
BEM/FDTD comparison, calibrate thresholds, launch GPU/HPC work, or run field
FWI.

## Output

```text
outputs/bem_experiments/353_project_core_bem_real_pair_trace_export_packet_staging_command_plan
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_staging_command_plan_command_rows.csv
data/project_core_bem_real_pair_trace_export_packet_staging_command_plan_commands.sh
data/project_core_bem_real_pair_trace_export_packet_staging_command_plan_summary.json
figures/project_core_bem_real_pair_trace_export_packet_staging_command_plan.png
docs/PROJECT_CORE_BEM_REAL_PAIR_TRACE_EXPORT_PACKET_STAGING_COMMAND_PLAN.md
scripts/script_snapshot_manifest.json
```

## Result

```text
packet contract guarded:           true
staging phases:                    8
command rows:                      8
all commands non-executed:         true
command script comment-only:       true
projected trace files expected:    26
metadata/control items expected:   8
packet items expected:             34
acceptance checks expected:        217
FDTD frequency-bin rows expected:  234
paired residual rows expected:     117
real packet files present:         false
real pair execution ready:         false
broad BEM replacement ready:       false
field transfer ready:              false
3D validation ready:               false
GPU work ready:                    false
field FWI ready:                   false
figure size:                       3293x931
figure dynamic range:              255
```

The eight staging phases are:

| Order | Phase | Expected output count | Executed |
| ---: | --- | ---: | --- |
| 1 | create packet directories | 8 | no |
| 2 | export projected trace files | 26 | no |
| 3 | write metadata and reference controls | 4 | no |
| 4 | compute packet checksums | 34 | no |
| 5 | extract FDTD frequency bins | 234 | no |
| 6 | build BEM/FDTD paired residual table | 117 | no |
| 7 | calibrate thresholds | 1 | no |
| 8 | run acceptance validators | 217 | no |

## Interpretation

The guarded packet contract now has a concrete staging sequence, but it remains
a handoff artifact only. The generated shell script intentionally comments out
every command so the run cannot accidentally imply that real packet files were
created.

## Decision

Use run `353` as the BEM real-pair packet staging command plan. Keep real
BEM/FDTD execution, threshold calibration, broad replacement, 3D validation,
GPU/HPC work, field transfer, and field FWI blocked until a real packet is
staged and validated.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_trace_export_packet_staging_command_plan.py
3 passed
```
