# BEM Experiment 256: Half-Space Finite-Rebar Real FDTD Trace Intake Populated-Root Synthetic Smoke

Date: 2026-06-28

## Purpose

Stage synthetic trace files into the real-FDTD trace intake layout and check
that the manifest accepts a correctly populated trace root.

This run is the positive counterpart to the fail-closed empty-root package in
runs `253-255`. It answers a narrow mechanics question:

```text
If every required trace file is present and follows the contract, do all
manifest checks pass without promoting the files as real FDTD evidence?
```

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/256_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke_trace_inventory.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke_checks.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_POPULATED_ROOT_SYNTHETIC_SMOKE.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke.py
```

## Result

```text
synthetic trace files:                     26
samples per trace file:                    16
total synthetic samples:                   416
populated-root checks:                     182
populated-root passes:                     182
populated-root failures:                   0
check groups:                              7
synthetic populated-root acceptance ready: true
real trace files present:                  false
real FDTD frequency extraction ready:      false
real BEM/FDTD comparison ready:            false
ready for 3D validation:                   false
inversion-scale half-space ready:          false
field transfer ready:                      false
ready for GPU work:                        false
field FWI ready:                           false
```

The seven check groups all pass for every synthetic trace:

| Check group | Passing checks |
| --- | ---: |
| file_present | 26 |
| schema_columns | 26 |
| receiver_key_match | 26 |
| constant_dt | 26 |
| reference_fields | 26 |
| projection_metadata | 26 |
| sha256_checksum | 26 |

## Interpretation

The real-FDTD trace intake contract can accept a correctly populated synthetic
trace root. The run stages 26 projected trace files, evaluates all 182 manifest
checks, and passes every check without executing shell commands.

The staged files are synthetic acceptance fixtures, not real FDTD output.
Therefore the run does not promote real trace intake, real frequency
extraction, real BEM/FDTD comparison, 3D validation, inversion, field transfer,
GPU/HPC readiness, or field FWI.

## Decision

Use run `256` as the positive populated-root smoke for trace-intake mechanics.
The next guarded step is a validator and sensitivity test for this synthetic
acceptance path before any real FDTD trace staging is treated as ready.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_populated_root_synthetic_smoke.png
2572x844, dynamic range=255
```
