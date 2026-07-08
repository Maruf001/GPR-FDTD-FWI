# Field 3D 0806 Two-Window Diameter Family Checkpoint

## What changed
- Tested whether a stronger two-window objective reduces `0806` diameter ambiguity.
- Ran conductivity-enabled AdamW two-window fits using sample starts `38,42`:
  - `326_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam12_iter8`
  - `327_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam16_iter8`
  - `328_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam08_iter8`
- Synthesized the two-window seed family:
  - `329_field_3d_0806_transfer_two_window_diameter_seed_family`

## Key numbers
- Two-window 12 mm seed `326`:
  - best loss `0.7924322486`
  - best field L1 `0.7922770977`
  - best diameter `10.8039 mm`
  - best length `0.08352 m`
  - best depth `1.92179 m`
  - epsr `3.51423`
  - background conductivity `0.005750 S/m`
- Two-window 16 mm seed `327`:
  - best field L1 `0.7925331593`
  - best diameter `15.3655 mm`
  - best length `0.09357 m`
- Two-window 8 mm seed `328`:
  - best field L1 `0.7924583554`
  - best diameter `8.0015 mm`
  - best length `0.09357 m`
- Two-window synthesis `329`:
  - decision `finite_length_seed_stability_inconclusive`
  - best label `0806_sample38_42_adamw_conductivity_diam12_iter8`
  - near-best diameter range `8.0015-15.3655 mm`
  - near-best length range `0.08352-0.09357 m`
  - near-best field L1 range `0.7922771-0.7925332`
  - near-best epsr range `3.37164-3.51423`
  - near-best background conductivity range `0.004396-0.005750 S/m`

## Current decision
The two-window objective does not solve diameter ambiguity. It confirms a best diameter near `10.8 mm`, but 8 mm and 15.4 mm alternatives remain near-best with similar losses. The remaining blocker is real, not just a single-window artifact.

## What remains blocked
- Unique diameter release claim remains unsupported.
- Further same-objective seed sweeps are unlikely to change the conclusion.
- To reduce diameter uncertainty, the next move needs a physical prior/policy, additional receiver/objective constraint, or external calibration/ground truth.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py tests/test_field_prediction_release_promotion_checklist.py -q`: `15 passed`.
- `git diff --check` on touched scripts/tests/checkpoints: passed.
- Figures:
  - `326` optimizer figure is `1957 x 767` PNG.
  - `327` optimizer figure is `1957 x 767` PNG.
  - `328` optimizer figure is `1957 x 767` PNG.
  - `329` synthesis figure is `2381 x 767` PNG.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/326_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam12_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/327_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam16_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/328_field_3d_0806_fastgpr_transfer_seed_sample38_42_profile_mean_source10_adamw_conductivity_diam08_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/329_field_3d_0806_transfer_two_window_diameter_seed_family`

## Next defensible task
Draft and implement a release policy variant that can ship a diameter range with a best candidate, instead of requiring unique diameter, while keeping the claim boundary explicit.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
