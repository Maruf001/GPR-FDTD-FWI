# External 2025 190424AA Event-Window Waveform Audit Checkpoint

## What changed

- Added `run_external_2025_190424aa_event_window_waveform_audit.py`.
- The audit reads saved observed/predicted/residual arrays from the current top field-fit candidates:
  - LID10002/rank2 artifact 277, top 24 mm candidate.
  - LID10001 source-aligned artifact 292, top 24 mm candidate.
  - LID10003 source-aligned/signed artifact 295, top 16 mm candidate.
- Added tests in `tests/test_external_2025_190424aa_event_window_waveform_audit.py`.
- Added the event-window waveform audit row to the method leaderboard.
- Generated artifact:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/297_external_2025_190424aa_event_window_waveform_audit`

## Key numbers

- Decision: `external_2025_190424aa_event_window_waveform_lid10003_mismatch`.
- LID10002/rank2:
  - Mean holdout loss: 0.61396.
  - Mean normalized residual norm: 0.72781.
  - Mean best-lag correlation: 0.87711.
  - Mean event loss: 0.25489.
  - Diameter: 23.99984 mm.
  - Epsr: 3.97638.
- LID10001 source-aligned:
  - Mean holdout loss: 0.98004.
  - Mean normalized residual norm: 0.90862.
  - Mean best-lag correlation: 0.72677.
  - Mean event loss: 0.39848.
  - Diameter: 23.99984 mm.
  - Epsr: 3.97231.
- LID10003 source-aligned/signed:
  - Mean holdout loss: 1.67812.
  - Mean normalized residual norm: 1.11585.
  - Mean best-lag correlation: 0.83327.
  - Mean event loss: 0.84834.
  - Diameter: 16.00000 mm.
  - Epsr: 3.96834.
- High residual profiles: LID10001 source-aligned and LID10003 source-aligned/signed.
- High loss profiles: LID10003 source-aligned/signed.

## What remains blocked

- LID10003 is still poorly explained by the current event-window/wavelet model even after source polarity, time-shift, and signed-amplitude controls.
- LID10001 has improved diameter ranking but still shows nontrivial residual structure, so it should be treated as a stronger field-fit estimate than before but not physical ground truth.
- The next LID10003 step should audit event picking and wavelet extraction, not just tune source time further.

## Current decision

The current 190424AA result is no longer “radius not identifiable everywhere.” It is more specific: LID10002 and source-aligned LID10001 both prefer 24 mm, while LID10003 has a waveform/event-window mismatch that blocks a stable three-profile transfer claim.

## Next defensible task

- Build a LID10003 event-window/apex sensitivity run:
  - Shift or widen the x/time event crop around LID10003.
  - Rerun the source-aligned/signed 16 mm and 24 mm candidates first, then only run the full radius matrix if the residual metric improves.
- Start the 3D survey geometry inventory in parallel so y-position and length are based on data with actual y/profile spacing.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_external_2025_190424aa_event_window_waveform_audit.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_event_window_waveform_audit.py -q` -> 4 passed.
- Audit command completed -> artifact 297.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_external_2025_190424aa_event_window_waveform_audit.py -q` -> 39 passed.
- `/home/lam002/miniforge3/bin/python run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_event_window_waveform_audit.py tests/test_external_2025_190424aa_source_alignment_ladder.py tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 55 passed.
- `git diff --check` passed for touched audit/leaderboard files and checkpoint docs.
- Figure metadata: 2314 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/297_external_2025_190424aa_event_window_waveform_audit/data/external_2025_190424aa_event_window_waveform_summary.json`
- Profile rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/297_external_2025_190424aa_event_window_waveform_audit/data/external_2025_190424aa_event_window_waveform_profile_rows.csv`
- Subrun rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/297_external_2025_190424aa_event_window_waveform_audit/data/external_2025_190424aa_event_window_waveform_subrun_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/297_external_2025_190424aa_event_window_waveform_audit/figures/external_2025_190424aa_event_window_waveform_audit.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
