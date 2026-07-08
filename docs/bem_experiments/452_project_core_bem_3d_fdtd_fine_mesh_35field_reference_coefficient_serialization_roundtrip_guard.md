# BEM Experiment 452: Reference-Coefficient Serialization Round-Trip Guard

Date: 2026-06-29

## Purpose

Turn the run `446` precision-budget result into a concrete storage/readback
rule for future real-return scorecards.

Run `446` showed that the normalized-comparator reference coefficient needs at
least 13 significant digits to satisfy the `1e-12` relative residual tolerance.
This run checks common JSON, CSV, and text round trips so that later scorecards
do not silently lose that precision.

## Output

```text
outputs/bem_experiments/452_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_serialization_rows.csv
data/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard_summary.json
figures/project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard.png
```

## Result

```text
source precision budget ready:          true
serialization round-trip ready:         true
reference coefficient:                  0.01907878402833891
relative tolerance:                     1e-12
serialization scenarios:                12
passing serialization scenarios:        9
failing serialization scenarios:        3
safe scorecard scenarios:               9
preferred scorecard scenarios:          4
preferred scenarios passing:            4
minimum passing significant digits:     13
maximum failing significant digits:     12
minimum safe scorecard digits:          13
recommended storage digits:             17
JSON 13 digits pass:                    true
CSV 13 digits pass:                     true
JSON 12 digits fail:                    true
CSV 12 digits fail:                     true
real BEM/FDTD comparison ready:         false
3D validation ready:                    false
GPU/HPC ready:                          false
field FWI ready:                        false
```

JSON and CSV text with 13 significant digits pass the existing comparator
tolerance. JSON and CSV text with 12 significant digits fail. Full Python/JSON
numeric representation and 17-significant-digit text are the preferred future
scorecard storage formats.

## Decision

Use full Python/JSON numeric representation or 17-significant-digit text for
production scorecards. Treat 13 significant digits as the minimum
tolerance-preserving floor. This is a storage guard, not real BEM/FDTD
comparison evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_fine_mesh_35field_reference_coefficient_serialization_roundtrip_guard.py
3 passed
```

Figure check:

```text
3435x888, dynamic range=255
```
