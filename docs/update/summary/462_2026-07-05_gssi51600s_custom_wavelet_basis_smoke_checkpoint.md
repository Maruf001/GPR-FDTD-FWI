# 462 - GSSI 51600S Custom Wavelet-Basis Smoke Checkpoint

## What changed

Implemented and tested an explicit user-waveform injection path for the copied Fast-GPR bridge, then used it for a fixed-geometry real-field source-wavelet basis check on the current GSSI 51600S 2.0 GHz geometry/material candidate.

Generated:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/209_gssi51600s_fastgpr_user_waveform_smoke`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/211_gssi51600s_fastgpr_wavelet_basis_field_smoke`

Updated:

- `run_gssi51600s_fastgpr_user_waveform_smoke.py`
- `run_gssi51600s_fastgpr_wavelet_basis_field_smoke.py`
- `tests/test_gssi51600s_fastgpr_user_waveform_smoke.py`
- `tests/test_gssi51600s_fastgpr_wavelet_basis_field_smoke.py`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Key numbers

User-waveform infrastructure smoke:

- Decision: `fastgpr_user_waveform_path_matches_builtin_ricker`.
- CUDA output shape: `[3, 41, 5]`.
- Relative max-absolute difference between built-in Ricker and user-array Ricker: `0.0`.
- Relative L2 difference: `0.0`.

Fixed-geometry GSSI field wavelet-basis smoke:

- Decision: `custom_wavelet_basis_no_shared_fixed_geometry_gain`.
- Best shared waveform: `ricker_2p0_reference`.
- Best mean objective delta versus 2.0 GHz Ricker: `0.0`.
- Best mean field L1 delta versus 2.0 GHz Ricker: `0.0`.
- `mix_2p0_2p2_a025` mean objective delta: `+0.00069466233253479`.
- `mix_2p0_2p2_a050` mean objective delta: `+0.0009584128856658936`.
- `ricker_1p8` mean objective delta: `+0.0165826678276062`.
- `ricker_2p2` mean objective delta: `+0.0034645497798919678`.
- Profiles0-2 had a small fixed-geometry improvement with `mix_2p0_2p2_a050`: objective delta `-0.0008322596549987793`, field L1 delta `-0.0010237693786621094`.
- Profiles1-3 worsened for the same mixture: objective delta `+0.0027490854263305664`, field L1 delta `+0.0025388002395629883`.

## Current decision

Keep the 2.0 GHz Ricker source as the shared source model for the current GSSI predictor.

The custom source-waveform injection path is now technically usable. The first simple mixed-wavelet field check did not produce a shared fixed-geometry gain across both overlapping profile subsets, so it should not be promoted into geometry/material optimization yet.

## What remains blocked

A richer wavelet optimizer could still be useful, but the next higher-return blocker is measured or stronger estimated crossline profile coordinates. The current source-model checks now support keeping the source fixed at 2.0 GHz Ricker while focusing on y geometry.

## Validation and resource checks

- User-waveform and wavelet-basis focused tests: `5 passed`.
- Expanded GSSI predictor/card regression suite: `179 passed`.
- Compile checks passed for the user-waveform smoke and wavelet-basis field smoke.
- `git diff --check` passed for touched tracked paths.
- User-waveform figure validation passed: `(1804, 767)` RGBA, nonblank, pixel standard deviation `51.09871790695353`.
- Wavelet-basis field figure validation passed: `(2229, 835)` RGBA, nonblank, pixel standard deviation `40.736617173519946`.

## Artifact paths

- User-waveform smoke summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/209_gssi51600s_fastgpr_user_waveform_smoke/data/gssi51600s_fastgpr_user_waveform_smoke_summary.json`
- User-waveform smoke figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/209_gssi51600s_fastgpr_user_waveform_smoke/figures/gssi51600s_fastgpr_user_waveform_smoke.png`
- Wavelet-basis field summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/211_gssi51600s_fastgpr_wavelet_basis_field_smoke/data/gssi51600s_fastgpr_wavelet_basis_field_smoke_summary.json`
- Wavelet-basis field figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/211_gssi51600s_fastgpr_wavelet_basis_field_smoke/figures/gssi51600s_fastgpr_wavelet_basis_field_smoke.png`

## Next defensible task

Move to measured or explicitly optimized crossline profile coordinates for the trusted GSSI scans, with the source model held at the 2.0 GHz Ricker default. The immediate product question is whether y geometry can tighten the reported x, cover depth, length, diameter, permittivity, and conductivity ranges more than additional simple source-wavelet changes.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.
