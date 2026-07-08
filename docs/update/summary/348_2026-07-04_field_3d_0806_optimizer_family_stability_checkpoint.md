# Field 3D 0806 Optimizer-Family Stability Checkpoint

## What changed
- Ran Adamax on the same `0806` profile-mean/10 MHz transfer seed:
  - `296_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_iter3`
- Synthesized AdamW vs Adamax:
  - `297_field_3d_0806_transfer_optimizer_family_synthesis`
- Regenerated the product transfer leaderboard with the optimizer-family `0806` evidence:
  - `071_field_prediction_transfer_leaderboard_with_0806_optimizer_family`

## Key numbers
- `0806` AdamW:
  - best loss `0.7946941853`
  - improvement `1.2159e-4`
- `0806` Adamax:
  - best loss `0.7946391702`
  - best field L1 `0.7946062088`
  - improvement `1.7661e-4`
  - best length `0.09385 m`
  - best diameter `8.00039 mm`
- Optimizer-family synthesis:
  - best label `0806_adamax`
  - best optimizer `adamax`
  - max improvement `1.7661e-4`
- Updated leaderboard:
  - `0806` status remains `transfer_optimizer_tiny_decrease_needs_confirmation`

## Current decision
The `0806` tiny descent repeats across AdamW and Adamax, with Adamax slightly better. This is a real but sub-threshold transfer signal. It is not a shippable 3D prediction yet.

## What remains blocked
- Improvement is still below the `1e-3` promotion threshold.
- Diameter/radius remains weak.
- Need source/objective improvement or a longer stability run before promoting transfer predictions.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `10 passed`.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/296_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/297_field_3d_0806_transfer_optimizer_family_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/071_field_prediction_transfer_leaderboard_with_0806_optimizer_family`

## Next defensible task
Run a slightly longer `0806` Adamax check, still bounded, to see whether the tiny descent accumulates or plateaus. Keep the product status blocked unless it crosses the promotion threshold and remains stable.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
