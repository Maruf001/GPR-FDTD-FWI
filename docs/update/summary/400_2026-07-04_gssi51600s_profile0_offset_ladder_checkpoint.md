# GSSI51600S Profile 0 Offset Ladder Checkpoint

## What Changed

- Used the new explicit profile-offset optimizer path to test whether profile `0` position changes can move the trusted GSSI `0-2` stack from the short branch to the longer `1-3` branch.
- Ran three five-window AdamW checks on profiles `0-2` in a `0.70 m` crossline domain:
  - explicit uniform offsets `[-0.16, 0.0, 0.16] m`.
  - profile `0` shifted outward `[-0.24, 0.0, 0.16] m`.
  - profile `0` shifted inward `[-0.08, 0.0, 0.16] m`.
- Synthesized the offset ladder into one stability artifact.

## Key Numbers

- Uniform control: `outputs/validation_exp_on_field_data/3d_geometry_inventory/426_gssi51600s_finite_length_3d_profiles0_2_explicit_uniform_offsets_y016_domainz070_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183171555 m`.
  - best diameter `17.295405 mm`.
  - best objective loss `0.977719069`.
  - best field L1 loss `0.955213547`.
- Profile `0` outward: `outputs/validation_exp_on_field_data/3d_geometry_inventory/427_gssi51600s_finite_length_3d_profiles0_2_profile0_outward_offsets_y016_domainz070_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183175027 m`.
  - best diameter `17.295277 mm`.
  - best objective loss `0.977726638`.
  - best field L1 loss `0.955233037`.
- Profile `0` inward: `outputs/validation_exp_on_field_data/3d_geometry_inventory/428_gssi51600s_finite_length_3d_profiles0_2_profile0_inward_offsets_y016_domainz070_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183240145 m`.
  - best diameter `17.296772 mm`.
  - best objective loss `1.047446966`.
  - best field L1 loss `1.007183433`.
- Offset ladder synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/429_gssi51600s_finite_length_3d_profile0_offset_ladder_profiles0_2_adamw_y016/`.
  - decision `finite_length_joint_xz_material_stability_supports_length_and_diameter`.
  - near-best labels `uniform_domain070`, `profile0_outward`.
  - near-best length range `0.183171555-0.183175027 m`.
  - near-best diameter range `17.295277-17.296772 mm`.

## Current Decision

Profile `0` offset changes do not produce the longer `0.216 m` branch in the `0-2` stack. Moving profile `0` outward leaves the short branch and fit quality nearly unchanged. Moving profile `0` inward worsens the fit substantially while still staying near the short length. This narrows the blocker: the long branch is not explained by a simple profile-0 crossline offset within this tested range.

The product default remains conservative because true profile spacing is still not metadata-confirmed and the `1-3` subset remains a near-best longer explanation.

## Validation

- All three optimizer runs completed with finite losses and gradients.
- The ladder synthesis figure was visually inspected and matches the numeric rows.

## Next Defensible Task

Refresh focused validation after the ladder, then test whether source/time alignment or profile amplitude weighting can explain why omitting profile `0` creates the longer `1-3` branch.

The local marathon request remains active.
