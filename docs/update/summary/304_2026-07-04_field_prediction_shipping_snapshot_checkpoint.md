# Field Prediction Shipping Snapshot Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_prediction_shipping_snapshot.py`.
- Added focused tests for product shipping status, blockers, and snapshot filtering.
- Built a current-best-product snapshot from leaderboard `017`.
- Regenerated the snapshot after filtering out legacy/non-best leaderboard rows.

## Key Numbers

- Final shipping snapshot:
  - artifact `019_field_prediction_shipping_snapshot`
  - row count `2`
  - datasets with x/y/z available `1`
  - diameter-blocked datasets:
    - `external_2025_pipe_0701`
    - `gssi51600s`
- Current best 0701 row:
  - method `fastgpr_3d_stack_y_length_proxy`
  - x/z status `available`
  - y status `available`
  - length status `available_range`
  - diameter compact status `fixed_scattered_candidate_with_adaptive_degeneracy`
  - blocker: adaptive global-y scattered optimizer remains diameter-degenerate `12.0-20.0 mm` despite fixed scattered `8.0-8.0 mm` overlap
- Current best GSSI row:
  - method `fastgpr_corrected_surface_bscan`
  - x/z status `available`
  - y status `missing`
  - length status `missing`
  - diameter compact status `seed_sensitive_range`
  - blocker: no y/length estimate and diameter seed-sensitive `8.095-18.800 mm`

## What Remains Blocked

- 0701 has the stronger 3D geometry product, but diameter is still not uniquely confirmed by the adaptive optimizer.
- GSSI has a cleaner surface B-scan product path, but lacks y/length and remains seed-sensitive in diameter.
- Neither current product is a fully shippable unique 3D rebar geometry/material predictor yet.

## Current Decision

The current shipping picture is clear:

- Use 0701 as the main 3D proof path because it now has x/y/z, supported length range, epsr, and conductivity.
- Use GSSI as a corrected 2D surface B-scan compatibility path.
- The next highest-value technical blocker is diameter identifiability under adaptive material/time optimization, especially on the 0701 global y-window.

## Next Defensible Task

Continue improving the real predictor by targeting one of these:

- add source/time regularization to the 0701 adaptive scattered optimizer so radius gradients are less timing-dominated,
- test receiver-mean adaptive global-y optimization to see whether it aligns better with the fixed scattered `8 mm` diagnostic,
- start a GSSI 3D/y extension only if a crossline/stack source exists or can be assembled from the dataset.

## Validation And Resources

- `python -m pytest tests/test_field_prediction_shipping_snapshot.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_predictor_product_report.py -q`
  - `12 passed`
- `python -m pytest tests/test_field_prediction_shipping_snapshot.py -q`
  - `3 passed`
- `python -m py_compile run_field_prediction_shipping_snapshot.py run_field_prediction_product_leaderboard.py run_field_3d_0701_predictor_product_report.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure check:
  - `019.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.48`

## Artifact Paths

- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/019_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
