# Field 3D 0701 Near-Object Radius Scan Checkpoint

Date: 2026-07-04

## What Changed

- Updated `run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py` so source polarization can be supplied by config.
- Updated `run_field_3d_0701_fastgpr_radius_sensitivity_scan.py` with fine-grid and bridge-geometry controls:
  - `--dx-m`
  - `--fast-dt-ns`
  - `--source-y-m`
  - `--receiver-y-m`
  - `--source-polarization`
- Ran a diagnostic fixed-radius scan using the radius-sensitive near-object bridge found in the grid search.

## Key Numbers

- Artifact:
  - `075_field_3d_0701_fastgpr_radius_sensitivity_scan_near_object_y145_dx01`
- Bridge:
  - source y `1.45 m`
  - receiver y `1.45 m`
  - source polarization `z`
  - `dx_m = 0.01`
  - `fast_dt_ns = 0.02`
- Diameters scanned:
  - `8, 12, 16, 20, 24, 30 mm`
- Best diameter:
  - `30.0 mm`
- Near-best range:
  - `8.0-30.0 mm`
- Status:
  - `weakly_identified_wide_near_best_range`
- Losses:
  - 8 mm: `0.779142`
  - 12 mm: `0.779065`
  - 16 mm: `0.778979`
  - 20 mm: `0.778884`
  - 24 mm: `0.778779`
  - 30 mm: `0.778603`
  - spread `5.390644e-04`
- Best material/time:
  - epsr `3.969004`
  - source shift `2.231041 ns`

## What Remains Blocked

- This is a diagnostic bridge, not the field-product bridge.
- Even with forward radius contrast, the fixed-radius field objective only weakly ranks diameter and keeps the full `8-30 mm` near-best range.
- The field-product diameter remains non-unique.

## Current Decision

Forward contrast is necessary but not sufficient. It can produce a weak monotonic diameter ranking in a sensitive bridge, but product-grade diameter prediction still requires a geometry/objective that creates stronger radius separation on real field data.

## Next Defensible Task

Design a surface-style radius-sensitive bridge rather than using the near-object diagnostic geometry:

- extend time window enough for surface-to-depth scattering,
- test source/receiver offsets near plausible GPR acquisition geometry,
- use forward contrast as the gate before fixed-radius optimization.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_radius_sensitivity_scan.py run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_radius_sensitivity_scan.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_radius_bridge_geometry_grid_search.py -q`
  - `12 passed`
- Touched-file `git diff --check` passed.
- Figure inspected:
  - `075.../figures/field_3d_0701_fastgpr_radius_sensitivity_scan.png`

## Artifact Paths

- Near-object radius scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/075_field_3d_0701_fastgpr_radius_sensitivity_scan_near_object_y145_dx01`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
