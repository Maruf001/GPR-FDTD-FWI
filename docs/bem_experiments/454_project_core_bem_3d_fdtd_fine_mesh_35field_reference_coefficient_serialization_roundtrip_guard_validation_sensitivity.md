# BEM Experiment 454: Serialization Round-Trip Guard Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `453` validator against controlled damage to the run `452`
serialization guard.

## Output

```text
outputs/bem_experiments/454_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_validation_sensitivity_scenario_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_validation_sensitivity_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_validation_sensitivity.png
```

## Result

```text
sensitivity scenarios:                  34
expected pass scenarios:                 1
observed pass scenarios:                 1
expected failure scenarios:              33
observed failure scenarios:              33
unexpected outcomes:                     0
validation sensitivity ready:            true
validator accepts exact run 452:         true
validator rejects damaged variants:      true
real BEM/FDTD comparison ready:          false
3D validation ready:                     false
GPU/HPC ready:                           false
field FWI ready:                         false
```

The damaged variants cover readiness drift, count drift, reference/tolerance
drift, 13-versus-12 digit threshold drift, preferred-format drift, downstream
promotion, figure drift, and missing script snapshots. The exact run `452`
passes and all damaged variants fail as expected.

## Decision

Use runs `452-454` as the guarded BEM serialization round-trip block for the
future 35-field real-return scorecard path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_validation_sensitivity.py
3 passed
```

Figure check:

```text
3599x888, dynamic range=255
```
