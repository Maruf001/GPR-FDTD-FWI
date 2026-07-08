# External 2025 190424AA/LID10003 Window Variant Checkpoint

## What Changed

- Tested a tighter LID10003 rank1 surface-prune loss window: `1.05-1.65 ns`.
- Added the tighter-window variant to the LID10003 surface-prune synthesis.
- Regenerated the LID10003 synthesis as artifact `239`.
- Refreshed the field-method leaderboard so its LID10003 diagnostic row cites `239`.

## Key Numbers

- Original LID10003 rank1 surface-prune `w=0.3` holdout mean: `1.8293899297714233`.
- Tighter `1.05-1.65 ns` window holdout mean: `1.8501960039138794`.
- Tighter-window delta versus original surface-prune branch: `+0.020806074142456055`.
- Best surface variant remains `rank1_surface_prune_w030`.
- Baseline one-step holdout mean remains `1.9118223786354065`.

## Current Decision

Decision string remains:

`external_2025_190424aa_lid10003_rank1_surface_prune_w030_improves_but_not_validated`

Interpretation: narrowing the LID10003 loss window did not repair the adjacent-profile failure. The branch remains an improved-but-not-validated diagnostic, not a location/diameter/material prediction.

## What Remains Blocked

- LID10003 adjacent-profile transfer is still not field-validated.
- Timing-window adjustment alone did not fix the waveform mismatch.
- The next useful test should isolate preprocessing/source behavior or move to another external profile rather than over-tuning this one window.

## Validation

- `python -m py_compile run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `17 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/212_2026-07-03_external_2025_190424aa_lid10003_surface_prune_checkpoint.md`
- LID10003 synthesis figure: `1804x767`, nonwhite fraction `0.26434737234654554`, RGB std `63.85478298739157`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/237_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_window105_165_even`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/238_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_window105_165_odd`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/239_external_2025_190424aa_lid10003_surface_prune_transfer_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue real-field validation by testing whether a source/preprocessing choice, rather than the loss window, is controlling LID10003 failure; keep the result scoped as diagnostic unless it crosses the same holdout and split-stability boundary.

## Marathon Status

The requested real-field-data marathon is still active.
