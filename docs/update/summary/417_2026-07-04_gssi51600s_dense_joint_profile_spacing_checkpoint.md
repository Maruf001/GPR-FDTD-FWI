# 2026-07-04 GSSI 51600S Dense Joint Profile-Spacing Checkpoint

## What changed

- Filled missing profiles 0-2 spacing rows at `0.20 m`, `0.24 m`, and `0.26 m`.
- Rebuilt the two-subset dense spacing synthesis with profiles 0-2 and profiles 1-3 at common spacings `0.16`, `0.20`, `0.22`, `0.24`, `0.26`, and `0.28 m`.
- Recomputed the joint profile-spacing posterior on the denser evidence.
- Updated the live predictor default and current bundle to use the dense joint spacing card.

## Key numbers

- New profiles 0-2 fill-in runs:
  - `0.20 m`: length `0.1832225174 m`, diameter `17.29518548 mm`, field L1 `0.9551727176`
  - `0.24 m`: length `0.1832049042 m`, diameter `17.29516685 mm`, field L1 `0.9551718831`
  - `0.26 m`: length `0.1832064539 m`, diameter `17.29516685 mm`, field L1 `0.9551718831`
- Dense 12-row synthesis artifact: `461_gssi51600s_finite_length_3d_unified_dense_spacing_profiles0_2_1_3_adamw_y016`
- Dense joint spacing card artifact: `116_gssi51600s_joint_profile_spacing_card_dense_current`
- Current bundle with dense joint spacing: `117_gssi51600s_current_prediction_bundle_with_dense_joint_spacing_context`
- Dense joint MAP spacing: `0.22 m`
- Dense joint weighted spacing: `0.2360949450 m`
- Dense joint 90% spacing interval: `0.16-0.28 m`
- Dense joint weighted length: `0.1873618514 m`
- Dense joint 90% mean-length interval: `0.1833631247-0.2002782226 m`
- Dense joint weighted diameter: `17.30561287 mm`
- Dense joint weighted relative permittivity: `2.041986999`
- Dense joint weighted conductivity: `0.0026600899 S/m`
- Dense short-only branch weight: `0.7630099110`
- Dense contains-long branch weight: `0.2369900890`

## Current decision

The denser two-subset estimate still prefers the short finite-length branch, but more conservatively than the sparse joint card. Adding the `0.20 m`, `0.24 m`, and `0.26 m` profiles 0-2 rows reduced the short-only branch weight from about `0.88` to about `0.76`, because the `0.20 m` common spacing still contains the long profiles 1-3 branch.

The product state remains geometry-conditioned: the best-fit and posterior evidence now lean toward the short branch, but the 90% spacing interval still spans `0.16-0.28 m`.

## What remains blocked

- Local GSSI metadata still does not provide measured crossline profile coordinates.
- The dense joint estimate is an optimizer-derived geometry estimate, not measured survey geometry.
- A single release-style finite-length claim should still wait for measured crossline spacing or a validated profile-position optimizer.

## Note on failed launch

- One mistyped `0.26 m` launch used a wrong stack manifest path and failed before model execution.
- It created an empty partial output directory `459_gssi51600s_finite_length_3d_profiles0_2_explicit_offsets_y026_domainz070_adamw_windows50_54_58_62_66_iter6`.
- The successful `0.26 m` row is `460_gssi51600s_finite_length_3d_profiles0_2_explicit_offsets_y026_domainz070_adamw_windows50_54_58_62_66_iter6`.
- The dense synthesis excludes the empty partial output.

## Next defensible task

Use the dense joint spacing card as the current strongest geometry-conditioned estimate, then either add a true bounded profile-position optimizer or locate measured crossline geometry so the predictor can promote a single 3D length with a defensible source.

## Validation/resource checks

- GPU was available before the fill-in runs.
- The three successful fill-in optimizer runs are finite and decreased loss.
- Dense synthesis and dense joint card completed.
- Focused validation is pending after this checkpoint.
- The local marathon request remains active.
