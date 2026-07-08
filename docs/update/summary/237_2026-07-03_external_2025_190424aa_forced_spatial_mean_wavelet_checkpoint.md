# External 2025 190424AA Forced Spatial-Mean Wavelet Checkpoint

## What changed

- Forced LID10001/rank1 and LID10003/rank1 through the same `spatial_mean_subtracted` preprocessing family used by the low-loss LID10002/rank2 field-fit case.
- Generated new preprocessors:
  - `outputs/validation_exp_on_field_data/jazayeri_2019_rebar_fwi/126_external_2025_ids_scattered_field_preprocessor_190424aa_lid10001_rank1_forced_spatial_mean`
  - `outputs/validation_exp_on_field_data/jazayeri_2019_rebar_fwi/127_external_2025_ids_scattered_field_preprocessor_190424aa_lid10003_rank1_forced_spatial_mean`
- Updated and reran `run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py` so forced preprocessor paths are explicit inputs and low wavelet correlation still flags a mismatch even when the preprocessing family matches.
- Added focused regression coverage for forced preprocessor path handling and the low-correlation decision rule.
- Regenerated the method leaderboard after artifact 286.

## Key numbers

- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/286_external_2025_190424aa_wavelet_preprocessing_forced_spatial_mean_diagnostics`.
- Decision: `external_2025_190424aa_wavelet_preprocessing_mismatch_present`.
- Compared preprocessing variants: all three profiles use `spatial_mean_subtracted`.
- Minimum adjacent absolute wavelet correlation to LID10002: 0.58641.
- LID10001 wavelet correlation to LID10002 improved under forced spatial mean, but LID10003 remains weak enough that transfer is still not a clean diameter/permittivity test.
- Interpretation: forcing the same preprocessing family reduces one confound, but the adjacent-profile wavelet/source/event mismatch remains.

## What remains blocked

- Adjacent-profile diameter/permittivity transfer is still not clean until source wavelet and event alignment are controlled across profiles.
- This does not block reporting local top-fit radius/permittivity for a given profile/window; it blocks claiming that one profile's settings transfer robustly to neighboring profiles.

## Current decision

The next field-fit branch should rerun the radius/epsilon candidate matrix on the forced-spatial-mean LID10001 and LID10003 preprocessors. That directly tests whether controlling preprocessing improves the high-loss adjacent-profile fits.

## Next defensible task

- Run the fixed-radius/epsilon field-fit matrix for LID10001 with preprocessor 126.
- Run the fixed-radius/epsilon field-fit matrix for LID10003 with preprocessor 127.
- Synthesize the forced-spatial transfer outcome and compare it against artifacts 278, 279, and 280.

## Validation/resource checks

- `python -m py_compile run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py`
- `python -m pytest tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py -q` -> 4 passed.
- `python run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py --run-name external_2025_190424aa_wavelet_preprocessing_forced_spatial_mean_diagnostics ...` -> artifact 286.
- `python run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 46 passed.
- Diagnostic figure dimensions checked previously for this branch: 1634 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/286_external_2025_190424aa_wavelet_preprocessing_forced_spatial_mean_diagnostics/data/external_2025_190424aa_wavelet_preprocessing_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/286_external_2025_190424aa_wavelet_preprocessing_forced_spatial_mean_diagnostics/data/external_2025_190424aa_wavelet_preprocessing_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/286_external_2025_190424aa_wavelet_preprocessing_forced_spatial_mean_diagnostics/figures/external_2025_190424aa_wavelet_preprocessing.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
