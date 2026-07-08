# Field 3D 0701 Fast-GPR Optimizer Comparison Checkpoint

## What changed

- Added optimizer selection to `run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py`.
- Supported optimizer choices are `adam`, `adamw`, and `adamax`.
- Added optimizer metadata to per-iteration rows and run summaries.
- Ran AdamW and Adamax on the same real-field local Fast-GPR objective used by the promoted continuous-shift candidate.
- Added `run_field_3d_0701_fastgpr_optimizer_comparison.py` to package optimizer accuracy/runtime tradeoffs into a numbered artifact.

## Key numbers

- Adam baseline artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/046_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time`
- AdamW artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/048_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time_adamw`
- Adamax artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/049_field_3d_0701_fastgpr_local_window_smooth_cylinder_rebar_conductivity_profile02_xshift_continuous_time_adamax`
- Optimizer comparison artifact: `outputs/validation_exp_on_field_data/3d_geometry_inventory/050_field_3d_0701_fastgpr_optimizer_comparison`

| optimizer | best loss | mean seconds/iteration | epsr | depth m | shift ns |
| --- | ---: | ---: | ---: | ---: | ---: |
| Adam | `0.723304629` | `0.213178` | `4.577147` | `1.507672` | `2.082457` |
| AdamW | `0.723304510` | `0.409888` | `4.588086` | `1.507637` | `2.082390` |
| Adamax | `0.723314106` | `0.390772` | `4.474009` | `1.507639` | `2.104490` |

- AdamW best-loss gain over Adam: `1.19e-7`, below the `1e-5` tie threshold.
- AdamW was about `1.92x` slower than Adam on this run.
- Adamax improved the initial objective but did not beat Adam/AdamW.

## Current decision

Keep Adam as the default optimizer for the current local Fast-GPR predictor objective. AdamW is numerically tied but slower on this window, and Adamax is slightly worse. AdamW/Adamax remain available through the CLI for broader stability tests.

## What remains blocked

- This comparison is one real-field candidate window, not a full cross-dataset optimizer benchmark.
- It does not solve diameter/radius degeneracy.
- It does not yet move length-y into the differentiable Fast-GPR objective.
- It does not add full 3D finite-length steel-cylinder physics.

## Validation/resource checks

- `python -m py_compile run_field_3d_0701_fastgpr_optimizer_comparison.py tests/test_field_3d_0701_fastgpr_optimizer_comparison.py`
- `python -m pytest tests/test_field_3d_0701_fastgpr_optimizer_comparison.py -q` -> `2 passed`
- `python -m pytest tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py -q` -> `5 passed`
- Combined optimizer-focused tests -> `7 passed`
- Optimizer comparison figure is nonblank, `1804 x 733`, RGBA, full channel extrema.
- AdamW and Adamax optimizer figures are nonblank, `2314 x 750`, RGBA, full channel extrema.
- `git diff --check` on changed optimizer comparison files was clean.
- Script snapshots were frozen under `050_field_3d_0701_fastgpr_optimizer_comparison/scripts/`.

## Artifact paths

- Comparison summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/050_field_3d_0701_fastgpr_optimizer_comparison/data/field_3d_0701_fastgpr_optimizer_comparison_summary.json`
- Comparison rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/050_field_3d_0701_fastgpr_optimizer_comparison/data/field_3d_0701_fastgpr_optimizer_comparison_rows.csv`
- Comparison figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/050_field_3d_0701_fastgpr_optimizer_comparison/figures/field_3d_0701_fastgpr_optimizer_comparison.png`

## Next defensible task

Move toward the requested 3D deliverable by testing y-window/length support directly on the real field stack. The immediate bounded branch is a profile-window/y-length refinement around the promoted candidate, using the same continuous source-time alignment and reporting whether a finite y-window/length is identifiable from neighboring profiles.

## Marathon status

The requested 20-hour local marathon is still active. Continue with y/length refinement rather than stopping at this checkpoint.
