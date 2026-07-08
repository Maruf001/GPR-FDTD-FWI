# External 2025 GGAE Profile Outcome Checkpoint

Date: 2026-07-03

## Scope

This checkpoint consolidates the external 2025 GGAE IFWI field-profile outcomes into a searchable method-control artifact. It is not an advisor packet; it is the current profile-level status for real-field validation.

## Artifact

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/222_external_2025_ggae_profile_outcome_synthesis`

Decision:

- `external_2025_ggae_profile_outcomes_three_provisional_one_failed_diameter_not_claimed`

## Profile Outcomes

- `190424AA_LID10002_rank2_right_shift`
  - Best family: `surface_prune_w030_right_shift`
  - Best holdout: `0.6064098179340363`
  - x: `0.13384640216827393 m`
  - cover: `0.093923419713974 m`
  - claim use: `location_cover_provisional`

- `LS1_LID10001_rank2`
  - Best family: `surface_prune_w030`
  - Best holdout: `0.7661208808422089`
  - x: `0.2962820678949356 m`
  - cover: `0.06934374198317528 m`
  - claim use: `location_cover_provisional`

- `LS1_LID10002`
  - Best family: `baseline_event_window_fixed_radius`
  - Best holdout: `0.8706095814704895`
  - x: `0.06459338217973709 m`
  - cover: `0.09434668347239494 m`
  - claim use: `location_cover_provisional`

- `LDH1_LID10001_rank2`
  - Best family: `forced_svd_window_075_135`
  - Best holdout: `1.6379399299621582`
  - x: `0.41470007598400116 m`
  - cover: `0.07516024261713028 m`
  - claim use: `none`

Summary:

- Tested profiles: 4
- Provisional profiles: 3
- Failed profiles: 1
- Median provisional holdout: `0.7661208808422089`
- Best profile: `190424AA_LID10002_rank2_right_shift`
- Worst profile: `LDH1_LID10001_rank2`
- Diameter claim: `not_claimed_all_profiles_fixed_or_nonidentifiable_radius`
- Material claim: `not_claimed_no_independent_permittivity_validation`

## Claim Boundary

Use only profile-scoped event-window location/cover claims for the three profiles below the provisional threshold. Do not claim global-profile prediction, autonomous candidate selection, diameter, concrete permittivity, or material inversion.

## Verification

- `python -m py_compile run_ggae2025_external_2025_profile_outcome_synthesis.py`
- `python -m pytest tests/test_ggae2025_external_2025_profile_outcome_synthesis.py -q`
- `python run_ggae2025_external_2025_profile_outcome_synthesis.py`
- `git diff --check`

## Next Step

Use this profile outcome table to pick the next field-data branch. The strongest option is independent confirmation on another external profile/candidate; the highest-risk option is trying to turn LDH1 into a validated profile, which has already resisted several method variants.
