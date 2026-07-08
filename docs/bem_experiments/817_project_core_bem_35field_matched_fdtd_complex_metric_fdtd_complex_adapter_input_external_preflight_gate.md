# BEM Experiment 817: Complex FDTD External Input Preflight Gate

Date: 2026-07-01

## Purpose

Define the preflight gate for a real complex FDTD input CSV.

Runs `814-816` guarded the external handoff boundary. This run defines the
checks that a real filled external input file must pass before completed BEM
stage files or a real BEM/FDTD comparison can be promoted.

## Output

```text
outputs/bem_experiments/817_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate
```

## Result

```text
source claim boundary ready:             true
source validation ready:                 true
source sensitivity ready:                true
preflight items:                         1
expected rows:                           279
external input file present:             false
external input rows:                     0
external input accepted:                 false
finite FDTD value cells:                 0
provenance/status cells:                 0
completed stage files ready:             false
real BEM/FDTD comparison ready:          false
field transfer ready:                    false
3D/HPC ready:                            false
gpu priority:                            none
```

Required acceptance checks for a future real CSV:

| Requirement | Expected |
| --- | ---: |
| matching receiver-frequency rows | 279 |
| finite real/imaginary FDTD value cells | 558 |
| provenance/status cells | 1395 |
| completed solver statuses | 279 |
| valid solver log hashes | 279 |
| real FDTD export flags | 279 |

## Interpretation

The preflight gate is now explicit. The expected external input file is absent,
so the gate correctly accepts zero rows and promotes no comparison state.

## Decision

Accept a real complex FDTD return only if it has 279 matching identities, 558
finite real/imaginary value cells, 1395 provenance/status cells, completed
solver statuses, valid solver log hashes, and the canonical input contract
hash.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_preflight_gate.py

3 passed
```

Figure check:

```text
2897x881, dynamic range=255
```
