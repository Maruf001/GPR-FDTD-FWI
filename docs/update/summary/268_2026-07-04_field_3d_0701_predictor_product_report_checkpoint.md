# Field 3D 0701 Predictor Product Report Checkpoint

## What changed

- Added `run_field_3d_0701_predictor_product_report.py`.
- The report consolidates the promoted scorecard, y/length scan, optimizer comparison, and stack manifest into a single product-facing prediction artifact.
- Generated a machine-readable JSON prediction, one-row CSV prediction, figure, README, manifest, and script snapshots.

## Key numbers

- Product report artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report`
- Prediction JSON: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/data/field_3d_0701_predictor_product_prediction.json`
- Prediction CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/data/field_3d_0701_predictor_product_prediction.csv`

Current product-facing prediction:

- dataset root: `data/2025-01-13_GPR_Dataset/Data Set/pipe/0701`
- x: `9.819386 m`
- y center: `0.200000 m` under the assumed `0.1 m` profile spacing
- z/cover depth: `1.507637 m`
- diameter supported range: `8-30 mm`
- radius supported range: `4-15 mm`
- y-length center-span proxy: `0.200000 m`
- y-length window-span proxy: `0.300000 m`
- epsr: `4.803974`
- background conductivity: `0.008404 S/m`
- anomaly conductivity: `0.050000 S/m`
- source shift: `2.137166 ns`
- fit loss: `0.707159` Fast-GPR normalized L1 over the local real-field B-scan window
- recommended optimizer: `Adam`

## Current decision

Artifact `054` is the current best handoff object for the 0701 real-field predictor. It reports the requested 3D-style quantities in one place: `x/y/z`, radius/diameter range, y-length proxy, epsr, conductivity, optimizer choice, fit loss, runtime context, and claim boundary.

## Claim boundary

This is a real-field local Fast-GPR smooth-cylinder conductivity proxy. It is not yet a full finite-length 3D steel-cylinder FDTD inversion. Diameter/radius is still a supported range, and y geometry is based on the stack-manifest spacing assumption rather than measured survey geometry.

## Validation/resource checks

- `python -m py_compile run_field_3d_0701_predictor_product_report.py tests/test_field_3d_0701_predictor_product_report.py`
- `python -m pytest tests/test_field_3d_0701_predictor_product_report.py -q` -> `2 passed`
- Focused predictor/report suite -> `17 passed`
- Product report figure is nonblank, `1889 x 767`, RGBA, full channel extrema.
- `git diff --check` on changed report/scorecard/y-length files was clean.
- Script snapshots were frozen under `054_field_3d_0701_predictor_product_report/scripts/`.

## Artifact paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/data/field_3d_0701_predictor_product_report_summary.json`
- Prediction JSON: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/data/field_3d_0701_predictor_product_prediction.json`
- Prediction CSV: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/data/field_3d_0701_predictor_product_prediction.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/054_field_3d_0701_predictor_product_report/figures/field_3d_0701_predictor_product_report.png`

## Next defensible task

Start cross-dataset/data-source validation against `data/2026-06-09_GSSI_model_51600S`. The immediate goal is an intake/manifest and product-compatibility report: identify B-scan files, dimensions, dt/dx metadata if available, and the fastest route to run the predictor pipeline on that data without hand-selected 0701 assumptions.

## Marathon status

The requested 20-hour local marathon is still active. Continue with GSSI 51600S cross-dataset validation rather than stopping at this checkpoint.
