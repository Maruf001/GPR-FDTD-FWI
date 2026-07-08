# Field 3D 0806 Conductivity Diameter Candidate Checkpoint

## What changed
- Ran a conductivity-enabled 12 mm diameter-seed stress on the `0806` transfer candidate:
  - `313_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam12_iter8`
- Synthesized 8 mm vs 12 mm conductivity-enabled diameter sensitivity:
  - `314_field_3d_0806_transfer_conductivity_diameter_sensitivity`
- Built a combined `0806` transfer synthesis that keeps prior sample-window/optimizer evidence plus the new conductivity/diameter stress:
  - `315_field_3d_0806_transfer_combined_conductivity_diameter_candidate`
- Regenerated product-facing artifacts:
  - `081_field_prediction_transfer_leaderboard_with_0806_combined_conductivity_diameter_candidate`
  - `082_field_prediction_current_product_pointer_with_0806_combined_conductivity_diameter_candidate`
- Fixed transfer leaderboard rows to prefer fitted depth/epsr over seed depth/epsr when optimizer best values are available.

## Key numbers
- 12 mm conductivity stress `313`:
  - initial loss `0.7915852070`
  - best loss/field L1 `0.7909555435`
  - improvement `0.0006296635`
  - best diameter `10.6360 mm`
  - final diameter `10.4929 mm`
  - best length `0.08136 m`
  - fitted local center x/depth `0.61246 m / 1.80544 m`
  - best epsr `3.54531`
  - best background conductivity `0.006203 S/m`
  - best anomaly conductivity `0.030462 S/m`
  - radius gradient max `1.14e-5`
- Combined synthesis `315`:
  - decision `finite_length_seed_stability_inconclusive`
  - best label `0806_sample42_source10_adamw_conductivity_diam12_iter8`
  - best field L1 `0.7909555435`
  - max loss improvement across evidence `0.0010514855`
  - near-best length range `0.08098-0.09357 m`
  - near-best diameter range `8.00037-10.63602 mm`
  - near-best epsr range `3.37157-3.55747`
  - near-best background conductivity range `0.004398-0.006203 S/m`
  - diameter status `diameter_gradient_available`
- Product pointer `082`:
  - current shipped 3D dataset remains `external_2025_pipe_0701`
  - current transfer candidate is `external_2025_pipe_0806`
  - `0806` best transfer candidate:
    - x/y/z `2.4576 m / 0.35 m / 1.80544 m`
    - local Fast-GPR center x `0.61246 m`
    - length range `0.08098-0.09357 m`
    - diameter range `8.00037-10.63602 mm`
    - epsr `3.54531`
    - background conductivity `0.006203 S/m`

## Current decision
The `0806` transfer candidate now has a stronger product-shaped prediction row: fitted z/depth, finite length, diameter range with a best larger-diameter candidate, epsr, and optimized conductivity. It is still not a release promotion because diameter remains seed-sensitive and the combined synthesis is inconclusive on unique diameter.

## What remains blocked
- Need one more larger-diameter seed stress to see whether diameter stabilizes near `10-12 mm` or drifts upward.
- Need repeat conductivity under a neighboring objective/window before claiming conductivity as stable.
- `0704` and `07011` still require source/window objective repair.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py tests/test_field_prediction_current_product_pointer.py -q`: `19 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_transfer_leaderboard.py -q`: `10 passed`.
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_current_product_pointer.py tests/test_field_prediction_transfer_leaderboard.py -q`: `6 passed`.
- `git diff --check` on touched scripts/tests/checkpoints: passed.
- Figures:
  - `313` optimizer figure is `1957 x 767` PNG.
  - `314` diameter sensitivity figure is `2394 x 767` PNG.
  - `315` combined synthesis figure is `2374 x 767` PNG.
  - `081` leaderboard figure is `2399 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/313_field_3d_0806_fastgpr_transfer_seed_sample42_profile_mean_source10_adamw_conductivity_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/314_field_3d_0806_transfer_conductivity_diameter_sensitivity`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/315_field_3d_0806_transfer_combined_conductivity_diameter_candidate`
- `outputs/validation_exp_on_field_data/product_leaderboard/081_field_prediction_transfer_leaderboard_with_0806_combined_conductivity_diameter_candidate`
- `outputs/validation_exp_on_field_data/product_leaderboard/082_field_prediction_current_product_pointer_with_0806_combined_conductivity_diameter_candidate`

## Next defensible task
Run a conductivity-enabled larger-diameter seed stress for `0806` from a 16 mm or 18 mm seed, then update the combined diameter sensitivity to decide whether the diameter range remains bounded near `8-11 mm` or expands.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
