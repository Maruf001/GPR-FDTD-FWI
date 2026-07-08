# Field 3D 0701 Scattered Radius Objective Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_fastgpr_radius_scattered_objective_scan.py`.
- Added focused tests for the scattered-objective radius scan.
- Ran two real-field scattered-response radius scans on the 0701 stack using the surface-style bridge from checkpoint 291.
- Added `run_field_3d_0701_scattered_radius_objective_synthesis.py`.
- Added focused tests for the residual-mode synthesis.
- Snapshotted the exact scripts into the synthesis output artifact.

## Key Numbers

- Shared scan setup:
  - field stack source: `data/2025-01-13_GPR_Dataset`
  - source y `0.05 m`
  - receiver y `0.50 m`
  - duration `30 ns`
  - `dx_m = 0.01`
  - `fast_dt_ns = 0.02`
  - scanned diameters `8, 12, 16, 20, 24, 30 mm`
- Profile-mean residual scan:
  - artifact `081_field_3d_0701_fastgpr_radius_scattered_objective_scan_surface_y005_y050_d30`
  - residual mode `profile_mean`
  - top diameter `20.0 mm`
  - near-best range `20.0-20.0 mm`
  - best scattered L1 loss `0.787291765213`
  - loss spread `0.021552681923`
  - status `scattered_objective_candidate_separated`
- Receiver-mean residual scan:
  - artifact `082_field_3d_0701_fastgpr_radius_scattered_objective_scan_surface_y005_y050_d30_receiver_mean`
  - residual mode `receiver_mean`
  - top diameter `20.0 mm`
  - near-best range `20.0-20.0 mm`
  - best scattered L1 loss `0.790006220341`
  - loss spread `0.021756708622`
  - status `scattered_objective_candidate_separated`
- Synthesis:
  - artifact `083_field_3d_0701_scattered_radius_objective_synthesis`
  - decision `scattered_radius_objective_residual_modes_agree`
  - common top diameter `20.0 mm`
  - all modes separated `true`

## What Remains Blocked

- This is a diagnostic scattered-response candidate, not yet a product-grade 3D diameter claim.
- The surface-style bridge uses receiver y `0.50 m`; that is still a sensitivity model, not a validated acquisition geometry.
- The scattered objective is currently a fixed-radius scan, not a full optimizer over x, y, z, radius, length, permittivity, conductivity, source timing, and amplitude.
- Product reporting still needs uncertainty/range logic that can present a top candidate while clearly showing degeneracy or bridge sensitivity.

## Current Decision

The scattered-response objective is the first 0701 field-data branch in this sequence that separates a realistic diameter candidate inside the `8-30 mm` range. The stable `20 mm` candidate is worth promoting into the next optimizer branch, but only as a diagnostic candidate until source/receiver geometry and timing are validated.

## Next Defensible Task

Build a product-facing diagnostic update that carries this `20 mm` scattered-radius candidate alongside the current predictor result, then start converting the scattered-response loss from a scan into an optimizer objective with explicit source/time/polarity alignment.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_fastgpr_radius_scattered_objective_scan.py run_field_3d_0701_scattered_radius_objective_synthesis.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `6 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py tests/test_field_3d_0701_surface_bridge_contrast_synthesis.py tests/test_field_3d_0701_fastgpr_radius_forward_contrast.py -q`
  - `13 passed`
- Touched-file `git diff --check` passed.
- Figure check for `083.../figures/field_3d_0701_scattered_radius_objective_synthesis.png`:
  - size `(1804, 733)`
  - grayscale min/max `(0, 255)`
  - standard deviation `69.94`

## Artifact Paths

- Profile-mean scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/081_field_3d_0701_fastgpr_radius_scattered_objective_scan_surface_y005_y050_d30`
- Receiver-mean scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/082_field_3d_0701_fastgpr_radius_scattered_objective_scan_surface_y005_y050_d30_receiver_mean`
- Residual-mode synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/083_field_3d_0701_scattered_radius_objective_synthesis`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
