# GSSI 51600S Regularized Optimizer Stability Checkpoint

## What Changed

- Added explicit diameter, finite-length, background-permittivity, and background-conductivity priors to the CUDA Fast-GPR 3D finite-length optimizer.
- Ran matched 24-iteration AdamW GSSI runs with the same nonuniform crossline seeds as the unregularized budget-stability branch.
- Built a regularized-vs-unregularized stability card and wired it into the current GSSI prediction bundle and query output.
- Updated the July 5 daily update with the regularized optimizer result.

## Key Numbers

- Run 498, profiles 0-2 regularized:
  - best field L1 loss: `0.9069852828979492`
  - best objective loss: `0.934929370880127`
  - diameter: `17.518840730190277` mm
  - finite length: `0.1871335208415985` m
  - background epsr: `2.030552387237549`
  - background conductivity: `0.002563122194260359` S/m
- Run 499, profiles 1-3 regularized:
  - best field L1 loss: `0.9579002261161804`
  - best objective loss: `0.9723491072654724`
  - diameter: `17.552457749843597` mm
  - finite length: `0.18705999851226807` m
  - background epsr: `2.016482353210449`
  - background conductivity: `0.0025597442872822285` S/m
- Regularized stability card:
  - decision: `regularized_high_budget_candidate_stabilizes_size_material_keep_conditioned`
  - mean field L1 delta versus unregularized 24-iteration runs: `-0.0019580721855163574`
  - max field L1 worsening on one subset: `0.0026331543922424316`
  - regularized diameter range: `17.518840730190277-17.552457749843597` mm
  - regularized length range: `0.18705999851226807-0.1871335208415985` m
  - regularized epsr range: `2.016482353210449-2.030552387237549`
  - regularized conductivity range: `0.0025597442872822285-0.002563122194260359` S/m

## Current Decision

The regularized 24-iteration AdamW result is now the preferred high-budget optimizer-conditioned size/material candidate because it avoids the unregularized drift toward a smaller 13 mm diameter while slightly improving the average field waveform fit. It is still not a release claim because crossline profile coordinates remain unmeasured and one overlapping subset has a small field-loss increase.

## What Remains Blocked

- Measured GSSI crossline profile coordinates are still missing.
- The y position and finite length remain geometry-conditioned.
- The public prediction still keeps the conservative GSSI range until measured or more strongly optimized crossline geometry is available.

## Validation And Resource Checks

- `python -m py_compile run_field_3d_0701_fastgpr_finite_length_scattered_optimizer.py run_gssi51600s_regularized_optimizer_stability_card.py run_gssi51600s_current_prediction_bundle.py run_field_prediction_current_query.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_scattered_optimizer_priors.py tests/test_gssi51600s_regularized_optimizer_stability_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_field_prediction_current_query.py -q`
- Result: `18 passed`.
- Figure sanity for the regularized card: size `(1974, 1243)`, nonblank RGB extrema with alpha fixed at 255.

## Artifact Paths

- Regularized profile 0-2 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/498_gssi51600s_finite_length_3d_profiles0_2_best_nonuniform_a020_b020_domainz070_adamw_prior_stability_windows50_54_58_62_66_iter24`
- Regularized profile 1-3 run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/499_gssi51600s_finite_length_3d_profiles1_3_best_nonuniform_b020_c014_domainz070_adamw_prior_stability_windows50_54_58_62_66_iter24`
- Regularized stability card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/157_gssi51600s_regularized_optimizer_stability_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/158_gssi51600s_current_prediction_bundle_with_regularized_optimizer_stability`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next Defensible Task

Run the next geometry-conditioning branch using the regularized 24-iteration objective: either a small crossline-coordinate perturbation around the current nonuniform seed, or a measured-geometry rerun if crossline coordinates become available.

## Marathon Status

The marathon request remains active. Continue with the trusted GSSI 51600S field-data predictor path and keep the mixed 2025 public archive out of product evidence unless a run explicitly targets and labels its rebar branch.
