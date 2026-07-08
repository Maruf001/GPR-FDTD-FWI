# External 2025 190424AA Wavelet/Preprocessing Transfer Checkpoint

## What changed

- Added `run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py`.
- The script compares the empirical aligned wavelets, selected preprocessing variants, spectral metrics, and event-window amplitudes for:
  - LID10001/rank1 preprocessor 117.
  - LID10002/rank2 preprocessor 120.
  - LID10003/rank1 preprocessor 121.
- Added focused tests in `tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py`.
- Added the wavelet/preprocessing diagnostic row to the method leaderboard.

## Key numbers

- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/282_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics`.
- Decision: `external_2025_190424aa_wavelet_preprocessing_mismatch_present`.
- Selected preprocessing variants:
  - LID10001/rank1: `svd_rank1_subtracted`.
  - LID10002/rank2: `spatial_mean_subtracted`.
  - LID10003/rank1: `svd_rank1_subtracted`.
- Wavelet correlation to LID10002:
  - LID10001/rank1: -0.47867.
  - LID10002/rank2: 1.00000.
  - LID10003/rank1: 0.52824.
- Minimum adjacent absolute wavelet correlation to LID10002: 0.47867.
- Event-window RMS:
  - LID10001/rank1: 0.15686.
  - LID10002/rank2: 0.81323.
  - LID10003/rank1: 0.55045.
- Peak wavelet frequency:
  - LID10001/rank1: 1.08649 GHz.
  - LID10002/rank2: 2.17297 GHz.
  - LID10003/rank1: 2.17297 GHz.

## What remains blocked

- Adjacent-profile transfer is not currently a fair diameter test because the preprocessing/wavelet inputs differ materially from the only low-loss LID10002 case.
- A shared radius/epsilon optimizer matrix should not be expected to transfer until the wavelet/source/preprocessing mismatch is addressed.

## Current decision

The high adjacent-profile residuals are consistent with profile-specific preprocessing/wavelet mismatch. The next optimizer run should control this variable before making any claim about transferable diameter.

## Next defensible task

- Run a controlled preprocessing-variant rerun: force LID10001/LID10003 through a LID10002-like spatial-mean-subtracted path, or force LID10002 through SVD-rank1, then compare wavelet correlation and field-fit loss.
- Only after a matched preprocessing family is established should radius/epsilon transfer be rerun.

## Validation/resource checks

- `python -m py_compile run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py`
- `python -m pytest tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py -q` -> 3 passed.
- `python run_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py` -> artifact 282.
- `python run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 45 passed.
- `git diff --check` passed for touched branch files.
- Diagnostic figure dimensions checked: 1634 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/282_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics/data/external_2025_190424aa_wavelet_preprocessing_summary.json`
- Rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/282_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics/data/external_2025_190424aa_wavelet_preprocessing_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/282_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics/figures/external_2025_190424aa_wavelet_preprocessing.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
