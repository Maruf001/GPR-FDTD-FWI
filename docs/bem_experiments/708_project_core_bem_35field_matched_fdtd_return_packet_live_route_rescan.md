# BEM Experiment 708: Matched BEM/FDTD Return-Packet Live Route Rescan

Date: 2026-06-30

## Purpose

Rescan the current external matched-FDTD route after the run `705` critical-path
audit.

This run reconciles three things: the accepted BEM baseline, the locked
matched-FDTD route specification, and the actual external staging directories
on disk.

This is CPU-only filesystem and readiness auditing. It does not create real
matched-FDTD files, run FDTD, execute the exporter, compare BEM with FDTD,
launch GPU/HPC work, or promote 3D or field claims.

## Output

```text
outputs/bem_experiments/708_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_route_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_action_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source critical path ready:               true
source route spec ready:                  true
source external guard ready:              true
live route files:                         4
live route actions:                       3
external parent directories present:      4
live external files present:              0
live external files accepted:             0
producer input routes:                    2
producer input files missing:             2
exporter return routes:                   2
exporter return files missing:            2
accepted BEM baseline files:              2
accepted BEM baseline rows:               558
comparison required files:                6
comparison missing files:                 4
producer inputs can start now:            true
exporter returns can start now:           false
critical path unchanged:                  true
real BEM/FDTD comparison ready:           false
new FDTD executed:                        false
GPU priority:                             none
```

## Interpretation

The current live route matches the run `705` critical path. The external
staging directories exist, but no matched-FDTD input or return files are
present. The first actionable blocker remains the two producer input CSV files.

## Decision

Continue to target the two matched-FDTD producer input files before exporter
returns or real BEM/FDTD comparison.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan.py
3 passed
```

Figure check:

```text
2572x852, dynamic range=255
```
