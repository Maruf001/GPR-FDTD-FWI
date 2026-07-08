# BEM Experiment 598: Matched FDTD Input-Bound Exporter Real Staging Producer Route Spec

Date: 2026-06-30

## Purpose

Convert the current BEM/FDTD closure plan into a producer-facing route
specification.

Runs `595-597` identify the four missing staged files. This run records the
file production order, expected row counts, value fields, and acceptance rules
needed before real BEM/FDTD comparison can proceed.

This run does not copy real FDTD files, execute the exporter, accept return
files, run real BEM/FDTD comparison, start GPU/HPC work, transfer to field
work, or run field FWI.

## Output

```text
outputs/bem_experiments/598_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_route_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_phase_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec.png
scripts/
```

## Result

```text
source closure ready:                 true
source validation ready:              true
source sensitivity ready:             true
routes:                               4
phases:                               3
external producer routes:             2
exporter return routes:               2
expected input rows:                  558
expected return rows:                 558
unique value fields:                  2
current present files:                0
current accepted files:               0
ready phases:                         0
real input packet ready:              false
exporter execution ready:             false
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                        false
field transfer ready:                 false
field FWI ready:                      false
gpu priority:                         none
```

The three phases are:

| Phase | Name | Required files | Present | Accepted |
| ---: | --- | ---: | ---: | ---: |
| 1 | external matched-FDTD producer | 2 | 0 | 0 |
| 2 | input-bound exporter return | 2 | 0 | 0 |
| 3 | comparison gate | 4 | 0 | 0 |

## Interpretation

The next real BEM/FDTD handoff is now explicit. The external producer must
supply two real input CSVs with 279 rows each: one carrying
`returned_fdtd_source_hash` values and one carrying
`returned_fdtd_scattered_norm` values. After those inputs pass receipt, the
input-bound exporter must produce two accepted return CSVs with the same row
counts and value-field rules.

## Decision

Use run `598` as the current BEM/FDTD producer route specification. Keep real
BEM/FDTD comparison blocked until the route files pass acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
