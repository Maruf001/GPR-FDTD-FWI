# Field 3D 0701 Product Report Scattered Diameter Refresh Checkpoint

Date: 2026-07-04

## What Changed

- Updated `run_field_3d_0701_predictor_product_report.py` to read the scattered-radius objective synthesis from checkpoint 292.
- Added diagnostic scattered-response diameter fields to the product JSON, CSV, README, and figure.
- Kept the main diameter fields conservative:
  - full-objective top diameter remains `8 mm`
  - full-objective supported range remains `8-30 mm`
  - full-objective diameter status remains `not_identified_flat_loss_across_scanned_diameters`
- Updated `run_field_prediction_product_leaderboard.py` to point at the refreshed 0701 product report and retain diagnostic scattered diameter columns.
- Added and updated focused tests for both report generators.

## Key Numbers

- Refreshed 0701 product report:
  - artifact `084_field_3d_0701_predictor_product_report`
  - x `9.819386151982 m`
  - assumed y center `0.200000 m`
  - z depth `1.507637023926 m`
  - y-length proxy `0.200000 m`
  - epsr `4.803974151611`
  - background conductivity `0.008403605781 S/m`
  - fit loss `0.707159221172`
  - full-objective diameter range `8-30 mm`
  - diagnostic scattered-response diameter candidate `20.0 mm`
  - diagnostic status `diagnostic_candidate_not_product_claim`
- Refreshed product leaderboard:
  - artifact `006_field_prediction_product_leaderboard`
  - best 0701 product now points to `084_field_3d_0701_predictor_product_report`
  - best GSSI product remains `049_gssi51600s_surface_bscan_product_report`
  - 0701 row carries `diagnostic_scattered_diameter_top_candidate_mm = 20.0`

## What Remains Blocked

- The `20 mm` scattered-response diameter is visible in the product table but remains diagnostic.
- The main product claim still cannot say diameter is uniquely identified because the full local waveform objective remains flat over `8-30 mm`.
- The acquisition bridge and source/receiver timing still need stronger validation before the diagnostic scattered diameter can become the shipped diameter claim.
- The current 0701 report still uses a y-length proxy, not a full finite-length 3D steel-cylinder inversion.

## Current Decision

The product-facing deliverable now exposes the best current field-data diameter candidate without over-claiming it. This is the right shape for shipping progress: a top candidate, a range/status, source artifacts, and clear claim boundaries.

## Next Defensible Task

Convert the scattered-response loss from a fixed-radius scan into an optimizer branch. The first bounded version should optimize source time shift, source amplitude/polarity, epsr, conductivity, and possibly x/z around the current 0701 candidate while scanning or optimizing diameter.

## Validation And Resources

- `python -m py_compile run_field_3d_0701_predictor_product_report.py`
- `python -m py_compile run_field_prediction_product_leaderboard.py`
- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py -q`
  - `3 passed`
- `python -m pytest tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_predictor_product_report.py -q`
  - `7 passed`
- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_radius_scattered_objective_scan.py tests/test_field_3d_0701_scattered_radius_objective_synthesis.py -q`
  - `13 passed`
- Touched-file `git diff --check` passed.
- Figure checks:
  - `084.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `53.36`
  - `006.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`

## Artifact Paths

- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/084_field_3d_0701_predictor_product_report`
- Refreshed product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/006_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
