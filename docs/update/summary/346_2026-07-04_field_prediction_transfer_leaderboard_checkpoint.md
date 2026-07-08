# Field Prediction Transfer Leaderboard Checkpoint

## What changed
- Added a product-facing transfer leaderboard generator:
  - `run_field_prediction_transfer_leaderboard.py`
- Added focused tests:
  - `tests/test_field_prediction_transfer_leaderboard.py`
- Generated the current product leaderboard:
  - `069_field_prediction_transfer_leaderboard_current_3d_product`

## Key numbers
- Leaderboard rows: `5`
- Product statuses:
  - `current_best_real_field_3d_candidate`: `1`
  - `limited_surface_bscan_candidate`: `1`
  - `transfer_seed_fit_optimizer_blocked`: `2`
  - `intake_ready_not_yet_optimized`: `1`
- Shippable 3D dataset:
  - `external_2025_pipe_0701`
- Transfer-blocked datasets:
  - `external_2025_pipe_07011`
  - `external_2025_pipe_0704`
- Intake-ready but not yet optimized:
  - `external_2025_pipe_0806`
- Current transfer seed fits:
  - `07011`: x `0.2048 m`, y `0.15 m`, z `2.6431 m`, fit L1 `0.778790`
  - `0704`: x `1.9456 m`, y `0.55 m`, z `2.4497 m`, fit L1 `0.785934`

## Current decision
`field_prediction_transfer_leaderboard_ready`.

Only the `0701` release-candidate row is currently shippable as a 3D field prediction. `0704` and `07011` are intake-ready and have seed fits, but are blocked because the optimizer does not decrease loss after the seed. `0806` is ready for intake but has not yet been optimized.

## What remains blocked
- Transfer stacks need source/objective improvement before geometry/material claims can ship.
- `0704` and `07011` seed fits are not final predictions.
- `0806` still needs a seed and optimizer check.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_transfer_readiness.py tests/test_field_prediction_release_candidate.py -q`: `9 passed`.
- `python -m py_compile run_field_prediction_transfer_leaderboard.py run_field_prediction_transfer_readiness.py run_field_prediction_release_candidate.py`: passed.
- `git diff --check` on touched files: passed.
- Leaderboard figure exists as PNG, `2399 x 767`.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/069_field_prediction_transfer_leaderboard_current_3d_product`

## Next defensible task
Run the `0806` seed and one-step profile-mean transfer check. This completes the real-stack transfer coverage table and tells us whether `0806` follows the same no-descent pattern.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
