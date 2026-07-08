# External 2025 190424AA/LID10001 Surface-Prune Checkpoint

## What Changed

- Ran the current GGAE/Fast-GPR-FWI surface-prune `w=0.3` schedule on 190424AA/LID10001 rank1.
- Added a LID10001 surface-prune synthesis script and test.
- Generated synthesis artifact `245`.
- Added a LID10001 diagnostic row to the method leaderboard.

## Key Numbers

- Baseline rank1 one-step even/odd holdout mean: `1.6316250562667847`.
- Surface-prune `w=0.3` even/odd holdout mean: `1.592418909072876`.
- Improvement versus baseline: `-0.03920614719390869`.
- Recovered x mean: `1.7099290490150452 m`.
- Recovered cover mean: `0.08552702516317368 m`.
- Mean epsr: `4.000495910644531`.
- Objective evaluations across the pair: `40`.
- Leaderboard evidence score: `0`.

## Current Decision

Decision string:

`external_2025_190424aa_lid10001_rank1_surface_prune_w030_improves_but_not_validated`

Interpretation: LID10001 improves under the surface-prune schedule, but the holdout remains far above the provisional validation threshold. This is another failed adjacent-profile transfer boundary, not a usable prediction result.

## What Remains Blocked

- LID10001 does not validate under the current surface-prune settings.
- Adjacent 190424AA profiles LID10001 and LID10003 both improve but remain too weak, while LID10002 is the only strong 190424AA crop.
- The surface-prune method is profile/window scoped; it is not an autonomous field-data detector yet.

## Validation

- `python -m py_compile run_ggae2025_external_2025_lid10001_surface_prune_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_lid10001_surface_prune_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `18 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_lid10001_surface_prune_synthesis.py tests/test_ggae2025_external_2025_lid10001_surface_prune_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py docs/update/summary/214_2026-07-03_external_2025_190424aa_lid10003_source_scaling_checkpoint.md`
- LID10001 synthesis figure: `1804x767`, nonwhite fraction `0.2805123772465649`, RGB std `64.91830016057172`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/243_external_2025_190424aa_lid10001_rank1_ggae2025_ifwi_surface_prune_w030_even`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/244_external_2025_190424aa_lid10001_rank1_ggae2025_ifwi_surface_prune_w030_odd`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/245_external_2025_190424aa_lid10001_surface_prune_transfer_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Consolidate the 190424AA profile-level boundary: LID10002 is usable as provisional location/cover evidence, while LID10001 and LID10003 are improved-but-not-validated diagnostics.

## Marathon Status

The requested real-field-data marathon is still active.
