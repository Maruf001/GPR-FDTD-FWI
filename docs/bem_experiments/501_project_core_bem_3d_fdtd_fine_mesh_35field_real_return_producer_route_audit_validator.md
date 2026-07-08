# BEM Experiment 501: 35-Field Real Return Producer-Route Audit Validator

Date: 2026-06-29

## Purpose

Validate the run `500` producer-route audit.

The validator checks the route counts, exact-producer gap, producer-gap
metrics, real-only action rows, downstream blocked states, figure, and script
snapshots.

## Output

```text
outputs/bem_experiments/501_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validator
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validator_checks.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validator_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validator.png
scripts/script_snapshot_manifest.json
```

## Result

```text
validation checks:                          5
validation passes:                          5
blocking failures:                          0
validation ready:                           true
required real return files:                 4
required real entries:                      1116
route rows:                                 4
action rows:                                5
exact real producer scripts ready:          0
producer gaps:                              4
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
```

## Decision

Use run `501` as the artifact guard for the run `500` producer-route audit.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validator.py
4 passed
```

Figure check:

```text
2213x840, dynamic range=255
```
