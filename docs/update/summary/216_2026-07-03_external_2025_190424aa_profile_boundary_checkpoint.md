# External 2025 190424AA Profile-Boundary Checkpoint

## What Changed

- Consolidated the 190424AA profile-level GGAE/Fast-GPR-FWI surface-prune boundary across LID10001, LID10002, and LID10003.
- Generated artifact `246_external_2025_190424aa_surface_prune_profile_boundary_synthesis`.
- Added a leaderboard row for the profile-scoped boundary.

## Key Numbers

- Validated/provisional profiles: `1`.
- Improved profiles: `3`.
- Failed profiles: `2`.
- Validated profile: `190424AA_LID10002_rank2_right_shift`.
- Failed adjacent profiles: `190424AA_LID10001_rank1`, `190424AA_LID10003_rank1`.
- Best profile holdout: `0.6064098179340363`.
- Worst profile holdout: `1.8293899297714233`.
- Mean delta versus baseline: `-0.05169794956843058`.
- Leaderboard evidence score for the boundary row: `1`.

## Current Decision

Decision string:

`external_2025_190424aa_surface_prune_profile_scoped_lid10002_only`

Interpretation: the current GGAE/Fast-GPR-FWI surface-prune optimizer is profile/window scoped on 190424AA. LID10002 supports provisional location/cover evidence, but adjacent LID10001 and LID10003 improve without validating. Do not claim autonomous adjacent-profile transfer, diameter, or material validation from this branch.

## What Remains Blocked

- Adjacent-profile transfer is not reliable on the 190424AA cluster.
- LID10001 and LID10003 should not be used as prediction evidence under the current method.
- The next real-data branch should move to another profile family or a clearly different preprocessing/source extraction rather than over-tuning this cluster.

## Validation

- `python -m py_compile run_ggae2025_external_2025_190424aa_profile_boundary_synthesis.py run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_ggae2025_external_2025_190424aa_profile_boundary_synthesis.py tests/test_field_method_validation_leaderboard.py -q`
- Result: `19 passed in 0.62s`.
- `git diff --check -- run_ggae2025_external_2025_190424aa_profile_boundary_synthesis.py tests/test_ggae2025_external_2025_190424aa_profile_boundary_synthesis.py run_field_method_validation_leaderboard.py tests/test_field_method_validation_leaderboard.py`
- Profile-boundary figure: `1753x835`, nonwhite fraction `0.3716127357378796`, RGB std `70.27707993363538`.
- Leaderboard figure: `1575x720`, nonwhite fraction `0.250015873015873`, RGB std `73.10366853310023`.

## Artifact Paths

- `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/246_external_2025_190424aa_surface_prune_profile_boundary_synthesis`
- `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard`

## Next Defensible Task

Move to another real field-data family or a clearly different preprocessing/source extraction branch. Avoid synthetic work and avoid over-tuning 190424AA after the adjacent-profile boundary is now documented.

## Marathon Status

The requested real-field-data marathon is still active.
