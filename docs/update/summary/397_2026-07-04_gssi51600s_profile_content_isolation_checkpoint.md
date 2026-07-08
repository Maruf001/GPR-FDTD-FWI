# GSSI51600S Profile-Content Isolation Checkpoint

## What Changed

- Built two diagnostic GSSI profile-subset stacks:
  - original profiles `0,1,3`.
  - original profiles `0,2,3`.
- Generated finite-length seeds for both diagnostic stacks.
- Ran the same five-window AdamW 3D finite-length optimizer used in the current GSSI profile-subset checks.
- Synthesized the new content-isolation runs against the prior `0-2` and `1-3` three-profile runs.

## Key Numbers

- `0,1,3` diagnostic stack: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/096_gssi51600s_profile_subset_stack_original0_1_3_content_isolation/`.
- `0,2,3` diagnostic stack: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/097_gssi51600s_profile_subset_stack_original0_2_3_content_isolation/`.
- `0,1,3` optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/420_gssi51600s_finite_length_3d_surface075_profiles0_1_3_content_seed099_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183369428 m`.
  - best diameter `17.297987 mm`.
  - best objective loss `0.984145999`.
  - best field L1 loss `0.961618125`.
- `0,2,3` optimizer: `outputs/validation_exp_on_field_data/3d_geometry_inventory/421_gssi51600s_finite_length_3d_surface075_profiles0_2_3_content_seed098_y016_adamw_windows50_54_58_62_66_iter6/`.
  - best length `0.183684886 m`.
  - best diameter `17.308040 mm`.
  - best objective loss `0.981772721`.
  - best field L1 loss `0.963648319`.
- Content-isolation synthesis: `outputs/validation_exp_on_field_data/3d_geometry_inventory/422_gssi51600s_finite_length_3d_profile_content_isolation_synthesis_adamw_y016/`.
  - decision `finite_length_seed_stability_inconclusive`.
  - best label `profiles0_2`.
  - near-best labels `profiles0_2`, `profiles1_3`, `content0_1_3`, `content0_2_3`.
  - near-best length range `0.183171824-0.216162652 m`.
  - near-best diameter range `17.295390-17.315585 mm`.

## Current Decision

The longer `1-3` branch is not explained by the presence of the high-energy/latest profile `3` alone. Both diagnostic stacks that include profile `0` stayed near the shorter `0.183 m` length branch, even when profile `3` was included. The long branch appears when profile `0` is omitted in the three-profile `1-3` stack, which points to profile-content or acquisition-layout interactions rather than a simple single-profile effect.

The noncontiguous stacks are diagnostic only because the current Fast-GPR bridge still assumes evenly spaced profiles. They do not update the product default. They narrow the next confirmation question: profile `0` and unresolved crossline geometry are the most important current blockers for turning the GSSI finite-length output into a release-style claim.

## Validation

- Both optimizer runs completed with finite losses and gradients.
- The synthesis figure was visually inspected and matches the numeric rows.
- Prior focused tests for the profile stack adapter and event-content audit passed before this run.

## Next Defensible Task

Run focused validation after the new outputs, then decide whether to add a profile-0 influence audit or a geometry-assumption ladder that tests profile `0` spacing/offset explicitly.

The local marathon request remains active.
