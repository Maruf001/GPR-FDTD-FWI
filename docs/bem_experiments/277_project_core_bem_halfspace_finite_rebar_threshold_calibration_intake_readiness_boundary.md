# BEM Experiment 277: Half-Space Finite-Rebar Threshold Calibration Intake Readiness Boundary

Date: 2026-06-28

## Purpose

Combine the guarded empty threshold template and guarded synthetic fill smoke
into one threshold-calibration intake readiness boundary. The goal is to state
what is now mechanically ready and what still requires real paired BEM/FDTD
data.

This run does not ingest real FDTD traces, set real thresholds, claim BEM/FDTD
agreement, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/277_project_core_bem_halfspace_finite_rebar_threshold_calibration_intake_readiness_boundary
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_intake_readiness_boundary_rows.csv
data/project_core_bem_halfspace_finite_rebar_threshold_calibration_intake_readiness_boundary_summary.json
figures/project_core_bem_halfspace_finite_rebar_threshold_calibration_intake_readiness_boundary.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_THRESHOLD_CALIBRATION_INTAKE_READINESS_BOUNDARY.md
```

## Result

```text
boundary items:                    7
support ready items:               2
blockers:                          5
real-data blockers:                5
template pack guarded:             true
synthetic fill smoke guarded:      true
intake boundary ready:             true
threshold calibration ready:       false
real trace files present:          false
real FDTD extraction ready:        false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
inversion-scale ready:             false
field transfer ready:              false
GPU work ready:                    false
field FWI ready:                   false
```

The two ready support items are the guarded blank threshold template and the
guarded synthetic fill positive control. The five blockers are real FDTD trace
files, real FDTD frequency extraction, real paired BEM/FDTD comparison, real
threshold calibration, and all downstream 3D/inversion/field/GPU/FWI claims.

## Interpretation

BEM threshold-calibration intake mechanics are ready, but threshold calibration
itself is not. The current project can accept and check the structure of a
future filled threshold-calibration package, but it cannot set thresholds from
synthetic positive controls.

Real paired BEM/FDTD data remain required before threshold calibration,
BEM/FDTD agreement, 3D validation, inversion-scale use, field transfer, GPU/HPC
work, or field FWI can be claimed.

## Decision

Use run `277` as the current threshold-calibration intake boundary. Do not set
thresholds or promote BEM/FDTD agreement until real paired data pass the
guarded intake path.

## Validation

Focused test:

```text
tests/test_project_core_bem_halfspace_finite_rebar_threshold_calibration_intake_readiness_boundary.py
3 passed
```

Figure validation:

```text
2789x847, dynamic range=255
```
