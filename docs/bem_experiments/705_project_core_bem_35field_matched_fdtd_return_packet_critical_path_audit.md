# BEM Experiment 705: Matched BEM/FDTD Return-Packet Critical-Path Audit

Date: 2026-06-30

## Purpose

Turn the run `693` closure sequence into a dependency-level critical path for
the 35-field BEM/FDTD comparison packet.

The key question is no longer whether the BEM side exists. It does. The key
question is which matched-FDTD files must appear first before exporter returns
and a real comparison can be attempted.

This is CPU-only file and readiness auditing. It does not run FDTD, create
matched-FDTD files, rerun Bempp, execute an exporter, compare BEM with FDTD,
launch GPU/HPC work, or promote 3D or field claims.

## Output

```text
outputs/bem_experiments/705_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_file_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source closure sequence ready:             true
dependency files:                          6
critical-path actions:                     4
dependency levels:                         4
accepted BEM baseline files:               2
accepted BEM baseline rows:                558
root matched-FDTD input files:             2
root matched-FDTD input files present:     0
root matched-FDTD input files missing:     2
exporter return files:                     2
exporter return files present:             0
exporter return files missing:             2
final comparison required files:           6
final comparison missing files:            4
complete actions:                          1
blocked actions:                           3
matched-FDTD producer inputs can start:    true
matched-FDTD exporter ready:               false
real BEM/FDTD comparison ready:            false
new FDTD executed:                         false
GPU priority:                              none
```

The four critical-path actions are:

| Level | Action | Required files | Present | Missing | Complete now |
| ---: | --- | ---: | ---: | ---: | --- |
| 1 | accepted BEM baseline | 2 | 2 | 0 | true |
| 2 | matched-FDTD producer inputs | 2 | 0 | 2 | false |
| 3 | input-bound exporter returns | 2 | 0 | 2 | false |
| 4 | final comparison gate | 6 | 2 | 4 | false |

## Interpretation

The root bridge blocker is the two missing matched-FDTD producer input CSV
files. The exporter return files depend on those producer inputs, and the final
comparison gate depends on all six required files.

## Decision

Target the next BEM/FDTD bridge work at the two producer input files. Keep
exporter execution, real BEM/FDTD comparison, 3D validation claims, GPU/HPC
work, field transfer, and field FWI blocked until those inputs exist and are
accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_critical_path_audit.py
3 passed
```

Figure check:

```text
2572x852, dynamic range=255
```
