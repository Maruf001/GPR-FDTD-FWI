# Field 3D 0701 Finite-Length Scattered-Objective Checkpoint

Date: 2026-07-04

## What Changed

- Updated `run_field_3d_0701_fastgpr_finite_length_forward_contrast.py` to compute:
  - full aligned field L1,
  - receiver-mean residualized scattered-field L1,
  - finite-vs-infinite scattered improvement.
- Regenerated the finite-length contrast with receiver-mean residualization.
- Wired the new finite-length scattered-objective result into the shipping snapshot.

## Key Numbers

- Finite-length scattered objective artifact:
  - `236_field_3d_0701_fastgpr_finite_length_forward_contrast_dx002_dt004_duration30_receiver_mean_scattered`
  - decision `finite_length_forward_scattered_objective_improves`
  - field objective status `finite_length_forward_field_objective_flat`
  - scattered objective status `finite_length_forward_scattered_objective_improves`
  - grid `dx=0.02 m`, `nx=80`, `ny=111`, `nz=51`
  - duration `30 ns`, `dt=0.04 ns`, `751` time steps
  - residual mode `receiver_mean`
  - full-field loss range `0.881642580-0.881642878`
  - full-field best finite improvement vs infinite `2.384e-07`
  - scattered loss range `0.768854022-0.926839471`
  - infinite scattered reference loss `0.922254443`
  - best finite scattered loss `0.768854022`
  - best finite scattered improvement vs infinite `0.153400421`
  - best finite scattered length `0.1 m`
  - best finite scattered diameter `8 mm`
  - max relative scattered L2 vs infinite `0.753861904`
- Shipping snapshot:
  - `053_field_prediction_shipping_snapshot`
  - 0701 row now reports both:
    - finite-length stack proxy `local but not continuous`,
    - finite-length Fast-GPR forward `scattered objective improves, full-field objective flat`.

## What Remains Blocked

- This is still forward contrast, not a fitted finite-length optimizer.
- The best scattered finite length is `0.1 m`, which conflicts with the promoted profile-window length `0.2 m`; this needs optimizer/stability stress before any product change.
- Full-field L1 remains flat, so the claim boundary must state that the improvement is receiver-mean scattered-objective-specific.
- Diameter remains a range.

## Current Decision

The finite-length branch is now worth a bounded optimizer.

Do not update the shipping prediction yet. Instead:

- keep current product row as provisional;
- launch a small finite-length optimizer only on the receiver-mean scattered objective;
- compare the optimized finite-length candidate against the current stability guard and full-field flatness.

## Next Defensible Task

Run a bounded finite-length optimizer branch:

- initialize from the promoted 0701 x/z/epsr/conductivity row;
- optimize finite length and diameter over the receiver-mean scattered objective;
- keep x/z/material either fixed or tightly bounded for the first run;
- use Adamax or AdamW with a small iteration budget;
- report whether the optimizer stabilizes around `0.1 m`, returns to `0.2 m`, or stays degenerate.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py -q`
  - `5 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `12 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `38 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_3d_0701_product_stability_synthesis.py run_field_3d_0701_finite_length_support_proxy.py run_field_3d_0701_finite_length_support_proxy_sensitivity.py run_field_3d_0701_fastgpr_finite_length_forward_contrast.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `236.../figures/field_3d_0701_fastgpr_finite_length_forward_contrast.png`: size `(2229, 818)`, min/max `(0, 255)`, stddev `67.916`
  - `053.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.402`

## Artifact Paths

- Finite-length scattered forward contrast:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/236_field_3d_0701_fastgpr_finite_length_forward_contrast_dx002_dt004_duration30_receiver_mean_scattered`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/053_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/324_2026-07-04_field_3d_0701_finite_length_scattered_objective_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
