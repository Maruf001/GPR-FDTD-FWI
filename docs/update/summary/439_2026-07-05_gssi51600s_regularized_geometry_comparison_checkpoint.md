# GSSI 51600S Regularized Geometry Comparison Checkpoint

## What Changed

- Ran a matched regularized 24-iteration AdamW counterfactual for uniform `0.22 m` crossline spacing.
- Compared uniform `0.22 m` geometry against the current nonuniform coordinate seed under the same regularized objective.
- Added a regularized geometry comparison card and wired it into the current GSSI prediction bundle and query output.
- Updated the July 5 daily update with the regularized geometry near-tie result.

## Key Numbers

- Run 500, profiles 0-2 uniform `0.22 m`:
  - best objective loss: `0.9349176287651062`
  - best field L1 loss: `0.906975269317627`
  - diameter: `17.518799751996994` mm
  - finite length: `0.18713364005088806` m
- Run 501, profiles 1-3 uniform `0.22 m`:
  - best objective loss: `0.972025454044342`
  - best field L1 loss: `0.9583150744438171`
  - diameter: `17.418239265680313` mm
  - finite length: `0.18566444516181946` m
- Regularized geometry comparison card:
  - decision: `regularized_geometry_uniform_nonuniform_near_tie_keep_geometry_conditioned`
  - mean objective delta, uniform minus nonuniform: `-0.00016769766807556152`
  - mean field L1 delta, uniform minus nonuniform: `0.00020241737365722656`
  - max absolute field L1 delta: `0.00041484832763671875`
  - uniform diameter range: `17.418239265680313-17.518799751996994` mm
  - nonuniform diameter range: `17.518840730190277-17.552457749843597` mm
  - uniform length range: `0.18566444516181946-0.18713364005088806` m
  - nonuniform length range: `0.18705999851226807-0.1871335208415985` m

## Current Decision

Under the regularized high-budget objective, uniform `0.22 m` and the current nonuniform coordinate seed are effectively tied. The regularized size/material estimate is robust to both tested crossline hypotheses, but the exact y geometry remains geometry-conditioned and should not be release-promoted without measured profile coordinates.

## What Remains Blocked

- Crossline profile coordinates for the GSSI scans remain unmeasured in metadata.
- A unique y position and finite-length claim remains blocked by that geometry ambiguity.
- The public prediction should keep the conservative GSSI range and report the regularized candidate as optimizer-conditioned.

## Validation And Resource Checks

- `python -m py_compile run_gssi51600s_regularized_geometry_comparison_card.py run_gssi51600s_current_prediction_bundle.py run_field_prediction_current_query.py`
- `python -m pytest tests/test_gssi51600s_regularized_geometry_comparison_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_field_prediction_current_query.py -q`
- Result: `15 passed`.
- Figure sanity for the regularized geometry card: size `(1974, 1243)`, nonblank RGB extrema with alpha fixed at 255.

## Artifact Paths

- Uniform profiles 0-2 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/500_gssi51600s_finite_length_3d_profiles0_2_uniform_y022_domainz070_adamw_prior_stability_windows50_54_58_62_66_iter24`
- Uniform profiles 1-3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/501_gssi51600s_finite_length_3d_profiles1_3_uniform_y022_domainz070_adamw_prior_stability_windows50_54_58_62_66_iter24`
- Regularized geometry comparison card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/159_gssi51600s_regularized_geometry_comparison_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/160_gssi51600s_current_prediction_bundle_with_regularized_geometry_comparison`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next Defensible Task

Use the regularized objective for a small timing/source or x-z geometry sensitivity check that does not depend on the 2025 mixed archive, or wait for measured GSSI crossline coordinates and rerun the measured-geometry planner.

## Marathon Status

The marathon request remains active. Continue with the trusted GSSI 51600S deliverable, and keep the 2025 archive labeled as separate mixed public data unless a run explicitly targets its rebar branch.
