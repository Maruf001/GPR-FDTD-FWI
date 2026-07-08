# External 2025 190424AA Forced Spatial-Mean Radius/Epsr Transfer Checkpoint

## What changed

- Reran the 190424AA fixed-radius/epsilon field-fit matrix for adjacent profiles after forcing the same `spatial_mean_subtracted` preprocessing family used by the low-loss LID10002/rank2 case.
- Generated new GGAE2025/Fast-GPR-FWI-style field-fit artifacts:
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/287_external_2025_190424aa_lid10001_rank1_forced_spatial_mean_radius_epsr_transfer_matrix`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/288_external_2025_190424aa_lid10003_rank1_forced_spatial_mean_radius_epsr_transfer_matrix`
  - `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/289_external_2025_190424aa_radius_epsr_forced_spatial_mean_profile_transfer_synthesis`
- Patched `run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py` so transfer synthesis can use explicit artifact directories instead of only the older default glob.
- Patched `run_field_method_validation_leaderboard.py` so the leaderboard selects the newest controlled forced-preprocessing profile transfer and wavelet/preprocessing diagnostics.

## Key numbers

- LID10002/rank2 reference, artifact 277:
  - Top diameter: 23.99984 mm.
  - 5 percent near-best diameter range: 8.00016-23.99984 mm.
  - Top epsr: 3.97638.
  - Top x: 0.13385693 m.
  - Top cover depth: 93.85294 mm.
  - Mean holdout loss: 0.61396.
  - Runtime sum: 49.321 s.
- LID10001/rank1 forced spatial mean, artifact 287:
  - Top diameter: 8.00016 mm.
  - 5 percent near-best diameter range: 8.00016-23.99984 mm.
  - Top epsr: 3.98552.
  - Top x: 1.70980215 m.
  - Top cover depth: 85.73818 mm.
  - Mean holdout loss: 2.00000.
  - Runtime sum: 49.331 s.
- LID10003/rank1 forced spatial mean, artifact 288:
  - Top diameter: 16.00000 mm.
  - 5 percent near-best diameter range: 8.00016-23.99984 mm.
  - Top epsr: 4.02397.
  - Top x: 1.27737874 m.
  - Top cover depth: 95.69186 mm.
  - Mean holdout loss: 1.84893.
  - Runtime sum: 48.847 s.
- Forced-spatial transfer synthesis, artifact 289:
  - Decision: `external_2025_190424aa_radius_epsr_profile_transfer_profile_local_only`.
  - Valid profiles under threshold 0.95: `LID10002_rank2` only.
  - Top diameter sequence: 24 mm, 8 mm, 16 mm.
  - Top epsr sequence: 3.97638, 3.98552, 4.02397.
  - Holdout loss sequence: 0.61396, 2.00000, 1.84893.

## What remains blocked

- Matched preprocessing did not make the adjacent profiles pass the current field-fit loss threshold.
- The optimizer should still report local top-fit diameter/epsr candidates and near-best ranges for each profile/window.
- The three-profile result does not yet justify a transferable physical diameter/permittivity claim across neighboring profiles.

## Current decision

For 190424AA, the current best defensible statement is profile-local estimation. LID10002/rank2 gives a low-loss local fit with a 24 mm top diameter but broad 8-24 mm near-best range. LID10001 and LID10003 now have controlled-preprocessing local candidates, but their losses remain high, so they do not stabilize the profile-transfer claim.

## Next defensible task

- Move from preprocessing control to source/event alignment control: fit or rank profile-specific time shift, polarity, and wavelet scaling before repeating the diameter/epsr matrix.
- In parallel, start the real 3D data-geometry intake for datasets that include profile spacing or survey grids, because y-location and rebar length cannot be estimated from a single isolated B-scan.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py -q` -> 2 passed.
- `/home/lam002/miniforge3/bin/python run_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py --run-name external_2025_190424aa_radius_epsr_forced_spatial_mean_profile_transfer_synthesis ...` -> artifact 289.
- `/home/lam002/miniforge3/bin/python -m py_compile run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_method_validation_leaderboard.py -q` -> 33 passed.
- `/home/lam002/miniforge3/bin/python run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 46 passed.
- Figure metadata:
  - Artifact 287 candidate figure: 1808 x 767 RGBA.
  - Artifact 288 candidate figure: 1816 x 767 RGBA.
  - Artifact 289 transfer figure: 1634 x 835 RGBA.

## Artifact paths

- LID10001 summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/287_external_2025_190424aa_lid10001_rank1_forced_spatial_mean_radius_epsr_transfer_matrix/data/external_2025_190424aa_radius_epsr_candidate_summary.json`
- LID10003 summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/288_external_2025_190424aa_lid10003_rank1_forced_spatial_mean_radius_epsr_transfer_matrix/data/external_2025_190424aa_radius_epsr_candidate_summary.json`
- Transfer summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/289_external_2025_190424aa_radius_epsr_forced_spatial_mean_profile_transfer_synthesis/data/external_2025_190424aa_radius_epsr_profile_transfer_summary.json`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
