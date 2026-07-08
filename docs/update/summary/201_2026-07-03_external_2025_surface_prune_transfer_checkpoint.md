# External 2025 GGAE Surface-Prune Transfer Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records the real-field-data transfer test of the GGAE2025/Fast-GPR-FWI-style shallow/source-zone surface-prune optimizer variant. The branch compares the same `w=0.3` regularization against paired baseline GGAE IFWI runs on two external IDS field profiles.

## Field Profiles

- `190424AA_LID10002_rank2_right_shift`
- `LS1_LID10001_rank2`

## Main Artifact

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/200_external_2025_ggae_surface_prune_transfer_synthesis`

## Result

- Decision: `external_2025_ggae_surface_prune_w030_transfers_to_two_field_profiles`
- Tested profiles: 2
- Improved profiles: 2
- Validated profiles under holdout threshold: 2
- Best profile: `190424AA_LID10002_rank2_right_shift`
- Best surface-prune holdout mean: `0.6064098179340363`
- Mean surface-prune holdout mean: `0.6862653493881226`
- Mean holdout delta versus paired baselines: `-0.04590635001659393`

## Leaderboard Update

The central field-method leaderboard was regenerated:

- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

New row:

- Method variant: `external_2025_surface_prune_optimizer_transfer`
- Objective loss: `0.6862653493881226`
- Evidence score: `2`
- Location/cover use: `provisional`
- Diameter use: `no`
- Source artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/200_external_2025_ggae_surface_prune_transfer_synthesis`

## Claim Boundary

This supports the `w=0.3` surface-prune penalty as a field-data stabilization for provisional event-window location/cover fits across the two tested profiles. It does not support autonomous candidate selection, adjacent-profile transfer, global-profile prediction, concrete permittivity validation, rebar diameter estimation, or material identification.

## Verification

- `python -m py_compile run_ggae2025_external_2025_surface_prune_transfer_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_surface_prune_transfer_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_surface_prune_transfer_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

Continue the real-data branch by stress-testing whether the same optimizer transfer holds or fails on another external field profile/window, preferably one already known to be weaker. A failure case is useful here because it will define the method boundary instead of overstating the GGAE/IFWI claim.
