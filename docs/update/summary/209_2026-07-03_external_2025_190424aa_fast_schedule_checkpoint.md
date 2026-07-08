# External 2025 190424AA Fast Schedule Checkpoint

Date: 2026-07-03

## Scope

This checkpoint records a Fast-GPR-FWI-style schedule-speed test on the strongest 190424AA/LID10002 GGAE IFWI setup. The test compares the full 20-evaluation staged schedule against a 12-evaluation schedule while keeping the same right-shift aperture, fixed 16 mm radius, and surface-prune `w=0.3`.

## New Runs

- `224_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_right_shift_surface_prune_w030_fast12_even`
- `225_external_2025_190424aa_lid10002_rank2_ggae2025_ifwi_right_shift_surface_prune_w030_fast12_odd`

## Synthesis

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/226_external_2025_190424aa_ggae_fast_schedule_synthesis`

Decision:

- `external_2025_190424aa_fast12_schedule_quick_screen_only_quality_loss`

Speed/quality comparison:

- Full20 holdout mean: `0.6064098179340363`
- Fast12 holdout mean: `0.8188601136207581`
- Fast12 holdout delta versus full20: `0.2124502956867218`
- Full20 runtime: `16.53725339192897 s`
- Fast12 runtime: `10.509372451109812 s`
- Runtime saved: `6.027880940819159 s`
- Runtime saved fraction: `0.3645031492207209`
- Full20 objective evaluations: `40`
- Fast12 objective evaluations: `24`
- Fast12 remains below provisional threshold: `true`

## Claim Boundary

Fast12 is faster and still below the provisional threshold on this profile, but the quality loss is too large for final evidence. Use Fast12 only as a quick-screen schedule. Use the full20 schedule for final profile evidence and any profile-level claim.

## Verification

- `python -m py_compile run_ggae2025_external_2025_fast_schedule_synthesis.py`
- `python -m pytest tests/test_ggae2025_external_2025_fast_schedule_synthesis.py -q`
- `python run_ggae2025_external_2025_fast_schedule_synthesis.py`
- `git diff --check`

## Next Step

If speed remains a priority, test a middle schedule rather than jumping straight to Fast12. A `5+5+6` or `5+5+8` schedule may preserve more waveform quality while still cutting runtime.
