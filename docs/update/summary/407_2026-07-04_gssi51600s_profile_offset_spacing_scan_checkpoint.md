# 2026-07-04 GSSI 51600S Profile-Offset Spacing Scan Checkpoint

## What changed

- Extended the `profiles1_3` explicit profile-offset ladder into a finer spacing scan.
- New optimizer runs:
  - `446_gssi51600s_finite_length_3d_profiles1_3_explicit_offsets_y020_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `447_gssi51600s_finite_length_3d_profiles1_3_explicit_offsets_y022_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `448_gssi51600s_finite_length_3d_profiles1_3_explicit_offsets_y026_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `449_gssi51600s_finite_length_3d_profiles1_3_explicit_offsets_y028_domainz070_adamw_windows50_54_58_62_66_iter6`
- New spacing-scan synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/450_gssi51600s_finite_length_3d_profiles1_3_explicit_offset_spacing_scan_adamw_y016`
- Updated the profile-offset claim card default to the fine scan and regenerated:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/105_gssi51600s_profile_offset_claim_card_current`
- Updated the current predictor query to consume the refined offset card.

## Key numbers

- `0.10 m` spacing: length `0.183204412 m`, field L1 `1.020882726`, objective `1.057519317`
- `0.16 m` spacing: length `0.216163829 m`, field L1 `0.961358964`, objective `0.979082942`
- `0.20 m` spacing: length `0.217333928 m`, field L1 `0.961262465`, objective `0.978628755`
- `0.22 m` spacing: length `0.183524072 m`, field L1 `0.961138844`, objective `0.978620410`
- `0.24 m` spacing: length `0.183567300 m`, field L1 `0.961140275`, objective `0.978622854`
- `0.26 m` spacing: length `0.183605716 m`, field L1 `0.961138427`, objective `0.978620410`
- `0.28 m` spacing: length `0.183611006 m`, field L1 `0.961137116`, objective `0.978620291`

The branch transition occurs between `0.20 m` and `0.22 m` in this scan. The objective surface is nearly flat from `0.16-0.28 m`, except that the compressed `0.10 m` case is clearly worse.

## Current decision

The refined profile-offset claim-card decision remains:

`crossline_geometry_controls_length_do_not_ship_single_length`

The best scanned spacing is `0.28 m`, but the loss difference across the `0.16-0.28 m` near-best interval is too small to treat the spacing estimate as unique. The product should report geometry-conditioned range, not a single length.

## What remains blocked

- Crossline profile coordinates are the dominant unresolved field-data variable for finite-length prediction.
- The scan gives a useful offset-conditioned map, but it is still a discrete sensitivity scan rather than a continuous profile-position optimizer.
- The current product query now surfaces this geometry context, but release-style claims still need measured or explicitly optimized profile positions.

## Next defensible task

Build a small release-style GSSI prediction card that reports:

- candidate x, z, diameter, relative permittivity, and conductivity from the current best product default
- finite-length range under current conservative policy
- offset-conditioned `profiles1_3` branch map from the spacing scan
- explicit statement that measured crossline profile positions are required to collapse the length range

## Validation/resource checks

- Four additional explicit-offset optimizer runs completed.
- `python run_field_3d_0701_finite_length_optimizer_seed_stability.py ...` generated artifact `450`.
- `python run_gssi51600s_profile_offset_claim_card.py ...` generated artifact `105`.
- `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty` now reports the refined spacing context.
- Figure `105/.../figures/gssi51600s_profile_offset_claim_card.png` was visually inspected.
- Marathon request remains active; continue toward a release-style GSSI prediction card.
