# 2026-07-03 190424AA GGAE Optimizer Variant Checkpoint

## What changed

- Tested a Fast-GPR-FWI-style Hamming FIR low-pass continuation on the same `190424AA_LID10002` rank2 central event window used by the validated GGAE/IFWI result.
- Tested a shallow/source-zone surface-artifact penalty (`--surface-artifact-weight 0.1`) as a local adaptation of the Fast-GPR-FWI source artifact suppression strategy.
- Added `run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py` and tests to compare FFT-box, FIR-lowpass, surface-pruning, and right-shift variants.
- Refreshed the evidence pack and leaderboard to include the optimizer/stabilization result.

## Key numbers

- Central FFT-box baseline:
  - mean holdout loss: `0.6834719777107239`
  - mean x: `0.13368532061576843 m`
  - mean cover: `0.09367473050951958 m`
- Central FIR-lowpass:
  - mean holdout loss: `0.6891225874423981`
  - delta vs FFT-box: `+0.005650609731674194`
  - mean x: `0.13355929404497147 m`
  - mean cover: `0.09346802532672882 m`
- Central surface-prune `w=0.1`:
  - mean holdout loss: `0.6771082282066345`
  - delta vs FFT-box: `-0.0063637495040893555`
  - mean x: `0.1335713043808937 m`
  - mean cover: `0.09348469972610474 m`
- Right-shift FFT-box remains the best paired loss in the current matrix:
  - mean holdout loss: `0.6398650705814362`

## Current decision

- Decision label: `external_2025_190424aa_lid10002_surface_prune_improves_fir_lowpass_validated_not_superior`.
- The Fast-GPR-FWI FIR low-pass continuation is valid on this crop but not superior to the FFT-box continuation.
- The shallow/source-zone surface-artifact penalty gives a small central-crop improvement with stable x/cover.
- Claim boundary remains provisional location/cover for `190424AA_LID10002` rank2 only. No diameter, material/permittivity, adjacent-profile, or global transfer claim.

## Artifacts

- FIR-lowpass full even/odd:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/175_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_fir_lowpass`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/176_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_fir_lowpass`
- Surface-prune full even/odd:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/179_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_timeshift_m030_narrow_aperture_surface_prune_w010`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/180_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_timeshift_m030_narrow_aperture_surface_prune_w010`
- Optimizer synthesis: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/181_external_2025_190424aa_lid10002_ggae_optimizer_variant_synthesis`
- Final evidence pack: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/183_external_2025_190424aa_narrow_aperture_ggae_evidence_pack_with_surface_prune_optimizer_v2`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Validation and hygiene

- `python -m py_compile run_field_method_validation_leaderboard.py run_ggae2025_external_2025_190424aa_evidence_pack.py run_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py -q` -> `13 passed`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_optimizer_variant_synthesis.py tests/test_ggae2025_external_2025_190424aa_aperture_robustness_synthesis.py tests/test_ggae2025_external_2025_190424aa_confirmation_synthesis.py tests/test_ggae2025_external_2025_190424aa_candidate_diagnostic_matrix.py -q` -> `15 passed`
- `git diff --check` -> clean.

## Next defensible task

- Continue with field-data method work, not synthetic:
  - either test whether surface-pruning transfers to the right-shift aperture or another `190424AA` profile;
  - or broaden to another available real dataset/profile under `data/2025-01-13_GPR_Dataset` using the same method separation and claim-boundary discipline.

## Marathon status

- The user-requested marathon remains active. This checkpoint is not a stop condition.
