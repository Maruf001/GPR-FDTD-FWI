# Field 3D 0701 Fast-GPR Y/Length Refinement Checkpoint

## What changed

- Added `run_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py`.
- The scan re-optimizes the real-field Fast-GPR local objective across profile/y windows instead of only transferring a fixed prediction.
- Ran a 25-candidate scan over profile starts `0-4` and profile lengths `2-6`, with smooth-cylinder rebar-scale conductivity and continuous source-time fitting.
- Reran the best y-window candidate with the full 12-iteration optimizer.
- Updated the promoted scorecard so the current candidate now includes a Fast-GPR y center and y-length proxy.

## Key numbers

- Y/length scan artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/051_field_3d_0701_fastgpr_y_length_window_optimizer_scan`
- Refined y-window optimizer artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/052_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile01_length3_xshift_continuous_time`
- Promoted scorecard artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/053_field_3d_0701_fastgpr_aligned_predictor_scorecard`

Best scan candidate:

- profile window: `1-3`
- assumed y window: `[0.1, 0.3] m`
- assumed y center: `0.2 m`
- center-to-center y-span proxy: `0.2 m`
- window-span proxy: `0.3 m`
- scan best loss: `0.707178`
- near-best count under the current cutoff: `1`

Full 12-iteration rerun of the best candidate:

- best loss: `0.707159`
- previous promoted 4-profile candidate loss: `0.723305`
- field x: `9.819386 m`
- analytic-event x: `9.665786 m`
- depth z: `1.507637 m`
- Fast-GPR epsr: `4.803974`
- analytic-event epsr: `3.830539`
- background conductivity: `0.008404 S/m`
- anomaly conductivity: `0.050000 S/m`
- source shift: `21.371658` samples = `2.137166 ns`
- diameter proxy remains at the upper bound: about `30.000 mm`
- diameter supported range remains `8-30 mm`
- mean iteration runtime: `0.220 s`

## Current decision

The current best product-facing field predictor candidate should use the refined y-window result:

- `x ~= 9.819 m`
- `y center ~= 0.2 m` under the assumed profile spacing
- `z ~= 1.508 m`
- `length-y proxy ~= 0.2 m` center-to-center, or `0.3 m` profile-window span
- `epsr ~= 4.804`
- `background conductivity ~= 0.0084 S/m`
- `diameter/radius remains a range, not a unique estimate`

This is materially better than the previous `2-5` profile-window candidate on the local Fast-GPR objective.

## What remains blocked

- The y-length value is still a profile-window support proxy. It is not yet a full finite-length 3D steel-cylinder FDTD inversion.
- Diameter remains non-unique and pinned near the smooth-cylinder proxy upper bound.
- Cross-dataset stability is not established yet.
- The method still needs a cleaner product wrapper that can run detection/fitting from field data and emit a single prediction report without hand-selecting artifacts.

## Validation/resource checks

- `python -m py_compile run_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py tests/test_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_y_length_window_optimizer_scan.py -q` -> `4 passed`
- Y/length plus optimizer tests -> `9 passed`
- Full focused Fast-GPR field suite including optimizer comparison and y/length scan -> `30 passed`
- `git diff --check` on changed Fast-GPR scripts/tests was clean.
- Y/length scan figure is nonblank, `1923 x 784`, RGBA, full channel extrema.
- Refined optimizer figure is nonblank, `2314 x 750`, RGBA, full channel extrema.
- Promoted scorecard figure is nonblank, `1974 x 784`, RGBA, full channel extrema.
- Script snapshots were frozen under artifacts `051`, `052`, and `053`.

## Artifact paths

- Scan summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/051_field_3d_0701_fastgpr_y_length_window_optimizer_scan/data/field_3d_0701_fastgpr_y_length_window_optimizer_scan_summary.json`
- Scan candidates: `outputs/validation_exp_on_field_data/3d_geometry_inventory/051_field_3d_0701_fastgpr_y_length_window_optimizer_scan/data/field_3d_0701_fastgpr_y_length_window_optimizer_scan_candidates.csv`
- Refined optimizer summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/052_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile01_length3_xshift_continuous_time/data/field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_summary.json`
- Refined scorecard summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/053_field_3d_0701_fastgpr_aligned_predictor_scorecard/data/field_3d_0701_fastgpr_aligned_predictor_scorecard_summary.json`

## Next defensible task

Build a single product-facing prediction report/CLI artifact from the promoted candidate, then start cross-dataset/data-source stability work against `data/2026-06-09_GSSI_model_51600S` or another available field profile. The deliverable should output predicted x/y/z, diameter range, length proxy, epsr, conductivity, fit loss, runtime, and claim boundary in one place.

## Marathon status

The requested 20-hour local marathon is still active. Continue with deliverable packaging and cross-dataset validation; do not stop at this checkpoint.
