# 250 2026-07-03 Field 3D 0701 Conditional Event Optimizer Checkpoint

## What Changed

- Added `run_field_3d_0701_conditional_event_optimizer.py`.
- Added focused tests in `tests/test_field_3d_0701_conditional_event_optimizer.py`.
- Generated corrected artifact `outputs/validation_exp_on_field_data/3d_geometry_inventory/011_field_3d_0701_conditional_event_optimizer/`.
- The earlier `010_field_3d_0701_conditional_event_optimizer/` artifact is superseded by `011` because `010` pinned `z_m` at the original upper bound; `011` reruns with wider depth/time bounds.

## Method

This is a bounded JAX/Adam fit of an analytic 3D event model to the real 0701
field stack. It estimates:

- `x0_m`
- assumed `y0_m`
- `z_m`
- `epsr`
- `length_y_m`
- source/time nuisance terms
- amplitude/background nuisance terms

Radius is handled as fixed candidates and reported as top candidate plus
near-best range. This is not a full FDTD/FWI physical inversion yet.

## Key Numbers

Input stack: run `007`, real 0701 normalized stack, shape `38 x 479 x 740`.

Fit matrix:

- y-spacing assumptions: `0.05 m`, `0.10 m`.
- radius candidates: `0.004 m`, `0.008 m`, `0.012 m`.
- diameter candidates: `8 mm`, `16 mm`, `24 mm`.
- optimizer: JAX/Adam.
- iterations per candidate: `120`.
- candidate count: `6`.

Top conditional candidate:

- diameter: `8 mm`
- radius: `0.004 m`
- `x0_m`: `9.665786`
- assumed `y0_m`: `0.000053`
- `z_m`: `1.507821`
- `epsr`: `3.830539`
- `length_y_m`: `0.190732`
- y-spacing assumption: `0.10 m`
- final weighted MSE: `0.021412`

Near-best 5% range:

- near-best count: `6/6`
- diameter range: `8-24 mm`
- epsr range: `3.830539-3.860769`
- z range: `1.507821-1.513951 m`
- length-y range: `0.095178-0.191499 m`
- y-spacing assumptions in near-best set: `0.05 m`, `0.10 m`

## Current Decision

`field_3d_0701_conditional_event_optimizer_reports_top_candidate_and_ranges`

The scaffold now produces a concrete top candidate and parameter ranges from
real field data. Diameter is strongly degenerate in this analytic event model:
all tested diameters remain within 5% of the best loss. The right output is
therefore not "no diameter"; it is top candidate `8 mm` with near-best
diameter range `8-24 mm`.

## Claim Boundary

The y coordinates are still conditional because row/profile spacing is assumed,
not measured. The model is also analytic event fitting, not full FDTD/FWI.
Therefore this artifact supports optimizer scaffolding and provisional field
candidate reporting, not final physical 3D rebar geometry.

## Validation

- `conda run -n dev python -m py_compile run_field_3d_0701_conditional_event_optimizer.py`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_conditional_event_optimizer.py -q`
- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_survey_geometry_inventory.py tests/test_field_3d_rad_grid_metadata_audit.py tests/test_field_3d_0701_grid_contract.py tests/test_field_3d_0701_rd3_intake_preview.py tests/test_field_3d_0701_y_spacing_sensitivity_contract.py tests/test_field_3d_0701_stack_manifest.py tests/test_field_3d_0701_acceleration_backend_benchmark.py tests/test_field_3d_0701_conditional_event_optimizer.py -q`
- Focused project-env result: `30 passed`.
- Focused dev-env acceleration/optimizer result: `9 passed`.
- `git diff --check -- run_field_3d_0701_conditional_event_optimizer.py tests/test_field_3d_0701_conditional_event_optimizer.py`
- Figure check: `field_3d_0701_conditional_event_optimizer.png` is `2059 x 835` PNG.

## Artifact Paths

- Summary: `outputs/validation_exp_on_field_data/3d_geometry_inventory/011_field_3d_0701_conditional_event_optimizer/data/field_3d_0701_conditional_event_optimizer_summary.json`
- Candidate rows: `outputs/validation_exp_on_field_data/3d_geometry_inventory/011_field_3d_0701_conditional_event_optimizer/data/field_3d_0701_conditional_event_optimizer_rows.csv`
- Curves: `outputs/validation_exp_on_field_data/3d_geometry_inventory/011_field_3d_0701_conditional_event_optimizer/data/field_3d_0701_conditional_event_optimizer_curves.csv`
- Figure: `outputs/validation_exp_on_field_data/3d_geometry_inventory/011_field_3d_0701_conditional_event_optimizer/figures/field_3d_0701_conditional_event_optimizer.png`

## Next Defensible Task

Upgrade the scaffold from analytic event fitting toward a paper-method path:
either wire the Fast-GPR-FWI forward function into a small field-stack smoke
using the rebuilt repo, or add a JAX differentiable forward proxy with the same
parameter contract and compare one optimizer iteration runtime. The deliverable
must keep reporting top candidates plus near-best ranges.

## Marathon Status

The local field-data marathon remains active; this is a checkpoint, not a stop.
