# BEM Experiment 602: Matched FDTD Input-Bound Exporter Real Staging Producer Route Synthetic Packet Smoke Validator

Date: 2026-06-30

## Purpose

Validate run `601` from saved artifacts.

This run checks that the route-level synthetic packet has the expected four
files, that all four files pass acceptance with the expected row count, and
that no real external route file or BEM/FDTD comparison evidence has been
created.

## Output

```text
outputs/bem_experiments/602_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
packet route count:             4
synthetic input packet files:   2
synthetic return packet files:  2
accepted packet files:          4
accepted packet rows:           1116
external real files present:    0
real evidence files:            0
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The five checks cover source readiness, route shape, packet acceptance and row
counts, real-route/downstream blocking, and figure/script artifacts.

## Interpretation

Run `601` is a valid route-level synthetic packet smoke. It proves the route
can be populated with accepted CSVs, while run `602` confirms that this did not
promote any real external files or comparison evidence.

## Decision

Use run `602` as the artifact guard for run `601`. Keep real BEM/FDTD
comparison blocked until real external matched-FDTD files pass acceptance.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
