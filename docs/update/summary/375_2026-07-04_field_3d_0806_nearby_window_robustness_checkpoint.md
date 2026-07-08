# Field 3D 0806 Nearby-Window Robustness Checkpoint

## What changed
- Ran a same-recipe nearby-window robustness check for the release-promoted `external_2025_pipe_0806` predictor:
  - window pair `36,40`
  - AdamW
  - conductivity/material/xz/time-shift optimization
  - negative prediction polarity
  - starting diameter `12 mm`
- Generated optimizer artifact:
  - `341_field_3d_0806_fastgpr_transfer_seed_sample36_40_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- Synthesized the nearby-window run with the promoted joint-window run:
  - `342_field_3d_0806_transfer_polarity_neg_joint_window_robustness_36_40_38_42`

## Key numbers
- Nearby-window optimizer `341`:
  - decision `finite_length_scattered_optimizer_decreased_loss`
  - field L1 loss `0.7883857488632202`
  - objective loss `0.7883884906768799`
  - loss improvement `0.0036323070526123047`
  - diameter `13.893931 mm`
  - length-y `0.12912491 m`
  - local center x `0.597909 m`
  - depth `1.802372 m`
  - epsr `3.073993`
  - conductivity `0.00223710 S/m`
  - time shift `2.362925 ns`
  - mean runtime `12.51 s`
- Robustness synthesis `342`:
  - decision `finite_length_joint_xz_material_stability_supports_length_and_diameter`
  - best label remains `0806_sample38_42_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - field-L1-best label remains `0806_sample38_42_source10_adamw_conductivity_diam12_polarity_neg_iter8`
  - field-L1-best loss `0.7879638671875`
  - objective-best loss `0.78804612159729`
  - near-best diameter range `13.893931-13.902999 mm`
  - near-best length-y range `0.129125-0.129270 m`
  - near-best depth range `1.802372-1.808614 m`
  - diameter status `diameter_near_best_stable_narrow_range`
  - length status `near_best_length_stable`

## Current decision
The promoted default predictor is not replaced by the nearby-window run because the existing `38,42` joint-window fit still has the lower field L1. The new `36,40` run supports the same finite-length 3D interpretation and narrows the practical robustness story around diameter, length, and depth.

## What remains blocked
- This still validates one field event family, not a universal detector across all B-scans.
- `0704` and `07011` remain blocked transfer datasets.
- The next improvement should either add another robustness window for `0806` or move the same release workflow to another real dataset/profile.

## Validation/resource checks
- Figure for `342` opened successfully at `2434 x 767`, RGBA.
- `342` includes a README, run manifest, CSV rows, summary JSON, figure, and source snapshots.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/341_field_3d_0806_fastgpr_transfer_seed_sample36_40_profile_mean_source10_adamw_conductivity_diam12_polarity_neg_iter8`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/342_field_3d_0806_transfer_polarity_neg_joint_window_robustness_36_40_38_42`

## Next defensible task
Continue real-field robustness by running another same-recipe local window pair or by applying the promoted workflow to another real dataset/profile, while keeping the product default pointed at the current release-promoted `0806` result.

## Marathon status
The requested local marathon remains active. Continue improving the real-data prediction deliverable rather than stopping at this checkpoint.
