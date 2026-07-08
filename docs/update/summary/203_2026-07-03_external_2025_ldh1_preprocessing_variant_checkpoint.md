# External 2025 LDH1 Preprocessing Variant Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records the LDH1 scattered-field preprocessing stress test for the GGAE2025 IFWI branch. The hypothesis was that LDH1 fails because the auto-selected preprocessing variant preserves too much direct-wave/source mismatch, unlike the LS1 profile that validated under SVD-rank1 subtraction.

## New Preprocessor

- `outputs/validation_exp_on_field_data/jazayeri_2019_rebar_fwi/125_external_2025_ids_scattered_field_preprocessor_ldh1_lid10001_rank2_forced_svd_rank1`

This forces `svd_rank1_subtracted` as the canonical LDH1 rank2 scattered-field variant.

## New IFWI Runs

- `204_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window`
- `205_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window`
- `206_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_even_xcover_inverted_event_window_surface_prune_w030`
- `207_external_2025_ldh1_lid10001_rank2_ggae2025_ifwi_forced_svd_rank1_odd_xcover_inverted_event_window_surface_prune_w030`

## Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/208_external_2025_ldh1_ggae_preprocessing_variant_synthesis`

Decision:

- `external_2025_ldh1_forced_svd_preprocessing_improves_but_not_validated`

Family comparison:

- Auto spatial-mean baseline: `1.8228492140769958`
- Auto spatial-mean + surface prune `w=0.3`: `1.8277581930160522`
- Forced SVD-rank1: `1.6522585153579712`
- Forced SVD-rank1 + surface prune `w=0.3`: `1.6575437188148499`

Key numbers:

- Forced SVD gain versus baseline: `0.17059069871902466`
- Best family: `forced_svd_rank1`
- Validated family count: `0`
- Best x parity gap: `0.3282129764556885 mm`
- Best cover parity gap: `0.06742030382156372 mm`

## Leaderboard Update

The central leaderboard now includes:

- Method variant: `external_2025_ldh1_preprocessing_variant_diagnostic`
- Objective loss: `1.6522585153579712`
- Evidence score: `0`
- Location/cover use: `no`
- Diameter use: `no`
- Source artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/208_external_2025_ldh1_ggae_preprocessing_variant_synthesis`

## Claim Boundary

Forced SVD reduces the LDH1 waveform mismatch, but LDH1 remains far above the provisional holdout threshold. This is failure-mode evidence only. It does not validate LDH1 location/cover, diameter, concrete permittivity, or material prediction.

## Verification

- `python -m py_compile run_ggae2025_external_2025_ldh1_preprocessing_variant_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_ldh1_preprocessing_variant_synthesis.py tests/test_ggae2025_external_2025_surface_prune_boundary_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- `python run_ggae2025_external_2025_ldh1_preprocessing_variant_synthesis.py`
- `python run_field_method_validation_leaderboard.py`
- `git diff --check`

## Next Step

Continue LDH1 failure analysis by testing whether the event window is too wide/misaligned after forced SVD, or whether a different source wavelet/time-zero parameterization is needed. The useful target is reducing LDH1 below the current best `1.6523`; no prediction claim should be made unless it crosses the provisional threshold.
