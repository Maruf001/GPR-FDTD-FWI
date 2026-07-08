# GSSI 51600S Regularized X/Z Stability Checkpoint

## What Changed

- Summarized optimized x position and cover depth across the four regularized high-budget GSSI runs.
- Added a regularized x/z stability card and wired it into the current GSSI prediction bundle and query output.
- Updated the July 5 daily update with the x/cover-depth range and profile-subset split.

## Key Numbers

- Regularized x range: `0.5006797313690186-0.5242064595222473` m
- Regularized mean x: `0.5125994831323624` m
- Regularized cover-depth range: `0.096347875893116-0.138297438621521` m
- Regularized mean cover depth: `0.1172651257365942` m
- Profiles 0-2 mean x: `0.524205207824707` m
- Profiles 1-3 mean x: `0.5009937584400177` m
- Profiles 0-2 mean cover depth: `0.09634910151362419` m
- Profiles 1-3 mean cover depth: `0.1381811499595642` m
- Profile-subset x gap: `0.02321144938468933` m
- Profile-subset cover-depth gap: `0.04183204844594002` m

## Current Decision

The regularized size/material estimate is more stable than the regularized x/z location. X and cover depth should remain profile-window conditioned because the split is driven mainly by the overlapping profile subset, not by uniform versus nonuniform crossline geometry.

## What Remains Blocked

- A single release-style x/z location remains blocked by profile-subset and event-window sensitivity.
- Measured crossline profile coordinates are still needed to support a stronger 3D y/length interpretation.
- The public predictor should continue showing the conservative location and geometry-conditioned regularized x/z range.

## Validation And Resource Checks

- `python -m py_compile run_gssi51600s_regularized_xz_stability_card.py run_gssi51600s_current_prediction_bundle.py run_field_prediction_current_query.py`
- `python -m pytest tests/test_gssi51600s_regularized_xz_stability_card.py tests/test_gssi51600s_current_prediction_bundle.py tests/test_field_prediction_current_query.py -q`
- Result: `14 passed`.
- Figure sanity for the regularized x/z card: size `(1804, 1175)`, nonblank RGB extrema with alpha fixed at 255.

## Artifact Paths

- Regularized x/z stability card: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/161_gssi51600s_regularized_xz_stability_card_current`
- Latest bundle: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/162_gssi51600s_current_prediction_bundle_with_regularized_xz_stability`
- Latest pointer: `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`

## Next Defensible Task

Test whether the x/z split is driven by event-window timing by running a bounded regularized window sensitivity branch, or wait for measured GSSI crossline coordinates and rerun the measured-geometry planner.

## Marathon Status

The marathon request remains active. Continue with trusted GSSI 51600S field-data predictor work; keep the 2025 public archive separate unless a run explicitly targets its rebar branch.
