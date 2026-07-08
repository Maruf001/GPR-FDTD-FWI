# Field Prediction Fit Recipe Execute Smoke Checkpoint

## What changed
- Executed the current `0806` fit recipe through the new wrapper:
  - `python run_field_prediction_fit_recipe.py --dataset external_2025_pipe_0806 --run-name field_3d_0806_fit_recipe_execute_smoke_iter1 --iterations 1 --execute`
- The wrapper launched the real Fast-GPR finite-length optimizer end-to-end and wrote:
  - `325_field_3d_0806_fit_recipe_execute_smoke_iter1`

## Key numbers
- Execute smoke `325`:
  - decision `finite_length_scattered_optimizer_no_material_loss_decrease`
  - iteration count `1`
  - initial/best loss `0.79158520699`
  - best diameter `12.0000001 mm`
  - best length `0.1000000 m`
  - background conductivity `0.0038000 S/m`
  - conductivity optimization enabled
  - finite outputs/gradients `true`
  - runtime `12.33 s`
- Figure:
  - optimizer figure is `1957 x 767` PNG.
- Script snapshots:
  - optimizer and finite-forward helper were snapshotted under the run folder.

## Current decision
The fit-recipe wrapper is not just a dry-run command builder; it can execute the current `0806` fitting recipe and produce a standard optimizer artifact.

## What remains blocked
- The wrapper does not yet automatically run synthesis/leaderboard/card updates after execution.
- The execute smoke used one iteration only, so it is a pipeline check, not a new scientific result.

## Validation/resource checks
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_prediction_fit_recipe.py tests/test_field_prediction_current_query.py -q`: `6 passed`.
- `git diff --check` on fit-recipe/query branch files: passed.

## Artifact paths
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/325_field_3d_0806_fit_recipe_execute_smoke_iter1`
- `outputs/validation_exp_on_field_data/3d_geometry_inventory/325_field_3d_0806_fit_recipe_execute_smoke_iter1/data/field_3d_0701_fastgpr_finite_length_scattered_optimizer_summary.json`
- `run_field_prediction_fit_recipe.py`

## Next defensible task
Add a synthesis/card update recipe or documented command pack that takes a new fit-recipe run and folds it into the current predictor-card workflow.

## Marathon status
The requested 20-hour local marathon remains active. Continue after this checkpoint rather than stopping here.
