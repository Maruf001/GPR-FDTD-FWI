# 2026-07-04 GSSI 51600S Source-Receiver Geometry Checkpoint

## What changed

- Ran a source-receiver geometry diagnostic on the trusted GSSI 51600S field stack.
- Compared the current collocated source/receiver assumption against a 60 mm bistatic source-receiver separation at the same 0.22 m profile-spacing branch.
- Included two profile subsets, profiles 0-2 and profiles 1-3, so the test checks both sides of the current finite-length ambiguity.

## Key numbers

- Collocated profiles 0-2:
  - field L1 loss: `0.9551720619`
  - objective loss: `0.9776558280`
  - length: `0.1832021773 m`
  - diameter: `17.29516685 mm`
- Collocated profiles 1-3:
  - field L1 loss: `0.9611356854`
  - objective loss: `0.9786204100`
  - length: `0.1835240722 m`
  - diameter: `17.31610671 mm`
- 60 mm bistatic profiles 0-2:
  - field L1 loss: `0.9721285105`
  - objective loss: `0.9971855879`
  - length: `0.1832105666 m`
  - diameter: `17.30643585 mm`
- 60 mm bistatic profiles 1-3:
  - field L1 loss: `0.9784704447`
  - objective loss: `1.0015161037`
  - length: `0.2172190398 m`
  - diameter: `17.29406416 mm`

## Current decision

This is a diagnostic-only source/receiver geometry check. Under the current field objective, the 60 mm bistatic assumption worsens both tested profile-subset fits relative to the collocated assumption, so it should not be used to promote a single finite-length product claim.

The result narrows the immediate product path: crossline profile spacing remains the larger release blocker, while antenna phase-center/source-receiver separation remains a secondary geometry uncertainty to keep in the model interface.

## What remains blocked

- The actual GSSI antenna phase-center separation and acquisition geometry have not been confirmed from local metadata.
- The DZX sidecars confirm along-scan sampling, but they do not provide the crossline spacing between the four profiles or a full antenna phase-center model.
- The current release-style product should continue to report a geometry-conditioned length range instead of a single length.

## Next defensible task

Continue with the GSSI-first product path: either locate measured crossline coordinates/antenna geometry or add profile-position/antenna-offset parameters to the predictor so it reports the fitted candidate conditioned on those geometry assumptions.

## Artifact paths

- Source/receiver diagnostic bundle: `outputs/validation_exp_on_field_data/3d_geometry_inventory/456_gssi51600s_finite_length_3d_source_receiver_geometry_check_y022_profiles0_2_1_3_adamw/`
- Collocated profiles 0-2 source run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/451_gssi51600s_finite_length_3d_profiles0_2_explicit_offsets_y022_domainz070_adamw_windows50_54_58_62_66_iter6/`
- Collocated profiles 1-3 source run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/447_gssi51600s_finite_length_3d_profiles1_3_explicit_offsets_y022_domainz070_adamw_windows50_54_58_62_66_iter6/`
- 60 mm bistatic profiles 0-2 source run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/454_gssi51600s_finite_length_3d_profiles0_2_offsets_y022_bistatic060_y020_080_domainz070_adamw_windows50_54_58_62_66_iter6/`
- 60 mm bistatic profiles 1-3 source run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/455_gssi51600s_finite_length_3d_profiles1_3_offsets_y022_bistatic060_y020_080_domainz070_adamw_windows50_54_58_62_66_iter6/`

## Validation/resource checks

- The diagnostic summary and rows are finite.
- The milestone output contains script snapshots and a snapshot manifest.
- Focused validation is still pending after this documentation update.
- The local marathon request remains active.
