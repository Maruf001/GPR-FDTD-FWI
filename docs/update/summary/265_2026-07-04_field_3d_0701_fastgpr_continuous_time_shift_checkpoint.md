# Field 3D 0701 Fast-GPR Continuous Time Shift Checkpoint

## What changed

- Added differentiable positive time-shift alignment to `run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`.
- Kept the existing integer fixed-overlap objective as the default path, and added `--optimize-time-shift`, `--shift-low-samples`, and `--shift-high-samples` for bounded source-timing refinement.
- Regenerated the current real-field predictor candidate using the same profile/window/x candidate as the previous scorecard, with smooth-cylinder rebar-scale conductivity and continuous source shift.
- Updated `run_field_3d_0701_fastgpr_aligned_predictor_scorecard.py` to promote the new continuous-shift candidate and carry the optimized source shift into the current-candidate summary.

## Key numbers

- New optimizer artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/046_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time`
- New promoted scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/047_field_3d_0701_fastgpr_aligned_predictor_scorecard`
- Previous comparable smooth-cylinder candidate loss: `0.724010`
- New best local Fast-GPR normalized L1 loss: `0.723305`
- Best iteration: `9 / 12`
- Optimized source shift: `20.824568` samples = `2.082457 ns`
- Shift bounds: `[16, 30]` samples, so the optimum was not pinned to a bound.
- Candidate field x: `9.819386 m`
- Analytic-event x: `9.665786 m`
- Candidate cover/depth z: `1.507821 m`
- Fast-GPR best epsr: `4.577147`
- Analytic-event epsr: `3.830539`
- Background conductivity: `0.007605 S/m`
- Anomaly conductivity: `0.050000 S/m`
- Diameter supported range remains `8-30 mm`; smooth-cylinder proxy best diameter is `30.000 mm`.
- Assumed y/profile window remains profiles `2-5`, approximately `[0.2, 0.5] m` under the current y-spacing convention.
- Conditional event length-y supported range remains `[0.095178, 0.191499] m`.
- Mean Fast-GPR iteration runtime for this run: `0.213 s` on the local NVIDIA GB10 path.

## Current decision

Continuous source-time optimization is a useful improvement and should stay in the predictor path. The promoted candidate now reports source timing as a fitted parameter instead of inheriting only the integer time/polarity ladder.

This still does not make a full 3D finite-length steel-cylinder FDTD inversion claim. The current geometry claim remains a local Fast-GPR smooth-cylinder proxy plus conditional 3D event length support.

## What remains blocked

- Diameter remains a supported range, not a uniquely identified single physical radius.
- Length-y is not yet optimized inside the Fast-GPR differentiable objective; it is still coming from the conditional 3D event model/profile window support.
- Full 3D finite-length steel-cylinder scattering physics is not yet modeled in this local Fast-GPR bridge.
- The current objective is still a local event window, not a full universal detector over all B-scans.

## Validation/resource checks

- `python -m py_compile run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`
- `python -m py_compile run_field_3d_0701_fastgpr_aligned_predictor_scorecard.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py -q` -> `7 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py -q` -> `4 passed`
- Focused Fast-GPR field suite -> `23 passed`
- Figure check: scorecard figure is nonblank, `1974 x 784`, RGBA, full channel extrema.
- `git diff --check` on the changed Fast-GPR scripts/tests was clean.
- GPU/resource check: CUDA available on NVIDIA GB10, memory headroom available; PyTorch warns that the installed build supports capability up to 12.0 while GB10 reports 12.1, but the Fast-GPR CUDA run completed with finite outputs/gradients.
- Script snapshots were frozen under the `046` and `047` artifact `scripts/` folders.

## Artifact paths

- Optimizer summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/046_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time/data/field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_summary.json`
- Optimizer rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/046_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time/data/field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rows.csv`
- Optimizer figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/046_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time/figures/field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.png`
- Scorecard summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/047_field_3d_0701_fastgpr_aligned_predictor_scorecard/data/field_3d_0701_fastgpr_aligned_predictor_scorecard_summary.json`
- Scorecard rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/047_field_3d_0701_fastgpr_aligned_predictor_scorecard/data/field_3d_0701_fastgpr_aligned_predictor_scorecard_rows.csv`
- Scorecard figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/047_field_3d_0701_fastgpr_aligned_predictor_scorecard/figures/field_3d_0701_fastgpr_aligned_predictor_scorecard.png`

## Next defensible task

Run a small optimizer comparison on the same real-field candidate: Adam baseline versus AdamW and Adamax with identical parameter bounds and artifact summaries. This directly targets the shipping predictor's accuracy/runtime rather than unrelated synthetic work.

## Marathon status

The requested 20-hour local marathon is still active. Do not stop at this checkpoint; continue with the optimizer comparison branch.
