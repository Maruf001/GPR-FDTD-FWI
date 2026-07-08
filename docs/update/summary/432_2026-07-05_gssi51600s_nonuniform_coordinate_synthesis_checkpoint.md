# GSSI 51600S Nonuniform Coordinate Synthesis Checkpoint

## What Changed

- Built a cross-subset nonuniform coordinate synthesis using the trusted GSSI 51600S runs.
- Combined:
  - profiles 0-2 compatible geometry `[-0.20, 0.00, 0.20]`
  - profiles 1-3 best local-search geometry `[-0.20, 0.00, 0.14]`
- Converted those subset offsets into a relative four-profile coordinate hypothesis with profile 1 set to zero:
  - profile 0: `-0.20 m`
  - profile 1: `0.00 m`
  - profile 2: `0.20 m`
  - profile 3: `0.34 m`
- Added a synthesis card comparing this nonuniform coordinate hypothesis against the current uniform `0.22 m` reference across both overlapping profile subsets.
- Regenerated the latest GSSI prediction bundle and live query so they report the nonuniform coordinate synthesis result.
- Updated the Sunday daily note with the nonuniform coordinate hypothesis.

## Key Numbers

- Synthesis decision: `nonuniform_coordinate_synthesis_improves_joint_short_branch_needs_confirmation`.
- Candidate profile spacings: `0.20 m`, `0.20 m`, `0.14 m`.
- Candidate mean objective loss: `0.978122354`.
- Uniform `0.22 m` reference mean objective loss: `0.978138119`.
- Candidate mean objective-loss delta vs uniform `0.22 m`: `-1.5765e-05`.
- Candidate mean field-L1 delta vs uniform `0.22 m`: `-8.8602e-05`.
- Candidate mean length: `0.183834 m`.
- Candidate length range across the two overlapping subsets: `0.183223-0.184445 m`.
- Candidate mean diameter: `17.306120 mm`.
- Candidate diameter range: `17.295185-17.317055 mm`.
- Candidate mean relative permittivity: `2.040485`.
- Candidate mean conductivity: `0.00265994 S/m`.

## Current Decision

The nonuniform coordinate hypothesis improves the joint field fit slightly and keeps both overlapping profile subsets on the short finite-length branch. It is now the strongest optimizer-estimated y-geometry hypothesis, but it is still not measured survey geometry.

## What Remains Blocked

- The profile y coordinates are optimizer-estimated, not measured.
- The profile 2 to profile 3 spacing of `0.14 m` needs denser confirmation around nearby values.
- The result should be checked against additional event windows before narrowing the public finite-length range.

## Next Defensible Task

Run a narrower local profile-position search around the nonuniform coordinate hypothesis, especially profile 2 to profile 3 spacing near `0.12-0.16 m`, and check whether the candidate remains stable across the same GSSI event windows.

## Validation And Resource Checks

- `python -m pytest tests/test_field_prediction_current_query.py tests/test_gssi51600s_optimizer_family_card.py tests/test_gssi51600s_crossline_spacing_release_gate.py tests/test_gssi51600s_profile_position_ladder_card.py tests/test_gssi51600s_nonuniform_coordinate_synthesis_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_runtime_benchmark_card.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: 30 passed.
- `python -m py_compile run_field_prediction_current_query.py run_gssi51600s_optimizer_family_card.py run_gssi51600s_crossline_spacing_release_gate.py run_gssi51600s_profile_position_ladder_card.py run_gssi51600s_nonuniform_coordinate_synthesis_card.py run_gssi51600s_current_prediction_bundle.py`
- Result: passed.
- `git diff --check` on touched scripts, tests, checkpoints, and daily update.
- Result: passed.

## Artifact Paths

- Nonuniform coordinate synthesis card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/145_gssi51600s_nonuniform_coordinate_synthesis_card_current`
- Latest bundle with nonuniform coordinate synthesis: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/146_gssi51600s_current_prediction_bundle_with_nonuniform_coordinate_synthesis`
- Stable latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Marathon Status

The marathon request is still active. Continue with the next product-improving GSSI field-data branch rather than stopping at this checkpoint.
