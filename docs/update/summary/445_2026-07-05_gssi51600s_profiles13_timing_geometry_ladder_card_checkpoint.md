# 445 2026-07-05 GSSI51600S Profiles 1/3 Timing-Geometry Ladder Card Checkpoint

## What changed

- Built a compact profiles 1/3 timing-geometry ladder card from the existing mid-window and earlier-window runs.
- Packaged the branch behavior into one table and figure.
- Wired the ladder decision into the latest GSSI prediction bundle and public query output.

## Key numbers

- Decision: `profiles13_shallow_branch_exists_but_deep_branch_fits_better`.
- Best field-fit label: `nonuniform_mid_b020_c014`.
- Best objective label: `uniform_mid_b022_c022`.
- Shallow branch labels: `uniform_early_b022_c022`.
- Deep branch labels:
  - `nonuniform_mid_b020_c014`
  - `uniform_mid_b022_c022`
  - `nonuniform_early_b020_c014`
  - `early_b020_c018`
  - `early_b020_c022`
  - `early_b022_c014`
- Shallow best field L1 loss: `0.9704806208610535`.
- Deep best field L1 loss: `0.9579002261161804`.
- Cover-depth range across the ladder: `0.10122688114643097-0.138297438621521 m`.
- Diameter range across the ladder: `17.217664048075676-17.552457749843597 mm`.
- Length range across the ladder: `0.18371789157390594-0.18705999851226807 m`.
- Relative permittivity range across the ladder: `2.001837968826294-2.1142635345458984`.

## Current decision

The shallow profiles 1/3 branch is real but currently not the best field-fit branch. It appears in the fully uniform earlier-window case, while the nonuniform and mid-window variants stay deep and fit better. This supports keeping profiles 1/3 timing and y geometry conditioned.

## What remains blocked

- The profiles 1/3 x/cover-depth branch cannot be collapsed to one release value without either measured crossline coordinates or a stronger joint source-time/y-geometry rule.
- The next improvement should not add a wider unconstrained grid; it should use a compact joint planner with explicit promotion criteria.

## Validation and resource checks

- `python -m py_compile run_gssi51600s_profiles13_timing_geometry_ladder_card.py`
- `python -m pytest tests/test_gssi51600s_profiles13_timing_geometry_ladder_card.py -q`
- Result: `2 passed`.
- Bundle/query focused validation passed before regeneration: `14 passed`.
- Query smoke: `python run_field_prediction_current_query.py --dataset gssi51600s --format pretty`.
- Figure sanity checked for the ladder card and bundled copy: both PNGs are nonblank RGBA images with size `1974 x 1243`.

## Artifact paths

- Ladder card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/170_gssi51600s_profiles13_timing_geometry_ladder_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/171_gssi51600s_current_prediction_bundle_with_profiles13_timing_geometry_ladder`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next defensible task

Build a compact joint timing/geometry grid planner that proposes only decision-changing runs and tracks promotion criteria before launch. The planner should avoid expanding the branch manually unless a candidate can improve waveform fit while reducing the x/cover-depth split.

## Marathon status

The marathon request remains active. Continue with the next bounded GSSI-only product-improvement branch.
