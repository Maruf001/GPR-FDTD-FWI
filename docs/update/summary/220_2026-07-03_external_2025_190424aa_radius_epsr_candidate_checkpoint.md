# External 2025 190424AA Radius/Epsr Candidate Checkpoint

## What Changed

- Ran matched trainable-radius GGAE/IFWI field fits on `190424AA_LID10002` using the current best right-shift + surface-prune window:
  - `254` even split.
  - `255` odd split.
- Ran fixed-radius profile-likelihood hypotheses on the same real-data setting for missing radius candidates:
  - `256/257`: radius `4 mm`, diameter `8 mm`.
  - `258/259`: radius `12 mm`, diameter `24 mm`.
  - Existing current-best fixed radius `8 mm`, diameter `16 mm` pair: `191/192`.
- Generated candidate report artifact `260_external_2025_190424aa_radius_epsr_candidate_synthesis`.
- Added a leaderboard row for the field-fit radius/epsr candidate with range.

## Key Numbers

- Top candidate diameter: `16.00 mm`.
- Top candidate radius: `8.00 mm`.
- Top candidate concrete epsr: `3.9855180978775024`.
- Top candidate mean holdout loss: `0.6064098179340363`.
- 1 percent near-best diameter range: `16.00-16.00 mm`.
- 5 percent near-best diameter range: `8.00-24.00 mm`.
- 5 percent near-best epsr range: `3.9718658924102783-3.9855180978775024`.
- Fixed-radius mean holdout losses:
  - `8 mm` diameter: `0.6302425563335419`.
  - `16 mm` diameter: `0.6064098179340363`.
  - `24 mm` diameter: `0.6260696649551392`.
- Matched trainable-radius pair stayed at `16.00 mm` diameter and epsr `3.9895882606506348`, with mean holdout `0.6093157827854156`.
- Leaderboard evidence score for this radius/epsr candidate row: `2`.
- Runtime for each matched trainable-radius split: about `8.22 s`; fixed-radius radius-hypothesis pairs total about `16.5 s` per diameter.

## Current Decision

Decision string:

`external_2025_190424aa_radius_epsr_candidate_top16mm_range8to24mm`

Interpretation: the current real-field event-window optimizer should report `16 mm` as the top diameter candidate and epsr about `3.986`, while also reporting the wider `8-24 mm` near-best diameter band under a 5 percent loss tolerance. This is the practical candidate/range output the user requested; it is not a ground-truth validation.

## What Remains Blocked

- The field data still does not provide physical ground truth for diameter or epsr.
- The 5 percent near-best band is wide, so a single diameter should not be presented without the range.
- This is still 2D event-window fitting: no `y` location, finite rebar length, or full 3D shape estimate yet.

## Validation

- `python -m py_compile run_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py -q`
- Result: `2 passed in 0.32s`.
- `python -m py_compile run_field_method_validation_leaderboard.py run_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py -q`
- Result: `23 passed in 0.42s`.
- `git diff --check -- run_ggae2025_external_2025_surface_weight_policy_synthesis.py tests/test_ggae2025_external_2025_surface_weight_policy_synthesis.py run_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/219_2026-07-03_external_2025_surface_weight_policy_checkpoint.md`
- Candidate figure: `1804x767`, nonblank RGB channel extrema.
- Leaderboard figure: `1575x720`, figure validation status `ok`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/254_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_radius_trainable_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/255_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_radius_trainable_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/256_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_radius_hypothesis_r04_even_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/257_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_radius_hypothesis_r04_odd_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/258_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_radius_hypothesis_r12_even_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/259_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_radius_hypothesis_r12_odd_event_window_timeshift_m030_narrow_aperture_right_shift_surface_prune_w030`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/260_external_2025_190424aa_radius_epsr_candidate_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Start the 3D/acceleration bridge: define and implement the first local field-data 3D geometry contract for `x, y, z, radius, length, epsr`, while separately benchmarking the current PyTorch/CUDA 2D event-window runtime against a minimal JAX/XLA or Fast-GPR-FWI-style backend if available.

## Marathon Status

The requested real-field-data marathon is still active.
