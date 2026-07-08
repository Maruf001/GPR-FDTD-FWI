# Field 3D 0701 Surface Bridge Contrast Checkpoint

Date: 2026-07-04

## What Changed

- Added `--duration-ns` to `run_field_3d_0701_fastgpr_radius_forward_contrast.py`.
- Added `--duration-ns` to `run_field_3d_0701_fastgpr_radius_sensitivity_scan.py`.
- Ran long-window surface-style radius forward probes.
- Added `run_field_3d_0701_surface_bridge_contrast_synthesis.py`.
- Added focused tests for the surface-bridge synthesis.
- Ran a bounded fixed-radius optimizer smoke on the strongest surface-style bridge candidate.

## Key Numbers

- Surface forward contrast probes used:
  - `dx_m = 0.01`
  - `fast_dt_ns = 0.02`
  - duration `30 ns`
  - diameters `8 mm` and `30 mm`
- Forward contrast:
  - `076_surface_y005_y005_duration30`: relative L2 `2.184724e-05`
  - `077_surface_y005_y020_duration30`: relative L2 `5.331227e-05`
  - `078_surface_y005_y050_duration30`: relative L2 `3.325245e-04`
- Surface synthesis:
  - artifact `079_field_3d_0701_surface_bridge_contrast_synthesis`
  - decision `surface_style_radius_contrast_candidate_found`
  - best candidate `surface_y005_y050_d30`
  - best source y `0.05 m`
  - best receiver y `0.50 m`
  - best relative L2 `3.325245e-04`
- Surface fixed-radius optimizer smoke:
  - artifact `080_field_3d_0701_fastgpr_radius_sensitivity_scan_surface_y005_y050_dx01_d30ns_smoke`
  - diameters `8, 20, 30 mm`
  - iterations per diameter `2`
  - top candidate `8.0 mm`
  - near-best range `8.0-30.0 mm`
  - loss range `[1.196949362755, 1.196949362755]`
  - status `not_identified_flat_loss_across_scanned_diameters`

## What Remains Blocked

- The surface-style bridge can create nonzero forward contrast, but the current full-field normalized L1 objective still flattens diameter after re-optimization.
- The strongest surface-style candidate uses a receiver at `0.50 m`, which is not yet a validated field acquisition model.
- Diameter is still not product-ready.

## Current Decision

Changing geometry can recover forward radius contrast, but the loss must change too. The next diameter branch should use a scattered/anomaly-focused loss instead of the current full/direct waveform normalized L1.

## Next Defensible Task

Implement a scattered-response field objective smoke:

- compute baseline and anomaly predictions,
- compare anomaly-minus-baseline prediction against a field residual/preprocessed event window,
- rerun fixed-radius scans only if the scattered objective separates `8-30 mm`.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_surface_bridge_contrast_synthesis.py run_field_3d_0701_fastgpr_radius_forward_contrast.py`
- `python -m pytest tests/test_field_3d_0701_surface_bridge_contrast_synthesis.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py tests/test_field_3d_0701_fastgpr_radius_sensitivity_scan.py -q`
  - `11 passed`
- Touched-file `git diff --check` passed.
- Figures inspected:
  - `079.../figures/field_3d_0701_surface_bridge_contrast_synthesis.png`
  - `080.../figures/field_3d_0701_fastgpr_radius_sensitivity_scan.png`

## Artifact Paths

- Surface forward probes:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/076_field_3d_0701_fastgpr_radius_forward_contrast_surface_y005_duration30`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/077_field_3d_0701_fastgpr_radius_forward_contrast_surface_y005_y020_duration30`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/078_field_3d_0701_fastgpr_radius_forward_contrast_surface_y005_y050_duration30`
- Surface synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/079_field_3d_0701_surface_bridge_contrast_synthesis`
- Surface fixed-radius smoke:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/080_field_3d_0701_fastgpr_radius_sensitivity_scan_surface_y005_y050_dx01_d30ns_smoke`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
