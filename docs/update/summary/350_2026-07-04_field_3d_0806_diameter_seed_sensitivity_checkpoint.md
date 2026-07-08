# Field 3D 0806 Diameter Seed Sensitivity Checkpoint

## What changed
- Ran an `0806` transfer optimizer with diameter seed `12 mm`:
  - `300_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_diam12_iter8`
- Synthesized diameter-seed sensitivity:
  - `301_field_3d_0806_transfer_diameter_seed_sensitivity`
- Regenerated product transfer leaderboard:
  - `073_field_prediction_transfer_leaderboard_with_0806_diameter_sensitivity`

## Key numbers
- `0806` diameter seed `8 mm`:
  - best loss `0.7937642932`
  - best length `0.08458 m`
  - best diameter `8.00037 mm`
  - best epsr `3.52168`
- `0806` diameter seed `12 mm`:
  - best loss `0.7939065099`
  - best length `0.08458 m`
  - best diameter `11.99956 mm`
  - best epsr `3.52145`
- Sensitivity synthesis:
  - best label `0806_diam08_adamax_iter8`
  - near-best diameter range `8.00037-11.99956 mm`
  - length range stable near `0.0846 m`
  - max improvement `0.0010848`
  - diameter status `diameter_not_identified_gradient_negligible`
- Updated leaderboard:
  - `0806`: `transfer_optimizer_decreased_loss`
  - diameter range `8.00037-11.99956 mm`
  - claim boundary still blocks final release pending stability/diameter checks.

## Current decision
`0806` keeps a threshold-level optimizer descent across diameter seeds, but diameter is not uniquely identified. The best product-safe statement is a transfer candidate with stable length/depth/material trend and a near-best diameter range, not a scalar diameter claim.

## What remains blocked
- Need length-seed sensitivity.
- Need repeatability over window/source settings.
- Need stronger evidence before shipping `0806` as a product prediction.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `10 passed`.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/300_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/301_field_3d_0806_transfer_diameter_seed_sensitivity`
- `outputs/validation_exp_on_field_data/product_leaderboard/073_field_prediction_transfer_leaderboard_with_0806_diameter_sensitivity`

## Next defensible task
Run `0806` length seed `0.20 m` with the same Adamax settings. This tests whether the apparent finite length near `0.085 m` is stable or a local basin selected by the `0.10 m` seed.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
