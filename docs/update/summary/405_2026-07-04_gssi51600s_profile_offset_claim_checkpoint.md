# 2026-07-04 GSSI 51600S Profile-Offset Claim Checkpoint

## What changed

- Ran an explicit profile-offset sensitivity ladder for the trusted GSSI `profiles1_3` branch.
- The goal was to test whether the long finite-length branch is controlled by assumed crossline profile spacing rather than by event windowing or time-shift prior.
- New optimizer runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/442_gssi51600s_finite_length_3d_profiles1_3_explicit_uniform_offsets_y016_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/443_gssi51600s_finite_length_3d_profiles1_3_explicit_compressed_offsets_y010_domainz070_adamw_windows50_54_58_62_66_iter6`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/444_gssi51600s_finite_length_3d_profiles1_3_explicit_expanded_offsets_y024_domainz070_adamw_windows50_54_58_62_66_iter6`
- New synthesis and product claim card:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/445_gssi51600s_finite_length_3d_profiles1_3_explicit_offset_ladder_adamw_y016`
  - `run_gssi51600s_profile_offset_claim_card.py`
  - `tests/test_gssi51600s_profile_offset_claim_card.py`
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/104_gssi51600s_profile_offset_claim_card_current`

## Key numbers

- Explicit `0.16 m` offsets reproduced the long branch:
  - length: `0.216163829 m`
  - diameter: `17.315600 mm`
  - field L1: `0.961358964`
  - objective loss: `0.979082942`
- Explicit compressed `0.10 m` offsets moved short but worsened fit:
  - length: `0.183204412 m`
  - diameter: `17.298795 mm`
  - field L1: `1.020882726`
  - objective loss: `1.057519317`
- Explicit expanded `0.24 m` offsets moved short with comparable/slightly better fit:
  - length: `0.183567300 m`
  - diameter: `17.316112 mm`
  - field L1: `0.961140275`
  - objective loss: `0.978622854`
- Near-best offset-ladder range:
  - length: `0.183567300-0.216163829 m`
  - diameter: `17.315585-17.316112 mm`
  - near-best labels: `implicit_y016`, `explicit_y016_domain070`, `explicit_y024_domain070`

## Current decision

The strict GSSI profile-offset claim-card decision is:

`crossline_geometry_controls_length_do_not_ship_single_length`

This is the strongest current explanation for the finite-length split. The tested offset assumptions can flip `profiles1_3` from long to short without a meaningful diameter change and without worsening the best fit in the expanded-offset case.

## What remains blocked

- The current field-data product should not report a single finite length without either measured crossline coordinates or an optimizer that estimates profile positions.
- The GSSI candidate diameter is now much tighter in this offset ladder than the broader historical product range, but diameter should still be reported under the conservative product policy until crossline geometry is resolved.
- The coordinate mapping inside the Fast-GPR adapter uses the profile-offset axis as the stack/profile axis; this is useful for sensitivity testing, but the physical crossline spacing still needs acquisition confirmation.

## Next defensible task

Build the next product-facing predictor branch around explicit crossline-geometry uncertainty: either a small offset-parameter optimizer/scan for profile positions, or a release-style prediction card that reports location, diameter, material estimates, and finite-length range conditioned on crossline spacing assumptions.

## Validation/resource checks

- Three explicit-offset optimizer runs completed.
- `python run_field_3d_0701_finite_length_optimizer_seed_stability.py ...` generated artifact `445`.
- `python run_gssi51600s_profile_offset_claim_card.py ...` generated artifact `104`.
- `python -m py_compile run_gssi51600s_profile_offset_claim_card.py` passed.
- `python -m pytest tests/test_gssi51600s_profile_offset_claim_card.py -q` passed: `2 passed`.
- Figure `104/.../figures/gssi51600s_profile_offset_claim_card.png` was visually inspected.
- Marathon request remains active; continue toward explicit crossline-geometry uncertainty in the predictor deliverable.
