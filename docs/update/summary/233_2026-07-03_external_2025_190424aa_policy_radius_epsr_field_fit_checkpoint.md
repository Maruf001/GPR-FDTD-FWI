# External 2025 190424AA Policy Radius/Epsr Field Fit Checkpoint

## What changed

- Added `run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`.
- The wrapper reads the latest 190424AA field-window policy adapter, executes fixed-radius field-window optimizer subruns, and reports the best-fit diameter/permittivity plus near-best ranges.
- Added focused tests in `tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`.
- Updated `run_field_method_validation_leaderboard.py` so the radius/epsr row carries x, cover depth, and runtime from the latest summary.

## Key numbers

- Latest artifact: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis`.
- Profile/window: `190424AA_LID10002_rank2`, 14 selected traces, x window 0.100-0.190 m, loss time window 1.15-1.75 ns.
- Optimizer: GGAE2025-style coordinate-MLP material field plus explicit rebar geometry, empirical field wavelet, Fast-GPR-FWI-style staged Adam schedule, even/odd internal consistency splits.
- Fixed-radius candidates: 4, 8, and 12 mm radius.
- Top field-fit candidate: 24.00 mm diameter, 11.9999 mm radius.
- Top concrete epsr estimate: 3.97638.
- 5 percent near-best diameter range: 8.00-24.00 mm.
- 5 percent near-best epsr range: 3.97492-3.98417.
- Top x estimate: 0.1338569 m.
- Top cover-depth estimate: 93.8529 mm.
- Near-best x range: 0.1338464-0.1338675 m.
- Near-best cover-depth range: 93.7825-93.9234 mm.
- Mean holdout loss for top candidate: 0.6139617.
- Total optimizer runtime across six subruns: 49.321 s.

## What remains blocked

- The diameter is reportable as a top field-fit estimate, but the 8-24 mm near-best band shows it is still non-unique on this single event window.
- The current Fast-GPR-FWI repo path remains treated as accelerated 2D-TMz/extruded until true z-derivative/full-field 3D kernels are implemented.
- y-position and rebar length are not claimed from this single 2D B-scan window.

## Current decision

`external_2025_190424aa_radius_epsr_candidate_top24mm_range8to24mm`

This is a real field-data estimate, not a synthetic gate. It supports a stable local x/cover prediction for the selected 190424AA event window and gives a top diameter/epsr candidate with an explicit uncertainty range. It does not prove physical ground truth.

## Next defensible task

- Run the same policy-radius matrix on an adjacent 190424AA profile/window, or on another available field dataset profile, to test whether the 24 mm top candidate and the tight x/cover estimate transfer.
- In parallel, start a true-3D field-data design branch that requires multiple profiles or a 3D acquisition stack before claiming y-position/length.

## Validation/resource checks

- `python -m py_compile run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py`
- `python -m pytest tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py -q` -> 6 passed.
- `python run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py --device auto --python-exe /home/lam002/miniforge3/bin/python` -> artifact 277.
- `python run_field_method_validation_leaderboard.py`
- `python -m pytest tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_ggae2025_external_2025_190424aa_radius_epsr_candidate_synthesis.py tests/test_field_method_validation_leaderboard.py -q` -> 38 passed.
- `git diff --check -- run_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py tests/test_external_2025_190424aa_policy_radius_epsr_field_fit_matrix.py run_field_method_validation_leaderboard.py`
- Main figure dimensions checked: `external_2025_190424aa_radius_epsr_candidate.png` is 1804 x 767 RGBA.
- Six subrun B-scan fit figures exist and are 2313 x 784.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis/data/external_2025_190424aa_radius_epsr_candidate_summary.json`
- Candidate rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis/data/external_2025_190424aa_radius_epsr_candidate_rows.csv`
- Per-run rows: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis/data/external_2025_190424aa_radius_epsr_candidate_run_rows.csv`
- Commands: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis/data/external_2025_190424aa_policy_radius_epsr_commands.csv`
- Figure: `outputs/validation_exp_on_field_data/ggae2025_ifwi_gpr/277_external_2025_190424aa_radius_epsr_candidate_synthesis/figures/external_2025_190424aa_radius_epsr_candidate.png`
- Leaderboard: `outputs/validation_exp_on_field_data/method_validation_leaderboard/001_gssi51600s_field_method_validation_leaderboard/data/field_method_validation_leaderboard.csv`

## Marathon status

The requested active-session marathon remains active; this is a checkpoint, not a stop.
