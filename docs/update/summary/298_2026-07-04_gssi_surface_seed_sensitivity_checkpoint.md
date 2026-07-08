# GSSI Surface Seed Sensitivity Checkpoint

Date: 2026-07-04

## What Changed

- Added explicit `--initial-diameter-mm` support to the GSSI surface B-scan geometry optimizer so diameter-seeded runs are reproducible.
- Ran a matched GSSI seed set using the current best product setting:
  - detector rank `3`
  - receiver offset `0.005 m`
  - lower diameter bound `2 mm`
  - AdamW with weight decay `0.01`
  - time-shift optimization enabled
  - eight optimizer iterations per seed
- Added `run_gssi51600s_surface_bscan_seed_synthesis.py` to summarize diameter seed stability.
- Refreshed the GSSI product report and field prediction leaderboard with seed-synthesis fields.
- Snapshotted the exact scripts used inside the generated output folders.

## Key Numbers

- Matched GSSI seed runs:
  - `054_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_seed08_grad`
    - initial diameter `8 mm`
    - best diameter `8.095408790 mm`
    - best loss `0.848501205444`
  - `055_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_seed12_grad`
    - initial diameter `12 mm`
    - best diameter `12.929782246 mm`
    - best loss `0.848482668400`
  - `056_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_seed16_grad`
    - initial diameter `16 mm`
    - best diameter `16.062322825 mm`
    - best loss `0.848477602005`
  - `057_gssi51600s_surface_bscan_geometry_optimizer_rank3_offset005_seed20_grad`
    - initial diameter `20 mm`
    - best diameter `18.799591810 mm`
    - best loss `0.848468482494`
- Seed synthesis:
  - artifact `058_gssi51600s_surface_bscan_seed_synthesis`
  - best seed-synthesis diameter `18.799591810 mm`
  - near-best diameter range `8.095408790-18.799591810 mm`
  - radius-gradient status `radius_gradient_visible`
  - seed status `gssi_surface_seed_sensitive_wide_near_best_range`
- Refreshed GSSI product report:
  - artifact `059_gssi51600s_surface_bscan_product_report`
  - x `0.413941013248 m`
  - z `0.128718197346 m`
  - product diameter proxy `18.586354330 mm`
  - product near-best diameter range `8.108957671-18.738288432 mm`
  - seed-synthesis best diameter `18.799591810 mm`
  - seed-synthesis near-best diameter range `8.095408790-18.799591810 mm`
  - epsr `2.044878721`
  - background conductivity `0.002187208273 S/m`
  - fit loss `0.848336815834`
  - radius-gradient status `radius_gradient_visible`
- Refreshed product leaderboard:
  - artifact `012_field_prediction_product_leaderboard`
  - GSSI row now carries both the radius-gradient diagnostic and seed-sensitivity range.

## What Remains Blocked

- The GSSI radius parameter is active in the objective, but the current optimizer does not converge to a unique diameter from different diameter seeds.
- The loss differences across the seed set are small, so the product output should report a best candidate and diameter range rather than a single confident size claim.
- This GSSI surface B-scan branch still estimates x/z/material parameters only. It does not yet estimate y position, rebar length, or full 3D shape.
- No destructive ground-truth diameter label is available for this field scan, so validation is based on fit quality, stability checks, and cross-optimizer consistency.

## Current Decision

GSSI is still the stronger field dataset for diameter sensitivity because the radius gradient is visible. However, the deliverable must expose the current uncertainty:

- current best surface product candidate: diameter around `18.6-18.8 mm`,
- plausible near-best range: about `8.1-18.8 mm`,
- x/z/material estimates are product-visible but provisional,
- 3D y/length is not claimed yet.

This is a product improvement over hiding the ambiguity: the predictor now reports the best candidate and the range induced by real optimizer seed sensitivity.

## Next Defensible Task

Continue on the real-data predictor path by testing optimizer convergence, not synthetic gates:

- run a matched GSSI optimizer comparison with Adam, AdamW, Adamax, and LBFGS or a two-stage AdamW-to-LBFGS polish where supported,
- keep the same detector rank/window/offset/seed set,
- measure runtime, loss, x/z/material stability, and diameter range,
- promote the optimizer schedule that reduces the seed-sensitive diameter band without worsening the B-scan fit.

## Validation And Resources

- `python -m pytest tests/test_gssi51600s_surface_bscan_product_report.py tests/test_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py tests/test_gssi51600s_surface_bscan_seed_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_predictor_product_report.py -q`
  - `18 passed`
- `python -m py_compile run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py run_gssi51600s_surface_bscan_gradient_diagnostic_synthesis.py run_gssi51600s_surface_bscan_geometry_optimizer.py run_gssi51600s_surface_bscan_seed_synthesis.py run_gssi51600s_surface_bscan_product_report.py run_field_prediction_product_leaderboard.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `058.../figures/gssi51600s_surface_bscan_seed_synthesis.png`: size `(1889, 750)`, min/max `(0, 255)`, stddev `70.49`
  - `059.../figures/gssi51600s_surface_bscan_product_report.png`: size `(1957, 750)`, min/max `(0, 255)`, stddev `58.93`
  - `012.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `64.79`
- GPU check at marathon resume: NVIDIA GB10 visible, utilization `6%`.

## Artifact Paths

- GSSI seed synthesis:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/058_gssi51600s_surface_bscan_seed_synthesis`
- Refreshed GSSI product report:
  - `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/059_gssi51600s_surface_bscan_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/012_field_prediction_product_leaderboard`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
