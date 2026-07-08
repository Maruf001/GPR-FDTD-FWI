# BEM Experiment 284: Half-Space Finite-Rebar Threshold Calibration Post-Execution Boundary

Date: 2026-06-28

## Purpose

Combine the guarded first-real-pair command checklist and guarded current-guard
execution smoke into one current BEM threshold-calibration boundary.

This run does not execute future real-pair commands, ingest real FDTD traces,
run a real BEM/FDTD comparison, set thresholds, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/284_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_POST_EXECUTION_BOUNDARY.md
scripts/run_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary.py
scripts/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary.py
scripts/script_snapshot_manifest.json
```

## Result

```text
boundary items:                     7
support ready items:                2
blockers:                           5
real-data blockers:                 5
command plan guarded:               true
current guard execution guarded:    true
post-execution boundary ready:      true
future real-pair commands executed: false
real trace files present:           false
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
3D validation ready:                false
inversion-scale half-space ready:   false
field transfer ready:               false
GPU work ready:                     false
field FWI ready:                    false
```

The command checklist and current guard execution are now guarded, but real
paired BEM/FDTD data are still required before calibration or downstream claims.

## Decision

Use run `284` as the current BEM threshold-calibration post-execution boundary.
Do not execute future real-pair commands or set thresholds until real paired
data are staged.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_post_execution_boundary.py
3 passed
```

Figure validation:

```text
2789x847, dynamic range=255
```
