# 460 - GSSI 51600S Source-Frequency Candidate Checkpoint

## What changed

Ran and packaged a matched source-frequency ladder on the trusted GSSI 51600S field B-scans, then updated the current predictor bundle and query output so the source-frequency-conditioned result is visible in the deliverable surface.

Generated:

- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/203_gssi51600s_source_frequency_ladder_card_current`
- `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/204_gssi51600s_current_prediction_bundle_with_source_frequency_candidate`

Updated:

- `run_gssi51600s_source_frequency_ladder_card.py`
- `run_gssi51600s_current_prediction_bundle.py`
- `run_field_prediction_current_query.py`
- `tests/test_gssi51600s_source_frequency_ladder_card.py`
- `tests/test_gssi51600s_current_prediction_bundle.py`
- `tests/test_field_prediction_current_query.py`
- `docs/update/daily_update/2026-06-29_to_2026-07-05_daily_update.md`

## Key numbers

Matched high-budget confirmation, 2.0 GHz versus the previous 1.6 GHz reference, with geometry, windows, optimizer, and budget held fixed:

- Decision: `high_budget_source_frequency_candidate_improves_all_subsets`.
- Reference source frequency: `1.6e9` Hz.
- Selected source frequency: `2.0e9` Hz.
- Mean objective delta versus 1.6 GHz: `-0.00814393162727356`.
- Mean field L1 delta versus 1.6 GHz: `-0.0016976594924926758`.
- Profiles 0/2 objective delta: `-0.013989448547363281`.
- Profiles 1/3 objective delta: `-0.002298414707183838`.
- Profiles 0/2 field L1 delta: `-0.0013895630836486816`.
- Profiles 1/3 field L1 delta: `-0.00200575590133667`.
- Selected x range: `0.4901575744152069` to `0.4983973205089569` m.
- Selected cover-depth range: `0.11960408091545105` to `0.14299434423446655` m.
- Selected length-y range: `0.1276356279850006` to `0.172419935464859` m.
- Selected diameter range: `13.487275689840317` to `16.209173947572708` mm.
- Selected background relative permittivity range: `2.1526012420654297` to `2.2108256816864014`.
- Selected conductivity range: `0.003187754424288869` to `0.005288766231387854` S/m.
- Selected time-shift range: `1.8932197093963623` to `1.9037941694259644` ns.

## Current decision

Use the 2.0 GHz source-frequency candidate as the next GSSI Fast-GPR predictor default, while reporting source-frequency-conditioned geometry and material ranges until a broader wavelet-basis check is complete.

This is a real field-data improvement on both overlapping profile subsets. It is not independent antenna calibration, so the claim remains conditioned on the source model.

## What remains blocked

The main blockers are still source wavelet shape, source/time alignment, and measured or stronger estimated crossline profile coordinates. The source-frequency result changes the current best-conditioned geometry/material ranges, but it does not by itself resolve y coordinate, finite-length, or source-wavelet uncertainty.

## Validation and resource checks

- Focused tests: `15 passed`.
- Broad GSSI predictor/card regression suite: `171 passed`.
- Compile check passed for the source-frequency card, current bundle, and current query.
- `git diff --check` passed for touched tracked paths.
- Figure validation passed for the source-frequency figure copy: `(2365, 852)` RGBA, nonblank, pixel standard deviation `54.927067962835885`.
- Latest current predictor pointer now targets bundle `204`.
- GPU and memory check before this branch: NVIDIA GB10 low utilization; about `91 GiB` free memory.

## Artifact paths

- Source-frequency summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/203_gssi51600s_source_frequency_ladder_card_current/data/gssi51600s_source_frequency_ladder_summary.json`
- Source-frequency figure: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/203_gssi51600s_source_frequency_ladder_card_current/figures/gssi51600s_source_frequency_ladder.png`
- Current bundle summary: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/204_gssi51600s_current_prediction_bundle_with_source_frequency_candidate/data/gssi51600s_current_prediction_bundle_summary.json`
- Current pretty prediction: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/204_gssi51600s_current_prediction_bundle_with_source_frequency_candidate/data/gssi51600s_current_prediction_pretty.txt`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Script snapshots: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/204_gssi51600s_current_prediction_bundle_with_source_frequency_candidate/scripts/`

## Next defensible task

Run a source wavelet-shape alignment branch on the same trusted GSSI field windows, starting from the 2.0 GHz candidate. The immediate question is whether a broader wavelet basis or source-time alignment tightens the x, cover-depth, length, diameter, permittivity, and conductivity ranges before adding more 3D geometry freedom.

## Marathon status

The local 20-hour marathon request is still active. This checkpoint is a progress artifact, not a stopping point.
