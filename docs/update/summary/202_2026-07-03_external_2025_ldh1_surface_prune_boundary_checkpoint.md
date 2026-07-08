# External 2025 LDH1 Surface-Prune Boundary Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records the LDH1 stress test for the GGAE2025/Fast-GPR-FWI-style shallow/source-zone surface-prune optimizer variant. The goal was to check whether the `w=0.3` surface penalty that helped `190424AA_LID10002` and `LS1_LID10001` also rescues a known weak field profile/window.

## New Runs

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/201_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/202_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_surface_prune_w030`

## Boundary Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/203_external_2025_ggae_surface_prune_profile_boundary_synthesis`

Decision:

- `external_2025_ggae_surface_prune_w030_profile_scoped_ldh1_boundary`

Three-profile result:

- `190424AA_LID10002_rank2_right_shift`: `0.6398650705814362 -> 0.6064098179340363`
- `LS1_LID10001_rank2`: `0.8244783282279968 -> 0.7661208808422089`
- `LDH1_LID10001_rank2`: `1.8228492140769958 -> 1.8277581930160522`

Summary:

- Tested profiles: 3
- Improved profiles: 2
- Validated profiles: 2
- Failed profiles: 1
- Failed profile: `LDH1_LID10001_rank2`
- Mean surface-prune holdout: `1.0667629639307659`
- Mean holdout delta: `-0.028967907031377155`

## Leaderboard Update

The central leaderboard now has two separate rows:

- `external_2025_surface_prune_optimizer_transfer`: evidence score `2`, provisional location/cover only, source artifact `200_external_2025_ggae_surface_prune_transfer_synthesis`.
- `external_2025_surface_prune_profile_boundary`: evidence score `1`, no location/cover use, source artifact `203_external_2025_ggae_surface_prune_profile_boundary_synthesis`.

## Claim Boundary

The `w=0.3` surface-prune optimizer is useful as a profile-scoped stabilization on the tested windows that already validate independently. It does not rescue LDH1, and it does not support autonomous profile transfer, global-profile prediction, diameter, concrete permittivity, or material prediction.

## Verification

- `python -m py_compile run_ggae2025_external_2025_surface_prune_boundary_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_surface_prune_boundary_synthesis.py tests/test_ggae2025_external_2025_surface_prune_transfer_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_surface_prune_boundary_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

Continue on real field data by improving the failure-mode diagnosis rather than broadening claims. The next useful branch is to determine whether LDH1 fails because of profile/window selection, source timing, polarity/source wavelet mismatch, or insufficient candidate initialization.
