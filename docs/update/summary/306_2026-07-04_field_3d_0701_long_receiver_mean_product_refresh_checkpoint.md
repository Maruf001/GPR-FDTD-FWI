# Field 3D 0701 Long Receiver-Mean Product Refresh Checkpoint

Date: 2026-07-04

## What Changed

- Completed the longer receiver-mean adaptive global-y diameter check requested in checkpoint `305`.
- Ran 8-iteration AdamW follow-up for the two near-best receiver-mean seeds:
  - seed `8 mm`
  - seed `12 mm`
- Synthesized the long-run seed result.
- Refreshed the 0701 product report, product leaderboard, and shipping snapshot so the deliverable points at the current long-run evidence.
- Updated report/leaderboard/shipping scripts to expose long-run adaptive metadata: run count, near-best labels, and mean iteration runtime.

## Key Numbers

- Long receiver-mean adaptive runs:
  - `124_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_long8`
    - best diameter `8.002206683 mm`
    - best loss `0.912250161`
    - best depth `1.517982483 m`
    - best epsr `3.330199242`
    - best background conductivity `0.003584524 S/m`
    - best time shift `2.313656769 ns`
    - mean iteration runtime `11.512889107 s`
  - `125_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_long8`
    - best diameter `11.927723885 mm`
    - best loss `0.912221193`
    - best depth `1.538056612 m`
    - best epsr `3.264328003`
    - best background conductivity `0.003744031 S/m`
    - best time shift `2.303859253 ns`
    - mean iteration runtime `10.764502422 s`
- Long receiver-mean synthesis:
  - artifact `126_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_long8`
  - best diameter `11.927723885 mm`
  - near-best range `8.002206683-11.927723885 mm`
  - near-best labels `seed08_long8`, `seed12_long8`
  - best loss spread `0.912221193-0.912250161`
  - diameter status `optimizer_seed_diameter_near_best_narrow_range`
  - gradient status `radius_gradient_negligible_timing_dominated`
  - mean iteration runtime `11.138695764 s`
- Refreshed 0701 product report:
  - artifact `127_field_3d_0701_predictor_product_report`
  - x `9.819386152 m`
  - y center `1.750 m`
  - z `1.507775545 m`
  - length proxy `0.100 m`, supported length `0.100-0.500 m`
  - epsr `3.364521503`
  - background conductivity `0.003581968 S/m`
  - fit loss `0.602550268`
  - adaptive long receiver-mean diameter best/range `11.927723885 mm` / `8.002206683-11.927723885 mm`
- Refreshed leaderboard:
  - artifact `022_field_prediction_product_leaderboard`
  - current best products:
    - `external_2025_pipe_0701:fastgpr_3d_stack_y_length_proxy`
    - `gssi51600s:fastgpr_corrected_surface_bscan`
- Refreshed shipping snapshot:
  - artifact `023_field_prediction_shipping_snapshot`
  - 0701 now reports x/y/z, y-length range, epsr, conductivity, and long AdamW receiver-mean adaptive diameter range.
  - GSSI remains x/z/material with seed-sensitive diameter and no y/length.

## What Remains Blocked

- The longer AdamW check confirms the `8-12 mm` receiver-mean adaptive band; it does not collapse diameter to a single unique value.
- Radius gradients in the long synthesis are still timing-dominated, so source/time regularization remains the next diameter robustness problem.
- The 0701 y/length estimate is still a stack/profile-window proxy, not a full finite-length 3D steel-cylinder FDTD inversion.
- GSSI still lacks y/length because the current product is a surface B-scan adapter without measured crossline stack geometry.

## Current Decision

The current shipping predictor state is stronger than checkpoint `305` because the promoted 0701 diameter band now has a longer receiver-mean AdamW confirmation. The product should report:

- 0701: x/y/z, length range, epsr, conductivity, and diameter as `8.00-11.93 mm` with best point `11.93 mm`.
- GSSI 51600S: x/z/material and diameter candidate/range from the corrected surface adapter, with no y/length claim.

Do not claim unique diameter or full 3D finite-length inversion yet.

## Next Defensible Task

Improve the 0701 adaptive radius objective instead of adding unrelated synthetic work:

- add source/time regularization or a constrained time-shift prior to reduce timing-dominated diameter tradeoff,
- rerun the receiver-mean adaptive seeds under that regularized objective,
- only promote a narrower diameter claim if the same real field window remains stable.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `17 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_predictor_product_report.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `126.../figures/field_3d_0701_scattered_optimizer_seed_synthesis.png`: size `(1889, 767)`, min/max `(0, 255)`, stddev `76.211`
  - `127.../figures/field_3d_0701_predictor_product_report.png`: size `(2314, 767)`, min/max `(0, 255)`, stddev `55.748`
  - `022.../figures/field_prediction_product_leaderboard.png`: size `(2093, 835)`, min/max `(0, 255)`, stddev `63.654`
  - `023.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `68.752`
- Resource check:
  - GPU visible as `NVIDIA GB10`, low utilization.
  - RAM available about `100 GiB`.

## Artifact Paths

- Long receiver-mean adaptive runs:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/124_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed08_long8`
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/125_field_3d_0701_fastgpr_scattered_geometry_material_optimizer_global_y175_receiver_mean_adamw_seed12_long8`
- Long receiver-mean adaptive synthesis:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/126_field_3d_0701_scattered_optimizer_seed_synthesis_global_y175_receiver_mean_adamw_long8`
- Refreshed 0701 product report:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/127_field_3d_0701_predictor_product_report`
- Refreshed leaderboard:
  - `outputs/validation_exp_on_field_data/product_leaderboard/022_field_prediction_product_leaderboard`
- Refreshed shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/023_field_prediction_shipping_snapshot`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
