# Field 3D 0806 Transfer Coverage Checkpoint

## What changed
- Generated a real-stack `0806` transfer seed:
  - `292_field_3d_0806_transfer_seed_energy_window_profile_axis_y`
- Ran bounded Fast-GPR optimizer checks:
  - `293_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamw_iter1`
  - `294_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamw_iter3`
- Synthesized `0806` transfer result:
  - `295_field_3d_0806_transfer_objective_synthesis`
- Regenerated product transfer leaderboard with `0806` included:
  - `070_field_prediction_transfer_leaderboard_with_0806_tiny_descent`

## Key numbers
- `0806` seed:
  - x `2.4576 m`
  - profile-axis y `0.35 m`
  - z `1.7406 m`
  - profile window `2-5`
  - sample start `38`
  - trace window `88-103`
- `0806` one-step:
  - loss `0.7948157787`
- `0806` three-step:
  - best loss `0.7946941853`
  - best field L1 `0.7946543097`
  - improvement `1.2159e-4`
  - best length `0.09356 m`
  - best diameter `8.00039 mm`
  - best depth `1.76024 m`
  - best epsr `3.37192`
- Product leaderboard status:
  - `0806`: `transfer_optimizer_tiny_decrease_needs_confirmation`

## Current decision
`0806` completes the current transfer coverage table. It is the first transfer stack with nonzero optimizer descent, but the improvement is below the `1e-3` promotion threshold. It should not be shipped as a geometry/material prediction yet.

## What remains blocked
- Need repeatability/stability around the `0806` tiny descent before it can influence claims.
- Diameter remains flat.
- `0704` and `07011` remain no-descent transfer-blocked.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_stack_transfer_seed.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `16 passed`.
- `git diff --check` on touched files: passed.
- Updated leaderboard figure exists as PNG, `2399 x 767`.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/292_field_3d_0806_transfer_seed_energy_window_profile_axis_y`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/293_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamw_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/294_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamw_iter3`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/295_field_3d_0806_transfer_objective_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/070_field_prediction_transfer_leaderboard_with_0806_tiny_descent`

## Next defensible task
Stress the `0806` tiny descent with one or two stability checks:
- repeat AdamW with lower learning rate;
- test Adamax at the same seed;
- keep promotion blocked unless the decrease repeats and grows beyond threshold.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
