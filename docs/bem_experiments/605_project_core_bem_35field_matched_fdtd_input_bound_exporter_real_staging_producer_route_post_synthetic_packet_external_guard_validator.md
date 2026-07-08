# BEM Experiment 605: Matched FDTD Input-Bound Exporter Real Staging Producer Route Post-Synthetic Packet External Guard Validator

Date: 2026-06-30

## Purpose

Validate run `604` from saved artifacts.

This run checks that the post-synthetic-packet external guard has the expected
four rows, that the locked external staging paths remain empty, and that the
synthetic packet remains output-local and non-evidence.

## Output

```text
outputs/bem_experiments/605_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validator
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validator_check_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validator_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validator.png
scripts/
```

## Result

```text
checks:                         5
passed checks:                  5
failed checks:                  0
external paths:                 4
external files present:         0
external files accepted:        0
packet files present:           4
packet/external path overlap:   0
packet under external root:     0
packet files accepted:          4
packet real evidence files:     0
real BEM/FDTD comparison ready: false
GPU/HPC ready:                  false
field transfer ready:           false
field FWI ready:                false
gpu priority:                   none
```

The five checks cover source readiness, external guard row shape, empty
external paths, output-local non-evidence packet state, blocked downstream
states, and figure/script artifacts.

## Interpretation

Run `604` is a valid post-synthetic-packet external guard. It confirms the
synthetic packet did not populate or overlap the locked external staging paths.

## Decision

Use run `605` as the artifact guard for run `604`. Keep real BEM/FDTD
comparison blocked until real external files are supplied and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_validator.py

3 passed
```

Figure validation:

```text
2285x841, dynamic range=255
```
