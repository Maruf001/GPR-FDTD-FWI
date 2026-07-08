# BEM Experiment 726: Producer Input Strict-Mode Live-Route Rescan

Date: 2026-07-01

## Purpose

Rescan the live matched-FDTD producer input routes using the strict
contract-hash acceptance path created in runs `723-725`.

This run checks the current external producer-input paths. It does not write to
those paths and does not create live producer files.

This is CPU-only filesystem and acceptance-readiness auditing. It does not run
FDTD, execute the exporter on live files, create real evidence, run a real
BEM/FDTD comparison, launch GPU/HPC work, transfer to field evidence, or
promote 3D validation claims.

## Output

```text
outputs/bem_experiments/726_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_route_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_action_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan.png
scripts/script_snapshot_manifest.json
```

## Result

```text
strict mode available:              true
producer input route files:            2
route parents present:                 2
live input files present:              0
live input files nonempty:             0
required strict-mode rows:           558
current live rows:                     0
strict accepted files:                 0
strict accepted rows:                  0
completed actions:                     0
exporter execution ready:          false
real BEM/FDTD comparison ready:     false
GPU/HPC ready:                     false
```

## Interpretation

The acceptance logic is now strict enough, but the required live producer files
are still absent. The next live requirement is unchanged: provide both matched
FDTD producer input CSV files with exact contract hashes and real solver values.

## Decision

Do not run the input-bound exporter or BEM/FDTD comparison until both live
producer input files exist and pass strict acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan.py
3 passed
```

Figure check:

```text
2464x868, dynamic range=255
```
