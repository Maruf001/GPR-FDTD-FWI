# BEM Experiment 727: Producer Input Strict-Mode Live-Route Rescan Validator

Date: 2026-07-01

## Purpose

Validate the saved run `726` strict-mode live-route rescan.

The validator checks that both producer route parents exist, both live files
are absent, no strict acceptance has occurred, no closure action is complete,
and all downstream BEM/FDTD work remains blocked.

This is CPU-only artifact validation. It does not run FDTD, execute the
exporter on live files, create real evidence, run a real BEM/FDTD comparison,
launch GPU/HPC work, transfer to field evidence, or promote 3D validation
claims.

## Output

```text
outputs/bem_experiments/727_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
checks:                               7
checks passed:                        7
checks failed:                        0
producer input route files:           2
live input files present:             0
strict accepted files:                0
completed actions:                    0
exporter execution ready:         false
real BEM/FDTD comparison ready:    false
```

## Interpretation

The strict-mode live-route rescan is valid. The live producer input paths are
still empty.

## Decision

Keep exporter execution and BEM/FDTD comparison blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_producer_input_strict_mode_live_route_rescan_validator.py
2 passed
```

Figure check:

```text
2393x859, dynamic range=255
```
