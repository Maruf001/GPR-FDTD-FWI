# BEM Experiment 502: 35-Field Real Return Producer-Route Audit Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `501` validator against controlled damage to the run `500`
producer-route audit.

## Output

```text
outputs/bem_experiments/502_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validation_sensitivity.png
scripts/script_snapshot_manifest.json
```

## Result

```text
sensitivity scenarios:                      31
expected pass scenarios:                    1
observed pass scenarios:                    1
expected failure scenarios:                 30
observed failure scenarios:                 30
unexpected outcomes:                        0
validation sensitivity ready:               true
validator accepts exact run 500:            true
validator rejects damaged variants:         true
real return production ready:               false
real BEM/FDTD comparison ready:             false
3D validation ready:                        false
GPU/HPC ready:                              false
field FWI ready:                            false
```

The damaged variants cover count drift, route-row drift, exact-producer
promotion, producer-gap metric drift, real-file promotion, action-row drift,
template/synthetic completion leakage, downstream promotion, figure damage,
and script-snapshot damage.

## Decision

Use runs `500-502` as the guarded BEM producer-route audit block.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_real_return_producer_route_audit_validation_sensitivity.py
3 passed
```

Figure check:

```text
3797x918, dynamic range=255
```
