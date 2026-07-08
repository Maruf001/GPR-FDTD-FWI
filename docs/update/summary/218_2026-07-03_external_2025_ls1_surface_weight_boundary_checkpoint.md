# External 2025 LS1 Surface-Weight Boundary Checkpoint

## What Changed

- Tested `w=0.03` surface-prune regularization on LS1/LID10001 rank2 after LS1/LID10002 showed no benefit from surface pruning.
- Generated LS1 profile-level weight synthesis artifact `252_external_2025_ls1_surface_prune_weight_synthesis`.
- Added a leaderboard row for the LS1 surface-weight boundary.

## Key Numbers

- Profiles tested: `2`.
- `w=0.3` best profiles: `1` (`LS1_LID10001_rank2`).
- Baseline/no-surface best profiles: `1` (`LS1_LID10002`).
- `w=0.03` best profiles: `0`.
- Mean `w=0.3` delta versus baseline: `-0.026723548769950867`.
- Mean `w=0.03` delta versus baseline: `+0.038865283131599426`.
- Mean `w=0.03` delta versus `w=0.3`: `+0.06558883190155029`.
- Leaderboard evidence score for this optimizer-boundary row: `1`.

## Current Decision

Decision string:

`external_2025_ls1_surface_weight_profile_dependent_w003_not_replacement`

Interpretation: on LS1 real field data, surface-prune weight is profile-dependent. The stronger `w=0.3` penalty is best for LS1/LID10001 rank2, no-surface baseline is best for LS1/LID10002, and `w=0.03` is not best on either profile. This supports profile-scoped optimizer selection rather than a universal surface-prune weight.

## What Remains Blocked

- No single tested surface-prune weight transfers cleanly across LS1 profiles.
- The optimizer can stabilize some profiles but should not be described as universally state-of-the-art for all field B-scans.
- This branch remains optimizer-sensitivity evidence only; no diameter/material claim.

## Validation

- `python -m py_compile run_ggae2025_external_2025_ls1_surface_weight_synthesis.py run_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_ls1_surface_weight_synthesis.py tests/test_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `23 passed in 0.84s`.
- `git diff --check -- run_ggae2025_external_2025_ls1_surface_weight_synthesis.py tests/test_ggae2025_external_2025_ls1_surface_weight_synthesis.py run_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py tests/test_ggae2025_external_2025_ls1_lid10002_surface_weight_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py`
- LS1 surface-weight figure: `1719x801`, nonwhite fraction `0.5225507092283569`, RGB std `92.3729486572803`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/250_external_2025_ls1_lid10001_rank2_ggae2025_ifwi_initializer_seeded_even_xcover_inverted_event_window_surface_prune_w003`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/251_external_2025_ls1_lid10001_rank2_ggae2025_ifwi_initializer_seeded_odd_xcover_inverted_event_window_surface_prune_w003`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/252_external_2025_ls1_surface_prune_weight_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue on real field data by testing a different optimizer component or preprocessing/source extraction branch. Do not continue tuning `w=0.03`; it is not supported by the LS1 paired holdout evidence.

## Marathon Status

The requested real-field-data marathon is still active.
