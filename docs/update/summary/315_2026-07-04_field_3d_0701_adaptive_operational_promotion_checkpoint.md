# Field 3D 0701 Adaptive Operational Promotion Checkpoint

Date: 2026-07-04

## What Changed

- Promoted the adaptive scattered common-objective y/length/material row as the operational 0701 product prediction.
- Retained the older global y/length row as legacy context instead of using it as the primary product row.
- Updated product report, leaderboard, and shipping snapshot schemas to carry:
  - `operational_prediction_source`,
  - legacy global-y values,
  - adaptive y/length values,
  - adaptive diameter range and fit loss.
- Updated claim-boundary text so the report explains that the operational row comes from the adaptive scattered objective.

## Key Numbers

- Product report `199_field_3d_0701_predictor_product_report` now prints:
  - operational source `adaptive_scattered_common_objective`
  - x `9.819386152 m`
  - y center `1.500 m`
  - z depth `1.488030195 m`
  - center-span length `0.200 m`
  - epsr `3.296650887`
  - background sigma `0.003776330 S/m`
  - fit loss / adaptive field L1 `0.537833989`
  - diameter range `8.002208546-11.896786280 mm`
- Legacy global-y row retained in the report:
  - y center `1.750 m`
  - center-span length `0.100 m`
  - fit loss `0.602550268`
  - conflict against operational adaptive y `0.250 m`
- Product index artifacts:
  - leaderboard `040_field_prediction_product_leaderboard`
  - shipping snapshot `042_field_prediction_shipping_snapshot`

## What Remains Blocked

- The operational row is now adaptive scattered, but the legacy global-y row still conflicts by `0.25 m`; this should be explained as a legacy-objective disagreement, not as the current primary estimate.
- Diameter is narrowed but still a range, not a unique value.
- This remains a profile-window length proxy, not a full finite-length 3D FDTD inversion.

## Current Decision

The current shippable 0701 prediction row is:

- source: adaptive scattered common objective
- x `9.819 m`
- y `1.500 m`
- z `1.488 m`
- length center-span `0.200 m`
- length window-span `0.300 m`
- epsr `3.297`
- background sigma `0.003776 S/m`
- diameter `8.00-11.90 mm`
- field L1 `0.537834`

The older global-y row remains recorded only for traceability and conflict awareness.

## Next Defensible Task

Stress-test the promoted `14-16` adaptive y/length row across optimizer families:

- AdamW already supports it.
- Run bounded checks for Adam and Adamax at the same profile window, source frequency, residual mode, timing prior, and diameter seeds.
- Synthesize whether the y/length, material values, and diameter range survive optimizer choice.

If optimizer-family sensitivity is acceptable, the next product branch should test residual-mode sensitivity around `14-16`.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `21 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `197.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `73.014`
  - `199.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `56.611`
  - `040.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.984`
  - `042.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.482`

## Artifact Paths

- Operational product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/199_field_3d_0701_predictor_product_report`
- Product leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/040_field_prediction_product_leaderboard`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/042_field_prediction_shipping_snapshot`
- Adaptive y/length support synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/197_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_freq30_y_length_support`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
