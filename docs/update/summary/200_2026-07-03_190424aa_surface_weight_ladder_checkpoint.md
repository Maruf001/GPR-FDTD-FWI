# 2026-07-03 190424AA Surface-Weight Ladder Checkpoint

## What changed

- Ran a right-shift surface-artifact penalty ladder on `190424AA_LID10002` rank2:
  - `w=0.03`: runs `189`, `190`
  - `w=0.3`: runs `191`, `192`
  - `w=1.0`: runs `193`, `194`
- Updated the optimizer-variant synthesis so the best GGAE optimizer/stabilization variant is selected from the ladder.
- Refreshed the 190424AA evidence pack and field-method leaderboard.

## Key numbers

- Right-shift FFT-box baseline:
  - mean holdout loss: `0.6398650705814362`
- Right-shift surface-prune `w=0.03`:
  - even holdout: `0.698579`
  - odd holdout: `0.546434`
  - mean holdout: about `0.622506`
- Right-shift surface-prune `w=0.3`:
  - even holdout: `0.678237`
  - odd holdout: `0.534582`
  - mean holdout: `0.6064098179340363`
  - delta vs right-shift baseline: `-0.0334552526473999`
- Right-shift surface-prune `w=1.0`:
  - even holdout: `0.700769`
  - odd holdout: `0.57169`
  - mean holdout: about `0.636229`

## Current decision

- Decision label: `external_2025_190424aa_lid10002_surface_prune_weight_ladder_w030_best_fir_validated_not_superior`.
- Best current GGAE optimizer/stabilization variant: `right_shift_surface_prune_w030`.
- The weight ladder suggests `w=0.3` is the useful source-zone suppression setting on this crop; `w=1.0` starts to degrade the even split.
- Claim boundary remains provisional location/cover only for `190424AA_LID10002` rank2. No diameter, material/permittivity, adjacent-profile, or global transfer claim.

## Artifacts

- Surface-prune ladder runs:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/189_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w003`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/190_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w003`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/191_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/192_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/193_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w100`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/194_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w100`
- Optimizer synthesis: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/195_external_2025_190424aa_lid10002_ggae_optimizer_variant_synthesis`
- Final evidence pack: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/196_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_surface_weight_ladder`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Validation and hygiene

- `python -m py_compile run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py run_ggae2025_external_2025_190424aa_evidence_pack.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_field_method_validation_leaderboard.py -q` -> `11 passed`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py tests/test_ggae2025_external_2025_190424aa_confirmation_synthesis.py tests/test_ggae2025_external_2025_190424aa_candidate_diagnostic_matrix.py -q` -> `15 passed`
- `git diff --check` -> clean.

## Next defensible task

- Continue on real field data:
  - try transferring the best `right_shift_surface_prune_w030` recipe to another real `190424AA` profile or another profile in `data/2025-01-13_GPR_Dataset`;
  - keep the current result scoped to `190424AA_LID10002` unless a transfer profile validates.

## Marathon status

- The user-requested marathon remains active. This checkpoint is not a stop condition.
