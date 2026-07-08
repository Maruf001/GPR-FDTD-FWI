# GSSI Surface Radius Gradient Diagnostic Checkpoint

Date: 2026-07-04

## What Changed

- Added per-parameter gradient logging to `run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`, the shared optimizer used by the GSSI surface adapter.
- Reran the current GSSI rank-3 surface product setting with gradient logging:
  - AdamW
  - receiver offset `0.005 m`
  - lower diameter bound `2 mm`
  - time-shift optimization enabled
- Added `run_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py`.
- Added focused tests for the GSSI gradient diagnostic.
- Refreshed the GSSI surface product report to include radius-gradient diagnostics.
- Refreshed the product leaderboard to include radius-gradient columns.

## Key Numbers

- GSSI gradient run:
  - artifact `051_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_grad_diagnostic`
  - detector rank `3`
  - best x `0.407892840536 m`
  - best z `0.113712072372 m`
  - best diameter `8.095408790 mm`
  - best epsr `2.128444195`
  - best loss `0.848501205444`
  - mean iteration runtime `0.570864 s`
- Gradient synthesis:
  - artifact `052_gssi51600s_surface_bscan_gradient_diagnostic_synthesis`
  - max raw radius gradient `0.041737474501`
  - max raw time-shift gradient `0.007099006325`
  - radius/time gradient ratio `5.8793`
  - radius-gradient status `radius_gradient_visible`
  - gradient-run diameter `8.095408790 mm`
  - product report diameter `18.586354330 mm`
  - product near-best diameter range `8.108957671-18.738288432 mm`
  - consistency status `gradient_run_outside_product_near_best_range`
- Refreshed GSSI product report:
  - artifact `053_gssi51600s_surface_bscan_product_report`
  - x `0.413941013248 m`
  - z `0.128718197346 m`
  - product diameter `18.586354330 mm`
  - near-best range `8.108957671-18.738288432 mm`
  - epsr `2.044878721`
  - background conductivity `0.002187208273 S/m`
  - fit loss `0.848336815834`
  - radius-gradient status `radius_gradient_visible`
- Refreshed product leaderboard:
  - artifact `011_field_prediction_product_leaderboard`
  - GSSI row now includes:
    - `radius_gradient_status = radius_gradient_visible`
    - `radius_gradient_max_abs_raw = 0.041737474501`
    - `radius_gradient_diagnostic_diameter_mm = 8.095408790`
    - `radius_gradient_diameter_consistency_status = gradient_run_outside_product_near_best_range`

## What Remains Blocked

- The GSSI radius gradient is visible, but the diameter is still window/setting sensitive.
- The gradient diagnostic run prefers about `8.1 mm`, while the current product optimizer setting reports `18.6 mm`; both sit near the lower edge or inside the broad product near-best band.
- GSSI still lacks y position, rebar length, and measured crossline geometry.
- There is no destructive ground-truth diameter label, so this remains a provisional predictor output.

## Current Decision

GSSI is more promising than the current 0701 scattered optimizer for radius sensitivity because radius gradients are not negligible. However, the product claim still must report a diameter range/status rather than a unique diameter. The current strongest GSSI product statement is:

- x/z/material estimate is product-visible and provisional,
- diameter proxy is `18.6 mm`,
- near-best diameter range is roughly `8.1-18.7 mm`,
- a short gradient diagnostic independently finds a visible radius gradient and an `8.1 mm` diagnostic diameter,
- no y/length/3D geometry claim yet.

## Next Defensible Task

Use the GSSI gradient signal to run a matched seed/optimizer set, analogous to the 0701 scattered optimizer checks:

- run GSSI surface optimizer from diameter seeds around `8, 12, 16, 20 mm`,
- keep detector rank, offset, window, optimizer, and shift settings fixed,
- synthesize whether the radius gradient converges to a stable diameter or remains seed/window sensitive.

## Validation And Resources

- `python -m py_compile run_gssi51600s_surface_bscan_product_report.py run_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`
- `python -m pytest tests/test_gssi51600s_surface_bscan_product_report.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py -q`
  - `5 passed`
- `python -m pytest tests/test_field_prediction_product_leaderboard.py tests/test_gssi51600s_surface_bscan_product_report.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py -q`
  - `9 passed`
- `python -m pytest tests/test_gssi51600s_surface_bscan_product_report.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_predictor_product_report.py -q`
  - `15 passed`
- Touched-file `git diff --check` passed.
- Figure checks:
  - `051.../figures/gssi51600s_surface_bscan_geometry_optimizer.png`: size `(2314, 750)`, min/max `(0, 255)`, stddev `39.05`
  - `052.../figures/gssi51600s_surface_bscan_gradient_diagnostic.png`: size `(1855, 750)`, min/max `(0, 255)`, stddev `63.99`
  - `053.../figures/gssi51600s_surface_bscan_product_report.png`: size `(1957, 750)`, min/max `(0, 255)`, stddev `58.93`
  - `011.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- GSSI gradient run:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/051_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_lower_bound_2mm_grad_diagnostic`
- GSSI gradient synthesis:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/052_gssi51600s_surface_bscan_gradient_diagnostic_synthesis`
- Refreshed GSSI product report:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/053_gssi51600s_surface_bscan_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/011_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
