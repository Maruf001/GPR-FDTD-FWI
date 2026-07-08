# External 2025 190424AA/LID10003 Source-Scaling Checkpoint

## What Changed

- Tested signed amplitude scaling on LID10003 rank1 with the same surface-prune `w=0.3` optimizer, window, wavelet, and geometry settings.
- Added the signed-scale variant to the LID10003 synthesis.
- Regenerated the LID10003 synthesis as artifact `242`.
- Refreshed the leaderboard so the LID10003 diagnostic row cites `242`.

## Key Numbers

- Best LID10003 branch remains `rank1_surface_prune_w030`.
- Positive-scale surface-prune holdout mean: `1.8293899297714233`.
- Signed-scale surface-prune holdout mean: `1.839630365371704`.
- Signed-scale delta versus positive scale: `+0.010240435600280762`.
- Tighter `1.05-1.65 ns` window holdout mean: `1.8501960039138794`.
- Tighter-window delta versus positive scale: `+0.020806074142456055`.

## Current Decision

Decision string remains:

`external_2025_190424aa_lid10003_rank1_surface_prune_w030_improves_but_not_validated`

Interpretation: signed amplitude scaling does not repair LID10003. The failure is not solved by the tested loss-window or source-scaling adjustments. This remains a diagnostic adjacent-profile boundary, not a prediction result.

## What Remains Blocked

- LID10003 still fails the provisional holdout threshold.
- Neither tighter event-windowing nor signed amplitude scaling improves on the positive-scale surface-prune branch.
- Further LID10003 work should avoid ad hoc over-tuning; either test a materially different preprocessing/source extraction or move to another field profile to understand transfer scope.

## Validation

- `python -m py_compile run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `17 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/213_2026-07-03_external_2025_190424aa_lid10003_window_checkpoint.md`
- LID10003 synthesis figure: `1804x767`, nonwhite fraction `0.26621414963705164`, RGB std `64.55253591408064`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/240_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_signed_scale_even`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/241_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_signed_scale_odd`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/242_external_2025_190424aa_lid10003_surface_prune_transfer_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue real-field validation on a different profile or with a clearly different preprocessing/source extraction. Do not claim LID10003 prediction from the current GGAE/Fast-GPR-FWI branch.

## Marathon Status

The requested real-field-data marathon is still active.
