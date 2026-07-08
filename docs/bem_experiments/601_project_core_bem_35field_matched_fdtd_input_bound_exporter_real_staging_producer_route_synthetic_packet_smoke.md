# BEM Experiment 601: Matched FDTD Input-Bound Exporter Real Staging Producer Route Synthetic Packet Smoke

Date: 2026-06-30

## Purpose

Exercise the producer-route specification from runs `598-600` with a complete
output-local synthetic packet.

This run binds the four route rows to already accepted synthetic files: two
synthetic matched-FDTD input CSVs from run `586` and two synthetic exporter
return CSVs from run `589`. It copies those files into the run `601` output
folder, validates them against the same file acceptance rules, and confirms
that the real external staging paths remain empty.

This is not real BEM/FDTD comparison evidence.

## Output

```text
outputs/bem_experiments/601_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke
```

Key artifacts:

```text
data/synthetic_producer_route_packet/
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_packet_rows.csv
data/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke.png
scripts/
```

## Result

```text
source route ready:                true
source route validation ready:     true
source route sensitivity ready:    true
source synthetic inputs ready:     true
source synthetic returns ready:    true
packet route count:                4
synthetic input packet files:      2
synthetic return packet files:     2
expected accepted packet files:    4
actual accepted packet files:      4
unexpected packet outcomes:        0
packet required rows:              1116
packet accepted rows:              1116
packet validation errors:          0
external real files present:       0
real evidence files:               0
real route ready:                  false
real BEM/FDTD comparison ready:    false
GPU/HPC ready:                     false
field transfer ready:              false
field FWI ready:                   false
gpu priority:                      none
```

The packet contains four accepted synthetic CSVs:

| Route role | Files | Accepted rows |
| --- | ---: | ---: |
| Matched-FDTD producer input | 2 | 558 |
| Input-bound exporter return | 2 | 558 |

## Interpretation

The route spec is mechanically satisfiable when valid CSVs are supplied. The
remaining blocker is not the route format; it is the absence of the real
external matched-FDTD input files and real accepted exporter return files.

## Decision

Use run `601` as a route-level synthetic packet smoke only. Keep real BEM/FDTD
comparison, 3D validation claims, GPU/HPC work, field transfer, and field FWI
blocked until real external files pass the same route and acceptance gates.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_input_bound_exporter_real_staging_producer_route_synthetic_packet_smoke.py

3 passed
```

Figure validation:

```text
2429x847, dynamic range=255
```
