# 2026-07-04 GSSI 51600S Unified Expanded-Spacing Checkpoint

## What changed

- Tested whether the expanded spacing that made `profiles1_3` short also keeps `profiles0_2` short under the same shared spacing assumption.
- New optimizer runs:
  - `451_gssi51600s_finite_length_3d_profiles0_2_explicit_offsets_y022_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `452_gssi51600s_finite_length_3d_profiles0_2_explicit_offsets_y028_domainz070_adamw_windows50_54_58_62_66_iter6`
- New synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/453_gssi51600s_finite_length_3d_unified_expanded_spacing_profiles0_2_1_3_adamw_y016`

## Key numbers

- `profiles0_2` at `0.22 m` spacing:
  - length: `0.183202177 m`
  - diameter: `17.295167 mm`
  - field L1: `0.955172062`
  - objective loss: `0.977655828`
- `profiles0_2` at `0.28 m` spacing:
  - length: `0.183206707 m`
  - diameter: `17.295167 mm`
  - field L1: `0.955171883`
  - objective loss: `0.977655590`
- Paired spacing interpretation:
  - at `0.16 m`, `profiles0_2` is short but `profiles1_3` is long
  - at `0.20 m`, tested `profiles1_3` remains long
  - at `0.22 m`, both tested subsets are short
  - at `0.28 m`, both tested subsets are short
- Unified synthesis near-best length range remains `0.183171555-0.217333928 m` because the `0.16-0.20 m` long branch is still near-best.

## Current decision

Measured crossline spacing is likely able to collapse the finite-length range. If the true spacing is at or above about `0.22 m`, the tested profile subsets favor the short `~0.183 m` finite length. If the true spacing is closer to `0.16-0.20 m`, the `profiles1_3` branch can remain long. This is stronger evidence that crossline geometry is the dominant release blocker.

## What remains blocked

- The true GSSI crossline spacing is still not known from metadata.
- The model cannot yet pick one spacing uniquely because losses are nearly flat over the near-best range.
- The current release-style card should remain confirmation-needed.

## Next defensible task

Either confirm the physical spacing from acquisition notes/metadata or add a profile-position estimator that reports the spacing uncertainty directly in the prediction card.

## Validation/resource checks

- Two additional `profiles0_2` explicit-spacing optimizer runs completed.
- `python run_field_3d_0701_finite_length_optimizer_seed_stability.py ...` generated artifact `453`.
- Figure `453/.../figures/field_3d_0701_finite_length_optimizer_seed_stability.png` was inspected numerically and structurally.
- Marathon request remains active; continue toward crossline-coordinate estimation or advisor-facing packaging.
