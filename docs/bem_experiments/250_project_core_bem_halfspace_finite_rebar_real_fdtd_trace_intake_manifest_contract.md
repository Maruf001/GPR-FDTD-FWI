# BEM Experiment 250: Half-Space Finite-Rebar Real FDTD Trace Intake Manifest Contract

Date: 2026-06-28

## Purpose

Convert the FDTD time-trace input schema into a concrete real-trace intake
manifest for future scalar BEM/FDTD comparison.

This run connects two earlier guarded pieces:

```text
run 241: FDTD-side time-trace input contract
run 249: guarded synthetic BEM/FDTD pairwise comparison package
```

It does not run real FDTD, ingest real trace files, extract real frequency
bins, compare real paired FDTD files, implement full 3D Maxwell BEM, launch
GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/250_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_rows.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_check_rows.csv
data/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract_summary.json
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_REAL_FDTD_TRACE_INTAKE_MANIFEST_CONTRACT.md
scripts/run_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract.py
scripts/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract.py
```

## Result

```text
source input contract ready:                true
source synthetic pairwise guard ready:      true
time-trace schema columns:                  13
receiver keys:                              13
frequency keys:                             9
trace roles:                                2
required trace files:                       26
background trace files:                     13
target trace files:                         13
planned check groups:                       7
planned checks:                             182
real FDTD trace intake manifest ready:      true
ready for real trace generation:            true
real trace files present:                   false
real scalar projection convention ready:    false
real time-zero reference ready:             false
real amplitude reference ready:             false
real FDTD frequency extraction ready:       false
real BEM/FDTD comparison ready:             false
ready for 3D validation:                    false
inversion-scale half-space ready:           false
field transfer ready:                       false
ready for GPU work:                         false
field FWI ready:                            false
```

The manifest requires two projected scalar trace files for each receiver:

| Trace role | Required files |
| --- | ---: |
| `fdtd_background` | 13 |
| `fdtd_target` | 13 |

Each required trace file has seven planned checks:

```text
file_present
schema_columns
receiver_key_match
constant_dt
reference_fields
projection_metadata
sha256_checksum
```

## Interpretation

The real-FDTD side now has a concrete intake target. Future FDTD output must
produce 26 projected scalar trace files: target and background traces at each
of the 13 receiver positions. Each trace must match the 13-column schema,
receiver key, constant time-step requirement, time-zero reference, amplitude
reference, scalar projection metadata, and checksum expectation.

This is still a contract. It does not create or accept real trace files.

## Decision

Use run `250` as the real FDTD trace intake contract for future scalar
BEM/FDTD comparison. Real trace files, real projection convention, real
time-zero/amplitude references, real frequency extraction, real BEM/FDTD
comparison, 3D validation, inversion-scale use, field transfer, GPU/HPC
readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract.py
5 passed
```

Figure validation:

```text
figures/project_core_bem_halfspace_finite_rebar_real_fdtd_trace_intake_manifest_contract.png
2644x847, dynamic range=255
```
