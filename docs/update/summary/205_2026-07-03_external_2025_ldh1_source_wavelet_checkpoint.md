# External 2025 LDH1 Source/Wavelet Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records the LDH1 source/wavelet failure-mode test for the GGAE2025 IFWI branch. The comparison uses the current best LDH1 setup before source testing: forced SVD-rank1 preprocessing with the `0.75-1.35 ns` event window.

## New Runs

- `214_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window_075_135_ricker`
- `215_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window_075_135_ricker`
- `216_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window_075_135_signed_scale`
- `217_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window_075_135_signed_scale`

## Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/218_external_2025_ldh1_ggae_source_wavelet_synthesis`

Decision:

- `external_2025_ldh1_empirical_positive_wavelet_best_but_not_validated`

Source comparison:

- Empirical wavelet + positive scale: `1.6379399299621582`
- Ricker 1.6 GHz + positive scale: `1.6552196741104126`
- Empirical wavelet + signed scale: `1.6663681268692017`

Key numbers:

- Ricker delta versus empirical-positive: `0.017279744148254395`
- Signed-scale delta versus empirical-positive: `0.028428196907043457`
- Validated source family count: `0`

## Leaderboard Update

The central leaderboard now includes:

- Method variant: `external_2025_ldh1_source_wavelet_diagnostic`
- Objective loss: `1.6379399299621582`
- Evidence score: `0`
- Location/cover use: `no`
- Diameter use: `no`
- Source artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/218_external_2025_ldh1_ggae_source_wavelet_synthesis`

## Claim Boundary

The empirical field wavelet with positive scaling remains the best tested LDH1 source model. Ricker and signed scaling do not rescue the profile. This is failure-mode evidence only and does not validate LDH1 location/cover, diameter, concrete permittivity, or material prediction.

## Verification

- `python -m py_compile run_ggae2025_external_2025_ldh1_source_wavelet_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_ldh1_source_wavelet_synthesis.py tests/test_ggae2025_external_2025_ldh1_window_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_ldh1_source_wavelet_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

LDH1 remains failed after candidate selection, timing/polarity, surface-prune, forced-SVD preprocessing, event-window tuning, and source/wavelet variants. The next high-value branch should move away from LDH1 rescue and back toward strengthening the profiles that do validate, or test a different field profile from the external dataset for independent confirmation.
