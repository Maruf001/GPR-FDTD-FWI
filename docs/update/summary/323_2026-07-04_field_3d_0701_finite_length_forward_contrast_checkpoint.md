# Field 3D 0701 Finite-Length Forward Contrast Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_fastgpr_finite_length_forward_contrast.py`.
- Added focused tests for:
  - local 3D Fast-GPR config,
  - custom crossline source/receiver coordinates,
  - CFL time-step validation,
  - finite-vs-infinite contrast synthesis.
- Ran finite-length Fast-GPR forward contrasts against the promoted 0701 field window.
- Wired the guarded finite-length forward result into the shipping snapshot.

## Key Numbers

- Coarse smoke:
  - artifact `230_field_3d_0701_fastgpr_finite_length_forward_contrast_smoke`
  - grid `dx=0.05 m`, `nx=81`, `ny=51`, `nz=41`
  - duration `6 ns`
  - decision `finite_length_forward_field_objective_flat`
  - scatter contrast was effectively zero because the 6 ns window was too early for the promoted depth event.
- Failed CFL smoke:
  - artifact directory `231...smoke_dx002`
  - attempted `dx=0.02 m`, `dt=0.1 ns`
  - Fast-GPR reported `dt is too large`; downstream prediction/observed shape mismatch followed.
  - Added explicit CFL validation to prevent repeating this failure.
- CFL-safe short smoke:
  - artifact `232_field_3d_0701_fastgpr_finite_length_forward_contrast_smoke_dx002_dt004`
  - grid `dx=0.02 m`, `nx=80`, `ny=111`, `nz=51`
  - duration `6 ns`, `dt=0.04 ns`
  - decision `finite_length_forward_field_objective_flat`
  - still no useful scatter because the window was too early.
- CFL-safe full-window smoke:
  - artifact `233_field_3d_0701_fastgpr_finite_length_forward_contrast_smoke_dx002_dt004_duration30`
  - duration `30 ns`, `dt=0.04 ns`, `time_iterations=751`
  - finite mask changed scattered field: relative scattered L2 vs infinite `0.372286`
  - field objective stayed flat: best finite improvement vs infinite `5.96e-08`
- Guarded bounded contrast:
  - artifact `235_field_3d_0701_fastgpr_finite_length_forward_contrast_dx002_dt004_duration30_guarded`
  - lengths tested `0.1`, `0.2`, `0.3`, `0.5 m`
  - diameters tested `8`, `12 mm`
  - decision `finite_length_forward_field_objective_flat`
  - loss range `0.881642580-0.881642878`
  - infinite reference loss `0.881642818`
  - best finite length `0.1 m`
  - best finite diameter `12 mm`
  - best finite improvement vs infinite `2.384e-07`
  - max relative scattered L2 vs infinite `0.753862`
- Shipping snapshot:
  - artifact `052_field_prediction_shipping_snapshot`
  - 0701 row now includes:
    - finite-length stack-proxy decision `finite_length_proxy_promoted_window_local_but_not_continuous`
    - finite-length Fast-GPR forward decision `finite_length_forward_field_objective_flat`
    - best finite forward length `0.1 m`
    - best finite forward diameter `12 mm`
    - best finite improvement vs infinite `2.384e-07`

## What Remains Blocked

- Finite-length masks are now numerically visible in the scattered field, but they do not improve the aligned field objective enough to justify a length claim upgrade.
- Diameter remains a stress-union range.
- The source/antenna/objective model likely controls the finite-length flatness more than the length parameter itself.
- Full finite-length optimization should not be launched until the finite-length forward objective becomes decision-changing.

## Current Decision

Do not promote the finite-length Fast-GPR branch into the product prediction.

The current shipping row should keep:

- x `9.819386 m`;
- y center `1.50 m`;
- z depth `1.488030 m`;
- length `0.20 m` as provisional/profile-window-supported;
- epsr `3.296651`;
- background conductivity `0.003776330 S/m`;
- diameter top candidate/range `8.002209-11.896786 mm`, with broader stress union `8.002196-11.965089 mm`.

Finite-length evidence should be reported as:

- stack support proxy: local but not continuous;
- Fast-GPR finite-length forward contrast: scattered field changes, but objective is flat.

## Next Defensible Task

Improve the finite-length forward objective before optimizing length:

- test source/antenna alignment variants inside the finite-length forward contrast;
- compare residualized/scattered objectives instead of full normalized L1 only;
- only launch finite-length Adam/Adamax optimization if one finite-length forward objective produces a nontrivial improvement over the infinite reference.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py -q`
  - `4 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `17 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_3d_0701_fastgpr_finite_length_forward_contrast.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `37 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_3d_0701_product_stability_synthesis.py run_field_3d_0701_finite_length_support_proxy.py run_field_3d_0701_finite_length_support_proxy_sensitivity.py run_field_3d_0701_fastgpr_finite_length_forward_contrast.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `234.../figures/field_3d_0701_fastgpr_finite_length_forward_contrast.png`: size `(2229, 818)`, min/max `(0, 255)`, stddev `68.723`
  - `052.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.402`

## Artifact Paths

- Guarded finite-length forward contrast:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/235_field_3d_0701_fastgpr_finite_length_forward_contrast_dx002_dt004_duration30_guarded`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/052_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/323_2026-07-04_field_3d_0701_finite_length_forward_contrast_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
