# BEM Experiment 238: Half-Space Finite-Rebar BEM Schema Exporter

Date: 2026-06-28

## Purpose

Export the run `231` scalar BEM fields into the BEM-side schema defined by the
guarded comparison contract from runs `235`-`237`.

The previous contract package defined how a future BEM/FDTD comparison should
be structured. This run implements the BEM-side export only: background,
scattered, and total complex scalar frequency fields are written into the
required schema.

This is a CPU-only exporter. It does not run FDTD, extract FDTD frequency bins,
compare real paired files, implement full 3D Maxwell BEM, run inversion, launch
GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/238_project_core_bem_halfspace_finite_rebar_bem_schema_exporter
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_bem_frequency_output.csv
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_checks.csv
data/project_core_bem_halfspace_finite_rebar_bem_schema_exporter_summary.json
figures/project_core_bem_halfspace_finite_rebar_bem_schema_exporter.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_BEM_SCHEMA_EXPORTER.md
scripts/script_snapshot_manifest.json
```

## Result

```text
schema columns:                    10
model roles:                       3
receiver samples:                  13
internal target points:            31
frequencies:                       9
export rows:                       351
expected export rows:              351
schema checks/pass:                4 / 4
max residual:                      1.4210854715202004e-14
scattered norm relative error:     0.0
BEM schema exporter ready:         true
FDTD frequency extraction ready:   false
real BEM/FDTD comparison ready:    false
3D validation ready:               false
field transfer ready:              false
GPU ready:                         false
field FWI ready:                   false
```

The four exporter checks confirm:

| Check | Outcome |
| --- | --- |
| Column order matches the run `235` BEM schema | Pass |
| Background, scattered, and total roles have complete row counts | Pass |
| Real and imaginary field components are finite | Pass |
| Geometry, observable, and normalization labels are locked | Pass |

## Interpretation

The BEM side of the scalar comparison contract now has a concrete exporter. It
writes background, scattered, and total complex fields with the required schema
columns, finite values, locked geometry/observable/normalization fields, and row
counts matching 13 receiver samples by 9 frequencies by 3 roles.

This does not create a real comparison. The FDTD-side extraction and paired-file
comparison are still missing.

## Decision

Use run `238` as the BEM-side exporter for the guarded scalar comparison
contract. The next BEM task can validate and stress-test this exporter. FDTD
frequency extraction, real BEM/FDTD comparison, 3D validation, inversion, field
transfer, GPU/HPC readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_bem_schema_exporter.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_bem_schema_exporter.py: pass
```

Figure check:

```text
2789x833, dynamic range=255
```
