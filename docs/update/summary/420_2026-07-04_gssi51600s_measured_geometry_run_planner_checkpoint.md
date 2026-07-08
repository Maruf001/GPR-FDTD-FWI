# GSSI 51600S Measured Geometry Run Planner Checkpoint

## Scope

- Added `run_gssi51600s_nonuniform_geometry_run_planner.py`.
- The planner reads a measured `profile_index,y_m` geometry CSV and emits explicit `--profile-offsets-m` optimizer commands for the trusted GSSI 51600S profile subsets.
- This closes the gap between "crossline geometry must be measured" and the actual CUDA Fast-GPR optimizer calls needed after the profile coordinates are supplied.

## Product Behavior

- Uniform measured spacing still works with the geometry-conditioned predictor.
- Nonuniform measured spacing is no longer reduced to a single average spacing; it now has a direct run-plan path.
- Default subset commands are generated for profiles 0-2 and profiles 1-3 using the same current GSSI optimizer settings: CUDA Fast-GPR bridge, AdamW, local event windows, optimized shift, x/z, material contrast, and conductivity.
- Added the planner to the GSSI prediction bundle source snapshots and compact bundle metadata.

## Generated Artifacts

- Planner artifact:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/121_gssi51600s_measured_geometry_run_planner_template`
- Updated bundle:
  `outputs/validation_exp_on_field_data/gssi51600s_predictor_compatibility/122_gssi51600s_current_prediction_bundle_with_measured_geometry_planner`

The planner artifact was generated from the current geometry template. It is a command-pack template, not a measured-geometry release claim.

## Current Bundle Signals

- `measured_geometry_run_plan_decision`: `measured_geometry_uniform_optimizer_commands_ready`
- `measured_geometry_run_plan_geometry_status`: `uniform_spacing_ready_for_conditioned_predictor`
- `measured_geometry_optimizer_command_count`: `2`
- Source snapshots now include `run_gssi51600s_nonuniform_geometry_run_planner.py`.

## Validation

- Compilation:
  `python -m py_compile run_gssi51600s_current_prediction_bundle.py run_gssi51600s_measured_geometry_intake.py run_gssi51600s_nonuniform_geometry_run_planner.py ...`
- Focused tests:
  `79 passed in 4.29s`
- Diff hygiene:
  `git diff --check` passed for touched planner, intake, bundle, test, and daily-update files.

## Next Step

Find or fill the real GSSI 51600S crossline profile coordinates, run the generated measured-offset optimizer commands, then rebuild the joint profile-spacing card and current prediction bundle from those measured-offset rows.
