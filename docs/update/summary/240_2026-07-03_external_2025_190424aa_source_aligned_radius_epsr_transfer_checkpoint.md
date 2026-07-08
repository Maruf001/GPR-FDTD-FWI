# External 2025 190424AA Source-Aligned Radius/Epsr Transfer Checkpoint

## What changed

- Reran the full fixed-radius/epsilon candidate matrix for LID10001 using the best source setting from artifact 291:
  - Source polarity: `normal`.
  - Time shift: 0.03 ns.
  - Same forced-spatial-mean preprocessor 126.
- Generated source-aligned LID10001 estimator artifact:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/292_external_2025_190424aa_lid10001_rank1_source_aligned_radius_epsr_transfer_matrix`
- Regenerated three-profile radius/epsr transfer synthesis using:
  - LID10002/rank2 artifact 277.
  - LID10001 source-aligned artifact 292.
  - LID10003 forced-spatial-mean artifact 288.
- Generated transfer synthesis:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/293_external_2025_190424aa_radius_epsr_source_aligned_profile_transfer_synthesis`
- Regenerated the method leaderboard so the profile-transfer row points at artifact 293.

## Key numbers

- LID10001 source-aligned matrix, artifact 292:
  - Decision: `external_2025_190424aa_lid10001_rank1_source_aligned_radius_epsr_candidate_top24mm_range24to24mm`.
  - Top diameter: 23.99984 mm.
  - 5 percent near-best diameter range: 23.99984-23.99984 mm.
  - Top epsr: 3.97231.
  - Top x: 1.70980215 m.
  - Top cover depth: 85.73818 mm.
  - Mean holdout loss: 0.98004.
  - Runtime sum: 49.498 s.
- Candidate losses for LID10001 source-aligned:
  - 8 mm: 1.09893.
  - 16 mm: 1.09285.
  - 24 mm: 0.98004.
- Source-aligned three-profile transfer, artifact 293:
  - Decision: `external_2025_190424aa_radius_epsr_profile_transfer_profile_local_only`.
  - Threshold: 0.95.
  - Valid profiles under threshold: `LID10002_rank2` only.
  - Top diameter sequence: 24 mm, 24 mm, 16 mm.
  - Top epsr sequence: 3.97638, 3.97231, 4.02397.
  - Holdout loss sequence: 0.61396, 0.98004, 1.84893.

## What remains blocked

- LID10001 now strongly supports the same 24 mm diameter candidate as LID10002 after source alignment, but its loss remains slightly above the strict 0.95 threshold.
- LID10003 remains the limiting profile. Its best tested source/time variant improved only 2.89 percent and the source-aligned transfer synthesis still has a 16 mm top candidate there.
- We still should report LID10001/LID10002 as field-fit estimates, not physical ground truth.

## Current decision

Source/time alignment materially changes the field-data radius/epsr estimate. For LID10001, the earlier 8 mm candidate was not robust; after using the source setting selected by a real optimizer ladder, the top candidate becomes 24 mm with no 5 percent near-best spread. The three-profile claim remains profile-local because LID10003 is unresolved.

## Next defensible task

- Expand LID10003 source/event alignment rather than immediately changing radius physics:
  - Wider time-shift ladder.
  - Possibly signed amplitude scaling.
  - Recheck event window and wavelet extraction.
- In parallel, start the 3D data geometry inventory for datasets with known profile spacing so y-position and length can be formulated honestly.

## Validation/resource checks

- LID10001 source-aligned matrix command completed -> artifact 292.
- Source-aligned profile synthesis command completed -> artifact 293.
- `/home/lam002/miniforge3/bin/python run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_source_alignment_ladder.py tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 50 passed.
- `git diff --check` passed for touched field-method files and checkpoints.
- Figure metadata:
  - Artifact 292 candidate figure: 1804 x 767 RGBA.
  - Artifact 293 transfer figure: 1634 x 835 RGBA.

## Artifact paths

- LID10001 source-aligned summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/292_external_2025_190424aa_lid10001_rank1_source_aligned_radius_epsr_transfer_matrix/data/external_2025_190424aa_radius_epsr_candidate_summary.json`
- LID10001 source-aligned candidate rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/292_external_2025_190424aa_lid10001_rank1_source_aligned_radius_epsr_transfer_matrix/data/external_2025_190424aa_radius_epsr_candidate_rows.csv`
- Source-aligned transfer summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/293_external_2025_190424aa_radius_epsr_source_aligned_profile_transfer_synthesis/data/external_2025_190424aa_radius_epsr_profile_transfer_summary.json`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
