# GSSI51600S Profile-Subset Y-Spacing Sensitivity Checkpoint

## What Changed

- Added y-spacing sensitivity checks for the two near-best trusted GSSI profile subsets:
  - profiles `0-2` at assumed `0.10 m` spacing.
  - profiles `1-3` at assumed `0.10 m` spacing.
- Compared those runs to the existing `0.16 m` spacing runs for the same two profile subsets, using the same five-window AdamW joint optimizer.
- Generated a four-run synthesis to separate crossline-spacing effects from profile-subset effects.

## Key Numbers

- Synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/417_gssi51600s_finite_length_3d_profiles0_2_1_3_y010_y016_sensitivity_adamw_windows50_54_58_62_66/`.
- Decision: `finite_length_seed_stability_inconclusive`.
- Near-best labels: `p0_2_y016`, `p1_3_y016`.
- Near-best length range: `0.183172-0.216163 m`.
- Near-best diameter range: `17.295390-17.315585 mm`.
- y=`0.10 m` profile `0-2`: length `0.183156 m`, diameter `17.300300 mm`, objective loss `1.038994`.
- y=`0.16 m` profile `0-2`: length `0.183172 m`, diameter `17.295390 mm`, objective loss `0.977719`.
- y=`0.10 m` profile `1-3`: length `0.183204 m`, diameter `17.298795 mm`, objective loss `1.057518`.
- y=`0.16 m` profile `1-3`: length `0.216163 m`, diameter `17.315585 mm`, objective loss `0.979077`.

## Current Decision

The shorter length can be forced by shrinking the assumed crossline spacing to `0.10 m`, but both profile subsets fit worse under that assumption. The current evidence therefore supports keeping the product query conservative under the profile-window range while continuing to search for measured crossline spacing or acquisition notes.

## Next Defensible Task

Test whether source/receiver crossline placement or profile ordering can explain why profiles `0-2` and `1-3` prefer different finite lengths at the better-fitting `0.16 m` spacing.

The local marathon request remains active.
