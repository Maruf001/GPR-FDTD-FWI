# BEM Experiment 356: Real-Pair Trace Export Packet Filesystem Gap Audit

Date: 2026-06-29

## Purpose

Audit whether the current expected BEM real-pair FDTD export packet root
contains the files required by the guarded packet contract and command plan.

Runs `350-355` define, validate, and harden the file-level packet contract and
the non-executed staging command plan. This run checks the current filesystem
state against that contract.

This run does not stage files, execute FDTD, run BEM/FDTD comparison, calibrate
thresholds, launch GPU work, transfer to field evidence, run field FWI, or
start 3D/HPC work.

## Output

```text
outputs/bem_experiments/356_project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit
```

Key artifacts:

```text
data/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_packet_file_rows.csv
data/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_action_rows.csv
data/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit_summary.json
data/figure_validation.csv
figures/project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
expected packet root:                outputs/bem_experiments/real_pair_fdtd_export_packet
packet contract guarded:             true
packet items:                        34
present packet items:                0
missing packet items:                34
missing projected traces:            26
missing metadata/control items:      8
open action groups:                  4
frequency rows expected after stage: 234
residual rows expected after stage:  117
real packet files present:           false
frequency extraction ready:          false
real BEM/FDTD comparison ready:      false
threshold calibration ready:         false
GPU work ready:                      false
field transfer ready:                false
3D validation ready:                 false
figure size:                         3580x944
figure dynamic range:                255
```

The four open action groups are:

| Priority | Action group | Missing files |
| ---: | --- | ---: |
| 1 | stage projected FDTD trace files | 26 |
| 2 | stage primary metadata and references | 4 |
| 3 | derive frequency export after traces exist | 2 |
| 4 | derive pairwise residuals and thresholds | 2 |

## Interpretation

The guarded packet contract and command plan are intact, but the expected
real-pair FDTD export packet is absent from the current packet root. All
required packet files remain missing.

The result is not a failure of the BEM adapter. It confirms the current
handoff state: the BEM side is waiting for staged projected FDTD traces and
metadata before real paired comparison can start.

## Decision

Use run `356` as the filesystem gap audit for the guarded real-pair packet.
The next BEM-side action is to stage the 26 projected FDTD traces and eight
metadata/control artifacts, then rerun this audit and the packet validators.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_trace_export_packet_filesystem_gap_audit.py
3 passed
```
