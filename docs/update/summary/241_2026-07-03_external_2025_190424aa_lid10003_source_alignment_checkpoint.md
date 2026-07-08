# External 2025 190424AA LID10003 Source Alignment Checkpoint

## What changed

- Ran a wider LID10003-only source/event alignment ladder with:
  - Time-shift offsets -0.18, -0.12, -0.06, 0.00, +0.06, +0.12 ns.
  - Source polarity `inverted` and `normal`.
  - Signed amplitude scaling.
  - Fixed 16 mm diameter hypothesis from the prior LID10003 top candidate.
- Generated artifact:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/294_external_2025_190424aa_lid10003_wide_signed_source_alignment_ladder`
- Reran the full LID10003 radius/epsr matrix using the best tested source setting:
  - Source polarity: `normal`.
  - Time shift: -0.03 ns.
  - Amplitude scale mode: `signed`.
- Generated artifact:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/295_external_2025_190424aa_lid10003_rank1_source_aligned_signed_radius_epsr_transfer_matrix`
- Regenerated latest three-profile transfer synthesis with artifacts 277, 292, and 295:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/296_external_2025_190424aa_radius_epsr_source_aligned_signed_profile_transfer_synthesis`
- Regenerated the method leaderboard.

## Key numbers

- LID10003 wide signed source ladder, artifact 294:
  - Decision: `external_2025_190424aa_source_alignment_no_material_adjacent_profile_gain`.
  - Best variant: `normal_dtp0.120ns`.
  - Best time shift: -0.03 ns.
  - Mean holdout loss: 1.75702.
  - Baseline holdout loss: 1.84893.
  - Improvement: 4.97 percent, below the 5 percent material-gain threshold.
  - Runtime sum: 133.022 s.
- LID10003 source-aligned/signed radius/epsr matrix, artifact 295:
  - Decision: `external_2025_190424aa_lid10003_rank1_source_aligned_signed_radius_epsr_candidate_top16mm_range8to24mm`.
  - Top diameter: 16.00000 mm.
  - 5 percent near-best diameter range: 8.00016-23.99984 mm.
  - Top epsr: 3.96834.
  - Top x: 1.27726400 m.
  - Top cover depth: 95.51340 mm.
  - Mean holdout loss: 1.67812.
  - Runtime sum: 49.068 s.
- Candidate losses for artifact 295:
  - 8 mm: 1.71501.
  - 16 mm: 1.67812.
  - 24 mm: 1.72015.
- Latest three-profile synthesis, artifact 296:
  - Decision: `external_2025_190424aa_radius_epsr_profile_transfer_profile_local_only`.
  - Valid profiles under threshold 0.95: `LID10002_rank2` only.
  - Top diameter sequence: 24 mm, 24 mm, 16 mm.
  - Top epsr sequence: 3.97638, 3.97231, 3.96834.
  - Holdout loss sequence: 0.61396, 0.98004, 1.67812.

## What remains blocked

- LID10003 remains a high-loss outlier after the wider source/time and signed-amplitude control.
- LID10003 still has broad 8-24 mm near-best diameter range, so it does not stabilize diameter transfer.
- The next LID10003 work should inspect event-window and wavelet extraction, not just continue small time-shift sweeps.

## Current decision

Source alignment solved a large part of LID10001 but not LID10003. The current 190424AA field-fit estimate is strongest for LID10002 and source-aligned LID10001, both preferring 24 mm, while LID10003 remains unresolved and blocks a three-profile transferable claim.

## Next defensible task

- Build a LID10003 event-window/wavelet audit:
  - Compare observed event-window energy and wavelet alignment against LID10002/LID10001.
  - Test alternate event apex/window selection if the current window is miscentered.
  - Only then rerun the radius/epsr matrix.
- Start the 3D survey geometry inventory in parallel so x/y/z/radius/length can be formulated on actual multi-profile data.

## Validation/resource checks

- LID10003 wide signed source ladder completed -> artifact 294.
- LID10003 source-aligned/signed matrix completed -> artifact 295.
- Latest transfer synthesis completed -> artifact 296.
- `/home/lam002/miniforge3/bin/python run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_source_alignment_ladder.py tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 50 passed.
- `git diff --check` passed for the touched field-method files and recent checkpoints.
- Figure metadata:
  - Artifact 294 source-alignment figure: 2144 x 835 RGBA.
  - Artifact 295 candidate figure: 1830 x 767 RGBA.

## Artifact paths

- Wide source ladder summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/294_external_2025_190424aa_lid10003_wide_signed_source_alignment_ladder/data/external_2025_190424aa_source_alignment_summary.json`
- LID10003 source-aligned/signed matrix summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/295_external_2025_190424aa_lid10003_rank1_source_aligned_signed_radius_epsr_transfer_matrix/data/external_2025_190424aa_radius_epsr_candidate_summary.json`
- Latest transfer summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/296_external_2025_190424aa_radius_epsr_source_aligned_signed_profile_transfer_synthesis/data/external_2025_190424aa_radius_epsr_profile_transfer_summary.json`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
