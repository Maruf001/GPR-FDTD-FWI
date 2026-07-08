# BEM Experiment 743: Strict Real-Producer Staged Handoff Packet

Date: 2026-07-01

## Purpose

Convert the execution-priority map from run `742` into a staged handoff packet
for the real matched-FDTD producer.

This run does not execute FDTD, create real BEM/FDTD evidence, run 3D
validation, launch GPU/HPC work, transfer to field data, or run field FWI.

## Output

```text
outputs/bem_experiments/743_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_staged_handoff_packet
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_staged_handoff_packet_manifest_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_staged_handoff_packet_written_file_rows.csv
data/staged_real_producer_handoff/
docs/REAL_PRODUCER_STAGED_HANDOFF.md
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_staged_handoff_packet.png
scripts/script_snapshot_manifest.json
```

## Result

```text
stages:                                 5
stage-only packet files:                10
cumulative packet files:                10
total packet files:                     20
stage-only file rows:                   558
final cumulative file rows:             558
stage-only blank producer-fill fields:  2790
final receiver-frequency pairs:         279
final real-data cells:                  2232
first-stage file rows:                  2
first-stage blank producer-fill fields: 10
strict acceptance only at final stage:  true
real BEM/FDTD comparison ready:         false
GPU/HPC ready:                          false
field transfer ready:                   false
field FWI ready:                        false
```

Stage packet:

| Stage | Stage key | Stage file rows | Cumulative file rows | Real-data cells | Strict final acceptance |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | center pair smoke | 2 | 2 | 8 | false |
| 2 | center receiver frequency sweep | 16 | 18 | 64 | false |
| 3 | center frequency receiver sweep | 60 | 78 | 240 | false |
| 4 | midband receiver matrix | 240 | 318 | 960 | false |
| 5 | edgeband receiver matrix | 240 | 558 | 960 | true |

## Interpretation

The real producer no longer needs to treat the 558-row handoff as one opaque
block. The packet provides stage-only CSV files for incremental returns and
cumulative CSV files for building toward the final strict input files.

The first stage is a minimal two-row smoke return: one center
receiver-frequency row in the source-hash file and the matching row in the
scattered-norm file. This can test the real return path before asking for the
full 558 rows.

## Decision

Use stage 1 for the first real producer return check, then advance through the
cumulative files. Keep real BEM/FDTD comparison, 3D validation, GPU/HPC work,
field transfer, and field FWI blocked until the final cumulative files are
fully populated and pass strict acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_real_producer_staged_handoff_packet.py
3 passed
```

Figure check:

```text
2392x845, dynamic range=255
```
