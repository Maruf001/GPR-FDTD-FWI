# Field 3D 0701 Finite-Length Proxy Shipping Checkpoint

Date: 2026-07-04

## What Changed

- Added `run_field_3d_0701_finite_length_support_proxy.py`.
- Added `run_field_3d_0701_finite_length_support_proxy_sensitivity.py`.
- Added focused tests for both finite-length proxy scripts.
- Generated a real-stack finite-length support proxy around the promoted 0701 event.
- Generated an aperture-sensitivity synthesis over `25` time/trace windows.
- Wired the finite-length proxy sensitivity into the shipping snapshot.

## Key Numbers

- Single-window finite-length proxy:
  - artifact `228_field_3d_0701_finite_length_support_proxy`
  - decision `finite_length_proxy_conflicts_with_promoted_window`
  - event window sample range `36-68`
  - trace range `372-396`
  - best proxy interval `16-16`
  - best y center `1.60 m`
  - best center-span length `0.00 m`
  - promoted product interval `14-16`
  - promoted product interval rank `12`
  - promoted product continuous-support ratio `-0.188`
- Aperture sensitivity:
  - artifact `229_field_3d_0701_finite_length_support_proxy_sensitivity`
  - decision `finite_length_proxy_promoted_window_local_but_not_continuous`
  - run count `25`
  - decision counts:
    - local bracket, not continuous: `14`
    - conflicts with promoted window: `11`
  - best-window counts:
    - `16-16`: `10`
    - `21-21`: `5`
    - `23-23`: `5`
    - `13-21`: `4`
    - `14-14`: `1`
  - product top-10 fraction `0.56`
  - product interval rank range `3-69`
  - best profile-length range `1-9`
  - continuous-support ratio range `-0.261-0.688`
- Shipping snapshot:
  - artifact `051_field_prediction_shipping_snapshot`
  - finite-length proxy decision now included in the 0701 row.

## What Remains Blocked

- The promoted y/length row remains optimizer-stability-supported but not a robust continuous finite-length claim.
- Diameter remains a stress-union range, not a unique size claim.
- A true finite-length 3D forward/inversion branch is still needed before upgrading y length or diameter.
- GSSI 51600S still lacks y/length support from the current surface-B-scan product.

## Current Decision

Do not replace the shipping y/length estimate with the finite-length proxy.

The current 0701 shipping row should say:

- x/y/z, epsr, and conductivity are available under the promoted Fast-GPR objective;
- y/length is stable across optimizer/residual/source/timing stresses;
- finite-length support from the stack is local but not continuous;
- length remains provisional until a finite-length 3D forward/optimizer improves the field objective.

## Next Defensible Task

Start the finite-length 3D forward/optimizer branch against the promoted 0701 event:

- keep promoted x/z/epsr/conductivity as initialization;
- vary finite-length y geometry and diameter locally;
- compare the field objective against the current infinite-cylinder/profile-window proxy;
- update the product only if the finite-length forward model improves the field objective and stabilizes support.

## Validation And Resources

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py -q`
  - `6 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `12 passed`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py tests/test_field_3d_0701_scattered_optimizer_seed_synthesis.py tests/test_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_product_stability_synthesis.py tests/test_field_3d_0701_finite_length_support_proxy.py tests/test_field_3d_0701_finite_length_support_proxy_sensitivity.py tests/test_field_prediction_product_leaderboard.py tests/test_field_prediction_shipping_snapshot.py -q`
  - `32 passed`
- `conda run -n gpr-fdtd-fwi python -m py_compile run_field_3d_0701_fastgpr_scattered_geometry_material_optimizer.py run_field_3d_0701_scattered_optimizer_seed_synthesis.py run_field_3d_0701_predictor_product_report.py run_field_3d_0701_product_stability_synthesis.py run_field_3d_0701_finite_length_support_proxy.py run_field_3d_0701_finite_length_support_proxy_sensitivity.py run_field_prediction_product_leaderboard.py run_field_prediction_shipping_snapshot.py`
  - passed
- Touched-file `git diff --check` passed.
- Figure checks:
  - `228.../figures/field_3d_0701_finite_length_support_proxy.png`: size `(2195, 801)`, min/max `(0, 255)`, stddev `56.432`
  - `229.../figures/field_3d_0701_finite_length_support_proxy_sensitivity.png`: size `(2125, 835)`, min/max `(0, 255)`, stddev `108.504`
  - `051.../figures/field_prediction_shipping_snapshot.png`: size `(2263, 750)`, min/max `(0, 255)`, stddev `64.402`

## Artifact Paths

- Finite-length proxy:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/228_field_3d_0701_finite_length_support_proxy`
- Finite-length sensitivity:
  - `outputs/validation_exp_on_field_data/3d_geometry_inventory/229_field_3d_0701_finite_length_support_proxy_sensitivity`
- Shipping snapshot:
  - `outputs/validation_exp_on_field_data/product_leaderboard/051_field_prediction_shipping_snapshot`
- Checkpoint:
  - `docs/update/summary/322_2026-07-04_field_3d_0701_finite_length_proxy_shipping_checkpoint.md`

## Marathon Status

The requested 20-hour marathon remains active. This checkpoint is not a stop condition.
