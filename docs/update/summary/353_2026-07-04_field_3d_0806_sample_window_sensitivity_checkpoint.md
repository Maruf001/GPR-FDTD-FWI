# Field 3D 0806 Sample Window Sensitivity Checkpoint

## What changed
- Generated a constrained `0806` sample-start-42 transfer seed:
  - `306_field_3d_0806_transfer_seed_sample42_window_profile_axis_y`
- Ran Adamax 8 iterations on that window:
  - `307_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamax_iter8`
- Synthesized sample-window sensitivity:
  - `308_field_3d_0806_transfer_sample_window_sensitivity`
- Regenerated product transfer leaderboard:
  - `075_field_prediction_transfer_leaderboard_with_0806_sample_window_sensitivity`

## Key numbers
- Sample start `38`:
  - best loss `0.7937642932`
  - threshold descent `0.001051`
  - best z/depth around `1.793 m`
- Sample start `42`:
  - initial loss `0.7915197015`
  - best loss `0.7914409041`
  - best field L1 `0.7913582325`
  - improvement `7.88e-5`
  - best z/depth around `1.823 m`
- Synthesis:
  - best label `0806_sample42_source10_adamax_iter8`
  - best field L1 `0.7913582325`
  - near-best length range `0.08458-0.08514 m`
- Updated leaderboard:
  - `0806` status `transfer_optimizer_decreased_loss`
  - x/y/z `2.4576 m / 0.35 m / 1.8695 m`
  - length range `0.08458-0.08514 m`

## Current decision
`0806` sample-window sensitivity improves the absolute fit at sample start `42`, while sample start `38` gives stronger within-run descent. The product-safe status remains a transfer candidate, not a shippable release prediction.

## What remains blocked
- Need decide whether product ranking should prioritize absolute fit or within-run descent; current leaderboard uses the synthesis best fit but keeps claim boundary conservative.
- Need repeat sample-window result with a second seed/source condition before release.
- Diameter remains non-unique.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `10 passed`.
- `git diff --check` on touched files: passed.
- Updated leaderboard figure exists as PNG, `2399 x 767`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/306_field_3d_0806_transfer_seed_sample42_window_profile_axis_y`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/307_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamax_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/308_field_3d_0806_transfer_sample_window_sensitivity`
- `outputs/validation_exp_on_field_data/product_leaderboard/075_field_prediction_transfer_leaderboard_with_0806_sample_window_sensitivity`

## Next defensible task
Build a current product pointer update that makes `075_field_prediction_transfer_leaderboard_with_0806_sample_window_sensitivity` the current transfer leaderboard while keeping `061/063/065` as the release-candidate package/pointer for shippable 0701.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
