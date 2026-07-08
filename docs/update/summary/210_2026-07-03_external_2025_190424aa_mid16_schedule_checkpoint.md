# External 2025 190424AA Mid16 Schedule Checkpoint

Date: 2026-07-03

## Scope

This checkpoint extends the 190424AA/LID10002 speed test by adding a middle `5+5+6` staged schedule (`mid16`) between the full20 and fast12 schedules.

## New Runs

- `227_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_right_shift_surface_prune_w030_mid16_even`
- `228_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_right_shift_surface_prune_w030_mid16_odd`

## Updated Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/229_external_2025_190424aa_ggae_fast_schedule_synthesis`

Decision:

- `external_2025_190424aa_fast12_schedule_quick_screen_only_quality_loss`

Schedule comparison:

- Full20: holdout `0.6064098179340363`, runtime `16.53725339192897 s`, evaluations `40`
- Fast12: holdout `0.8188601136207581`, runtime `10.509372451109812 s`, evaluations `24`
- Mid16: holdout `0.8239832520484924`, runtime `13.404258355032653 s`, evaluations `32`

Key numbers:

- Fast12 holdout delta versus full20: `0.2124502956867218`
- Mid16 holdout delta versus full20: `0.21757343411445618`
- Fast12 runtime saved fraction: `0.3645031492207209`
- Mid16 runtime saved fraction: `0.1894507487213917`

## Claim Boundary

Mid16 is not useful on this profile: it is slower and slightly worse than Fast12. Full20 remains the final-evidence schedule. Fast12 remains quick-screen-only.

## Verification

- `python -m py_compile run_ggae2025_external_2025_fast_schedule_synthesis.py`
- `python -m pytest tests/test_ggae2025_external_2025_fast_schedule_synthesis.py -q`
- `python run_ggae2025_external_2025_fast_schedule_synthesis.py`
- `git diff --check`

## Next Step

Do not spend more time on simple iteration-count trimming for this profile unless a different optimizer is introduced. The current schedule evidence says quality loss is dominated by shortened optimization, not just wall-clock overhead.
