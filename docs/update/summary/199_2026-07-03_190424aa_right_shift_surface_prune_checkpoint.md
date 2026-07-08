# 2026-07-03 190424AA Right-Shift Surface-Prune Checkpoint

## What changed

- Applied the shallow/source-zone surface-artifact penalty (`--surface-artifact-weight 0.1`) to the stronger `190424AA_LID10002` +1 cm right-shift aperture.
- Regenerated the optimizer-variant synthesis to include both central and right-shift surface-prune results.
- Refreshed the evidence pack and leaderboard so the optimizer row reports the best optimizer variant rather than only the central-crop result.

## Key numbers

- Right-shift FFT-box baseline:
  - mean holdout loss: `0.6398650705814362`
  - mean x: `0.13380017131567 m`
  - mean cover: `0.09385191649198532 m`
- Right-shift surface-prune `w=0.1`:
  - mean holdout loss: `0.6318371295928955`
  - delta vs right-shift baseline: `-0.00802794098854065`
  - mean x: `0.13383134454488754 m`
  - mean cover: `0.09378091618418694 m`
- Central surface-prune `w=0.1`:
  - mean holdout loss: `0.6771082282066345`
  - delta vs central FFT-box baseline: `-0.0063637495040893555`

## Current decision

- Decision label: `external_2025_190424aa_lid10002_surface_prune_improves_central_and_right_fir_validated_not_superior`.
- Best current optimizer/stabilization variant: `right_shift_surface_prune_w010`, mean holdout loss `0.6318371295928955`.
- The Fast-GPR-FWI-style FIR low-pass continuation is still valid but not superior to FFT-box on this field crop.
- Claim boundary remains unchanged: provisional location/cover for `190424AA_LID10002` rank2 only; no diameter, material/permittivity, adjacent-profile, or global transfer claim.

## Artifacts

- Right-shift surface-prune full even/odd:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/184_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w010`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/185_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w010`
- Updated optimizer synthesis: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/186_external_2025_190424aa_lid10002_ggae_optimizer_variant_synthesis`
- Final evidence pack: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/188_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_right_surface_prune_optimizer_v2`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Validation and hygiene

- `python -m py_compile run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py run_ggae2025_external_2025_190424aa_evidence_pack.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_field_method_validation_leaderboard.py -q` -> `11 passed`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py tests/test_ggae2025_external_2025_190424aa_confirmation_synthesis.py tests/test_ggae2025_external_2025_190424aa_candidate_diagnostic_matrix.py -q` -> `15 passed`
- `git diff --check` -> clean.

## Next defensible task

- Continue field-data method validation without synthetic detours:
  - try a small surface-prune weight ladder (`0.03`, `0.1`, `0.3`) only on the validated `190424AA_LID10002` right-shift aperture, or
  - move to another real profile/dataset under `data/2025-01-13_GPR_Dataset` to test transfer of the best GGAE recipe.

## Marathon status

- The user-requested marathon remains active. This checkpoint is not a stop condition.
