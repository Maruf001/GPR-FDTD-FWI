# Field 3D 0806 Length Seed Sensitivity Checkpoint

## What changed
- Ran an `0806` transfer optimizer with length seed `0.20 m`:
  - `302_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_len020_iter8`
- Synthesized length/diameter seed sensitivity:
  - `303_field_3d_0806_transfer_length_seed_sensitivity`
- Updated transfer leaderboard to expose transfer length ranges:
  - `074_field_prediction_transfer_leaderboard_with_0806_length_sensitivity`

## Key numbers
- Best `0.10 m` length seed:
  - best loss `0.7937642932`
  - best length `0.08458 m`
- `0.20 m` length seed:
  - best loss `0.7955755591`
  - best length `0.16408 m`
- Diameter `12 mm` seed:
  - best loss `0.7939065099`
  - best length `0.08458 m`
- Synthesis:
  - decision `finite_length_seed_stability_inconclusive`
  - length status `finite_length_seed_sensitive`
  - near-best length range `0.08458-0.16408 m`
  - near-best diameter range `8.00034-11.99956 mm`
  - max improvement `0.001547`
- Updated leaderboard:
  - `0806` remains `transfer_optimizer_decreased_loss`
  - length range now reported as `0.08458-0.16408 m`
  - diameter range `8.00034-11.99956 mm`

## Current decision
`0806` has threshold-level transfer descent, but finite length is seed-sensitive. This supports reporting a transfer candidate range, not a unique length or diameter.

## What remains blocked
- Need repeatability over sample/window/source choices.
- Need stronger source/objective evidence before shipping `0806`.
- Need distinguish whether `0806` geometry corresponds to the intended rebar/pipe target class.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_transfer_leaderboard.py tests/test_field_3d_0701_finite_length_optimizer_seed_stability.py -q`: `10 passed`.
- `git diff --check` on touched files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/302_field_3d_0806_fastgpr_transfer_seed_profile_mean_source10_adamax_len020_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/303_field_3d_0806_transfer_length_seed_sensitivity`
- `outputs/validation_exp_on_field_data/product_leaderboard/074_field_prediction_transfer_leaderboard_with_0806_length_sensitivity`

## Next defensible task
Run a source/window sensitivity check around the successful `0806` candidate, starting with sample start `42` or source frequency `20 MHz`, to see if the threshold descent is robust to nearby acquisition choices.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
