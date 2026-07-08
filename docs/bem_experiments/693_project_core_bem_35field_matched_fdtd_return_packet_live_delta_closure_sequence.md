# BEM Experiment 693: Matched BEM/FDTD Return-Packet Live Delta Closure Sequence

Date: 2026-06-30

## Purpose

Convert the run `690` live-delta monitor into an ordered closure sequence for
the 35-field BEM/FDTD comparison packet.

The BEM half is already accepted. The missing work is the matched-FDTD half:
two real producer input CSV files and two accepted exporter return CSV files.

This is CPU-only file and readiness auditing. It does not rerun Bempp, run
FDTD, create matched-FDTD files, compare BEM with FDTD, launch GPU/HPC work, or
promote field transfer.

## Output

```text
outputs/bem_experiments/693_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_file_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source monitor ready:                      true
sequence files:                            6
sequence actions:                          4
accepted BEM baseline files:               2
matched-FDTD input files required:         2
matched-FDTD return files required:        2
present files:                             2
accepted files:                            2
missing files:                             4
BEM accepted files:                        2
matched-FDTD files present:                0
matched-FDTD files accepted:               0
matched-FDTD files missing:                4
accepted BEM rows:                         558
expected matched-FDTD input rows:          558
expected matched-FDTD return rows:         558
complete closure actions:                  0
real BEM/FDTD comparison ready:            false
exporter execution ready:                  false
3D validation claim ready:                 false
field transfer ready:                      false
field FWI ready:                           false
GPU priority:                              none
```

The four sequence actions are:

| Order | Action | Required files | Present | Accepted | Missing |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | accepted BEM baseline | 2 | 2 | 2 | 0 |
| 2 | matched-FDTD producer inputs | 2 | 0 | 0 | 2 |
| 3 | input-bound exporter returns | 2 | 0 | 0 | 2 |
| 4 | final comparison gate | 6 | 2 | 2 | 4 |

## Interpretation

The accepted BEM files are now a baseline, not an open task. The comparison
still needs four matched-FDTD files before any real BEM/FDTD comparison can be
claimed.

## Decision

Use run `693` as the BEM/FDTD comparison closure checklist. Keep comparison,
3D validation claims, GPU/HPC work, field transfer, and field FWI blocked until
the four matched-FDTD files are accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence.py
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_delta_closure_sequence_validator.py

7 passed
```

Figure check:

```text
2536x849, dynamic range=255
```
