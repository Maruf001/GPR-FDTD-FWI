# External 2025 LS1/LID10002 Surface-Weight Checkpoint

## What Changed

- Tested a lower surface-prune weight on real LS1/LID10002 field data: `w=0.03` versus existing `w=0.3` and baseline.
- Generated synthesis artifact `249_external_2025_ls1_lid10002_surface_prune_weight_synthesis`.
- Added a leaderboard diagnostic row for the LS1/LID10002 surface-weight sensitivity.

## Key Numbers

- Baseline/no-surface holdout mean: `0.8706095814704895`.
- Surface-prune `w=0.3` holdout mean: `0.8755199313163757`.
- Surface-prune `w=0.03` holdout mean: `0.8777920305728912`.
- Delta `w=0.3` minus baseline: `+0.0049103498458862305`.
- Delta `w=0.03` minus baseline: `+0.007182449102401733`.
- Delta `w=0.03` minus `w=0.3`: `+0.002272099256515503`.
- Validated variants under the holdout threshold: `3`.
- Leaderboard evidence score for this optimizer-sensitivity row: `1`.

## Current Decision

Decision string:

`external_2025_ls1_lid10002_surface_weight_no_surface_prune_best`

Interpretation: LS1/LID10002 validates under all tested settings, but surface-prune regularization is not beneficial for paired holdout on this profile. Lowering the penalty from `w=0.3` to `w=0.03` improves the even split but worsens the odd split enough that baseline remains best.

## What Remains Blocked

- Surface-prune `w=0.3` is useful on LS1/LID10001 and 190424AA/LID10002, but not LS1/LID10002.
- The optimizer is profile-sensitive; a single fixed surface-prune weight is not a general solver.
- This branch supports optimizer sensitivity only, not diameter/material prediction.

## Validation

- `python -m py_compile run_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `20 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py tests/test_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/216_2026-07-03_external_2025_190424aa_profile_boundary_checkpoint.md`
- LS1/LID10002 weight figure: `1634x784`, nonwhite fraction `0.5142171770789099`, RGB std `76.80946137101125`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/247_external_2025_ls1_lid10002_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_surface_prune_w003`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/248_external_2025_ls1_lid10002_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_surface_prune_w003`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/249_external_2025_ls1_lid10002_surface_prune_weight_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue on real field data by testing another profile family or a clearly different optimizer component. Do not extrapolate a single surface-prune weight across profiles.

## Marathon Status

The requested real-field-data marathon is still active.
