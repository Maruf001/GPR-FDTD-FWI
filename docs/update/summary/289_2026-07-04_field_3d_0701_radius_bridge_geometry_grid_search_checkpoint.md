# Field 3D 0701 Radius Bridge Geometry Grid Search Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_radius_bridge_geometry_grid_search.py`.
- Added focused tests in `tests/test_field_3d_0701_radius_bridge_geometry_grid_search.py`.
- Ran a forward-contrast geometry grid over:
  - source/receiver y pairs `0.05:0.05`, `0.05:0.20`, `0.50:1.20`, `1.00:1.20`, `1.20:1.20`, `1.45:1.45`
  - source polarizations `z`, `x`, `y`
  - fixed diameters `8 mm` and `30 mm`
  - `dx_m = 0.01`, `fast_dt_ns = 0.02`

## Key Numbers

- Grid-search artifact:
  - `074_field_3d_0701_radius_bridge_geometry_grid_search`
- Candidate count:
  - `18`
- Sensitive candidate count at threshold `1e-4`:
  - `1`
- Best candidate:
  - source y `1.45 m`
  - receiver y `1.45 m`
  - source polarization `z`
  - relative L2, `8 mm` vs `30 mm`: `2.981246e-03`
  - scatter-to-baseline ratio at `30 mm`: `5.380652e-03`
  - field-loss spread, `8 mm` vs `30 mm`: `1.912117e-04`
- Next closest current-ish candidates:
  - `1.20/1.20 z`: relative L2 `1.60e-06`
  - `1.00/1.20 z`: relative L2 `1.15e-06`
  - current product geometry `0.50/1.20` remained `0.0` for z/x/y.

## What Remains Blocked

- The only radius-sensitive candidate in this grid is a near-object diagnostic geometry. It is useful for bridge design but not yet a defensible field-product acquisition model.
- Current geometry and source-polarization variants remain radius-invariant.
- A unique diameter prediction is still blocked for the shipping product.

## Current Decision

Forward contrast must be used as a gate before optimizer runs. The next radius-capable bridge must move the geometry/objective toward a sensitive setup; optimizer changes alone are not enough.

## Next Defensible Task

Use the `1.45/1.45 z` sensitive candidate as a diagnostic branch:

- run a fixed-radius field-objective scan under that bridge to confirm the field objective can rank diameters when forward contrast exists,
- keep it labelled diagnostic because the geometry is not yet the actual field acquisition,
- then design a surface-style/time-window bridge that can produce nonzero `8-30 mm` contrast without using near-object receiver placement.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_radius_bridge_geometry_grid_search.py`
- `python -m pytest tests/test_field_3d_0701_radius_bridge_geometry_grid_search.py tests/test_field_3d_0701_radius_bridge_geometry_synthesis.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py -q`
  - `10 passed`
- Touched-file `git diff --check` passed.
- Figure inspected:
  - `074.../figures/field_3d_0701_radius_bridge_geometry_grid_search.png`

## Artifact Paths

- Grid search:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/074_field_3d_0701_radius_bridge_geometry_grid_search`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
