# Field 3D 0806 Threshold-Descent Checkpoint

## What changed
- Ran a bounded longer `0806` Adamax transfer optimizer:
  - `298_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_iter8`
- Synthesized with earlier `0806` AdamW/Adamax runs:
  - `299_field_3d_0806_transfer_adamax_long_run_synthesis`
- Regenerated product transfer leaderboard:
  - `072_field_prediction_transfer_leaderboard_with_0806_threshold_descent`

## Key numbers
- `0806` Adamax 8-iteration run:
  - initial loss `0.7948157787`
  - best loss `0.7937642932`
  - best field L1 `0.7937612534`
  - loss improvement `0.0010514855`
  - best iteration `7`
  - best length `0.08458 m`
  - best diameter `8.00037 mm`
  - best local center x `0.58421 m`
  - best center depth `1.79299 m`
  - best epsr `3.52168`
  - best anomaly delta epsr `0.77545`
  - best time shift `2.43905 ns`
- Updated leaderboard status:
  - `0806`: `transfer_optimizer_decreased_loss`
  - `0704` and `07011`: still `transfer_seed_fit_optimizer_blocked`
  - `0701`: still the only shippable 3D release candidate

## Current decision
`0806` is now the first transfer stack with optimizer descent above the `1e-3` threshold. It is not yet shippable, but it is a credible transfer follow-up candidate requiring stability, seed sensitivity, and diameter checks.

## What remains blocked
- Need repeatability around the 8-iteration result.
- Need check whether the descent depends on length/diameter seed.
- Diameter remains effectively unchanged near `8 mm`; no unique diameter claim.
- Need decide whether `0806` represents the same physical target type as the desired deliverable before promoting beyond transfer candidate.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `10 passed`.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/298_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/299_field_3d_0806_transfer_adamax_long_run_synthesis`
- `outputs/validation_exp_on_field_data/product_leaderboard/072_field_prediction_transfer_leaderboard_with_0806_threshold_descent`

## Next defensible task
Run a seed sensitivity check on `0806`:
- diameter seed `12 mm` at the same settings;
- optionally length seed `0.20 m`;
- synthesize whether the descent and geometry are stable or seed-sensitive.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
