# External 2025 190424AA/LID10003 Surface-Prune Checkpoint

## What Changed

- Ran the current best GGAE/Fast-GPR-FWI surface-prune schedule on the adjacent 190424AA/LID10003 rank1 field profile.
- Added a synthesis script for LID10003 surface-prune transfer and generated artifact `236`.
- Added a leaderboard row for this diagnostic adjacent-profile result.

## Key Numbers

- Baseline rank1 one-step even/odd holdout mean: `1.9118223786354065`.
- Surface-prune `w=0.3` even/odd holdout mean: `1.8293899297714233`.
- Improvement versus baseline: `-0.08243244886398315`.
- Even split holdout: `1.796018123626709`.
- Odd split holdout: `1.8627617359161377`.
- Recovered x mean: `1.2771291732788086 m`.
- Recovered cover mean: `0.09572175145149231 m`.
- Mean epsr: `4.027745246887207`.
- Objective evaluations across the pair: `40`.

## Current Decision

Decision string:

`external_2025_190424aa_lid10003_rank1_surface_prune_w030_improves_but_not_validated`

Interpretation: the current surface-prune multiscale optimizer improves LID10003, but the holdout remains far above the provisional validation threshold. This is an adjacent-profile failure boundary, not a location/diameter/material claim.

## What Remains Blocked

- LID10003 does not validate under the LID10002-derived surface-prune settings.
- Adjacent-profile transfer remains unreliable.
- The current GGAE/Fast-GPR-FWI branch still needs a stronger timing/window/preprocessing strategy before LID10003 can support prediction.

## Validation

- `python -m py_compile run_field_method_validation_leaderboard.py run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py`
- `python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py -q`
- Result: `17 passed in 0.66s`.
- `git diff --check -- run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py run_ggae2025_external_2025_lid10003_surface_prune_synthesis.py tests/test_ggae2025_external_2025_lid10003_surface_prune_synthesis.py`
- LID10003 synthesis figure: `1804x767`, nonwhite fraction `0.29126423390582135`, RGB std `65.58908892827172`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/234_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_even`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/235_external_2025_190424aa_lid10003_rank1_ggae2025_ifwi_surface_prune_w030_odd`
- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/236_external_2025_190424aa_lid10003_surface_prune_transfer_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Continue on real field data by testing whether LID10003 failure is primarily due to timing/window mismatch or preprocessing, starting with a bounded timing/window variant before changing the inversion model.

## Marathon Status

The requested real-field-data marathon is still active.
