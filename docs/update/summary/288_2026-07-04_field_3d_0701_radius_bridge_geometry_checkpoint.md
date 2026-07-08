# Field 3D 0701 Radius Bridge Geometry Checkpoint

Date: 2026-07-04

## What Changed

- Extended `run_field_3d_0701_fastgpr_radius_forward_contrast.py` with geometry controls:
  - `--source-y-m`
  - `--receiver-y-m`
  - `--source-polarization {x,y,z}`
- Ran forward contrast probes for:
  - current geometry with z polarization,
  - current geometry with x polarization,
  - current geometry with y polarization,
  - near-object diagnostic geometry.
- Added `run_field_3d_0701_radius_bridge_geometry_synthesis.py`.
- Added focused tests for the geometry synthesis decision logic.

## Key Numbers

- Current geometry, z/scattered:
  - artifact `067_field_3d_0701_fastgpr_radius_forward_contrast_dx01_dt002_scattered`
  - max relative L2 for `8-30 mm`: `0.0`
  - max scatter-to-baseline ratio: `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Current geometry, x polarization:
  - artifact `071_field_3d_0701_fastgpr_radius_forward_contrast_dx01_current_geom_polx`
  - max relative L2 for `8-30 mm`: `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Current geometry, y polarization:
  - artifact `072_field_3d_0701_fastgpr_radius_forward_contrast_dx01_current_geom_poly`
  - max relative L2 for `8-30 mm`: `0.0`
  - status `forward_predictions_radius_invariant_at_current_precision`
- Near-object diagnostic geometry:
  - artifact `070_field_3d_0701_fastgpr_radius_forward_contrast_dx01_near_object_y145`
  - source y `1.45 m`
  - receiver y `1.45 m`
  - max relative L2 for `8-30 mm`: `2.981246e-03`
  - max scattered relative L2: `1.237745`
  - max scatter-to-baseline ratio: `5.380652e-03`
  - field loss spread `1.912117e-04`
  - status `forward_and_field_loss_radius_sensitive`
- Synthesis artifact:
  - `073_field_3d_0701_radius_bridge_geometry_synthesis`
  - decision `current_geometry_radius_invariant_near_object_sensitive`
  - best contrast label `near_object_z`

## What Remains Blocked

- The current field-product geometry remains radius-blind at rebar scale.
- Changing source polarization alone did not recover radius sensitivity.
- Near-object geometry proves the Fast-GPR forward code can respond to radius, but that geometry is diagnostic and not yet the field-product acquisition geometry.

## Current Decision

The next radius-capable product path needs a bridge geometry/objective redesign. Continuing with Adam/AdamW/Adamax on the current geometry will not recover diameter.

## Next Defensible Task

Build a candidate radius-sensitive product bridge by moving from the current crosshole-style adapter toward a surface-style or matched acquisition geometry, then rerun forward contrast before any optimizer:

- keep `dx_m <= 0.01` and `fast_dt_ns <= 0.02`,
- search source/receiver positions and time windows for nonzero `8-30 mm` radius contrast,
- only after forward contrast passes, run fixed-radius field objective scans.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_radius_bridge_geometry_synthesis.py run_field_3d_0701_fastgpr_radius_forward_contrast.py`
- `python -m pytest tests/test_field_3d_0701_radius_bridge_geometry_synthesis.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py tests/test_field_3d_0701_fastgpr_radius_sensitivity_scan.py -q`
  - `11 passed`
- Touched-file `git diff --check` passed.
- Figure inspected:
  - `073.../figures/field_3d_0701_radius_bridge_geometry_synthesis.png`

## Artifact Paths

- Near-object probe:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/070_field_3d_0701_fastgpr_radius_forward_contrast_dx01_near_object_y145`
- Current-geometry polarization probes:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/071_field_3d_0701_fastgpr_radius_forward_contrast_dx01_current_geom_polx`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/072_field_3d_0701_fastgpr_radius_forward_contrast_dx01_current_geom_poly`
- Geometry synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/073_field_3d_0701_radius_bridge_geometry_synthesis`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
