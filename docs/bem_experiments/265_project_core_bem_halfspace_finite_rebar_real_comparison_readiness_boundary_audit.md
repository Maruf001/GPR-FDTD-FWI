# BEM Experiment 265: Half-Space Finite-Rebar Real Comparison Readiness Boundary Audit

Date: 2026-06-28

## Purpose

Audit what is ready and what remains missing before a real BEM/FDTD comparison
can be claimed.

This run joins the guarded comparison contract, the BEM exporter, the synthetic
trace-intake mechanics, the synthetic trace-frequency extraction mechanics, and
the synthetic negative-control boundary into one readiness table.

It does not run real FDTD, ingest real trace files, claim BEM/FDTD agreement,
launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/265_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_rows.csv
data/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_COMPARISON_READINESS_BOUNDARY_AUDIT.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit.py
```

## Result

```text
boundary items:                    10
ready support items:               5
blocking items:                    4
readiness boundary ready:          true
real trace files present:          false
real FDTD extraction ready:        false
real BEM/FDTD comparison ready:    false
ready for GPU work:                false
field FWI ready:                   false
```

The current support items are:

| Item | Status |
| --- | --- |
| comparison contract | ready |
| BEM schema exporter | ready |
| synthetic trace intake mechanics | ready synthetic-only |
| synthetic trace frequency extraction mechanics | ready synthetic-only |
| synthetic negative-control boundary | ready boundary |

The blockers are:

| Blocker | Needed next |
| --- | --- |
| real trace files | provide matched real FDTD background and target traces for the 13 receiver positions |
| real FDTD frequency extraction | extract finite complex frequency bins from real traces on the nine-frequency grid |
| real BEM/FDTD pairwise comparison | pair real FDTD bins with BEM exporter rows and compute residuals |
| threshold calibration | calibrate normalized L2, peak-error, and phase gates after the first real pair |

## Interpretation

The BEM side and the synthetic plumbing are guarded, but they do not constitute
real agreement. The blockers are concrete: real FDTD trace files, real
frequency extraction, a real paired comparison, and threshold calibration after
the first real pair.

## Decision

Use run `265` as the current real-comparison boundary. Do not claim BEM/FDTD
agreement, 3D validation, inversion scale, field transfer, GPU/HPC readiness,
or field FWI until real paired files pass this path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit.py
4 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_comparison_readiness_boundary_audit.png
2680x836, dynamic range=255
```
