# Field 3D 0701 Source-Frequency Product Integration Checkpoint

Date: 2026-07-04

## What Changed

- Tested source-frequency sensitivity around the promoted adaptive `14-16` y/length row.
- Compared `25 MHz`, `30 MHz`, and `35 MHz` using:
  - receiver-mean residualization,
  - Adamax,
  - timing regularization weight `0.005`,
  - diameter seeds `8 mm` and `12 mm`.
- Wired source-frequency sensitivity into:
  - 0701 product report,
  - product leaderboard,
  - shipping snapshot.

## Key Numbers

- `25 MHz`:
  - `213...freq25mhz...seed08`
    - field L1 `0.537765`
    - diameter `8.002 mm`
    - depth `1.490 m`
    - epsr `3.297`
  - `214...freq25mhz...seed12`
    - field L1 `0.537815`
    - diameter `11.929 mm`
    - depth `1.490 m`
    - epsr `3.297`
- `30 MHz` references:
  - `203...freq30mhz...seed08`
    - field L1 `0.537808`
    - diameter `8.002 mm`
  - `204...freq30mhz...seed12`
    - field L1 `0.537949`
    - diameter `11.908 mm`
- `35 MHz`:
  - `215...freq35mhz...seed08`
    - field L1 `0.538090`
    - diameter `8.002 mm`
    - depth `1.490 m`
    - epsr `3.300`
  - `216...freq35mhz...seed12`
    - field L1 `0.538146`
    - diameter `11.874 mm`
    - depth `1.490 m`
    - epsr `3.303`
- Source-frequency synthesis:
  - artifact `217_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamax_y_length_source_frequency_sensitivity`
  - best label `freq25_seed08`
  - all tested source frequencies are near-best: `25`, `30`, `35 MHz`
  - field-L1 range `0.537764728-0.538145840`
  - near-best diameter range `8.002195507-11.928718537 mm`
  - y center `1.50 m`
  - length center-span `0.20 m`
- Product artifacts:
  - product report `218_field_3d_0701_predictor_product_report`
  - leaderboard `046_field_prediction_product_leaderboard`
  - shipping snapshot `047_field_prediction_shipping_snapshot`
  - source-frequency status `tested_source_frequencies_all_near_best_y_length_stable`

## What Remains Blocked

- Diameter remains a narrow range, not a unique value.
- Timing-prior sensitivity remains to be tested around the promoted row.
- Profile-window sensitivity was narrowed but should remain in the claim boundary until timing/source/residual findings are all consolidated.
- Still not a full finite-length 3D FDTD inversion.

## Current Decision

The promoted 0701 operational row is stable across `25-35 MHz`:

- y center stays `1.50 m`,
- length stays `0.20 m` center-span,
- z stays near `1.49 m`,
- epsr stays near `3.30`,
- field L1 changes only at the `4e-4` scale.

Source-frequency is no longer the leading blocker for the current y/length/material estimate.

## Next Defensible Task

Run timing-prior sensitivity around the promoted row:

- profile window `14-16`,
- receiver-mean residualization,
- Adamax,
- source frequency can use `25 MHz` or retain operational `30 MHz`,
- compare timing-prior regularization weights around `0`, `0.0025`, `0.005`, and `0.01`.

Then consolidate source/residual/timing into one product-stability summary.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `217.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `70.929`
  - `218.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `56.611`
  - `046.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.984`
  - `047.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`

## Artifact Paths

- Source-frequency synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/217_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamax_y_length_source_frequency_sensitivity`
- Product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/218_field_3d_0701_predictor_product_report`
- Product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/046_field_prediction_product_leaderboard`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/047_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
