# Field Prediction Current Pointer Transfer Leaderboard Checkpoint

## What changed
- Extended `run_field_prediction_current_product_pointer.py` so the current product pointer now records:
  - current release package/audit artifacts,
  - current transfer leaderboard summary,
  - shippable 3D datasets,
  - transfer candidate datasets,
  - optimizer-blocked transfer datasets,
  - compact prediction rows and the best transfer candidate.
- Added a focused regression test that keeps transfer candidates from being silently promoted as shipped release results.
- Generated the updated pointer:
  - `076_field_prediction_current_product_pointer_with_transfer_leaderboard`

## Key numbers
- Current shipped 3D dataset:
  - `external_2025_pipe_0701`
- Current transfer candidate:
  - `external_2025_pipe_0806`
  - x/y/z `2.4576 m / 0.35 m / 1.8695 m`
  - length range `0.08458-0.08514 m`
  - diameter range `8.00037-8.00038 mm` for the current sample-window synthesis, with diameter status still `diameter_not_identified_gradient_negligible`
  - fit field L1 `0.7913582325`
  - best label `0806_sample42_source10_adamax_iter8`
- Optimizer-blocked transfer stacks:
  - `external_2025_pipe_07011`
  - `external_2025_pipe_0704`

## Current decision
The current product pointer is ready. It keeps `0701` as the only shippable real-field 3D product and exposes `0806` as the next transfer candidate without promoting it before stability, diameter, and material checks.

## What remains blocked
- `0806` still needs a second confirmation run before release promotion.
- Diameter remains non-unique and should be reported as a range/sensitivity result, not a single identified diameter.
- `0704` and `07011` still need objective/source alignment improvements because their transfer optimizers do not decrease loss from the seed.

## Validation/resource checks
- `python -m py_compile run_field_prediction_current_product_pointer.py`: passed.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_transfer_leaderboard.py -q`: `6 passed`.
- `git diff --check -- run_field_prediction_current_product_pointer.py tests/test_field_prediction_current_product_pointer.py`: passed.
- The changed pointer script, test, and `076` output are untracked in this worktree; unrelated existing worktree changes were not touched.

## Artifact paths
- `outputs/validation_exp_on_field_data/product_leaderboard/076_field_prediction_current_product_pointer_with_transfer_leaderboard`
- `outputs/validation_exp_on_field_data/product_leaderboard/076_field_prediction_current_product_pointer_with_transfer_leaderboard/data/field_prediction_current_product_pointer_summary.json`
- `outputs/validation_exp_on_field_data/product_leaderboard/076_field_prediction_current_product_pointer_with_transfer_leaderboard/scripts/script_snapshot_manifest.json`

## Next defensible task
Run a bounded second-confirmation branch for `0806`: keep the real stack and sample-window result fixed, vary one optimizer/objective axis at a time, and test whether the transfer candidate survives enough stability to move closer to release.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
