# Field 3D 0806 Sample Window Diameter Confirmation Checkpoint

## What changed
- Ran a neighboring-window conductivity-enabled 12 mm diameter confirmation on `0806`:
  - `319_field_3d_0806_fastgpr_transfer_seed_sample38_profile_mean_source10_adamw_conductivity_diam12_iter8`
- Synthesized the 12 mm diameter candidate across sample windows:
  - `320_field_3d_0806_transfer_conductivity_diam12_sample_window_confirmation`
- Updated the full combined `0806` synthesis:
  - `321_field_3d_0806_transfer_combined_sample_window_diameter_seed_family`
- Regenerated product-facing artifacts:
  - `085_field_prediction_transfer_leaderboard_with_0806_sample_window_diameter_family`
  - `086_field_prediction_current_product_pointer_with_0806_sample_window_diameter_family`

## Key numbers
- Neighboring sample-38 12 mm run `319`:
  - decision `finite_length_scattered_optimizer_decreased_loss`
  - initial loss `0.7949942946`
  - best objective loss `0.7937549353`
  - best field L1 `0.7937113643`
  - loss improvement `0.0012393594`
  - best diameter `10.9727 mm`
  - best length `0.08582 m`
  - fitted local center x/depth `0.58208 m / 1.78293 m`
  - best epsr `3.47708`
  - best background conductivity `0.005403 S/m`
- 12 mm two-window synthesis `320`:
  - best label `0806_sample42_source10_adamw_conductivity_diam12_iter8`
  - near-best diameter range `10.6360-10.9727 mm`
  - near-best length range `0.08136-0.08582 m`
  - near-best depth range `1.78293-1.80544 m`
  - near-best background conductivity range `0.005403-0.006203 S/m`
- Full combined synthesis `321`:
  - decision `finite_length_seed_stability_inconclusive`
  - run count `7`
  - best field L1 `0.7909555435`
  - max loss improvement `0.0012393594`
  - near-best diameter range `8.00037-13.92007 mm`
  - near-best length range `0.08098-0.09357 m`
  - near-best depth range `1.78293-1.84962 m`
  - near-best epsr range `3.37157-3.55747`
  - near-best conductivity range `0.004398-0.006203 S/m`
- Current pointer `086`:
  - shipped dataset remains `external_2025_pipe_0701`
  - transfer candidate remains `external_2025_pipe_0806`
  - `0806` best row is x/y/z `2.4576 m / 0.35 m / 1.80544 m`
  - `0806` length `0.08098-0.09357 m`
  - `0806` diameter `8.00037-13.92007 mm`
  - `0806` epsr `3.54531`
  - `0806` background conductivity `0.006203 S/m`

## Current decision
The 12 mm diameter basin is supported by a neighboring sample window: sample-38 gives `10.97 mm` and sample-42 gives `10.64 mm`. The product-safe diameter range remains broader because the same combined evidence includes 8 mm and 16 mm seed-family near-best fits.

## What remains blocked
- Still no unique diameter claim. Best candidate is about `10.6-11.0 mm`, but product range remains `8.0-13.9 mm`.
- Need decide whether to add a prior/regularization or a second receiver/objective constraint to shrink diameter uncertainty.
- `0704` and `07011` still need source/window repair.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `13 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py -q`: `19 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_transfer_leaderboard.py -q`: `6 passed`.
- `git diff --check` on touched scripts/tests/checkpoints: passed.
- Figures:
  - `319` optimizer figure is `1957 x 767` PNG.
  - `320` sample-window synthesis figure is `2394 x 767` PNG.
  - `321` combined synthesis figure is `2372 x 767` PNG.
  - `085` leaderboard figure is `2399 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/319_field_3d_0806_fastgpr_transfer_seed_sample38_profile_mean_source10_adamw_conductivity_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/320_field_3d_0806_transfer_conductivity_diam12_sample_window_confirmation`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/321_field_3d_0806_transfer_combined_sample_window_diameter_seed_family`
- `outputs/validation_exp_on_field_data/product_leaderboard/085_field_prediction_transfer_leaderboard_with_0806_sample_window_diameter_family`
- `outputs/validation_exp_on_field_data/product_leaderboard/086_field_prediction_current_product_pointer_with_0806_sample_window_diameter_family`

## Next defensible task
Build a product-facing predictor card/export for the current pointer so the shipping deliverable has one compact machine-readable and human-readable artifact with the current `0701` release and `0806` transfer candidate.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
