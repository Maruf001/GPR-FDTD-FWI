# Field 3D 0701 Global Y/Length Refresh Checkpoint

Date: 2026-07-04

## What Changed

- Revisited the 0701 3D-stack y/length estimate because the previous product report only used a narrow early-profile window family.
- Ran a broader real field-stack y-window scan:
  - artifact `103_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_coarse`
  - profile starts `0,3,6,...,33`
  - profile lengths `2,4,6`
  - four Adam iterations per candidate
- Ran a focused real field-stack y-window scan around the better global region:
  - artifact `104_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_fine_y165`
  - profile starts `13-17`
  - profile lengths `2-6`
  - eight Adam iterations per candidate
- Added `run_field_3d_0701_y_length_global_claim_synthesis.py`.
- Refreshed the 0701 product report to promote the global y/length evidence while keeping diameter claim boundaries.
- Refreshed the field prediction product leaderboard to point to the new 0701 product report.

## Key Numbers

- Previous local y/length product:
  - y center `0.200 m`
  - center-span length proxy `0.200 m`
  - local y/length scan loss `0.707178115845`
- Global coarse scan:
  - artifact `103_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_coarse`
  - best profiles `15-18`
  - y center `1.650 m`
  - center-span length proxy `0.300 m`
  - best loss `0.694217562675`
- Global fine scan:
  - artifact `104_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_fine_y165`
  - raw best profiles `17-18`
  - raw best y center `1.750 m`
  - raw best center-span length proxy `0.100 m`
  - raw best loss `0.602550268173`
  - best-by-length candidates for lengths `2-6` share end profile `18`
- Global y/length synthesis:
  - artifact `105_field_3d_0701_y_length_global_claim_synthesis`
  - decision `field_3d_0701_global_y_length_raw_best_improves_with_endpoint_range`
  - raw best y center `1.750 m`
  - raw best length proxy `0.100 m`
  - endpoint-stable supported length range `0.100-0.500 m`
  - supported y-center range `1.550-1.750 m`
  - loss improvement versus local y scan `0.104627847672`
- Refreshed 0701 product report:
  - artifact `106_field_3d_0701_predictor_product_report`
  - x `9.819386151982 m`
  - y center `1.750 m`
  - legacy y center `0.200 m`
  - z `1.507775545120 m`
  - raw length proxy `0.100 m`
  - supported length range `0.100-0.500 m`
  - epsr `3.364521503448`
  - background conductivity `0.003581967903 S/m`
  - fit loss `0.602550268173`
  - diameter remains claim-bounded: full objective range `8-30 mm`, scattered optimizer diagnostic range roughly `16-24 mm`
- Refreshed product leaderboard:
  - artifact `015_field_prediction_product_leaderboard`
  - current best products remain:
    - `external_2025_pipe_0701:fastgpr_3d_stack_y_length_proxy`
    - `gssi51600s:fastgpr_corrected_surface_bscan`

## What Remains Blocked

- The global y/length raw best favors a short two-profile window, so the physical rebar length is not uniquely identified.
- The endpoint-stable family supports a length range `0.1-0.5 m`, not a single length.
- The y coordinate is still inferred from profile index and assumed y spacing; it is not measured survey geometry.
- The 0701 diameter is still not product-unique. The global y scan raw width hits the upper bound, while the radius/scattered diagnostics require a bounded range claim.

## Current Decision

The 0701 3D product should no longer use y center `0.2 m` as the promoted prediction. The strongest current 3D field-stack product is:

- x `9.819 m`,
- y center `1.750 m` raw best,
- y-center supported range `1.550-1.750 m`,
- z `1.508 m`,
- raw length proxy `0.100 m`,
- supported length range `0.100-0.500 m`,
- epsr around `3.365`,
- background conductivity around `0.00358 S/m`,
- diameter reported as a bounded candidate/range, not uniquely identified.

## Next Defensible Task

Use this new 3D y/length result to improve diameter/material identification:

- rerun the scattered-radius or geometry/material optimizer using the global y-window region rather than the old early-profile window,
- compare whether the better y-window also strengthens radius gradients or narrows the diameter range,
- keep output product-facing: update the 0701 report only if diameter/material fit improves without hiding uncertainty.

## Validation And Resources

- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_y_length_global_claim_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_y_length_optimizer_comparison.py -q`
  - `13 passed`
- `python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_3d_0701_y_length_global_claim_synthesis.py run_field_prediction_product_leaderboard.py run_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `103.../figures/field_3d_0701_fastgpr_y_length_window_optimizer_scan.png`: size `(1923, 784)`, min/max `(0, 255)`, stddev `43.46`
  - `104.../figures/field_3d_0701_fastgpr_y_length_window_optimizer_scan.png`: size `(1923, 784)`, min/max `(0, 255)`, stddev `42.16`
  - `105.../figures/field_3d_0701_y_length_global_claim.png`: size `(1923, 750)`, min/max `(0, 255)`, stddev `66.34`
  - `106.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.29`
  - `015.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.29`

## Artifact Paths

- Global coarse y/length scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/103_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_coarse`
- Global fine y/length scan:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/104_field_3d_0701_fastgpr_y_length_window_optimizer_scan_global_fine_y165`
- Global y/length synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/105_field_3d_0701_y_length_global_claim_synthesis`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/106_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/015_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
