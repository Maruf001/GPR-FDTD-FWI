# BEM Experiment 599: Matched FDTD Input-Bound Exporter Real Staging Producer Route Spec Validator

Date: 2026-06-30

## Purpose

Validate the producer route specification from run `598`.

Run `598` records the real BEM/FDTD staging route: two external matched-FDTD
input files, two input-bound exporter return files, and comparison-gate reruns.
This run verifies route shape, row counts, value fields, current absence state,
downstream blocking, and artifacts.

## Output

```text
outputs/bem_experiments/599_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validator.png
scripts/
```

## Result

```text
checks:                       5
passed checks:                5
failed checks:                0
routes:                       4
phases:                       3
external producer routes:     2
exporter return routes:       2
expected input rows:          558
expected return rows:         558
current present files:        0
current accepted files:       0
real BEM/FDTD comparison ready: false
GPU/HPC ready:                false
field transfer ready:         false
field FWI ready:              false
gpu priority:                 none
```

## Interpretation

The producer route spec is valid and remains a route contract, not real
BEM/FDTD comparison evidence.

## Decision

Use run `599` as the validator for run `598`. Keep real BEM/FDTD comparison
blocked until the full route passes acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_spec_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
