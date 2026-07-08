# External 2025 190424AA Transfer Residual Diagnostics Checkpoint

## What changed

- Added `run_external_2025_190424aa_transfer_residual_diagnostics.py`.
- The diagnostic reads saved observed/predicted/residual arrays from the top-candidate subruns in artifacts 277, 278, and 279.
- It computes zero-lag correlation, best-lag correlation, best time lag, normalized residual norm, and a coarse failure mode.
- Added focused tests in `tests/test_external_2025_190424aa_transfer_residual_diagnostics.py`.
- Added a residual-diagnostic row to the method leaderboard.

## Key numbers

- Residual artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/281_external_2025_190424aa_transfer_residual_diagnostics`.
- Decision: `external_2025_190424aa_transfer_failure_wavelet_or_event_mismatch`.
- LID10002/rank2:
  - Mean holdout loss: 0.61396.
  - Mean best-lag correlation: 0.70386.
  - Mean absolute best lag: 0.02123 ns.
  - Mean normalized residual norm: 0.72781.
  - Failure mode: `low_loss_local_fit`.
- LID10001/rank1:
  - Mean holdout loss: 1.56922.
  - Mean best-lag correlation: 0.27917.
  - Mean absolute best lag: 0.02547 ns.
  - Mean normalized residual norm: 0.96749.
  - Failure mode: `high_loss_geometry_or_wavelet_amplitude_mismatch`.
- LID10003/rank1:
  - Mean holdout loss: 1.80153.
  - Mean best-lag correlation: 0.27083.
  - Mean absolute best lag: 0.03821 ns.
  - Mean normalized residual norm: 0.97210.
  - Failure modes: `high_loss_geometry_or_wavelet_amplitude_mismatch`; one split is also timing-lag sensitive.

## What remains blocked

- Adjacent-profile losses are too high for diameter/material claims.
- The dominant failure is not fixed by a simple uniform time shift; correlation remains weak even after small lag adjustment.
- More radius sweeps are not the next best use of time until wavelet/source/preprocessing/event selection improves for LID10001 and LID10003.

## Current decision

The 190424AA LID10002 radius/epsr estimate is a local event-window result. Adjacent-profile failures look like waveform/source/event mismatch first, not a mature transferable diameter inversion.

## Next defensible task

- Build a source/preprocessing diagnostic for LID10001/LID10003: compare empirical wavelets, observed event polarity, amplitude spectra, and event-window masks against LID10002.
- Use that result to decide whether to rerun adjacent profiles with profile-specific wavelet/timing/preprocessing or to move to a multi-profile/3D acquisition packet.

## Validation/resource checks

- `python -m py_compile run_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py`
- `python -m pytest tests/test_external_2025_190424aa_transfer_residual_diagnostics.py -q` -> 3 passed.
- `python run_external_2025_190424aa_transfer_residual_diagnostics.py` -> artifact 281.
- `python run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 42 passed.
- `git diff --check` passed for the touched branch files.
- Diagnostic figure dimensions checked: 1634 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/281_external_2025_190424aa_transfer_residual_diagnostics/data/external_2025_190424aa_transfer_residual_diagnostics_summary.json`
- Profile rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/281_external_2025_190424aa_transfer_residual_diagnostics/data/external_2025_190424aa_transfer_residual_profile_rows.csv`
- Per-run rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/281_external_2025_190424aa_transfer_residual_diagnostics/data/external_2025_190424aa_transfer_residual_diagnostic_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/281_external_2025_190424aa_transfer_residual_diagnostics/figures/external_2025_190424aa_transfer_residual_diagnostics.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
