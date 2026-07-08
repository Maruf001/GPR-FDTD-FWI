# External 2025 Surface-Prune Four-Profile Boundary Checkpoint

Date: 2026-07-03

## Scope

This checkpoint updates the GGAE2025/Fast-GPR-FWI-style surface-prune optimizer boundary after adding `LS1_LID10002` to the transfer audit. The test uses the same `w=0.3` shallow/source-zone surface penalty.

## New Runs

- `219_external_2025_ls1_lid10002_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_surface_prune_w030`
- `220_external_2025_ls1_lid10002_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_surface_prune_w030`

## Updated Boundary Artifact

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/221_external_2025_ggae_surface_prune_profile_boundary_synthesis`

Decision:

- `external_2025_ggae_surface_prune_w030_profile_scoped_ldh1_boundary`

Four-profile comparison:

- `190424AA_LID10002_rank2_right_shift`: `0.6398650705814362 -> 0.6064098179340363`
- `LS1_LID10001_rank2`: `0.8244783282279968 -> 0.7661208808422089`
- `LDH1_LID10001_rank2`: `1.8228492140769958 -> 1.8277581930160522`
- `LS1_LID10002`: `0.8706095814704895 -> 0.8755199313163757`

Summary:

- Tested profiles: 4
- Improved profiles: 2
- Validated profiles under threshold: 3
- Failed profiles: 1
- Improved profiles: `190424AA_LID10002_rank2_right_shift`, `LS1_LID10001_rank2`
- Validated profiles: `190424AA_LID10002_rank2_right_shift`, `LS1_LID10001_rank2`, `LS1_LID10002`
- Failed profile: `LDH1_LID10001_rank2`
- Mean surface-prune delta: `-0.02049834281206131`

## Leaderboard Update

The boundary row now points at the four-profile artifact:

- Method variant: `external_2025_surface_prune_profile_boundary`
- Objective loss: `1.8277581930160522`
- Evidence score: `1`
- Source artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/221_external_2025_ggae_surface_prune_profile_boundary_synthesis`

The separate two-profile transfer row remains as the scoped positive optimizer-transfer evidence:

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/200_external_2025_ggae_surface_prune_transfer_synthesis`

## Claim Boundary

The `w=0.3` surface-prune optimizer is not a universal improvement. It improves two validated windows, slightly worsens but preserves provisional `LS1_LID10002`, and does not rescue LDH1. Use it only as profile-scoped stabilization evidence, not as a general solver or diameter/material predictor.

## Verification

- `python -m py_compile run_ggae2025_external_2025_surface_prune_boundary_synthesis.py`
- `python -m pytest tests/test_ggae2025_external_2025_surface_prune_boundary_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_surface_prune_boundary_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

The external validation focus should move from optimizer rescue to independent confirmation and ranking: keep `190424AA_LID10002`, `LS1_LID10001`, and `LS1_LID10002` as provisional location/cover supports, keep LDH1 as a documented failure case, and next test a separate profile/candidate or build a compact synthesis that ranks all external field-profile outcomes by validated status.
