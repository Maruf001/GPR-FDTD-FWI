# GSSI 51600S Embedded Measured-Geometry Commands Checkpoint

## Scope

- Updated the measured-geometry planner summary to expose its rows CSV and shell command script paths.
- Updated the current GSSI prediction bundle to copy the measured-geometry optimizer command script into the bundle data folder.
- Regenerated the current bundle and latest pointer.

## Updated Planner

- Artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/132_gssi51600s_measured_geometry_run_planner_template_with_command_paths`
- The planner summary now includes:
  - `rows_csv`
  - `commands_sh`

## Updated Bundle

- Latest bundle:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/133_gssi51600s_current_prediction_bundle_with_embedded_geometry_commands`
- Stable pointer:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/gssi51600s_current_prediction_bundle_latest.json`
- Embedded command script:
  `data/gssi51600s_nonuniform_geometry_optimizer_commands.sh`

## Validation

- `python -m pytest tests/test_gssi51600s_current_prediction_bundle.py tests/test_gssi51600s_nonuniform_geometry_run_planner.py -q`
- Result: `7 passed in 0.48s`
- Full focused GSSI suite after this change:
  `84 passed in 4.69s`
- `git diff --check` passed for the touched bundle, planner, and related tests.

## Product Interpretation

The current GSSI bundle now contains the command script needed to rerun the measured-offset optimizer path, rather than only pointing to a separate planner artifact. This improves handoff and repeatability for the field-data predictor.
