# BEM Experiment 690: Matched BEM/FDTD Return-Packet Live Delta Monitor

Date: 2026-06-30

## Purpose

Create the current readiness view for the 35-field BEM/FDTD comparison packet.

The BEM-side return files from run `557` are accepted and validated, while the
matched-FDTD route from runs `598-606` still has no real external files. This
run combines those two facts into one monitor so the comparison state is
unambiguous: what is already accepted, what is still missing, and which
downstream claims remain blocked.

This is CPU-only file and metadata auditing. It does not rerun Bempp, run FDTD,
write matched-FDTD files, compare BEM with FDTD, launch GPU/HPC work, or
promote field transfer.

## Output

```text
outputs/bem_experiments/690_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_component_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_phase_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source BEM acceptance ready:               true
source route ready:                        true
source external guard ready:               true
comparison component files:                6
BEM component files:                       2
matched-FDTD component files:              4
BEM accepted files:                        2
BEM accepted rows:                         558
matched-FDTD input files required:         2
matched-FDTD return files required:        2
matched-FDTD files present:                0
matched-FDTD files accepted:               0
matched-FDTD files missing:                4
expected matched-FDTD input rows:          558
expected matched-FDTD return rows:         558
ready phases:                              1 / 4
comparison files present:                  2 / 6
comparison files accepted:                 2 / 6
real BEM/FDTD comparison ready:            false
exporter execution ready:                  false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

## Interpretation

The 35-field comparison has a real accepted BEM half: two files and 558 rows.
The matched-FDTD half has not arrived: two real input CSV files and two
accepted return CSV files are still missing.

This closes an ambiguity from the earlier route and guard runs. The comparison
is not blocked by BEM file format or BEM return-file acceptance anymore. It is
blocked by the four matched-FDTD files.

## Decision

Use run `690` as the current BEM/FDTD return-packet live monitor. Keep real
BEM/FDTD comparison, 3D validation claims, GPU/HPC work, field transfer, and
field FWI blocked until the four matched-FDTD files are supplied and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_monitor_validator.py

7 passed
```

Figure check:

```text
2572x851, dynamic range=255
```
