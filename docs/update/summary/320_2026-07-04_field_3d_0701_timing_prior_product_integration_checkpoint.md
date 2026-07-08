# Field 3D 0701 Timing-Prior Product Integration Checkpoint

Date: 2026-07-04

## What Changed

- Tested timing-prior sensitivity around the promoted adaptive scattered `14-16` y/length row.
- Compared time-shift regularization weights `0`, `0.0025`, `0.005`, and `0.01` using:
  - receiver-mean residualization,
  - Adamax,
  - `25 MHz` source frequency,
  - diameter seeds `8 mm` and `12 mm`.
- Wired timing-prior sensitivity into:
  - 0701 product report,
  - product leaderboard,
  - shipping snapshot.

## Key Numbers

- Timing-prior synthesis:
  - artifact `225_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamax_freq25_y_length_timing_prior_sensitivity`
  - best label `w0000_seed08`
  - all tested timing-prior weights are near-best: `0`, `0.0025`, `0.005`, `0.01`
  - field-L1 range `0.5376729369-0.5378339887`
  - near-best diameter range `8.002195507-11.965089478 mm`
  - y center `1.50 m`
  - length center-span `0.20 m`
  - length window-span `0.30 m`
  - depth `1.488572598 m` for the best run
  - epsr `3.281233311` for the best run
  - background conductivity `0.003813082 S/m` for the best run
- Product artifacts:
  - product report `226_field_3d_0701_predictor_product_report`
  - leaderboard `048_field_prediction_product_leaderboard`
  - shipping snapshot `049_field_prediction_shipping_snapshot`
  - timing-prior status `tested_timing_prior_weights_all_near_best_y_length_stable`

## What Remains Blocked

- Diameter remains a supported range, not a unique field-data claim.
- Adaptive y conflicts with the older legacy global-y row by `0.25 m`.
- The current 0701 product row is still a local Fast-GPR smooth-cylinder proxy, not a full finite-length 3D FDTD steel-cylinder inversion.
- The GSSI 51600S product row still has no y/length support because it is a surface B-scan rather than a crossline stack.

## Current Decision

The promoted 0701 operational row is stable across the sensitivity checks run so far:

- optimizer family: Adam, AdamW, Adamax stay on the same adaptive y/length row;
- residual mode: receiver-mean controls the current loss and keeps y/length stable;
- source frequency: `25`, `30`, and `35 MHz` remain near-best;
- timing-prior weight: `0-0.01` remains near-best.

The product should keep reporting:

- x `9.819386 m`,
- y center `1.50 m`,
- z depth `1.488030 m`,
- y length center-span `0.20 m`,
- epsr `3.296651`,
- background conductivity `0.003776330 S/m`,
- diameter top candidate `8.002209 mm`,
- diameter supported range `8.002209-11.896786 mm`.

## Next Defensible Task

Consolidate profile-window support and product-stability status for the promoted adaptive row:

- load the current product report plus optimizer-family, residual-mode, source-frequency, and timing-prior synthesis artifacts;
- produce a single stability summary table and figure;
- expose a compact status suitable for the shipping snapshot;
- keep the claim boundary explicit around diameter range, profile-window/legacy conflict, and full 3D finite-length inversion.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed before this checkpoint was written.
- Figure checks:
  - `225.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1888, 767)`, min/max `(0, 255)`, stddev `71.207`
  - `226.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `56.611`
  - `048.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.984`
  - `049.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`

## Artifact Paths

- Timing-prior synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/225_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamax_freq25_y_length_timing_prior_sensitivity`
- Product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/226_field_3d_0701_predictor_product_report`
- Product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/048_field_prediction_product_leaderboard`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/049_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
