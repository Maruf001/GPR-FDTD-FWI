# 461 - GSSI 51600S Source-Alignment Refinement Checkpoint

## What changed

Ran a matched source-alignment refinement branch on the trusted GSSI 51600S field B-scans after promoting the 2.0 GHz source-frequency candidate. The branch tested a fine Ricker frequency ladder around 2.0 GHz and a free source-time-shift variant, then packaged the result into the current predictor bundle and query output.

Generated:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/206_gssi51600s_source_alignment_refinement_card_current`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/207_gssi51600s_current_prediction_bundle_with_source_alignment_refinement`

Updated:

- `run_gssi51600s_source_alignment_refinement_card.py`
- `run_gssi51600s_current_prediction_bundle.py`
- `run_field_prediction_current_query.py`
- `tests/test_gssi51600s_source_alignment_refinement_card.py`
- `tests/test_gssi51600s_current_prediction_bundle.py`
- `tests/test_field_prediction_current_query.py`

## Key numbers

Matched 12-iteration fine-frequency ladder, with geometry, windows, optimizer, material bounds, polarity, and amplitude loss held fixed:

- 1.8 GHz mean objective: `0.9532012641429901`; mean field L1: `0.9379534125328064`.
- 2.0 GHz mean objective: `0.9486662149429321`; mean field L1: `0.9361599981784821`.
- 2.2 GHz mean objective: `0.9621214270591736`; mean field L1: `0.9509869813919067`.
- 1.8 GHz objective deltas versus 2.0 GHz: profiles0-2 `+0.005281329154968262`, profiles1-3 `+0.003788769245147705`.
- 2.2 GHz objective deltas versus 2.0 GHz: profiles0-2 `-0.007257938385009766`, profiles1-3 `+0.034168362617492676`.
- 2.2 GHz field L1 deltas versus 2.0 GHz: profiles0-2 `-0.004003405570983887`, profiles1-3 `+0.03365737199783325`.
- Free source-time shift at 2.0 GHz changed the mean objective by only `-2.9802322387695312e-08` and did not change mean field L1.
- Free-shift subset objective deltas: profiles0-2 `0.0`, profiles1-3 `-5.960464477539063e-08`.

## Current decision

`source_alignment_refinement_keeps_2p0ghz_shared_default`

The 2.0 GHz source frequency remains the shared GSSI predictor default. The 2.2 GHz result is useful diagnostic evidence for profiles 0-2, but it is not a shared source model because it worsens profiles 1-3 substantially. The free-shift result also does not justify changing the source-time prior.

## What remains blocked

The next source-model blocker is the lack of a tested custom wavelet-basis implementation in the Fast-GPR bridge. The copied Fast-GPR source path advertises several waveform names, but only the Ricker analytic branch is implemented in the active `calculate_value` code path. A custom wavelet should be implemented and smoke-tested before using it for product-facing geometry or material claims.

Crossline profile coordinates and y-dependent depth/length interpretation remain conditioned as before.

## Validation and resource checks

- Source-alignment focused tests: `3 passed`.
- Source-frequency/card/bundle/query focused tests: `18 passed`.
- Broad GSSI predictor/card regression suite: `174 passed`.
- Compile checks passed for the source-alignment card, source-frequency card, current bundle, and current query.
- `git diff --check` passed for touched tracked paths.
- Source-alignment figure validation passed: `(2399, 835)` RGBA, nonblank, pixel standard deviation `51.32283291791803`.
- Latest current predictor pointer now targets bundle `207`.

## Artifact paths

- Source-alignment summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/206_gssi51600s_source_alignment_refinement_card_current/data/gssi51600s_source_alignment_refinement_summary.json`
- Source-alignment figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/206_gssi51600s_source_alignment_refinement_card_current/figures/gssi51600s_source_alignment_refinement.png`
- Current bundle summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/207_gssi51600s_current_prediction_bundle_with_source_alignment_refinement/data/gssi51600s_current_prediction_bundle_summary.json`
- Current pretty prediction: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/207_gssi51600s_current_prediction_bundle_with_source_alignment_refinement/data/gssi51600s_current_prediction_pretty.txt`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Implement a tested custom source-wavelet path for the Fast-GPR bridge, then run a small fixed-geometry wavelet-basis smoke check before allowing the basis to interact with geometry/material optimization. If the custom wavelet path does not pass the smoke check, continue with measured crossline-coordinate intake instead.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.
