# BEM Experiment 604: Matched FDTD Input-Bound Exporter Real Staging Producer Route Post-Synthetic Packet External Guard

Date: 2026-06-30

## Purpose

Audit the locked external BEM/FDTD staging paths after the route-level
synthetic packet block `601-603`.

The synthetic packet intentionally wrote four accepted CSVs inside run `601`.
This run checks that those packet files stayed output-local and did not
populate or overlap the locked real external staging paths.

## Output

```text
outputs/bem_experiments/604_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_guard_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard.png
scripts/
```

## Result

```text
source packet ready:              true
source validation ready:          true
source sensitivity ready:         true
external paths:                   4
external parent directories:      4
external files present:           0
external files nonempty:          0
external files accepted:          0
packet files present:             4
packet/external path overlap:     0
packet files under external root: 0
packet files accepted:            4
packet real evidence files:       0
real BEM/FDTD comparison ready:   false
GPU/HPC ready:                    false
field transfer ready:             false
field FWI ready:                  false
gpu priority:                     none
```

## Interpretation

The route-level synthetic packet stayed confined to the run `601` output
directory. The four locked real external staging paths remain empty.

## Decision

Use run `604` as the post-synthetic-packet external guard. Keep real BEM/FDTD
comparison, 3D validation claims, GPU/HPC work, field transfer, and field FWI
blocked until actual external files are supplied and accepted.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_post_synthetic_packet_external_guard.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
