# External 2025 LDH1 Window Tuning Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records the LDH1 forced-SVD event-window tuning test for the GGAE2025 IFWI branch. The goal was to check whether LDH1 remains high-loss because the original event window was too late or too broad for the hyperbola apex.

## New Runs

- `209_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window_075_135`
- `210_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window_075_135`
- `211_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window_085_125`
- `212_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window_085_125`

## Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/213_external_2025_ldh1_ggae_forced_svd_window_synthesis`

Decision:

- `external_2025_ldh1_forced_svd_window_tuning_improves_but_not_validated`

Window comparison:

- Forced SVD, `0.95-1.70 ns`: `1.6522585153579712`
- Forced SVD, `0.75-1.35 ns`: `1.6379399299621582`
- Forced SVD, `0.85-1.25 ns`: `1.6462956666946411`

Key numbers:

- Best window: `0.75-1.35 ns`
- Best gain versus forced-SVD baseline: `0.014318585395812988`
- Validated window count: `0`
- Best holdout gap: `0.03293275833129883`

## Leaderboard Update

The central leaderboard now includes:

- Method variant: `external_2025_ldh1_forced_svd_window_diagnostic`
- Objective loss: `1.6379399299621582`
- Evidence score: `0`
- Location/cover use: `no`
- Diameter use: `no`
- Source artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/213_external_2025_ldh1_ggae_forced_svd_window_synthesis`

## Claim Boundary

Window tuning slightly reduces LDH1 mismatch, but the best result is still far above the provisional threshold. This remains failure-mode evidence only and does not support LDH1 location/cover, diameter, concrete permittivity, or material prediction.

## Verification

- `python -m py_compile run_ggae2025_external_2025_ldh1_window_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_ldh1_window_synthesis.py tests/test_ggae2025_external_2025_ldh1_preprocessing_variant_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_ldh1_window_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

The next useful LDH1 branch is source/wavelet mismatch, not more narrow-window tuning. The current best LDH1 result is `1.6379`, so the next test should change the empirical wavelet/time-zero parameterization or compare a learned/free wavelet variant while keeping field holdout splits intact.
