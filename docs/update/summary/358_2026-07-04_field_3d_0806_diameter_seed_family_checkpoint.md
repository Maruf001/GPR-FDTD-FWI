# Field 3D 0806 Diameter Seed Family Checkpoint

## What changed
- Ran a conductivity-enabled 16 mm diameter-seed stress on the `0806` transfer objective:
  - `316_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam16_iter8`
- Synthesized the conductivity-enabled diameter seed family:
  - `317_field_3d_0806_transfer_conductivity_diameter_seed_family`
- Updated the combined `0806` transfer synthesis:
  - `318_field_3d_0806_transfer_combined_conductivity_diameter_seed_family`
- Regenerated product-facing artifacts:
  - `083_field_prediction_transfer_leaderboard_with_0806_diameter_seed_family`
  - `084_field_prediction_current_product_pointer_with_0806_diameter_seed_family`

## Key numbers
- 16 mm diameter stress `316`:
  - initial loss `0.7916604877`
  - best objective loss `0.7910219431`
  - best field L1 `0.7910026908`
  - best diameter `13.9201 mm`
  - final diameter `13.6659 mm`
  - best length `0.08139 m`
  - fitted local center x/depth `0.61212 m / 1.80659 m`
  - best epsr `3.54502`
  - best background conductivity `0.006199 S/m`
  - best anomaly conductivity `0.030485 S/m`
- Diameter-family synthesis `317`:
  - best label remains `0806_sample42_source10_adamw_conductivity_diam12_iter8`
  - best diameter `10.6360 mm`
  - near-best diameter range expands to `8.00039-13.92007 mm`
  - near-best length range `0.08136-0.09357 m`
  - near-best field L1 range `0.7909555-0.7912157`
- Combined synthesis `318`:
  - decision `finite_length_seed_stability_inconclusive`
  - best field L1 `0.7909555435`
  - max improvement across evidence `0.0010514855`
  - near-best diameter range `8.00037-13.92007 mm`
  - near-best epsr range `3.37157-3.55747`
  - near-best background conductivity range `0.004398-0.006203 S/m`
- Current pointer `084`:
  - shipped dataset remains `external_2025_pipe_0701`
  - transfer candidate remains `external_2025_pipe_0806`
  - `0806` x/y/z `2.4576 m / 0.35 m / 1.80544 m`
  - `0806` length `0.08098-0.09357 m`
  - `0806` diameter `8.00037-13.92007 mm`
  - `0806` epsr `3.54531`
  - `0806` background conductivity `0.006203 S/m`

## Current decision
The larger-diameter stress did not beat the 12 mm-seeded run, so the best current diameter candidate remains `10.64 mm`. However, the 16 mm-seeded run is close enough that the product-safe diameter output must be a range reaching about `13.9 mm`; a unique diameter claim is not justified.

## What remains blocked
- Diameter is now gradient-sensitive but still seed-sensitive.
- Conductivity is optimized, but needs at least one neighboring objective/window confirmation before release promotion.
- `0704` and `07011` remain blocked by no optimizer descent.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `13 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py -q`: `19 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_transfer_leaderboard.py -q`: `6 passed`.
- `git diff --check` on touched scripts/tests/checkpoints: passed.
- Figures:
  - `316` optimizer figure is `1957 x 767` PNG.
  - `317` seed-family synthesis figure is `2389 x 767` PNG.
  - `318` combined synthesis figure is `2373 x 767` PNG.
  - `083` leaderboard figure is `2399 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/316_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam16_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/317_field_3d_0806_transfer_conductivity_diameter_seed_family`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/318_field_3d_0806_transfer_combined_conductivity_diameter_seed_family`
- `outputs/validation_exp_on_field_data/product_leaderboard/083_field_prediction_transfer_leaderboard_with_0806_diameter_seed_family`
- `outputs/validation_exp_on_field_data/product_leaderboard/084_field_prediction_current_product_pointer_with_0806_diameter_seed_family`

## Next defensible task
Run a neighboring-window conductivity confirmation for the best 12 mm diameter candidate, because release promotion now depends more on whether the 10.6 mm / conductivity result survives a nearby objective/window than on another same-window diameter seed.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
