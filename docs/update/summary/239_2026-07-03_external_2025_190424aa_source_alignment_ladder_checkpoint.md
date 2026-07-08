# External 2025 190424AA Source Alignment Ladder Checkpoint

## What changed

- Exposed `--source-polarity` and `--amplitude-scale-mode` in `run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`; defaults remain `inverted` and `positive`.
- Added `run_external_2025_190424aa_source_alignment_ladder.py`.
- The ladder runs real GGAE2025/Fast-GPR-FWI-style optimizer subruns with:
  - Fixed current top-radius hypotheses from the forced-spatial-mean matrix.
  - Even/odd holdout pairs.
  - Time-shift offsets -0.06 ns, 0.00 ns, +0.06 ns.
  - Source polarity `inverted` and `normal`.
  - Short staged Adam schedule `epsr:0.35,1.20:4;dual:0.75,2.40:4;geometry:full:5`.
- Added tests in `tests/test_external_2025_190424aa_source_alignment_ladder.py`.
- Added the source-alignment diagnostic row to the method leaderboard.

## Key numbers

- Artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/291_external_2025_190424aa_source_alignment_ladder`.
- Decision: `external_2025_190424aa_source_alignment_improves_adjacent_profile_fit`.
- Subruns: 24.
- Runtime sum: 133.329 s.
- LID10001/rank1 forced spatial mean:
  - Baseline mean holdout loss from artifact 287: 2.00000.
  - Best source variant: `normal_dtp0.060ns`.
  - Best source time shift: 0.03 ns.
  - Mean holdout loss: 1.02147.
  - Improvement vs baseline: 48.93 percent.
  - Fixed diameter hypothesis: 8.00016 mm.
  - Mean epsr: 3.96957.
  - Mean x: 1.70973659 m.
  - Mean cover depth: 85.68427 mm.
- LID10003/rank1 forced spatial mean:
  - Baseline mean holdout loss from artifact 288: 1.84893.
  - Best source variant: `inverted_dtm0.060ns`.
  - Best source time shift: -0.21 ns.
  - Mean holdout loss: 1.79549.
  - Improvement vs baseline: 2.89 percent.
  - Fixed diameter hypothesis: 16.00000 mm.
  - Mean epsr: 4.05167.
  - Mean x: 1.27712679 m.
  - Mean cover depth: 95.72359 mm.

## What remains blocked

- LID10001 now has evidence that source polarity/time alignment was a major cause of the high-loss adjacent-profile fit.
- LID10003 remains high-loss after this small source alignment ladder, so its failure is not fixed by the tested polarity/time-shift grid.
- This ladder is not a diameter estimator by itself; it identifies better source/event settings for follow-up radius/epsr candidate matrices.

## Current decision

The adjacent-profile transfer failure is not only a radius/permittivity issue. For LID10001, source polarity and time-zero alignment materially change field-fit quality. The next radius/epsr matrix for LID10001 should use normal polarity and +0.06 ns relative time-shift before interpreting diameter ranking.

## Next defensible task

- Rerun the full fixed-radius/epsilon candidate matrix for LID10001 using `source_polarity=normal` and `time_shift_init_ns=0.03`.
- Keep LID10003 as a separate unresolved profile and either expand its source/time grid or revisit event-window/wavelet extraction.
- After the corrected LID10001 matrix, update the three-profile transfer synthesis and leaderboard.

## Validation/resource checks

- `/home/lam002/miniforge3/bin/python -m py_compile run_external_2025_190424aa_source_alignment_ladder.py run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_source_alignment_ladder.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py -q` -> 7 passed.
- Dry run: `/home/lam002/miniforge3/bin/python run_external_2025_190424aa_source_alignment_ladder.py --run-name external_2025_190424aa_source_alignment_ladder_dry_run --dry-run` -> artifact 290.
- Real run: `/home/lam002/miniforge3/bin/python run_external_2025_190424aa_source_alignment_ladder.py --run-name external_2025_190424aa_source_alignment_ladder` -> artifact 291.
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_field_method_validation_leaderboard.py tests/test_external_2025_190424aa_source_alignment_ladder.py -q` -> 37 passed.
- `/home/lam002/miniforge3/bin/python run_field_method_validation_leaderboard.py`
- `/home/lam002/miniforge3/bin/python -m pytest tests/test_external_2025_190424aa_source_alignment_ladder.py tests/test_external_2025_190424aa_wavelet_preprocessing_transfer_diagnostics.py tests/test_external_2025_190424aa_transfer_residual_diagnostics.py tests/test_external_2025_190424aa_radius_epsr_profile_transfer_synthesis.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_field_method_validation_leaderboard.py -q` -> 50 passed.
- `git diff --check` passed for the touched source, tests, and checkpoint docs.
- Figure metadata: source-alignment figure is 2144 x 835 RGBA.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/291_external_2025_190424aa_source_alignment_ladder/data/external_2025_190424aa_source_alignment_summary.json`
- Variant rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/291_external_2025_190424aa_source_alignment_ladder/data/external_2025_190424aa_source_alignment_variant_rows.csv`
- Run rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/291_external_2025_190424aa_source_alignment_ladder/data/external_2025_190424aa_source_alignment_run_rows.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/291_external_2025_190424aa_source_alignment_ladder/figures/external_2025_190424aa_source_alignment_ladder.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
