# External 2025 190424AA Radius/Epsr Profile Transfer Checkpoint

## What changed

- Generalized `run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py` to accept profile-specific initializer, profile stem, aperture, time window, source timing, and decision prefix.
- Ran the same policy-constrained fixed-radius field-fit matrix on adjacent 190424AA profiles:
  - `LID10001_rank1` -> artifact 278.
  - `LID10003_rank1` -> artifact 279.
- Added `run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py` to compare artifacts 277, 278, and 279.
- Added focused tests for the profile-transfer synthesis.
- Updated the field-method leaderboard with a separate profile-transfer diagnostic row.

## Key numbers

- LID10002/rank2 artifact 277:
  - Top diameter: 24.00 mm.
  - 5 percent near-best diameter range: 8.00-24.00 mm.
  - Top epsr: 3.97638.
  - Top holdout loss: 0.61396.
  - Passes provisional 0.95 loss threshold: yes.
- LID10001/rank1 artifact 278:
  - Top diameter: 8.00 mm.
  - 5 percent near-best diameter range: 8.00-24.00 mm.
  - Top epsr: 3.98868.
  - Top holdout loss: 1.56922.
  - Passes provisional 0.95 loss threshold: no.
- LID10003/rank1 artifact 279:
  - Top diameter: 8.00 mm.
  - 5 percent near-best diameter range: 8.00-24.00 mm.
  - Top epsr: 4.00617.
  - Top holdout loss: 1.80153.
  - Passes provisional 0.95 loss threshold: no.
- Transfer artifact 280 decision: `external_2025_190424aa_radius_epsr_profile_transfer_profile_local_only`.
- Top diameter sequence across the three profiles: 24.00, 8.00, 8.00 mm.
- Valid profiles under the provisional loss threshold: `LID10002_rank2` only.

## What remains blocked

- The 24 mm LID10002 diameter is a local field-fit candidate, not a transferable profile-level claim.
- Adjacent profiles currently have high losses, so their 8 mm top candidates should not be used as physical claims either.
- y-position and rebar length still require a multi-profile or true 3D data product before inversion claims are defensible.

## Current decision

The radius/epsr method is useful for local event-window candidate estimation on LID10002, but the diameter estimate is not stable across adjacent 190424AA profiles. Location/cover remains much more stable within each selected event window than diameter.

## Next defensible task

- Improve the adjacent-profile field fit before treating profile transfer as a diameter test. The likely next branch is source/preprocessing/antenna mismatch diagnostics for LID10001 and LID10003, because their holdout losses are far above the LID10002 window.
- In parallel, start designing a true 3D/multi-profile inversion input packet for y/length estimation.

## Validation/resource checks

- `python -m py_compile run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`
- `python -m pytest tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py -q` -> 6 passed.
- `python run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py ...LID10001...` -> artifact 278.
- `python run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py ...LID10003...` -> artifact 279.
- `python -m py_compile run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py`
- `python -m pytest tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py -q` -> 6 passed.
- `python run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py` -> artifact 280.
- `python run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 39 passed.
- `git diff --check` passed for the touched branch files.
- Profile-transfer figure dimensions checked: 1634 x 835 RGBA.

## Artifact paths

- LID10002 matrix: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis`
- LID10001 matrix: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/278_external_2025_190424aa_lid10001_rank1_radius_epsr_transfer_matrix`
- LID10003 matrix: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/279_external_2025_190424aa_lid10003_rank1_radius_epsr_transfer_matrix`
- Transfer synthesis: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/280_external_2025_190424aa_radius_epsr_profile_transfer_synthesis`
- Transfer summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/280_external_2025_190424aa_radius_epsr_profile_transfer_synthesis/data/external_2025_190424aa_radius_epsr_profile_transfer_summary.json`
- Transfer rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/280_external_2025_190424aa_radius_epsr_profile_transfer_synthesis/data/external_2025_190424aa_radius_epsr_profile_transfer_rows.csv`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
