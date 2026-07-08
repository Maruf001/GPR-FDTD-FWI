# BEM Experiment 709: Matched BEM/FDTD Return-Packet Live Route Rescan Validator

Date: 2026-06-30

## Purpose

Validate run `708` from disk.

This run checks the live route shape, confirms that the external staging paths
are still empty, verifies that the producer input files remain the root
blocker, and keeps exporter/comparison/downstream states blocked.

## Output

```text
outputs/bem_experiments/709_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                         6
passed checks:                  6
failed checks:                  0
live route files:               4
live actions:                   3
live external files present:    0
live external files accepted:   0
producer inputs missing:        2
exporter returns missing:       2
comparison missing files:       4
accepted BEM baseline files:    2
accepted BEM baseline rows:     558
real BEM/FDTD comparison ready: false
new FDTD executed:              false
GPU priority:                   none
```

## Interpretation

Run `708` validates as a current live-route rescan. The external route has not
changed since the guarded synthetic packet block.

## Decision

Keep exporter execution and real BEM/FDTD comparison blocked until the two
producer input files are supplied.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_return_packet_live_route_rescan_validator.py
3 passed
```

Figure check:

```text
2357x836, dynamic range=255
```
